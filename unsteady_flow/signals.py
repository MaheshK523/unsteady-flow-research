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
