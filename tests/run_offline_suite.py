"""Run unittest tests plus upstream's fixture-free test_fan_curve functions."""
import importlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "tests"))
suite = unittest.defaultTestLoader.discover("tests")
fan = importlib.import_module("test_fan_curve")
for name, function in sorted(vars(fan).items()):
    if name.startswith("test_") and callable(function):
        suite.addTest(unittest.FunctionTestCase(function))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
