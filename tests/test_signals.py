import unittest

import numpy as np

from unsteady_flow.analysis import estimate_shock_position
from unsteady_flow.signals import Signal, damped_tone, shock_interaction


class SignalTests(unittest.TestCase):
    def test_rejects_frequency_above_nyquist(self):
        with self.assertRaisesRegex(ValueError, "Nyquist"):
            damped_tone(sample_rate=1000, frequency=600)
