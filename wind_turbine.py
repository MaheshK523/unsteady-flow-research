"""Compatibility entry point for the original wind-turbine signal sketch."""

from unsteady_flow.cli import run_scenario


if __name__ == "__main__":
    result = run_scenario("wind", "artifacts")
    print(result)
