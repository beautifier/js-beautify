import re
import unittest
from ...core.inputscanner import InputScanner


class TestInputScanner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.value = 'howdy'
        self.inputscanner = InputScanner(self.value)

    def test_new(self):
        inputscanner = InputScanner(None)
        self.assertEqual(inputscanner.hasNext(), False)

    def test_next(self):
        self.assertEqual(self.inputscanner.next(), self.value[0])
        self.assertEqual(self.inputscanner.next(), self.value[1])

    def test_peek(self):
        self.assertEqual(self.inputscanner.peek(3), self.value[3])
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(3), self.value[4])

    def test_no_param(self):
        self.assertEqual(self.inputscanner.peek(), self.value[0])
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(), self.value[1])

    def test_pattern(self):
        pattern = re.compile(r'how')
        index = 0
        self.assertEqual(self.inputscanner.test(pattern, index), True)
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.test(pattern, index), False)

    def test_Char(self):
        pattern = re.compile(r'o')
        index = 1
        self.assertEqual(self.inputscanner.testChar(pattern, index), True)


if __name__ == '__main__':
    unittest.main()
