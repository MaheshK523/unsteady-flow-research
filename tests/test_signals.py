import unittest

import numpy as np

from unsteady_flow.analysis import estimate_shock_position
from unsteady_flow.signals import Signal, damped_tone, shock_interaction


class SignalTests(unittest.TestCase):
    def test_rejects_frequency_above_nyquist(self):
        with self.assertRaisesRegex(ValueError, "Nyquist"):
            damped_tone(sample_rate=1000, frequency=600)

    def test_shock_location_is_recovered(self):
        signal = shock_interaction(points=2048, shock_position=0.37, thickness=0.005)
        estimate = estimate_shock_position(signal)
        self.assertAlmostEqual(estimate["shock_position"], 0.37, delta=0.004)

    def test_nonuniform_sampling_is_rejected_for_spectrum(self):
        signal = Signal(np.array([0.0, 0.1, 0.21, 0.3]), np.ones(4), "time", "s", "value", "1")
        with self.assertRaisesRegex(ValueError, "uniform"):
            _ = signal.sample_spacing


