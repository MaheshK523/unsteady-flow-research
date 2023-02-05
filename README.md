# Unsteady Flow Signal Toolkit

A reproducible Python toolkit for learning and testing signal-analysis methods used
around unsteady-flow and aeroacoustic data.

The original repository contained four plotting sketches, including one file that was
not valid Python. The completed project turns those ideas into a tested package with
parameterized scenarios, physically labeled exports, normalized FFT and Welch
spectra, deterministic noise, command-line workflows, and headless plots.

> This is a reduced-order educational toolkit, not a CFD solver. The synthetic jet,
> wind, turbulence, and shock signals must not be presented as numerical flow
> solutions or experimental evidence.

## Quick start

```bash
python -m pip install -e .
python -m unsteady_flow jet --config configs/jet.json
python -m unsteady_flow shock --config configs/shock.json
python -m unittest discover -s tests -v
```

Each temporal scenario writes:

- `signal.csv` with coordinate and value units;
- `fft.csv` with a normalized one-sided amplitude spectrum;
- `welch.csv` with a window-energy-normalized power spectral density;
- `summary.json` with sample rate, RMS, peaks, and dominant frequencies;
- `analysis.png` with time- and frequency-domain views.

The shock scenario writes its spatial profile, estimated shock location, and plot.

## Scenarios

| Scenario | Model | Primary check |
|---|---|---|
| `turbulence` | seeded noisy tone | dominant-frequency recovery under noise |
| `jet` | exponentially damped acoustic tone | damping and high-rate sampling |
| `wind` | blade-passage tone + harmonic + broadband noise | tonal/harmonic separation |
| `shock` | smooth spatial jump + oscillatory disturbance | gradient-based position recovery |

Parameters may be supplied with a JSON configuration file. All generators validate
sample counts, units, positive parameters, and the Nyquist limit.

## Python API

```python
from unsteady_flow.analysis import summarize_temporal_signal
from unsteady_flow.signals import damped_tone

signal = damped_tone(frequency=5_000, damping_rate=500)
print(summarize_temporal_signal(signal))
```

## Repository map

```text
unsteady_flow/      supported generators, spectra, analysis, I/O, plots, and CLI
tests/              tone, shock, sampling, and artifact regression tests
configs/            reproducible example parameters
examples/           small Python API example
docs/               normalization details and scientific scope
*.py                compatibility entry points for the original demonstrations
.github/workflows/  CI across tests and a CLI smoke run
```
