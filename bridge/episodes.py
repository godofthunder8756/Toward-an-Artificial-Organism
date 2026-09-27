"""Save/load helpers for evaluation episodes.

Every arm in the study must reuse the same underlying environment and, where
appropriate, the same saved evaluation episodes. This module provides a tiny,
stdlib-only JSONL format for recording and replaying episodes so an arm can be
scored against an identical observation stream.

An episode is a list of per-tick records. Each record carries the tick index,
the observation the agent saw, the action taken, and the reward/labels that
were actually delivered. Saving is incremental (append-friendly); loading
returns the raw records unchanged so downstream code owns the interpretation.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List

__all__ = ["save_episodes", "load_episodes", "EpisodeRecorder"]


def save_episodes(path: str, episodes: Iterable[List[Dict[str, Any]]]) -> int:
    """Write episodes to a JSONL file (one episode per line). Returns count.

    ``episodes`` is an iterable of episodes; each episode is a list of per-tick
    record dicts. Any JSON-serializable record works — the module imposes no
    schema so the bridge's own environment can define one.
    """
    n = 0
    with open(path, "w", encoding="utf-8") as fh:
        for episode in episodes:
            fh.write(json.dumps(episode, ensure_ascii=False))
            fh.write("\n")
            n += 1
    return n


def load_episodes(path: str) -> List[List[Dict[str, Any]]]:
    """Read a JSONL episode file back into a list of episodes."""
    out: List[List[Dict[str, Any]]] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


class EpisodeRecorder:
    """Incremental episode writer; flushes each episode so crashes don't lose
    earlier ones."""

    def __init__(self, path: str):
        self.path = path
        self._fh = open(path, "w", encoding="utf-8")
        self.count = 0

    def record(self, episode: List[Dict[str, Any]]) -> None:
        self._fh.write(json.dumps(episode, ensure_ascii=False))
        self._fh.write("\n")
        self._fh.flush()
        self.count += 1

    def close(self) -> None:
        self._fh.close()

    def __enter__(self) -> "EpisodeRecorder":
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False
