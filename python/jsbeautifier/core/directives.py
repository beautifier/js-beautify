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


class Directives:
    def __init__(self, start_block_pattern, end_block_pattern):

        self.__directives_block_pattern = re.compile(
            start_block_pattern + r" beautify( \w+[:]\w+)+ " + end_block_pattern
        )
        self.__directive_pattern = re.compile(r" (\w+)[:](\w+)")

        self.__directives_end_ignore_pattern = re.compile(
            start_block_pattern + r"\sbeautify\signore:end\s" + end_block_pattern
        )

    def get_directives(self, text):
        if not self.__directives_block_pattern.match(text):
            return None

        directives = {}
        directive_match = self.__directive_pattern.search(text)

        while directive_match:
            directives[directive_match.group(1)] = directive_match.group(2)
            directive_match = self.__directive_pattern.search(
                text, directive_match.end()
            )

        return directives

    def readIgnored(self, input):
        return input.readUntilAfter(self.__directives_end_ignore_pattern)
