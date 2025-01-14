# Import necessary modules and classes
# tests.py
import unittest
import os

def load_tests(loader, tests, pattern):
    """Discover and load all unit tests in the `tests/` directory."""
    suite = unittest.TestSuite()
    # Discover tests in the tests/ folder
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')

    # Discover all test files matching the pattern "test_*.py" in the `tests/` directory
    discovered_tests = loader.discover(start_dir=test_dir, pattern="test_*.py")

    # Add the discovered tests to the suite
    suite.addTests(discovered_tests)
    return suite
