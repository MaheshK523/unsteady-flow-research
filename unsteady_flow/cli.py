from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import estimate_shock_position, summarize_temporal_signal
from .io import write_json, write_signal_csv, write_spectrum_csv
from .plots import plot_signal_and_spectrum, plot_spatial_signal
from .signals import damped_tone, shock_interaction, turbulent_tone, wind_turbine_signal
from .spectrum import one_sided_fft, welch_psd


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="unsteady-flow", description="Reduced-order unsteady-flow signal experiments")
    parser.add_argument("scenario", choices=["turbulence", "jet", "wind", "shock"])
    parser.add_argument("--output", default="artifacts")
    parser.add_argument("--config", help="JSON object of scenario parameters")
    parser.add_argument("--seed", type=int, default=523)
    parser.add_argument("--welch-segment", type=int, default=256)
    return parser


def run_scenario(
