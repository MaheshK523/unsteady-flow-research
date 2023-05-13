from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Signal:
    coordinate: np.ndarray
    values: np.ndarray
    coordinate_name: str
