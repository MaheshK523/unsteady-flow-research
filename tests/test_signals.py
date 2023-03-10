import unittest

import numpy as np

from unsteady_flow.analysis import estimate_shock_position
from unsteady_flow.signals import Signal, damped_tone, shock_interaction
