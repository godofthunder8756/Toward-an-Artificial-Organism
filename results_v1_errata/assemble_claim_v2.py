"""Formatting repair for the frozen claim assembler. Additive. No rerun.

`recurrent_core_transfer_verdicts.assemble_claim` is unchanged. On the
recorded inputs it prints the bare negative constant ``not met`` and leaves
the variation sentence without a final period. This helper names that label
and ends the paragraph with a period. It does not select a different
scientific sentence, and it does not emit the E-1 presentation paragraph.
"""

from __future__ import annotations

from recurrent_core_transfer_verdicts import (
    RIVAL_AFIT,
    RIVAL_AFIT_NOT,
    assemble_claim,
)


def assemble_claim_v2(
    e1: str,
    transfer: str,
    specific: dict,
    variation: dict,
    advantage: str,
    rival_afit: str,
    rival_afit_count: int,
) -> str:
    text = assemble_claim(
        e1, transfer, specific, variation, advantage, rival_afit, rival_afit_count
    )
    if rival_afit == RIVAL_AFIT_NOT:
        bare = "Tuned-rival results: %s. %s (%d/10)." % (
            advantage,
            RIVAL_AFIT_NOT,
            rival_afit_count,
        )
        named = "Tuned-rival results: %s. %s: %s (%d/10)." % (
            advantage,
            RIVAL_AFIT,
            RIVAL_AFIT_NOT,
            rival_afit_count,
        )
        if bare not in text:
            raise RuntimeError("frozen rival clause not found")
        text = text.replace(bare, named, 1)
    if not text.endswith("."):
        text += "."
    return text
