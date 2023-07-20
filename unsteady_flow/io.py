from __future__ import annotations

import csv
import json
from pathlib import Path

from .signals import Signal
from .spectrum import Spectrum


def write_signal_csv(signal: Signal, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([f"{signal.coordinate_name}_{signal.coordinate_unit}", f"{signal.value_name}_{signal.value_unit}"])
        writer.writerows(zip(signal.coordinate, signal.values, strict=True))
    return target


def write_spectrum_csv(spectrum: Spectrum, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["frequency_hz", f"{spectrum.kind}_{spectrum.unit}"])
        writer.writerows(zip(spectrum.frequency, spectrum.magnitude, strict=True))
    return target


