from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Signal:
    coordinate: np.ndarray
    values: np.ndarray
    coordinate_name: str
    coordinate_unit: str
    value_name: str
    value_unit: str

    def __post_init__(self) -> None:
        if self.coordinate.ndim != 1 or self.values.ndim != 1:
            raise ValueError("signal coordinate and values must be one-dimensional")
        if len(self.coordinate) != len(self.values) or len(self.values) < 4:
            raise ValueError("signal coordinate and values must be aligned with at least four samples")
        if not np.all(np.isfinite(self.coordinate)) or not np.all(np.isfinite(self.values)):
            raise ValueError("signal values must be finite")
        if np.any(np.diff(self.coordinate) <= 0):
