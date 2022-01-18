import os
import subprocess
import sys
from typing import Dict, List, Optional


def main(run_formatters: bool = False):
    def run_command(command: List[str], env: Optional[Dict[str, str]] = None):
        joined_command = " ".join(command)
        working_env = os.environ.copy()

        if env is None:
            print(f"> {joined_command}")
            return subprocess.run(command, check=True, env=working_env, shell=True)

        for name, value in env.items():
            working_env[name] = value
        print(f"> {joined_command}  {env}")
        return subprocess.run(command, check=True, env=working_env, shell=True)

    if run_formatters:
        run_command(["python", "-m", "black", "."])
        run_command(["python", "-m", "isort", "."])
        return run_command(["python", "-m", "pytest", "--black", "--isort", "--pylint", "--mypy", "--cov", "."])
    return run_command(["python", "-m", "pytest", "."])


if __name__ == "__main__":
    test_only = len(sys.argv) >= 2 and sys.argv[1] == "test_only"
    main(run_formatters=not test_only)
