import unittest
from openapi_server.test.test_analysis import run_tests_de, run_tests_en

suite_de = unittest.TestLoader().loadTestsFromModule(run_tests_de)
unittest.TextTestRunner(verbosity=2).run(suite_de)

suite_en = unittest.TestLoader().loadTestsFromModule(run_tests_en)
unittest.TextTestRunner(verbosity=2).run(suite_en)