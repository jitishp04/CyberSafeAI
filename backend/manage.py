#!/usr/bin/env python
# Import necessary modules and classes
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory (project root) and add it to the Python path
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, parent_dir)  # Add the parent directory to the Python path

    # Set the default settings module for Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# Entry point for the script
if __name__ == '__main__':
    main()
