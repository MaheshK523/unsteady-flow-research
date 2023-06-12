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
    blade_pass_frequency: float = 50.0,
    harmonic_ratio: float = 0.35,
    turbulence_std: float = 0.2,
    seed: int = 523,
) -> Signal:
    _validate_temporal(duration, sample_rate, blade_pass_frequency)
    rng = np.random.default_rng(seed)
    time = _time_axis(duration, sample_rate)
    periodic = np.sin(2 * np.pi * blade_pass_frequency * time)
    harmonic = harmonic_ratio * np.sin(2 * np.pi * 2 * blade_pass_frequency * time + 0.3)
    turbulence = rng.normal(0, turbulence_std, len(time))
    return Signal(time, periodic + harmonic + turbulence, "time", "s", "pressure fluctuation", "Pa")


def shock_interaction(
    points: int = 512,
    length: float = 1.0,
    shock_position: float = 0.5,
    wave_number: float = 4.0,
    shock_strength: float = 1.0,
    thickness: float = 0.012,
) -> Signal:
    if points < 32 or length <= 0 or not 0 < shock_position < length:
        raise ValueError("invalid spatial grid or shock position")
    if wave_number <= 0 or shock_strength <= 0 or thickness <= 0:
        raise ValueError("wave_number, shock_strength, and thickness must be positive")
    position = np.linspace(0, length, points)
    turbulence = 0.28 * np.sin(2 * np.pi * wave_number * position / length)
    smooth_shock = 0.5 * shock_strength * (1 + np.tanh((position - shock_position) / thickness))
    return Signal(position, turbulence + smooth_shock, "position", "m", "normalized velocity", "1")


def _time_axis(duration: float, sample_rate: float) -> np.ndarray:
    points = int(round(duration * sample_rate))
    if points < 8:
        raise ValueError("duration and sample_rate must produce at least eight samples")
    return np.arange(points, dtype=np.float64) / sample_rate


def _validate_temporal(duration: float, sample_rate: float, frequency: float) -> None:
    if duration <= 0 or sample_rate <= 0 or frequency <= 0:
        raise ValueError("duration, sample_rate, and frequency must be positive")
    if frequency >= sample_rate / 2:
        raise ValueError("frequency must be below the Nyquist frequency")
