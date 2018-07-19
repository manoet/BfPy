import unittest
from . import tests

suite = unittest.TestLoader().loadTestsFromTestCase(tests.BfPyTest)
unittest.TextTestRunner(verbosity=1).run(suite)
