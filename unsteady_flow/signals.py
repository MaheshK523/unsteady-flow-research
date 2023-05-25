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
            raise ValueError("signal coordinate must be strictly increasing")

    @property
    def sample_spacing(self) -> float:
        spacing = np.diff(self.coordinate)
        if not np.allclose(spacing, spacing[0], rtol=1e-6, atol=1e-12):
            raise ValueError("spectral analysis requires uniform sample spacing")
        return float(spacing[0])


def turbulent_tone(
    duration: float = 1.0,
    sample_rate: float = 500.0,
    frequency: float = 10.0,
    noise_std: float = 0.5,
    seed: int = 523,
) -> Signal:
    _validate_temporal(duration, sample_rate, frequency)
    rng = np.random.default_rng(seed)
    time = _time_axis(duration, sample_rate)
    values = np.sin(2 * np.pi * frequency * time) + rng.normal(0, noise_std, len(time))
    return Signal(time, values, "time", "s", "velocity fluctuation", "m/s")


def damped_tone(
    duration: float = 0.01,
    sample_rate: float = 100_000.0,
    frequency: float = 5_000.0,
    damping_rate: float = 500.0,
    amplitude: float = 1.0,
) -> Signal:
    _validate_temporal(duration, sample_rate, frequency)
    if damping_rate < 0 or amplitude <= 0:
        raise ValueError("damping_rate must be non-negative and amplitude must be positive")
    time = _time_axis(duration, sample_rate)
    values = amplitude * np.sin(2 * np.pi * frequency * time) * np.exp(-damping_rate * time)
    return Signal(time, values, "time", "s", "pressure fluctuation", "Pa")


def wind_turbine_signal(
    duration: float = 2.0,
    sample_rate: float = 2_000.0,
