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

import re
from ..core.pattern import Pattern

__all__ = ["WhitespacePattern"]


class WhitespacePattern(Pattern):
    def __init__(self, input_scanner, parent=None):
        Pattern.__init__(self, input_scanner, parent)

        if parent is not None:
            self._newline_regexp = \
                self._input.get_regexp(parent._newline_regexp)
        else:
            self.__set_whitespace_patterns('', '')

        self.newline_count = 0
        self.whitespace_before_token = ''

    def __set_whitespace_patterns(self, whitespace_chars, newline_chars):
        whitespace_chars += '\\t '
        newline_chars += '\\n\\r'

        self._match_pattern = self._input.get_regexp(
            '[' + whitespace_chars + newline_chars + ']+')
        self._newline_regexp = self._input.get_regexp(
            '\\r\\n|[' + newline_chars + ']')


    def read(self):
        self.newline_count = 0
        self.whitespace_before_token = ''

        resulting_string = self._input.read(self._match_pattern)
        if resulting_string == ' ':
            self.whitespace_before_token = ' '
        elif bool(resulting_string):
            lines = self._newline_regexp.split(resulting_string)
            self.newline_count = len(lines) - 1
            self.whitespace_before_token = lines[-1]

        return resulting_string


    def matching(self, whitespace_chars, newline_chars):
        result = self._create()
        result.__set_whitespace_patterns(whitespace_chars, newline_chars)
        result._update()
        return result

    def _create(self):
        return WhitespacePattern(self._input, self)


