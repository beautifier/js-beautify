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
from ..core.tokenizer import TokenTypes as BaseTokenTypes
from ..core.tokenizer import Tokenizer as BaseTokenizer
from ..core.directives import Directives


class TokenTypes(BaseTokenTypes):
    START_EXPR = 'TK_START_EXPR'
    END_EXPR = 'TK_END_EXPR'
    START_BLOCK = 'TK_START_BLOCK'
    END_BLOCK = 'TK_END_BLOCK'
    WORD = 'TK_WORD'
    RESERVED = 'TK_RESERVED'
    SEMICOLON = 'TK_SEMICOLON'
    STRING = 'TK_STRING'
    EQUALS = 'TK_EQUALS'
    OPERATOR = 'TK_OPERATOR'
    COMMA = 'TK_COMMA'
    BLOCK_COMMENT = 'TK_BLOCK_COMMENT'
    COMMENT = 'TK_COMMENT'
    DOT = 'TK_DOT'
    UNKNOWN = 'TK_UNKNOWN'

    def __init__(self):
        pass


TOKEN = TokenTypes()


class Tokenizer(BaseTokenizer):

    number_pattern = re.compile(
        r'0[xX][0123456789abcdefABCDEF]*|0[oO][01234567]*|0[bB][01]*|\d+n|(?:\.\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?')
    digit = re.compile(r'[0-9]')

    startXmlRegExp = re.compile(
        r'<()([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')
    xmlRegExp = re.compile(
        r'[\s\S]*?<(\/?)([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')

    positionable_operators = frozenset(
        '!= !== % & && * ** + - / : < << <= == === > >= >> >>> ? ^ | ||'.split(
        ' '))
    punct = frozenset(positionable_operators) | frozenset(
             # non-positionable operators - these do not follow operator
             # position settings
             '! %= &= *= **= ++ += , -- -= /= :: <<= = => >>= >>>= ^= |= ~ ...'.split(' '))

    # Words which always should start on a new line
    line_starters = frozenset(
        ('continue,try,throw,return,var,let,const,if,switch,case,default,for,' +
        'while,break,function,import,export').split(','))
    reserved_words = line_starters | frozenset(['do',
                                      'in',
                                      'of',
                                      'else',
                                      'get',
                                      'set',
                                      'new',
                                      'catch',
                                      'finally',
                                      'typeof',
                                      'yield',
                                      'async',
                                      'await',
                                      'from',
                                      'as'])

    reserved_word_pattern = re.compile(r'^(?:' + '|'.join(reserved_words) + r')$')

    def __init__(self, input_string, opts, indent_string):
        BaseTokenizer.__init__(self, input_string)

        self.opts = opts
        self.indent_string = indent_string
        self.in_html_comment = False

        #  /* ... */ comment ends with nearest */ or end of file
        self.block_comment_pattern = re.compile(r'([\s\S]*?)((?:\*\/)|$)')

        # comment ends just before nearest linefeed or end of file
        self.comment_pattern = re.compile(
            self.acorn.six.u(r'([^\n\r\u2028\u2029]*)'))

        self.directives_core = Directives(r'/\*', r'\*/')

        self.template_pattern = re.compile(
            r'((<\?php|<\?=)[\s\S]*?\?>)|(<%[\s\S]*?%>)')

    def reset(self):
        self.in_html_comment = False

    def is_comment(self, current_token):
        return current_token.type == TOKEN.COMMENT or \
            current_token.type == TOKEN.BLOCK_COMMENT or \
            current_token.type == TOKEN.UNKNOWN


    def is_opening(self, current_token):
        return current_token.type == TOKEN.START_BLOCK or current_token.type == TOKEN.START_EXPR

    def is_closing(self, current_token, open_token):
        return (current_token.type == TOKEN.END_BLOCK or current_token.type == TOKEN.END_EXPR) and \
                    (open_token is not None and (
                            (current_token.text == ']' and open_token.text == '[') or
                            (current_token.text == ')' and open_token.text == '(') or
                            (current_token.text == '}' and open_token.text == '{')))

    def get_next_token(self, last_token):
        self.readWhitespace()

        resulting_string = self._input.read(self.acorn.identifier)
        if resulting_string != '':
            if not (last_token.type == TOKEN.DOT or (
                    last_token.type == TOKEN.RESERVED and last_token.text in [
                        'set',
                        'get'])) and self.reserved_word_pattern.match(resulting_string):
                if resulting_string in ['in', 'of']:  # in and of are operators, need to hack
                    return self.create_token(TOKEN.OPERATOR, resulting_string)

                return self.create_token(TOKEN.RESERVED, resulting_string)

            return self.create_token(TOKEN.WORD, resulting_string)

        resulting_string = self._input.read(self.number_pattern)
        if resulting_string != '':
            return self.create_token(TOKEN.WORD, resulting_string)

        c = self._input.next()

        if c is None:
            return self.create_token(TOKEN.EOF, '')

        if c in '([':
            return self.create_token(TOKEN.START_EXPR, c)

        if c in ')]':
            return self.create_token(TOKEN.END_EXPR, c)

        if c == '{':
            return self.create_token(TOKEN.START_BLOCK, c)

        if c == '}':
            return self.create_token(TOKEN.END_BLOCK, c)

        if c == ';':
            return self.create_token(TOKEN.SEMICOLON, c)

        if c == '/':
            comment = ''
            if self._input.peek() == '*':  # peek /* .. */ comment
                self._input.next()
                comment_match = self._input.match(self.block_comment_pattern)
                comment = '/*' + comment_match.group(0)

                directives = self.directives_core.get_directives(comment)
                if directives and directives.get('ignore') == 'start':
                    comment += self.directives_core.readIgnored(self._input)
                comment = re.sub(self.acorn.allLineBreaks, '\n', comment)
                token = self.create_token(TOKEN.BLOCK_COMMENT, comment)
                token.directives = directives
                return token

            if self._input.peek() == '/':  # peek // comment
                self._input.next()
                comment_match = self._input.match(self.comment_pattern)
                comment = '//' + comment_match.group(0)
                return self.create_token(TOKEN.COMMENT, comment)

        def allowRegExOrXML(self):
            return (last_token.type == TOKEN.RESERVED and last_token.text in ['return', 'case', 'throw', 'else', 'do', 'typeof', 'yield']) or \
                (last_token.type == TOKEN.END_EXPR and last_token.text == ')' and
                 last_token.parent and last_token.parent.type == TOKEN.RESERVED and last_token.parent.text in ['if', 'while', 'for']) or \
                (last_token.type in [TOKEN.COMMENT, TOKEN.START_EXPR, TOKEN.START_BLOCK, TOKEN.START, TOKEN.END_BLOCK, TOKEN.OPERATOR,
                                     TOKEN.EQUALS, TOKEN.EOF, TOKEN.SEMICOLON, TOKEN.COMMA])

        self.has_char_escapes = False

        isString = (c == '`' or c == "'" or c == '"')
        isRegExp = (c == '/' and allowRegExOrXML(self))
        isXML = (self.opts.e4x and c == "<" and self._input.test(
            self.startXmlRegExp, -1) and allowRegExOrXML(self))

        sep = c
        esc = False
        resulting_string = c
        in_char_class = False

        if isString:
            # handle string
            def parse_string(
                    self,
                    resulting_string,
                    delimiter,
                    allow_unescaped_newlines=False,
                    start_sub=None):
                esc = False
                while self._input.hasNext():
                    current_char = self._input.peek()
                    if not (esc or (current_char != delimiter and (
                            allow_unescaped_newlines or not bool(
                                self.acorn.newline.match(current_char))))):
                        break

                    # Handle \r\n linebreaks after escapes or in template
                    # strings
                    if (esc or allow_unescaped_newlines) and bool(
                            self.acorn.newline.match(current_char)):
                        if current_char == '\r' and self._input.peek(1) == '\n':
                            self._input.next()
                            current_char = self._input.peek()

                        resulting_string += '\n'
                    else:
                        resulting_string += current_char

                    if esc:
                        if current_char == 'x' or current_char == 'u':
                            self.has_char_escapes = True

                        esc = False
                    else:
                        esc = current_char == '\\'

                    self._input.next()

                    if start_sub and resulting_string.endswith(start_sub):
                        if delimiter == '`':
                            resulting_string = parse_string(
                                self, resulting_string, '}', allow_unescaped_newlines, '`')
                        else:
                            resulting_string = parse_string(
                                self, resulting_string, '`', allow_unescaped_newlines, '${')

                        if self._input.hasNext():
                            resulting_string += self._input.next()

                return resulting_string

            if sep == '`':
                resulting_string = parse_string(
                    self, resulting_string, '`', True, '${')
            else:
                resulting_string = parse_string(self, resulting_string, sep)
        elif isRegExp:
            # handle regexp
            in_char_class = False
            while self._input.hasNext() and \
                    (esc or in_char_class or self._input.peek() != sep) and \
                    not self._input.testChar(self.acorn.newline):
                resulting_string += self._input.peek()
                if not esc:
                    esc = self._input.peek() == '\\'
                    if self._input.peek() == '[':
                        in_char_class = True
                    elif self._input.peek() == ']':
                        in_char_class = False
                else:
                    esc = False
                self._input.next()

        elif isXML:
            # handle e4x xml literals
            self._input.back()
            xmlStr = ""
            match = self._input.match(self.xmlRegExp)
            if match:
                rootTag = match.group(2)
                rootTag = re.sub(r'^{\s+', '{', re.sub(r'\s+}$', '}', rootTag))
                isCurlyRoot = rootTag.startswith('{')
                depth = 0
                while bool(match):
                    isEndTag = match.group(1)
                    tagName = match.group(2)
                    isSingletonTag = (
                        match.groups()[-1] != "") or (match.group(2)[0:8] == "![CDATA[")
                    if not isSingletonTag and (tagName == rootTag or (
                            isCurlyRoot and re.sub(r'^{\s+', '{', re.sub(r'\s+}$', '}', tagName)))):
                        if isEndTag:
                            depth -= 1
                        else:
                            depth += 1

                    xmlStr += match.group(0)
                    if depth <= 0:
                        break

                    match = self._input.match(self.xmlRegExp)

                # if we didn't close correctly, keep unformatted.
                if not match:
                    xmlStr += self._input.match(re.compile(r'[\s\S]*')).group(0)

                xmlStr = re.sub(self.acorn.allLineBreaks, '\n', xmlStr)
                return self.create_token(TOKEN.STRING, xmlStr)

        if isRegExp or isString:
            if self.has_char_escapes and self.opts.unescape_strings:
                resulting_string = self.unescape_string(resulting_string)

            if self._input.peek() == sep:
                resulting_string += self._input.next()

                if sep == '/':
                    # regexps may have modifiers /regexp/MOD, so fetch those too
                    # Only [gim] are valid, but if the user puts in garbage, do
                    # what we can to take it.
                    resulting_string += self._input.read(
                        self.acorn.identifier)

            resulting_string = re.sub(
                self.acorn.allLineBreaks, '\n', resulting_string)

            return self.create_token(TOKEN.STRING, resulting_string)

        if c == '#':

            # she-bang
            if self._tokens.isEmpty() and self._input.peek() == '!':
                resulting_string = c
                while self._input.hasNext() and c != '\n':
                    c = self._input.next()
                    resulting_string += c
                return self.create_token(TOKEN.UNKNOWN, resulting_string.strip() + '\n')

            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp
            # around line 1935
            sharp = '#'
            if self._input.hasNext() and self._input.testChar(self.digit):
                while True:
                    c = self._input.next()
                    sharp += c
                    if (not self._input.hasNext()) or c == '#' or c == '=':
                        break
            if c == '#':
                pass
            elif self._input.peek() == '[' and self._input.peek(1) == ']':
                sharp += '[]'
                self._input.next()
                self._input.next()
            elif self._input.peek() == '{' and self._input.peek(1) == '}':
                sharp += '{}'
                self._input.next()
                self._input.next()
            return self.create_token(TOKEN.WORD, sharp)

        if c == '<' and self._input.peek() in ['?', '%']:
            self._input.back()
            template_match = self._input.match(self.template_pattern)
            if template_match:
                c = template_match.group(0)
                c = re.sub(self.acorn.allLineBreaks, '\n', c)
                return self.create_token(TOKEN.STRING, c)

        if c == '<' and self._input.match(re.compile(r'\!--')):
            c = '<!--'
            while self._input.hasNext() and not self._input.testChar(self.acorn.newline):
                c += self._input.next()

            self.in_html_comment = True
            return self.create_token(TOKEN.COMMENT, c)

        if c == '-' and self.in_html_comment and self._input.match(
                re.compile('->')):
            self.in_html_comment = False
            return self.create_token(TOKEN.COMMENT, '-->')

        if c == '.':
            if self._input.peek() == '.' and self._input.peek(1) == '.':
                c += self._input.next() + self._input.next()
                return self.create_token(TOKEN.OPERATOR, c)

            return self.create_token(TOKEN.DOT, c)

        if c in self.punct:
            while self._input.hasNext() and c + self._input.peek() in self.punct:
                c += self._input.next()
                if not self._input.hasNext():
                    break

            if c == ',':
                return self.create_token(TOKEN.COMMA, c)
            if c == '=':
                return self.create_token(TOKEN.EQUALS, c)

            return self.create_token(TOKEN.OPERATOR, c)

        return self.create_token(TOKEN.UNKNOWN, c)

    def unescape_string(self, s):
        # You think that a regex would work for this
        # return s.replace(/\\x([0-9a-f]{2})/gi, function(match, val) {
        #         return String.fromCharCode(parseInt(val, 16));
        #     })
        # However, dealing with '\xff', '\\xff', '\\\xff' makes this more fun.
        out = self.acorn.six.u('')
        escaped = 0

        input_scan = InputScanner(s)
        matched = None

        while input_scan.hasNext():
            # Keep any whitespace, non-slash characters
            # also keep slash pairs.
            matched = input_scan.match(re.compile(r'([\s]|[^\\]|\\\\)+'))

            if matched:
                out += matched.group(0)

            if input_scan.peek() != '\\':
                continue

            input_scan.next()
            if input_scan.peek() == 'x':
                matched = input_scan.match(re.compile(r'x([0-9A-Fa-f]{2})'))
            elif input_scan.peek() == 'u':
                matched = input_scan.match(re.compile(r'u([0-9A-Fa-f]{4})'))
            else:
                out += '\\'
                if input_scan.hasNext():
                    out += input_scan.next()
                continue

            # If there's some error decoding, return the original string
            if not matched:
                return s

            escaped = int(matched.group(1), 16)

            if escaped > 0x7e and escaped <= 0xff and matched.group(
                    0).startswith('x'):
                # we bail out on \x7f..\xff,
                # leaving whole string escaped,
                # as it's probably completely binary
                return s
            elif escaped >= 0x00 and escaped < 0x20:
                # leave 0x00...0x1f escaped
                out += '\\' + matched.group(0)
                continue
            elif escaped == 0x22 or escaped == 0x27 or escaped == 0x5c:
                # single-quote, apostrophe, backslash - escape these
                out += ('\\' + chr(escaped))
            else:
                out += self.acorn.six.unichr(escaped)

        return out
