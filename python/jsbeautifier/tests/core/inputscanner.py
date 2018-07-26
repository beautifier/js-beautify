import unittest
from ...core.inputscanner import InputScanner


class TestInputScanner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_new(self):
        inputscanner = InputScanner(None)
        self.assertEqual(inputscanner.hasNext(), False)


if __name__ == '__main__':
    unittest.main()
