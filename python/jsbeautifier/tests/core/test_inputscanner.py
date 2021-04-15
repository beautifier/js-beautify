import re
import unittest
from ...core.inputscanner import InputScanner


class TestInputScanner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.value = "howdy"
        self.inputscanner = InputScanner(self.value)

    def test_new(self):
        inputscanner = InputScanner(None)
        self.assertEqual(inputscanner.hasNext(), False)

    def test_next(self):
        self.assertEqual(self.inputscanner.next(), self.value[0])
        self.assertEqual(self.inputscanner.next(), self.value[1])

        # should return None if index is at then end of the value
        pattern = re.compile(r"howdy")
        self.inputscanner.readUntilAfter(pattern)
        self.assertEqual(self.inputscanner.next(), None)

    def test_peek(self):
        self.assertEqual(self.inputscanner.peek(3), self.value[3])
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(3), self.value[4])

        # should return None if index is less than 0 or greater than text length
        self.assertEqual(self.inputscanner.peek(-2), None)
        self.assertEqual(self.inputscanner.peek(5), None)

    def test_no_param(self):
        self.assertEqual(self.inputscanner.peek(), self.value[0])
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(), self.value[1])

    def test_pattern(self):
        pattern = re.compile(r"how")
        index = 0
        self.assertEqual(self.inputscanner.test(pattern, index), True)
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.test(pattern, index), False)

    def test_Char(self):
        pattern = re.compile(r"o")
        index = 1
        self.assertEqual(self.inputscanner.testChar(pattern, index), True)

    def test_restart(self):
        # should reset index to 0
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(), self.value[1])
        self.inputscanner.restart()
        self.assertEqual(self.inputscanner.peek(), self.value[0])

    def test_back(self):
        # should move the index one place back if current position is not 0
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.peek(), self.value[1])
        self.inputscanner.back()
        self.assertEqual(self.inputscanner.peek(), self.value[0])

        # should not move the index back if current position is 0
        self.inputscanner.back()
        self.assertEqual(self.inputscanner.peek(), self.value[0])

    def test_hasNext(self):
        # should return true if index is not at the last position
        pattern = re.compile(r"howd")
        self.inputscanner.readUntilAfter(pattern)
        self.assertEqual(self.inputscanner.hasNext(), True)

        # should return false if index is at the last position
        self.inputscanner.next()
        self.assertEqual(self.inputscanner.hasNext(), False)

    def test_match(self):
        # should return details of pattern match and move index to next position
        pattern = re.compile(r"how")
        patternmatch = self.inputscanner.match(pattern)
        self.assertEqual(self.inputscanner.peek(), self.value[3])
        self.assertNotEqual(patternmatch, None)
        self.assertEqual(patternmatch.group(0), "how")

        self.inputscanner.restart()

        # should return None and not move index if there is no match
        pattern = re.compile(r"test")
        patternmatch = self.inputscanner.match(pattern)
        self.assertEqual(self.inputscanner.peek(), self.value[0])
        self.assertEqual(patternmatch, None)

    def test_read(self):
        # should return the matched substring
        pattern = re.compile(r"how")
        patternmatch = self.inputscanner.read(pattern)
        self.assertEqual(patternmatch, "how")

        self.inputscanner.restart()

        # should return the empty string if there is no match
        pattern = re.compile(r"ow")
        patternmatch = self.inputscanner.read(pattern)
        self.assertEqual(patternmatch, "")

        self.inputscanner.restart()

        # should return substring from start to until pattern when unitilAfter is true
        startPattern = re.compile(r"how")
        untilPattern = re.compile(r"dy")
        untilAfter = True
        patternmatch = self.inputscanner.read(startPattern, untilPattern, untilAfter)
        self.assertEqual(patternmatch, "howdy")

        self.inputscanner.restart()

        # should return the substring matched for startPattern when untilPattern is given but unitilAfter is false
        startPattern = re.compile(r"how")
        untilPattern = re.compile(r"dy")
        untilAfter = False
        patternmatch = self.inputscanner.read(startPattern, untilPattern, untilAfter)
        self.assertEqual(patternmatch, "how")

        self.inputscanner.restart()

        # should return substring matched for untilPattern when startPattern is None
        startPattern = None
        untilPattern = re.compile(r"how")
        untilAfter = True
        patternmatch = self.inputscanner.read(startPattern, untilPattern, untilAfter)

        self.inputscanner.restart()

        # should return substring matched for untilPattern when startPattern is None and untilAfter is false
        startPattern = None
        untilPattern = re.compile(r"how")
        untilAfter = False
        patternmatch = self.inputscanner.read(startPattern, untilPattern, untilAfter)
        self.assertEqual(patternmatch, "")

    def test_readUntil(self):
        # should return substring matched for pattern when untilAfter is true
        pattern = re.compile(r"how")
        untilAfter = True
        patternmatch = self.inputscanner.readUntil(pattern, untilAfter)
        self.assertEqual(patternmatch, "how")

        self.inputscanner.restart()

        # should return substring from index 0 to start index of matched substring when untilAfter is false
        pattern = re.compile(r"wd")
        untilAfter = False
        patternmatch = self.inputscanner.readUntil(pattern, untilAfter)
        self.assertEqual(patternmatch, "ho")

        self.inputscanner.restart()

        # should return empty string when start index of matched substring is 0 and untilAfter is false
        pattern = re.compile(r"how")
        untilAfter = False
        patternmatch = self.inputscanner.readUntil(pattern, untilAfter)
        self.assertEqual(patternmatch, "")

    def test_readUntilAfter(self):
        # should return matched substring
        pattern = re.compile(r"how")
        patternmatch = self.inputscanner.readUntilAfter(pattern)
        self.assertEqual(patternmatch, "how")

    def test_get_regexp(self):
        # should return regex pattern for string passed
        pattern = re.compile(r"ow")
        self.assertEqual(self.inputscanner.get_regexp("ow"), pattern)

    def test_peekUntilAfter(self):
        # should return matched substring and retain index position
        pattern = re.compile(r"how")
        self.assertEqual(self.inputscanner.peek(), self.value[0])
        self.assertEqual(self.inputscanner.peekUntilAfter(pattern), "how")
        self.assertEqual(self.inputscanner.peek(), self.value[0])

    def test_lookBack(self):
        # should return whether testVal is obtained by shifting index to the left
        testVal = "how"
        pattern = re.compile(r"howd")
        self.inputscanner.readUntilAfter(pattern)
        self.assertEqual(self.inputscanner.lookBack(testVal), True)
        testVal = "ho"
        self.assertEqual(self.inputscanner.lookBack(testVal), False)


if __name__ == "__main__":
    unittest.main()
