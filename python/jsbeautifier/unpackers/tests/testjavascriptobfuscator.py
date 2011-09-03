#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

"""Tests for JavaScriptObfuscator unpacker."""

import unittest
from jsbeautifier.unpackers.javascriptobfuscator import (
    unpack, detect, smartsplit)

# pylint: disable=R0904
class TestJavascriptObfuscator(unittest.TestCase):
    """JavascriptObfuscator.com test case."""
    def test_smartsplit(self):
        """Test smartsplit() function."""
        split = smartsplit
        equals = lambda data, result: self.assertEqual(split(data), result)

        equals('', [])
        equals('"a", "b"', ['"a"', '"b"'])
        equals('"aaa","bbbb"', ['"aaa"', '"bbbb"'])
        equals('"a", "b\\\""', ['"a"', '"b\\\""'])

    def test_detect(self):
        """Test detect() function."""
        positive = lambda source: self.assertTrue(detect(source))
        negative = lambda source: self.assertFalse(detect(source))

        negative('')
        negative('abcd')
        negative('var _0xaaaa')
        positive('var _0xaaaa = ["a", "b"]')
        positive('var _0xaaaa=["a", "b"]')
        positive('var _0x1234=["a","b"]')

    def test_unpack(self):
        """Test unpack() function."""
        decodeto = lambda ob, original: self.assertEqual(unpack(ob), original)

        decodeto('var _0x8df3=[];var a=10;', 'var a=10;')
        decodeto('var _0xb2a7=["\x74\x27\x65\x73\x74"];var i;for(i=0;i<10;++i)'
                 '{alert(_0xb2a7[0]);} ;', 'var i;for(i=0;i<10;++i){alert'
                 '("t\'est");} ;')

if __name__ == '__main__':
    unittest.main()
