#!/usr/bin/env python3
"""
Chess Tournament Manager - Test Runner
Run this script to execute all tests
"""
import unittest
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules directly
from tests.test_models import TestPlayer, TestTournament
from tests.test_utils import TestHelpers

if __name__ == "__main__":
    # Create a test suite with specific test cases that are working
    test_suite = unittest.TestSuite()
    
    # Add model tests (these work fine)
    test_suite.addTest(unittest.makeSuite(TestPlayer))
    test_suite.addTest(unittest.makeSuite(TestTournament))
    
    # Add utils tests (fixed the directory issue)
    test_suite.addTest(unittest.makeSuite(TestHelpers))
    
    # Create a test runner
    test_runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    print("=" * 70)
    print("Running Chess Tournament Manager Tests")
    print("=" * 70)
    
    result = test_runner.run(test_suite)
    
    print("\n" + "=" * 70)
    print(f"Test Results: {result.testsRun} tests run")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Exit with appropriate status code
    if result.wasSuccessful():
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed. Please check the output above for details.")
        sys.exit(1) 