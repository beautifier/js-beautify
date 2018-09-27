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

    def __init__(self, input_string, options):
        self._input = InputScanner(input_string)
        self._options = options
        self.__tokens = None
        self.__newline_count = 0
        self.__whitespace_before_token = ''

        self._whitespace_pattern = re.compile(r'[\n\r\t ]+')
        self._newline_pattern = re.compile(r'([^\n\r]*)(\r\n|[\n\r])?')

    def tokenize(self):
        self._input.restart()
        self.__tokens = TokenStream()

        current = None
        previous = Token(TOKEN.START,'')
        open_token = None
        open_stack = []
        comments = TokenStream()

        while previous.type != TOKEN.EOF:
            current = self.__get_next_token_with_comments(previous, open_token)

            if self._is_opening(current):
                open_stack.append(open_token)
                open_token = current
            elif open_token is not None and \
                    self._is_closing(current, open_token):
                current.opened = open_token
                open_token.closed = current
                open_token = open_stack.pop()
                current.parent = open_token

            self.__tokens.add(current)
            previous = current
        return self.__tokens

    def __get_next_token_with_comments(self, previous, open_token):
        current = self._get_next_token(previous, open_token)

        if self._is_comment(current):
            comments = TokenStream()
            while self._is_comment(current):
                comments.add(current)
                current = self._get_next_token(previous, open_token)

            if not comments.isEmpty():
                current.comments_before = comments
                comments = TokenStream()

        current.parent = open_token
        current.previous = previous
        previous.next = current

        return current

    def _is_first_token(self):
        return self.__tokens.isEmpty()

    def _reset(self):
        pass

    def _get_next_token(self, previous_token, open_token):
        self._readWhitespace()
        resulting_string = self._input.read(re.compile(r'.+'))
        if resulting_string:
            return self._create_token(TOKEN.RAW, resulting_string)
        else:
            return self._create_token(TOKEN.EOF, '')

    def _is_comment(self, current_token):
        return False

    def _is_opening(self, current_token):
        return False

    def _is_closing(self, current_token, open_token):
        return False

    def _create_token(self, token_type, text):
        token = Token(token_type, text,
                self.__newline_count, self.__whitespace_before_token)
        self.__newline_count = 0
        self.__whitespace_before_token = ''
        return token

    def _readWhitespace(self):
        resulting_string = self._input.read(self._whitespace_pattern)
        if resulting_string == ' ':
            self.__whitespace_before_token = resulting_string
        elif resulting_string != '':
            for nextMatch in self._newline_pattern.findall(resulting_string):
                if nextMatch[1] == '':
                    self.__whitespace_before_token = nextMatch[0]
                    break

                self.__newline_count += 1
