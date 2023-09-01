from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .signals import Signal


@dataclass(frozen=True)
class Spectrum:
    frequency: np.ndarray
