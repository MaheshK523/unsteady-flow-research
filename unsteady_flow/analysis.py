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
