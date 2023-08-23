from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .signals import Signal
from .spectrum import Spectrum


def plot_signal_and_spectrum(signal: Signal, spectrum: Spectrum, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
    axes[0].plot(signal.coordinate, signal.values, color="#1565c0", linewidth=1.1)
    axes[0].set_xlabel(f"{signal.coordinate_name} ({signal.coordinate_unit})")
    axes[0].set_ylabel(f"{signal.value_name} ({signal.value_unit})")
    axes[0].grid(alpha=0.25)
    axes[1].plot(spectrum.frequency, spectrum.magnitude, color="#ef6c00", linewidth=1.1)
    axes[1].set_xlabel("frequency (Hz)")
    axes[1].set_ylabel(f"{spectrum.kind} ({spectrum.unit})")
