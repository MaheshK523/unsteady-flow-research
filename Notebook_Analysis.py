"""Compatibility entry point for the original turbulence demonstration."""

from unsteady_flow.cli import run_scenario


if __name__ == "__main__":
    result = run_scenario("turbulence", "artifacts")
    print(result)
