#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

"""Tests for urlencoded unpacker."""

import unittest

from jsbeautifier.unpackers.urlencode import detect, unpack

# pylint: disable=R0904
class TestUrlencode(unittest.TestCase):
    """urlencode test case."""
    def test_detect(self):
        """Test detect() function."""
        encoded = lambda source: self.assertTrue(detect(source))
        unencoded = lambda source: self.assertFalse(detect(source))

        unencoded('')
        unencoded('var a = b')
        encoded('var%20a+=+b')
        encoded('var%20a=b')
        encoded('var%20%21%22')

    def test_unpack(self):
        """Test unpack function."""
        equals = lambda source, result: self.assertEqual(unpack(source), result)

        equals('', '')
        equals('abcd', 'abcd')
        equals('var a = b', 'var a = b')
        equals('var%20a=b', 'var a=b')
        equals('var%20a+=+b', 'var a = b')

if __name__ == '__main__':
    unittest.main()
