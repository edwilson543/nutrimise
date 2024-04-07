#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""
# Standard library imports
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reciply.config.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")

    # Third party imports
    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
