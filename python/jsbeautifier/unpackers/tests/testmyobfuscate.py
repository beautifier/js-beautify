#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

"""Tests for MyObfuscate unpacker."""

import unittest
import os
from jsbeautifier.unpackers.myobfuscate import detect, unpack
from jsbeautifier.unpackers.tests import __path__ as path

INPUT = os.path.join(path[0], "test-myobfuscate-input.js")
OUTPUT = os.path.join(path[0], "test-myobfuscate-output.js")

# pylint: disable=R0904


class TestMyObfuscate(unittest.TestCase):
    # pylint: disable=C0103
    """MyObfuscate obfuscator testcase."""

    @classmethod
    def setUpClass(cls):
        """Load source files (encoded and decoded version) for tests."""
        with open(INPUT, "r") as data:
            cls.input = data.read()
        with open(OUTPUT, "r") as data:
            cls.output = data.read()

    def test_detect(self):
        """Test detect() function."""

        def detected(source):
            return self.assertTrue(detect(source))

        detected(self.input)

    def test_unpack(self):
        """Test unpack() function."""

        def check(inp, out):
            return self.assertEqual(unpack(inp), out)

        check(self.input, self.output)


if __name__ == "__main__":
    unittest.main()
