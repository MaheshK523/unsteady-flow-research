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
    scenario: str,
    output: str | Path,
    parameters: dict | None = None,
    seed: int = 523,
    welch_segment: int = 256,
) -> dict:
    params = dict(parameters or {})
    target = Path(output) / scenario
    if scenario == "turbulence":
        params.setdefault("seed", seed)
        signal = turbulent_tone(**params)
    elif scenario == "jet":
        signal = damped_tone(**params)
    elif scenario == "wind":
        params.setdefault("seed", seed)
        signal = wind_turbine_signal(**params)
    elif scenario == "shock":
        signal = shock_interaction(**params)
        summary = estimate_shock_position(signal)
        write_signal_csv(signal, target / "signal.csv")
        write_json(summary, target / "summary.json")
        plot_spatial_signal(signal, target / "signal.png")
        return summary
    else:
        raise ValueError(f"unsupported scenario: {scenario}")

    fft = one_sided_fft(signal)
    segment = min(welch_segment, len(signal.values))
    psd = welch_psd(signal, segment_length=segment)
    summary = summarize_temporal_signal(signal, welch_segment=segment)
    write_signal_csv(signal, target / "signal.csv")
    write_spectrum_csv(fft, target / "fft.csv")
    write_spectrum_csv(psd, target / "welch.csv")
    write_json(summary, target / "summary.json")
    plot_signal_and_spectrum(signal, fft, target / "analysis.png")
    return summary


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    parameters = json.loads(Path(args.config).read_text(encoding="utf-8")) if args.config else {}
    summary = run_scenario(args.scenario, args.output, parameters, args.seed, args.welch_segment)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
