from __future__ import annotations

import csv
import json
from pathlib import Path

from .signals import Signal
from .spectrum import Spectrum


def write_signal_csv(signal: Signal, path: str | Path) -> Path:
    target = Path(path)
