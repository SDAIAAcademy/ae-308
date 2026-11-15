"""Your team's hardened build of Mukhallis. The other team attacks what controls() returns.

Start from the course's reference build and change it. Every change needs a reason in your threat
model and a test in ci/security_suite.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import reference_build as RB  # noqa: E402


def controls() -> dict:
    """A fresh controls dict for M.Agent. Called once per run."""
    return RB.hardened()
