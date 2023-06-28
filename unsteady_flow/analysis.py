from __future__ import annotations

import numpy as np

from .signals import Signal
from .spectrum import one_sided_fft, welch_psd


def summarize_temporal_signal(signal: Signal, welch_segment: int | None = None) -> dict[str, float | int | str]:
    segment = welch_segment or min(256, len(signal.values))
    spectrum = one_sided_fft(signal)
    psd = welch_psd(signal, segment_length=segment)
    return {
        "samples": len(signal.values),
        "duration": float(signal.coordinate[-1] - signal.coordinate[0]),
        "sample_rate_hz": 1.0 / signal.sample_spacing,
        "mean": float(np.mean(signal.values)),
        "rms": float(np.sqrt(np.mean(signal.values**2))),
        "peak_absolute": float(np.max(np.abs(signal.values))),
        "dominant_fft_hz": spectrum.dominant_frequency(minimum_frequency=1e-12),
        "dominant_welch_hz": psd.dominant_frequency(minimum_frequency=1e-12),
        "value_unit": signal.value_unit,
    }


def estimate_shock_position(signal: Signal) -> dict[str, float]:
    if signal.coordinate_name != "position":
        raise ValueError("shock estimation requires a spatial signal")
    gradient = np.gradient(signal.values, signal.coordinate)
    index = int(np.argmax(np.abs(gradient)))
