"""Compatibility entry point for the original shock interaction sketch."""

from unsteady_flow.cli import run_scenario


if __name__ == "__main__":
    result = run_scenario("shock", "artifacts")
    print(result)
