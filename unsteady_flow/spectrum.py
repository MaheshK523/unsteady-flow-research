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
        if not np.any(mask):
            raise ValueError("minimum_frequency is outside the spectrum")
        frequency = self.frequency[mask]
        magnitude = self.magnitude[mask]
        return float(frequency[int(np.argmax(magnitude))])


def one_sided_fft(signal: Signal, detrend: bool = True, window: str = "hann") -> Spectrum:
    values = signal.values.astype(np.float64)
    if detrend:
        values = values - np.mean(values)
    weights = _window(window, len(values))
