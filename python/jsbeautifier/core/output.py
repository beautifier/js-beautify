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

    def get_character_count(self):
        return self.__character_count

    def is_empty(self):
        return len(self.__items) == 0

    def set_indent(self, indent=0, alignment=0):
        self.__indent_count = indent
        self.__alignment_count = alignment
        self.__character_count = self.__parent.baseIndentLength + \
            self.__alignment_count + \
            self.__indent_count * self.__parent.indent_length

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
            self.__character_count -= self.__parent.indent_length

    def trim(self):
        while self.last() == ' ':
            self.__items.pop()
            self.__character_count -= 1

    def toString(self):
        result = ''
        if not self.is_empty():
            if self.__indent_count >= 0:
                result = self.__parent.get_indent_string(self.__indent_count)
            if self.__alignment_count >= 0:
                result += self.__parent.get_alignment_string(
                    self.__alignment_count)
            result += ''.join(self.__items)
        return result


class IndentCache:
    def __init__(self, base_string, level_string):
        self.__cache = [base_string]
        self.__level_string = level_string

    def __ensure_cache(self, level):
        while level >= len(self.__cache):
            self.__cache.append(
                self.__cache[-1] + self.__level_string)

    def get_level_string(self, level):
        self.__ensure_cache(level)
        return self.__cache[level]


class Output:
    def __init__(self, options, baseIndentString=''):

        indent_string = options.indent_char
        if options.indent_size > 0:
            indent_string = options.indent_char * options.indent_size

        # Set to null to continue support for auto detection of base levelself.
        if options.indent_level > 0:
            baseIndentString = options.indent_level * indent_string

        self.__indent_cache = IndentCache(baseIndentString, indent_string)
        self.__alignment_cache = IndentCache('', ' ')
        self.baseIndentLength = len(baseIndentString)
        self.indent_length = len(indent_string)
        self.raw = False
        self._end_with_newline = options.end_with_newline
        self.__lines = []
        self.previous_line = None
        self.current_line = None
        self.space_before_token = False

        self.__add_outputline()

    def __add_outputline(self):
        self.previous_line = self.current_line
        self.current_line = OutputLine(self)
        self.__lines.append(self.current_line)

    def get_line_number(self):
        return len(self.__lines)

    def get_indent_string(self, level):
        return self.__indent_cache.get_level_string(level)

    def get_alignment_string(self, level):
        return self.__alignment_cache.get_level_string(level)

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
