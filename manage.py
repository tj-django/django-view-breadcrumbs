#!/usr/bin/env python
import sys

if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
        from conftest import pytest_configure
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    pytest_configure()
    execute_from_command_line(sys.argv)
