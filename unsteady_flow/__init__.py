"""Reduced-order signal models for unsteady-flow education and experiments."""

from .signals import Signal, damped_tone, shock_interaction, turbulent_tone, wind_turbine_signal
from .spectrum import Spectrum, one_sided_fft, welch_psd

__all__ = [
    "Signal",
    "Spectrum",
    "damped_tone",
    "one_sided_fft",
    "shock_interaction",
    "turbulent_tone",
