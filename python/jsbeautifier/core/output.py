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
import math

# Using object instead of string to allow for later expansion of info
# about each line

__all__ = ["Output"]


class OutputLine:
    def __init__(self, parent):
        self.__parent = parent
        self.__character_count = 0
        self.__indent_count = -1
        self.__alignment_count = 0

        self.__items = []

    def item(self, index):
        return self.__items[index]

    def is_empty(self):
        return len(self.__items) == 0

    def set_indent(self, indent=0, alignment=0):
        self.__indent_count = indent
        self.__alignment_count = alignment
        self.__character_count = self.__parent.get_indent_size(
            self.__indent_count, self.__alignment_count)

    def get_character_count(self):
        return self.__character_count

    def last(self):
        if not self.is_empty():
            return self.__items[-1]

        return None

    def push(self, item):
        self.__items.append(item)
        self.__character_count += len(item)

    def pop(self):
        item = None
        if not self.is_empty():
            item = self.__items.pop()
            self.__character_count -= len(item)
        return item

    def remove_indent(self):
        if self.__indent_count > 0:
            self.__indent_count -= 1
            self.__character_count -= self.__parent.indent_size

    def trim(self):
        while self.last() == ' ':
            self.__items.pop()
            self.__character_count -= 1

    def toString(self):
        result = ''
        if not self.is_empty():
            result = self.__parent.get_indent_string(
                self.__indent_count, self.__alignment_count)
            result += ''.join(self.__items)
        return result


class IndentStringCache:
    def __init__(self, options, base_string):
        self.__cache = ['']
        self.__indent_size = options.indent_size
        self.__indent_string = options.indent_char
        if not options.indent_with_tabs:
            self.__indent_string = options.indent_char * options.indent_size

        # Set to null to continue support of auto detection of base indent
        base_string = base_string or ''
        if options.indent_level > 0:
            base_string = options.indent_level * self.__indent_string

        self.__base_string = base_string
        self.__base_string_length = len(base_string)

    def get_indent_size(self, indent, column=0):
        result = self.__base_string_length
        if indent < 0:
            result = 0
        result += indent * self.__indent_size
        result += column
        return result

    def get_indent_string(self, indent_level, column=0):
        result = self.__base_string
        if indent_level < 0:
            indent_level = 0
            result = ''
        column += indent_level * self.__indent_size
        self.__ensure_cache(column)
        result += self.__cache[column]
        return result

    def __ensure_cache(self, column):
        while column >= len(self.__cache):
            self.__add_column()

    def __add_column(self):
        column = len(self.__cache)
        indent = 0
        result = ''
        if self.__indent_size and column >= self.__indent_size:
            indent = int(math.floor(column / self.__indent_size))
            column -= indent * self.__indent_size
            result = indent * self.__indent_string
        if column:
            result += column * ' '
        self.__cache.append(result)


class Output:
    def __init__(self, options, baseIndentString=''):

        self.__indent_cache = IndentStringCache(options, baseIndentString)
        self.raw = False
        self._end_with_newline = options.end_with_newline
        self.indent_size = options.indent_size
        self.__lines = []
        self.previous_line = None
        self.current_line = None
        self.space_before_token = False
        # initialize
        self.__add_outputline()

    def __add_outputline(self):
        self.previous_line = self.current_line
        self.current_line = OutputLine(self)
        self.__lines.append(self.current_line)

    def get_line_number(self):
        return len(self.__lines)

    def get_indent_string(self, indent, column=0):
        return self.__indent_cache.get_indent_string(indent, column)

    def get_indent_size(self, indent, column=0):
        return self.__indent_cache.get_indent_size(indent, column)

    def is_empty(self):
        return self.previous_line is None and self.current_line.is_empty()

    def add_new_line(self, force_newline=False):
        # never newline at the start of file
        # otherwise, newline only if we didn't just add one or we're forced
        if self.is_empty() or \
                (not force_newline and self.just_added_newline()):
            return False

        # if raw output is enabled, don't print additional newlines,
        # but still return True as though you had
        if not self.raw:
            self.__add_outputline()
        return True

    def get_code(self, eol):
        sweet_code = "\n".join(line.toString() for line in self.__lines)
        sweet_code = re.sub('[\r\n\t ]+$', '', sweet_code)

        if self._end_with_newline:
            sweet_code += '\n'

        if not eol == '\n':
            sweet_code = sweet_code.replace('\n', eol)

        return sweet_code

    def set_indent(self, indent=0, alignment=0):
        # Never indent your first output indent at the start of the file
        if len(self.__lines) > 1:
            self.current_line.set_indent(indent, alignment)
            return True
        self.current_line.set_indent()
        return False

    def add_raw_token(self, token):
        for _ in range(token.newlines):
            self.__add_outputline()

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

    def remove_indent(self, index):
        while index < len(self.__lines):
            self.__lines[index].remove_indent()
            index += 1

    def trim(self, eat_newlines=False):
        self.current_line.trim()

        while eat_newlines and len(
                self.__lines) > 1 and self.current_line.is_empty():
            self.__lines.pop()
            self.current_line = self.__lines[-1]
            self.current_line.trim()

        if len(self.__lines) > 1:
            self.previous_line = self.__lines[-2]
        else:
            self.previous_line = None

    def just_added_newline(self):
        return self.current_line.is_empty()

    def just_added_blankline(self):
        return self.is_empty() or \
            (self.current_line.is_empty() and self.previous_line.is_empty())

    def ensure_empty_line_above(self, starts_with, ends_with):
        index = len(self.__lines) - 2
        while index >= 0:
            potentialEmptyLine = self.__lines[index]
            if potentialEmptyLine.is_empty():
                break
            elif not potentialEmptyLine.item(0).startswith(starts_with) and \
                    potentialEmptyLine.item(-1) != ends_with:
                self.__lines.insert(index + 1, OutputLine(self))
                self.previous_line = self.__lines[-2]
                break
            index -= 1
