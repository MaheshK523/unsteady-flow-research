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
