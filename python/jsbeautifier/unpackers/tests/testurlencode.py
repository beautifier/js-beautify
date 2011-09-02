#
# Tests for urlencoded unpacker
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

import unittest

from jsbeautifier.unpackers.urlencode import detect, unpack

class TestUrlencode(unittest.TestCase):
    def test_detect(self):
        encoded = lambda source: self.assertTrue(detect(source))
        unencoded = lambda source: self.assertFalse(detect(source))

        unencoded('')
        unencoded('var a = b')
        encoded('var%20a+=+b')
        encoded('var%20a=b')
        encoded('var%20%21%22')

    def test_unpack(self):
        equals = lambda source, result: self.assertEqual(unpack(source), result)

        equals('', '')
        equals('abcd', 'abcd')
        equals('var a = b', 'var a = b')
        equals('var%20a=b', 'var a=b')
        equals('var%20a+=+b', 'var a = b')

if __name__ == '__main__':
    unittest.main()
