#
# Tests for MyObfuscate unpacker
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

import unittest
from jsbeautifier.unpackers.myobfuscate import detect, unpack

class TestMyObfuscate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('test-myobfuscate-input.js', 'r') as data:
            cls.input = data.read()
        with open('test-myobfuscate-output.js', 'r') as data:
            cls.output = data.read()

    def test_detect(self):
        detected = lambda source: self.assertTrue(detect(source))

        detected(self.input)

    def test_unpack(self):
        check = lambda inp, out: self.assertEqual(unpack(inp), out)

        check(self.input, self.output)

if __name__ == '__main__':
    unittest.main()
