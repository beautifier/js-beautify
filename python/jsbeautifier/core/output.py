# The MIT License (MIT)
#
# Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.
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

# Using object instead of string to allow for later expansion of info about each line
class OutputLine:
    def __init__(self, parent):
        self.__parent = parent
        self.__character_count = 0
        self.__indent_count = -1

        self.__items = []
        self.__empty = True

    def get_character_count(self):
        return self.__character_count

    def is_empty(self):
        return self.__empty

    def set_indent(self, level):
        self.__character_count = self.__parent.baseIndentLength + level * self.__parent.indent_length
        self.__indent_count = level;

    def last(self):
        if not self.is_empty():
            return self.__items[-1]
        else:
            return None

    def push(self, input):
        self.__items.append(input)
        self.__character_count += len(input)
        self.__empty = False


    def pop(self):
        item = None
        if not self.is_empty():
            item = self.__items.pop()
            self.__character_count -= len(item)
            self.__empty = len(self.__items) == 0
        return item

    def remove_indent(self):
        if self.__indent_count > 0:
            self.__indent_count -= 1
            self.__character_count -= self.__parent.indent_length

    def trim(self):
        while self.last() == ' ':
            item = self._items.pop()
            self.__character_count -= 1
        self.__empty = len(self.__items) == 0

    def toString(self):
        result = ''
        if not self.is_empty():
            if self.__indent_count >= 0:
                result = self.__parent.indent_cache[self.__indent_count]
            result += ''.join(self.__items)
        return result


class Output:
    def __init__(self, indent_string, baseIndentString = ''):

        self.indent_string = indent_string
        self.baseIndentString = baseIndentString
        self.indent_cache = [ baseIndentString ]
        self.baseIndentLength = len(baseIndentString)
        self.indent_length = len(indent_string)
        self.raw = False
        self.lines = []
        self.previous_line = None
        self.current_line = None
        self.space_before_token = False
        self.add_outputline()

    def add_outputline(self):
        self.previous_line = self.current_line
        self.current_line = OutputLine(self)
        self.lines.append(self.current_line)

    def get_line_number(self):
        return len(self.lines)

    def add_new_line(self, force_newline=False):
        if len(self.lines) == 1 and self.just_added_newline():
            # no newline on start of file
            return False

        if force_newline or not self.just_added_newline():
            if not self.raw:
                self.add_outputline()
            return True
        return False

    def get_code(self, end_with_newline, eol):
        sweet_code = "\n".join(line.toString() for line in self.lines)
        sweet_code = re.sub('[\r\n\t ]+$', '', sweet_code)

        if end_with_newline:
            sweet_code += '\n'

        if not eol == '\n':
            sweet_code = sweet_code.replace('\n', eol)

        return sweet_code

    def set_indent(self, level):
        # Never indent your first output indent at the start of the file
        if len(self.lines) > 1:
            while level >= len(self.indent_cache):
                self.indent_cache.append(self.indent_cache[-1] + self.indent_string)


            self.current_line.set_indent(level)
            return True
        self.current_line.set_indent(0)
        return False

    def add_raw_token(self, token):
        for _ in range(token.newlines):
            self.add_outputline()

        self.current_line.push(token.whitespace_before)
        self.current_line.push(token.text)
        self.space_before_token = False

    def add_token(self, printable_token):
        self.add_space_before_token()
        self.current_line.push(printable_token)

    def add_space_before_token(self):
        if self.space_before_token and not self.just_added_newline():
            self.current_line.push(' ')
        self.space_before_token = False

    def trim(self, eat_newlines = False):
        self.current_line.trim()

        while eat_newlines and len(self.lines) > 1 and self.current_line.is_empty():
            self.lines.pop()
            self.current_line = self.lines[-1]
            self.current_line.trim()

        if len(self.lines) > 1:
            self.previous_line = self.lines[-2]
        else:
            self.previous_line = None

    def just_added_newline(self):
        return self.current_line.is_empty()

    def just_added_blankline(self):
        if self.just_added_newline():
            if len(self.lines) == 1:
                return True

            line = self.lines[-2]
            return line.is_empty()

        return False
