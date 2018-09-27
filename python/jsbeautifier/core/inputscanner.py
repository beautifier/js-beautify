# The MIT License (MIT)
#
# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class InputScanner:
    def __init__(self, input_string):
        if input_string is None:
            input_string = ''
        self.__input = input_string
        self.__input_length = len(self.__input)
        self.__position = 0

    def restart(self):
        self.__position = 0

    def back(self):
        if self.__position > 0:
            self.__position -= 1

    def hasNext(self):
        return self.__position < self.__input_length

    def next(self):
        val = None
        if self.hasNext():
            val = self.__input[self.__position]
            self.__position += 1

        return val

    def peek(self, index=0):
        val = None
        index += self.__position
        if index >= 0 and index < self.__input_length:
            val = self.__input[index]

        return val

    def test(self, pattern, index=0):
        index += self.__position
        return index >= 0 and index < self.__input_length and bool(
            pattern.match(self.__input, index))

    def testChar(self, pattern, index=0):
        # test one character regex match
        val = self.peek(index)
        return val is not None and bool(pattern.match(val))

    def match(self, pattern):
        pattern_match = None
        if self.hasNext():
            pattern_match = pattern.match(self.__input, self.__position)
            if bool(pattern_match):
                self.__position = pattern_match.end(0)
        return pattern_match

    def read(self, pattern):
        val = ''
        pattern_match = self.match(pattern)
        if bool(pattern_match):
            val = pattern_match.group(0)
        return val

    def readUntil(self, pattern, include_match=False):
        val = ''
        pattern_match = None
        match_index = self.__position
        if self.hasNext():
            pattern_match = pattern.search(self.__input, self.__position)
            if bool(pattern_match):
                if include_match:
                    match_index = pattern_match.end(0)
                else:
                    match_index = pattern_match.start(0)
            else:
                match_index = self.__input_length

            val = self.__input[self.__position:match_index]
            self.__position = match_index

        return val

    def readUntilAfter(self, pattern):
        return self.readUntil(pattern, include_match=True)

    # css beautifier legacy helpers
    def peekUntilAfter(self, pattern):
        start = self.__position
        val = self.readUntilAfter(pattern)
        self.__position = start
        return val

    def lookBack(self, testVal):
        start = self.__position - 1
        return start >= len(testVal) and \
            self.__input[start - len(testVal):start].lower() == testVal
