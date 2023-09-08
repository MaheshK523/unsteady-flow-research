from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .signals import Signal


@dataclass(frozen=True)
class Spectrum:
    frequency: np.ndarray
    magnitude: np.ndarray
    kind: str
    unit: str

    def dominant_frequency(self, minimum_frequency: float = 0.0) -> float:
        mask = self.frequency >= minimum_frequency
