#
# Tests for MyObfuscate unpacker
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

import unittest
import os
from jsbeautifier.unpackers.myobfuscate import detect, unpack
from jsbeautifier.unpackers.tests import __path__ as path

class TestMyObfuscate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(path[0], 'test-myobfuscate-input.js'), 'r') as data:
            cls.input = data.read()
        with open(os.path.join(path[0], 'test-myobfuscate-output.js'), 'r') as data:
            cls.output = data.read()

    def test_detect(self):
        detected = lambda source: self.assertTrue(detect(source))

        detected(self.input)

    def test_unpack(self):
        check = lambda inp, out: self.assertEqual(unpack(inp), out)

        check(self.input, self.output)

if __name__ == '__main__':
    unittest.main()
