import unittest
test_suite = unittest.TestLoader().discover('tests_e2e')
unittest.TextTestRunner(verbosity=2).run(test_suite)