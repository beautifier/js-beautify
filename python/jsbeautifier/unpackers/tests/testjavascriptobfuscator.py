#
# Tests for JavaScriptObfuscator unpacker
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

import unittest
from jsbeautifier.unpackers.javascriptobfuscator import unpack, detect, smartsplit

class TestJavascriptObfuscator(unittest.TestCase):
    def test_smartsplit(self):
        split = smartsplit
        equals = lambda data, result: self.assertEqual(split(data), result)

        equals('', [])
        equals('"a", "b"', ['"a"', '"b"'])
        equals('"aaa","bbbb"', ['"aaa"', '"bbbb"'])
        equals('"a", "b\\\""', ['"a"', '"b\\\""'])

    def test_detect(self):
        positive = lambda source: detect(source)
        negative = lambda source: not positive(source)

        negative('');
        negative('abcd')
        negative('var _0xaaaa')
        positive('var _0xaaaa = ["a", "b"]')
        positive('var _0xaaaa=["a", "b"]')
        positive('var _0x1234=["a","b"]')

    def test_unpack(self):
        decodeto = lambda obf, original: self.assertEqual(unpack(obf), original)

        decodeto('var _0x8df3=[];var a=10;', 'var a=10;')
        decodeto('var _0xb2a7=["\x74\x27\x65\x73\x74"];var i;for(i=0;i<10;++i){alert(_0xb2a7[0]);} ;',
                 'var i;for(i=0;i<10;++i){alert("t\'est");} ;')

if __name__ == '__main__':
    unittest.main()
