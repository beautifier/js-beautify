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


class TokenStream:
    def __init__(self, parent_token=None):
        self.__tokens = []
        self.__tokens_length = len(self.__tokens)
        self.__position = 0
        self.__parent_token = parent_token

    def restart(self):
        self.__position = 0

    def isEmpty(self):
        return self.__tokens_length == 0

    def hasNext(self):
        return self.__position < self.__tokens_length

    def next(self):
        if self.hasNext():
            val = self.__tokens[self.__position]
            self.__position += 1
            return val
        else:
            raise StopIteration

    def peek(self, index=0):
        val = None
        index += self.__position
        if index >= 0 and index < self.__tokens_length:
            val = self.__tokens[index]

        return val

    def add(self, token):
        if self.__parent_token:
            token.parent = self.__parent_token

        self.__tokens.append(token)
        self.__tokens_length += 1

    def __iter__(self):
        self.restart()
        return self

    def __next__(self):
        return self.next()
