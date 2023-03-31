import unittest

from unsteady_flow.signals import damped_tone, wind_turbine_signal
from unsteady_flow.spectrum import one_sided_fft, welch_psd


class SpectrumTests(unittest.TestCase):
    def test_fft_recovers_known_tone(self):
        signal = damped_tone(duration=0.1, sample_rate=20_000, frequency=1_250, damping_rate=10)
        dominant = one_sided_fft(signal).dominant_frequency(1)
        self.assertAlmostEqual(dominant, 1_250, delta=12)

