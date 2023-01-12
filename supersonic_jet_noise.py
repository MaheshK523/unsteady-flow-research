"""Compatibility entry point for the original damped jet-tone sketch."""

from unsteady_flow.cli import run_scenario


if __name__ == "__main__":
    result = run_scenario("jet", "artifacts")
    print(result)
