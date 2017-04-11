import unittest


class AbstrTest(unittest.TestCase):

    @staticmethod
    def success(func_name):
        print "[PASS] Test: " + func_name

    @staticmethod
    def failure(func_name):
        print "[FAIL] Test: " + func_name
        