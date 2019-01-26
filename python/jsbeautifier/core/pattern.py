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

__all__ = ["Pattern"]

class Pattern:
    def __init__(self, input_scanner, parent=None):
        self._input = input_scanner
        self._starting_pattern = None
        self._match_pattern = None
        self._until_pattern = None
        self._until_after = False

        if parent is not None:
            self._starting_pattern = self._input.get_regexp(parent._starting_pattern)
            self._match_pattern = self._input.get_regexp(parent._match_pattern)
            self._until_pattern = self._input.get_regexp(parent._until_pattern)
            self._until_after = parent._until_after

    def read(self):
        result = self._input.read(self._starting_pattern)
        if (self._starting_pattern is None) or result:
            result += self._input.read(self._match_pattern,
                self._until_pattern, self._until_after)
        return result

    def read_match(self):
        return self._input.match(self._match_pattern)

    def until_after(self, pattern):
        result = self._create()
        result._until_after = True
        result._until_pattern = self._input.get_regexp(pattern)
        result._update()
        return result

    def until(self, pattern):
        result = self._create()
        result._until_after = False
        result._until_pattern = self._input.get_regexp(pattern)
        result._update()
        return result

    def starting_with(self, pattern):
        result = self._create()
        result._starting_pattern = self._input.get_regexp(pattern)
        result._update()
        return result

    def matching(self, pattern):
        result = self._create()
        result._match_pattern = self._input.get_regexp(pattern)
        result._update()
        return result

    def _create(self):
        return Pattern(self._input, self)

    def _update(self):
        pass

