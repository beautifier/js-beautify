#!/usr/bin/env python

import sys
import unittest


def run_tests():
    suite = unittest.TestLoader().discover(
        'jsbeautifier', pattern="test*.py")
    suite.addTests(unittest.TestLoader().discover(
        'cssbeautifier', pattern="test*.py"))
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    sys.exit(not run_tests().wasSuccessful())
