"""H9 interventions. Counterfactual cuts are OUTSIDE the eight-word alphabet.

Diagnostics are distinct learnable modules, never extra candidate inputs.
Lesions cannot be reported as primary rival-exclusive wins.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from phase3b.models import Arm, Trace, _token


class NoMessage(nn.Module):
    """I2/I6 out-of-band readout; untrained instances have no scored losses."""

    def __init__(self):
        super().__init__()
        self.heads = nn.ModuleList(nn.Linear(5, n) for n in (2, 3, 2))
        self.trained = False

    def read(self, bit: torch.Tensor, context: int, consumer: int) -> torch.Tensor:
        ctx = F.one_hot(torch.full_like(bit, context), 4).float()
        return self.heads[consumer](torch.cat((ctx, bit.float().unsqueeze(-1)), -1))


class ExpandedWord(nn.Module):
    """I4 frozen-state 4/8/16-bit diagnostic, separate selector and heads."""

    def __init__(self, width: int, bits: int):
        super().__init__()
        if bits not in (4, 8, 16):
            raise ValueError("I4 bits must be 4, 8 or 16")
        self.bits = bits
        self.selector = nn.Linear(4 * width + 4, 4)
        self.payloads = nn.ModuleList(nn.Linear(width, bits - 2) for _ in range(4))
        self.heads = nn.ModuleList(nn.Linear(bits + 5, n) for n in (2, 3, 2))

    def forward(self, frozen: torch.Tensor, local: torch.Tensor,
                *, stochastic: bool = False) -> Trace:
        batch, contexts, _ = local.shape
        frozen = frozen.detach()  # no gradients to the original sensory encoders
        words, addresses, payloads, logps = [], [], [], []
        logits: list[list[torch.Tensor]] = [[], [], []]
        actions: list[list[torch.Tensor]] = [[], [], []]
        alp: list[list[torch.Tensor]] = [[], [], []]
        for c in range(contexts):
            ctx = F.one_hot(torch.full((batch,), c, device=frozen.device), 4).float()
            address, slp = _token(self.selector(torch.cat((frozen.flatten(1), ctx), -1)), stochastic)
            pl = torch.stack([layer(frozen[:, j]) for j, layer in enumerate(self.payloads)], 1)
            chosen = pl.gather(1, address[:, None, None].expand(-1, 1, self.bits - 2)).squeeze(1)
            pbits = torch.bernoulli(torch.sigmoid(chosen)).long() if stochastic else (chosen > 0).long()
            pb_logp = -F.binary_cross_entropy_with_logits(chosen, pbits.float(), reduction="none").sum(-1)
            bits = torch.cat((torch.stack((address // 2, address % 2), -1), pbits), -1)
            word = (bits * (2 ** torch.arange(self.bits - 1, -1, -1, device=frozen.device))).sum(-1)
            words.append(word)
            addresses.append(address)
            payloads.append(pbits)
            logps.append(slp + pb_logp)
            for i in range(3):
                score = self.heads[i](torch.cat((bits.float(), ctx, local[:, c, i:i+1].float()), -1))
                a, lp = _token(score, stochastic)
                logits[i].append(score)
                actions[i].append(a)
                alp[i].append(lp)
        return Trace(tuple(torch.stack(x, 1) for x in logits),
                     tuple(torch.stack(x, 1) for x in actions),
                     torch.stack(words, 1), torch.stack(addresses, 1),
                     torch.stack(payloads, 1), torch.stack(logps, 1),
                     tuple(torch.stack(x, 1) for x in alp))


class UnlimitedRead(nn.Module):
    """I5: frozen four-port vector bypass, all-state bandwidth disclosed."""

    def __init__(self, width: int):
        super().__init__()
        self.heads = nn.ModuleList(nn.Linear(4 * width + 5, n) for n in (2, 3, 2))

    def forward(self, frozen: torch.Tensor, local: torch.Tensor,
                *, stochastic: bool = False) -> Trace:
        frozen = frozen.detach().flatten(1)
        batch, contexts, _ = local.shape
        logits, actions, logps = [], [], []
        for i in range(3):
            score = torch.stack([self.heads[i](torch.cat((frozen,
                                  F.one_hot(torch.full((batch,), c, device=frozen.device), 4).float(),
                                  local[:, c, i:i+1].float()), -1)) for c in range(contexts)], 1)
            a, lp = _token(score, stochastic)
            logits.append(score)
            actions.append(a)
            logps.append(lp)
        return Trace(tuple(logits), tuple(actions), action_logp=tuple(logps))


def _replay(model: Arm, states: torch.Tensor, local: torch.Tensor, word: torch.Tensor,
            *, cut: int | None = None, diagnostic: NoMessage | None = None) -> Trace:
    """Read only the supplied word; no encoder tensor is handed to a head."""
    contexts = word.shape[1]
    scores, acts = [], []
    for i in range(3):
        if cut is not None and diagnostic is None:
            raise ValueError("out-of-band cut requires a diagnostic readout")
        logits_per_context: list[torch.Tensor] = []
        for c in range(contexts):
            if cut == i or cut == -1:
                if diagnostic is None:
                    raise ValueError("missing diagnostic readout")
                logits_per_context.append(diagnostic.read(local[:, c, i], c, i))
            else:
                logits_per_context.append(model.read(word[:, c], local[:, c, i], c, i))
        logits = torch.stack(logits_per_context, 1)
        scores.append(logits)
        acts.append(logits.argmax(-1))
    return Trace(tuple(scores), tuple(acts), word, states=states)


def intervene(model: Arm, common: torch.Tensor, local: torch.Tensor, which: str,
              *, address: int | None = None, consumer: int | None = None,
              paired_common: torch.Tensor | None = None, port: int | None = None,
              diagnostic: NoMessage | None = None, expanded: ExpandedWord | None = None,
              unlimited: UnlimitedRead | None = None) -> Trace:
    """I1/I2/I3/I4/I5/I6/I7/noop; all inputs replay identical histories.

    I1 substitutes address bits *at read* without recomputing payload. I3
    forces address *before* payload. I7 replaces just one port's state.
    For I2/I6, trained=False forbids calling the resulting loss a score.
    """
    if model.name != "candidate":
        raise ValueError("candidate-specific structural intervention; rivals N/A")
    intact = model(common, local, contexts=local.shape[1])
    if which == "noop":
        return intact
    if which == "I4" and expanded is not None:
        return expanded(intact.states, local)
    if which == "I5" and unlimited is not None:
        return unlimited(intact.states, local)
    if which in ("I2", "I6"):
        if diagnostic is None or (which == "I6" and consumer not in range(3)):
            raise ValueError("missing diagnostic readout or cut consumer")
        return _replay(model, intact.states, local, intact.word, cut=-1 if which == "I2" else consumer,
                       diagnostic=diagnostic)
    if which in ("I1", "I3"):
        if address not in range(4):
            raise ValueError("select one of four addresses")
        if address is None or intact.address is None or intact.payload is None or intact.states is None:
            raise AssertionError("candidate intervention has no occupancy state")
        forced = torch.full_like(intact.address, address)
        word = forced * 2 + intact.payload if which == "I1" else model.write(intact.states, local.shape[1], forced=forced)[0]
        return _replay(model, intact.states, local, word)
    if which == "I7":
        if paired_common is None or port not in range(4) or paired_common.shape != common.shape:
            raise ValueError("paired history and port required")
        paired = model.encode(paired_common)
        states = intact.states.clone()
        states[:, port] = paired[:, port]
        word = model.write(states, local.shape[1])[0]
        return _replay(model, states, local, word)
    raise ValueError("unknown or incomplete intervention")


def first_divergence(intact: Trace, changed: Trace) -> torch.Tensor:
    """First differing decision tick per episode; -1 means no divergence."""
    differing = torch.zeros_like(intact.actions[0], dtype=torch.bool)
    if intact.word is not None and changed.word is not None:
        differing |= intact.word != changed.word
    for before, after in zip(intact.actions, changed.actions):
        differing |= before != after
    return torch.where(differing.any(1), differing.long().argmax(1) + 8,
                       torch.full((differing.shape[0],), -1, device=differing.device))