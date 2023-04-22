# Methodology and scope

This package demonstrates signal-analysis techniques with reduced-order synthetic
models. It does not solve the Navier–Stokes equations and is not a CFD code.

## Spectral normalization

`one_sided_fft` removes the mean, applies a Hann window, divides by the coherent
gain, and doubles positive-frequency amplitudes except DC and the Nyquist bin. A
unit-amplitude bin-centered sine therefore recovers approximately unit amplitude.

`welch_psd` divides each windowed periodogram by sample rate and window energy,
doubles the appropriate positive-frequency bins, and averages overlapping segments.
The result is reported in value-unit squared per hertz.

## Synthetic scenarios

- `turbulence`: a seeded noisy sinusoid for testing spectral recovery;
