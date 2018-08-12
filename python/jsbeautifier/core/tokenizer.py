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
from ..core.inputscanner import InputScanner
from ..core.token import Token
from ..core.tokenstream import TokenStream


__all__ = ["TOKEN", "Tokenizer", "TokenTypes"]

class TokenTypes:
    START = 'TK_START'
    RAW = 'TK_RAW'
    EOF = 'TK_EOF'

    def __init__(self):
        pass

TOKEN = TokenTypes()

class Tokenizer:

    def __init__(self, input_string):
        import jsbeautifier.core.acorn as acorn
        self.acorn = acorn

        self._input = InputScanner(input_string)
        self._tokens = None
        self._newline_count = 0
        self._whitespace_before_token = ''

        self._whitespace_pattern = re.compile(
            self.acorn.six.u(r'[\n\r\u2028\u2029\t ]+'))
        self._newline_pattern = re.compile(
            self.acorn.six.u(r'([\t ]*)(\r\n|[\n\r\u2028\u2029])?'))

    def tokenize(self):
        self._input.restart()
        self._tokens = TokenStream()

        current = None
        previous = Token(TOKEN.START,'')
        open_token = None
        open_stack = []
        comments = TokenStream()

        while previous.type != TOKEN.EOF:
            current = self.get_next_token(previous, open_token)

            while self.is_comment(current):
                comments.add(current)
                current = self.get_next_token(previous, open_token)

            if not comments.isEmpty():
                current.comments_before = comments
                comments = TokenStream()

            if self.is_opening(current):
                current.parent = open_token
                open_stack.append(open_token)
                open_token = current
            elif open_token is not None and self.is_closing(current, open_token):
                current.opened = open_token
                open_token = open_stack.pop()
                current.parent = open_token

            current.previous = previous

            self._tokens.add(current)
            previous = current
        return self._tokens

    def reset(self):
        pass

    def get_next_token(self, previous_token, open_token):
        self.readWhitespace()
        resulting_string = self._input.read(re.compile(r'.+'))
        if resulting_string:
            return self.create_token(TOKEN.RAW, resulting_string)
        else:
            return self.create_token(TOKEN.EOF, '')

    def is_comment(self, current_token):
        return False

    def is_opening(self, current_token):
        return False

    def is_closing(self, current_token, open_token):
        return False

    def create_token(self, token_type, text):
        token = Token(token_type, text, self._newline_count, self._whitespace_before_token)
        self._newline_count = 0
        self._whitespace_before_token = ''
        return token

    def readWhitespace(self):
        resulting_string = self._input.read(self._whitespace_pattern)
        if resulting_string != '':
            if resulting_string == ' ':
                self._whitespace_before_token = resulting_string
            else:
                for nextMatch in self._newline_pattern.findall(resulting_string):
                    if nextMatch[1] != '':
                        self._newline_count += 1
                    else:
                        self._whitespace_before_token = nextMatch[0]
                        break
