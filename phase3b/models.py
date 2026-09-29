"""Vectorized whole-arm topologies. Forward graphs cannot accept truth or feedback.

The sole consumer interface is ``read(shared, local_bit, context)``. For
word arms ``shared`` is the same three-bit word for all three consumers;
head modules have no recurrent state, selector logits or hidden-state input.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F

from phase3b import PRIMARY
from phase3b.resources import charge


class Recurrent(nn.Module):
    """Explicit port/full-history recurrent cell (two linear MACs per tick)."""

    def __init__(self, inputs: int, width: int):
        super().__init__()
        self.input = nn.Linear(inputs, width)
        self.hidden = nn.Linear(width, width, bias=False)
        self.width = width

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        h = sequence.new_zeros(sequence.shape[0], self.width)
        for t in range(sequence.shape[1]):
            charge(indexed=sequence[:, t])
            h = torch.tanh(self.input(sequence[:, t]) + self.hidden(h))
            charge(tanh=h)
        return h


@dataclass
class Trace:
    logits: tuple[torch.Tensor, ...]
    actions: tuple[torch.Tensor, ...]
    word: torch.Tensor | None = None
    address: torch.Tensor | None = None
    payload: torch.Tensor | None = None
    token_logp: torch.Tensor | None = None  # (B,C), shared selector + payload
    action_logp: tuple[torch.Tensor, ...] | None = None
    states: torch.Tensor | None = None  # (B,4,D), diagnostic only, never a head input


def _token(logits: torch.Tensor, stochastic: bool) -> tuple[torch.Tensor, torch.Tensor]:
    if stochastic:
        token = torch.distributions.Categorical(logits=logits).sample()
        charge(draws=token)
    else:
        charge(argmax=logits)
        token = logits.argmax(-1)  # lowest-index tie break
    charge(log_softmax=logits, indexed=token)
    return token, F.log_softmax(logits, -1).gather(-1, token.unsqueeze(-1)).squeeze(-1)


class Arm(nn.Module):
    """Candidate, all six independent primary families, or R9 clone subfamily.

    R5/R6/R7 are EXTERNAL evaluator controls, never constructed as learned arms.
    R4 must be given a public route or explicit round-robin training addresses.
    """

    def __init__(self, name: str, width: int, *, clone: bool = False):
        super().__init__()
        if name not in PRIMARY or width < 1:
            raise ValueError("unknown primary family or invalid width")
        self.name, self.width, self.clone = name, width, clone
        self.word_arm = name in ("candidate", "R4", "R9")
        self.port_arm = name in ("candidate", "R1", "R4") or clone
        if self.port_arm:
            self.ports = nn.ModuleList(Recurrent(1, width) for _ in range(4))
        elif name == "R3":
            self.private = nn.ModuleList(Recurrent(5, width) for _ in range(3))
        else:
            self.trunk = Recurrent(5, width)
        if name == "candidate" or clone:
            self.selector = nn.Linear(4 * width + 4, 4)
            self.payloads = nn.ModuleList(nn.Linear(width, 2) for _ in range(4))
        elif name == "R4":
            self.payloads = nn.ModuleList(nn.Linear(width, 2) for _ in range(4))
        elif name == "R9":
            self.code = nn.Linear(width + 4, 8)
        if name == "R8":
            self.broadcast = nn.Linear(width, width)
        feature_size = (8 if self.word_arm else
                        4 * width if name == "R1" else width) + 5
        self.heads = nn.ModuleList(nn.Linear(feature_size, n) for n in (2, 3, 2))
        self.route: tuple[int, int, int, int] | None = None

    def encode(self, common: torch.Tensor) -> torch.Tensor:
        if common.ndim != 2 or common.shape[1] != 8 or not torch.all((common == 0) | (common == 1)):
            raise ValueError("expected eight public scheduled BSC readings")
        if self.port_arm:
            # Each port receives *only* its two observations, no other port.
            charge(indexed=common)
            return torch.stack([port(common[:, (j, j + 4)].float().unsqueeze(-1))
                                for j, port in enumerate(self.ports)], 1)
        charge(indexed=common)
        seq = torch.cat((F.one_hot(torch.arange(8, device=common.device) % 4, 4)
                         .float().expand(common.shape[0], -1, -1),
                         common.float().unsqueeze(-1)), -1)
        if self.name == "R3":
            return torch.stack([encoder(seq) for encoder in self.private], 1)
        state = self.trunk(seq)
        return self.broadcast(state) if self.name == "R8" else state

    def write(self, states: torch.Tensor, contexts: int, *, stochastic: bool = False,
              forced: torch.Tensor | None = None) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Write exactly one of eight legal words per tick; forced is diagnostic.

        R4's route is public, history-independent; training passes explicit
        round-robin addresses. R9's full-history code has no source semantics.
        """
        batch = states.shape[0]
        clock = F.one_hot(torch.arange(contexts, device=states.device), 4).float()
        ctx = clock.expand(batch, -1, -1)
        if self.name == "R9" and not self.clone:
            code_logits = self.code(torch.cat((states.unsqueeze(1).expand(-1, contexts, -1), ctx), -1))
            word, logp = _token(code_logits, stochastic)
            charge(indexed=word)
            return word, word // 2, word % 2, logp
        if self.name == "candidate" or self.clone:
            select_logits = self.selector(torch.cat((states.flatten(1).unsqueeze(1)
                                                     .expand(-1, contexts, -1), ctx), -1))
            address, select_logp = _token(select_logits, stochastic)
        elif self.name == "R4":
            if self.route is None and forced is None:
                raise ValueError("R4 needs public route or round-robin training addresses")
            if forced is None:
                if self.route is None:
                    raise ValueError("R4 route missing")
                address = torch.tensor(self.route[:contexts], device=states.device).expand(batch, -1)
            else:
                address = forced
            charge(indexed=address)
            select_logp = torch.zeros((batch, contexts), device=states.device)
        else:
            raise ValueError("not a word arm")
        if forced is not None:
            address = forced
            select_logp = torch.zeros_like(address, dtype=torch.float32)
        if address.shape != (batch, contexts) or torch.any((address < 0) | (address > 3)):
            raise ValueError("illegal address")
        all_logits = torch.stack([p(states[:, j]) for j, p in enumerate(self.payloads)], 1)
        chosen = all_logits.gather(1, address.unsqueeze(-1).expand(-1, -1, 2))
        charge(indexed=chosen)
        payload, payload_logp = _token(chosen, stochastic)
        return address * 2 + payload, address, payload, select_logp + payload_logp

    def read(self, shared: torch.Tensor, bit: torch.Tensor, context: int,
             consumer: int) -> torch.Tensor:
        """No truth, history, other local bit, old word, or reward is accepted."""
        if consumer not in (0, 1, 2) or context not in range(4):
            raise ValueError("illegal consumer/context")
        if shared.ndim == 1:
            if not self.word_arm or torch.any((shared < 0) | (shared >= 8)):
                raise ValueError("illegal word")
            feature = F.one_hot(shared.long(), 8).float()
            charge(indexed=shared)
        else:
            if self.word_arm:
                raise ValueError("word consumer cannot read hidden representation")
            feature = shared[:, consumer] if self.name == "R3" else shared.flatten(1)
            charge(indexed=feature)
        if bit.ndim != 1 or bit.shape[0] != feature.shape[0]:
            raise ValueError("local bit shape mismatch")
        public = F.one_hot(torch.full_like(bit, context), 4).float()
        return self.heads[consumer](torch.cat((feature, public, bit.float().unsqueeze(-1)), -1))

    def forward(self, common: torch.Tensor, local: torch.Tensor, *, contexts: int = 4,
                stochastic: bool = False, forced: torch.Tensor | None = None,
                words: torch.Tensor | None = None) -> Trace:
        if contexts not in (3, 4) or local.shape != (common.shape[0], contexts, 3):
            raise ValueError("local data must be (B, contexts, three PRIVATE bits)")
        if not torch.all((local == 0) | (local == 1)):
            raise ValueError("local sensor must be binary")
        states = self.encode(common)
        word: torch.Tensor | None = None
        address: torch.Tensor | None = None
        payload: torch.Tensor | None = None
        token_logp: torch.Tensor | None = None
        if self.word_arm:
            word, address, payload, token_logp = self.write(states, contexts, stochastic=stochastic, forced=forced)
            if words is not None:
                if words.shape != word.shape or torch.any((words < 0) | (words > 7)):
                    raise ValueError("illegal injected word")
                word = words
        elif forced is not None or words is not None:
            raise ValueError("no word to inject in this topology")
        logits: list[torch.Tensor] = []
        actions: list[torch.Tensor] = []
        action_logp: list[torch.Tensor] = []
        for i in range(3):
            charge(indexed=local[:, :, i])
            if self.word_arm and word is None:
                raise AssertionError("word arm failed to produce a word")
            logits_i = torch.stack([self.read(word[:, c] if word is not None else states,
                                              local[:, c, i], c, i)
                                    for c in range(contexts)], 1)
            a, lp = _token(logits_i, stochastic)
            logits.append(logits_i)
            actions.append(a)
            action_logp.append(lp)
        return Trace(tuple(logits), tuple(actions), word, address, payload,
                     token_logp, tuple(action_logp), states if self.port_arm else None)


def clone_as_r9(candidate: Arm) -> Arm:
    """Exact R9 inclusion: allowed candidate graph copied, never a trained win."""
    if candidate.name != "candidate":
        raise ValueError("only a candidate may be copied")
    clone = Arm("R9", candidate.width, clone=True)
    clone.ports.load_state_dict(candidate.ports.state_dict())
    clone.selector.load_state_dict(candidate.selector.state_dict())
    clone.payloads.load_state_dict(candidate.payloads.state_dict())
    clone.heads.load_state_dict(candidate.heads.state_dict())
    return clone