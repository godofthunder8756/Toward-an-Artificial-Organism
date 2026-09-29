"""R5/R6/R7 evaluator-only controls. None is a learned primary comparator."""

from __future__ import annotations

import torch

from phase3b.models import Arm, Trace
from phase3b.world import Episode, posterior_counts


def _belief(common: torch.Tensor) -> torch.Tensor:
    levels = torch.tensor((1 / 17, 0.5, 16 / 17), dtype=torch.float64, device=common.device)
    return levels[posterior_counts(common)]


def _local_update(q: torch.Tensor, bit: int) -> torch.Tensor:
    odds = q / (1 - q) * (4 if bit else 0.25)
    return odds / (1 + odds)


def _risk(action: torch.Tensor, which: int, context: int, bit: int,
          belief: torch.Tensor) -> torch.Tensor:
    first = (context + which) % 4
    updated = _local_update(belief[:, first], bit)
    q = updated if which != 2 else (updated + belief[:, (context + 3) % 4]
                                        - 2 * updated * belief[:, (context + 3) % 4])
    risk = torch.where(action == 0, q, 1 - q)
    return torch.where(action == 2, torch.full_like(risk, 0.18), risk) if which == 1 else risk


@torch.no_grad()
def oracle_copies(episode: Episode, name: str) -> tuple[torch.Tensor, ...]:
    """R5 broadcast or R7 separate exact belief copies; same Bayes risk."""
    return oracle_actions(episode, name)


@torch.no_grad()
def oracle_actions(episode: Episode, name: str) -> tuple[torch.Tensor, ...]:
    """Actual local-bit Bayes actions; only the evaluator may call this."""
    if name not in ("R5", "R7"):
        raise ValueError("EXTERNAL R5/R7 only")
    q = _belief(episode.common)
    actions = []
    for i in range(3):
        per_context = []
        for c in range(4):
            odds = q[:, (c + i) % 4] / (1 - q[:, (c + i) % 4])
            mult = torch.where(episode.local[:, c, i] == 1, 4.0, 0.25)
            p = odds * mult / (1 + odds * mult)
            if i == 2:
                other = q[:, (c + 3) % 4]
                p = p + other - 2 * p * other
            if i == 1:
                a = torch.stack((p, 1 - p, torch.full_like(p, 0.18)), -1).argmin(-1)
            else:
                a = (p > 0.5).long()
            per_context.append(a)
        actions.append(torch.stack(per_context, 1))
    return tuple(actions)


@torch.no_grad()
def oracle_selector(candidate: Arm, episode: Episode) -> Trace:
    """R6 EXTERNAL: integrated-out local bits, fixed candidate L/quantizers/heads.

    The oracle knows the exact posterior but never injects it into an arm.
    For each candidate address it computes the expected *joint* loss across
    independent possible local readings. Report as headroom, not learned win.
    """
    if candidate.name != "candidate":
        raise ValueError("R6 requires a frozen candidate")
    candidate.eval()
    q = _belief(episode.common)
    states = candidate.encode(episode.common)
    batch = states.shape[0]
    words = [candidate.write(states, 4, forced=torch.full((batch, 4), j, dtype=torch.long))[0]
             for j in range(4)]
    risk = torch.zeros(batch, 4, 4, dtype=torch.float64)
    for j in range(4):
        for c in range(4):
            for i in range(3):
                prob = q[:, (c + i) % 4]
                for bit in (0, 1):
                    sensor_prob = (0.2 + 0.6 * prob) if bit else (0.8 - 0.6 * prob)
                    act = candidate.read(words[j][:, c], torch.full((batch,), bit, dtype=torch.long), c, i).argmax(-1)
                    risk[:, c, j] += sensor_prob * _risk(act, i, c, bit, q) / 3
    chosen = risk.argmin(-1)  # smallest address tie break
    word = torch.stack(words, 2).gather(2, chosen.unsqueeze(-1)).squeeze(-1)
    logits = tuple(torch.stack([candidate.read(word[:, c], episode.local[:, c, i], c, i)
                                for c in range(4)], 1) for i in range(3))
    return Trace(logits, tuple(x.argmax(-1) for x in logits), word, chosen, word % 2, states=states)