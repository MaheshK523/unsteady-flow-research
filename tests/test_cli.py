import tempfile
import unittest
from pathlib import Path

from unsteady_flow.cli import run_scenario


class CliTests(unittest.TestCase):
    def test_jet_scenario_writes_reproducible_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            summary = run_scenario("jet", directory, {"frequency": 2000, "sample_rate": 40000, "duration": 0.02})
            root = Path(directory) / "jet"
