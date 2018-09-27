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

__all__ = ["TOKEN", "Tokenizer", "TokenTypes"]

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

dot_pattern = re.compile(r'[^\d\.]')

number_pattern = re.compile(
    r'0[xX][0123456789abcdefABCDEF]*|0[oO][01234567]*|0[bB][01]*|\d+n|(?:\.\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?')
digit = re.compile(r'[0-9]')

startXmlRegExp = re.compile(
    r'<()([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')
xmlRegExp = re.compile(
    r'[\s\S]*?<(\/?)([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')

positionable_operators = frozenset(
    (">>> === !== " +
    "<< && >= ** != == <= >> || " +
    "< / - + > : & % ? ^ | *").split(' '))

punct =  (">>>= " +
    "... >>= <<= === >>> !== **= " +
    "=> ^= :: /= << <= == && -= >= >> != -- += ** || ++ %= &= *= |= " +
    "= ! ? > < : / ^ - + * & % ~ |")

punct = re.compile(r'([-[\]{}()*+?.,\\^$|#])').sub(r'\\\1', punct)
punct = punct.replace(' ', '|')

punct_pattern = re.compile(punct)
shebang_pattern = re.compile(r'#![^\n]*(?:\r\n|[\n\r\u2028\u2029])?')
include_pattern = re.compile(r'#include[^\n\r\u2028\u2029]*(?:\r\n|[\n\r\u2028\u2029])?')

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

#  /* ... */ comment ends with nearest */ or end of file
block_comment_pattern = re.compile(r'/\*([\s\S]*?)((?:\*\/)|$)')

directives_core = Directives(r'/\*', r'\*/')

template_pattern = re.compile(
    r'(?:(?:<\?php|<\?=)[\s\S]*?\?>)|(?:<%[\s\S]*?%>)')


class Tokenizer(BaseTokenizer):
    positionable_operators = positionable_operators
    line_starters = line_starters

    def __init__(self, input_string, opts):
        BaseTokenizer.__init__(self, input_string, opts)
        # This is not pretty, but given how we did the version import
        # it is the only way to do this without having setup.py fail on a missing
        # six dependency.
        self._six = __import__("six")

        import jsbeautifier.javascript.acorn as acorn
        self.acorn = acorn

        self.in_html_comment = False
        self.has_char_escapes = False

        # comment ends just before nearest linefeed or end of file
        # IMPORTANT: This string must be run through six to handle \u chars
        self._whitespace_pattern = re.compile(
            self._six.u(r'[\n\r\u2028\u2029\t\u000B\u00A0\u1680\u180e\u2000-\u200a\u202f\u205f\u3000\ufeff ]+'))
        self._newline_pattern = re.compile(
            self._six.u(r'([^\n\r\u2028\u2029]*)(\r\n|[\n\r\u2028\u2029])?'))
        # // comment ends just before nearest linefeed or end of file

        self.comment_pattern = re.compile(
            self._six.u(r'//([^\n\r\u2028\u2029]*)'))



    def _reset(self):
        self.in_html_comment = False

    def _is_comment(self, current_token):
        return current_token.type == TOKEN.COMMENT or \
            current_token.type == TOKEN.BLOCK_COMMENT or \
            current_token.type == TOKEN.UNKNOWN


    def _is_opening(self, current_token):
        return current_token.type == TOKEN.START_BLOCK or current_token.type == TOKEN.START_EXPR

    def _is_closing(self, current_token, open_token):
        return (current_token.type == TOKEN.END_BLOCK or current_token.type == TOKEN.END_EXPR) and \
                    (open_token is not None and (
                            (current_token.text == ']' and open_token.text == '[') or
                            (current_token.text == ')' and open_token.text == '(') or
                            (current_token.text == '}' and open_token.text == '{')))

    def _get_next_token(self, previous_token, open_token):
        self._readWhitespace()
        token = None
        c = self._input.peek()

        token = token or self._read_singles(c)
        token = token or self._read_word(previous_token)
        token = token or self._read_comment(c)
        token = token or self._read_string(c)
        token = token or self._read_regexp(c, previous_token)
        token = token or self._read_xml(c, previous_token)
        token = token or self._read_non_javascript(c)
        token = token or self._read_punctuation()
        token = token or self._create_token(TOKEN.UNKNOWN, self._input.next())

        return token

    def _read_singles(self, c):
        token = None

        if c is None:
            token = self._create_token(TOKEN.EOF, '')
        elif c == '(' or c == '[':
            token = self._create_token(TOKEN.START_EXPR, c)
        elif c == ')' or c == ']':
            token = self._create_token(TOKEN.END_EXPR, c)
        elif c == '{':
            token = self._create_token(TOKEN.START_BLOCK, c)
        elif c == '}':
            token = self._create_token(TOKEN.END_BLOCK, c)
        elif c == ';':
            token = self._create_token(TOKEN.SEMICOLON, c)
        elif c == '.' and bool(dot_pattern.match(self._input.peek(1))):
            token = self._create_token(TOKEN.DOT, c)
        elif c == ',':
            token = self._create_token(TOKEN.COMMA, c)

        if token is not None:
            self._input.next()

        return token

    def _read_word(self, previous_token):
        resulting_string = self._input.read(self.acorn.identifier)
        if resulting_string != '':
            if not (previous_token.type == TOKEN.DOT or (
                    previous_token.type == TOKEN.RESERVED and (
                        previous_token.text == 'set' or previous_token.text == 'get')
                        )) and reserved_word_pattern.match(resulting_string):
                if resulting_string == 'in' or resulting_string == 'of':
                    # in and of are operators, need to hack
                    return self._create_token(TOKEN.OPERATOR, resulting_string)

                return self._create_token(TOKEN.RESERVED, resulting_string)

            return self._create_token(TOKEN.WORD, resulting_string)

        resulting_string = self._input.read(number_pattern)
        if resulting_string != '':
            return self._create_token(TOKEN.WORD, resulting_string)

    def _read_comment(self, c):
        token = None
        if c == '/':
            comment = ''
            if self._input.peek(1) == '*':  # peek /* .. */ comment
                comment = self._input.read(block_comment_pattern)

                directives = directives_core.get_directives(comment)
                if directives and directives.get('ignore') == 'start':
                    comment += directives_core.readIgnored(self._input)
                comment = re.sub(self.acorn.allLineBreaks, '\n', comment)
                token = self._create_token(TOKEN.BLOCK_COMMENT, comment)
                token.directives = directives

            elif self._input.peek(1) == '/':  # peek // comment
                comment = self._input.read(self.comment_pattern)
                token = self._create_token(TOKEN.COMMENT, comment)

        return token


    def _read_string(self, c):
        if c == '`' or c == "'" or c == '"':
            resulting_string = self._input.next()
            self.has_char_escapes = False

            if c == '`':
                resulting_string = self.parse_string(
                    resulting_string, '`', True, '${')
            else:
                resulting_string = self.parse_string(resulting_string, c)

            if self.has_char_escapes and self._options.unescape_strings:
                resulting_string = self.unescape_string(resulting_string)

            if self._input.peek() == c :
                resulting_string += self._input.next()

            resulting_string = re.sub(
                self.acorn.allLineBreaks, '\n', resulting_string)

            return self._create_token(TOKEN.STRING, resulting_string)

        return None

    def _read_regexp(self, c, previous_token):

        if c == '/' and self.allowRegExOrXML(previous_token):
            # handle regexp
            resulting_string = self._input.next()
            esc = False

            in_char_class = False
            while self._input.hasNext() and \
                    (esc or in_char_class or self._input.peek() != c) and \
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

            if self._input.peek() == c:
                resulting_string += self._input.next()

                if c == '/':
                    # regexps may have modifiers /regexp/MOD, so fetch those too
                    # Only [gim] are valid, but if the user puts in garbage, do
                    # what we can to take it.
                    resulting_string += self._input.read(
                        self.acorn.identifier)

            return self._create_token(TOKEN.STRING, resulting_string)

        return None


    def _read_xml(self, c, previous_token):
        if self._options.e4x and c == "<" and self._input.test(
                startXmlRegExp) and self.allowRegExOrXML(previous_token):
            # handle e4x xml literals
            xmlStr = ""
            match = self._input.match(xmlRegExp)
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

                    match = self._input.match(xmlRegExp)

                # if we didn't close correctly, keep unformatted.
                if not match:
                    xmlStr += self._input.match(re.compile(r'[\s\S]*')).group(0)

                xmlStr = re.sub(self.acorn.allLineBreaks, '\n', xmlStr)
                return self._create_token(TOKEN.STRING, xmlStr)

        return None

    def _read_non_javascript(self, c):
        resulting_string = ''

        if c == '#':

            # she-bang
            if self._is_first_token():
                resulting_string = self._input.read(shebang_pattern)
                if resulting_string:
                    return self._create_token(TOKEN.UNKNOWN, resulting_string.strip() + '\n')

            # handles extendscript #includes
            resulting_string = self._input.read(include_pattern)

            if resulting_string:
                return self._create_token(TOKEN.UNKNOWN, resulting_string.strip() + '\n')

            c = self._input.next()

            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp
            # around line 1935
            sharp = '#'
            if self._input.hasNext() and self._input.testChar(digit):
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

                return self._create_token(TOKEN.WORD, sharp)

            self._input.back()

        elif c == '<':
            if self._input.peek(1) == '?' or self._input.peek(1) == '%':
                resulting_string = self._input.read(template_pattern)
                if resulting_string:
                    resulting_string = re.sub(self.acorn.allLineBreaks, '\n', resulting_string)
                    return self._create_token(TOKEN.STRING, resulting_string)

            elif self._input.match(re.compile(r'<\!--')):
                c = '<!--'
                while self._input.hasNext() and not self._input.testChar(self.acorn.newline):
                    c += self._input.next()

                self.in_html_comment = True
                return self._create_token(TOKEN.COMMENT, c)

        elif c == '-' and self.in_html_comment and self._input.match(
                re.compile('-->')):
            self.in_html_comment = False
            return self._create_token(TOKEN.COMMENT, '-->')

        return None

    def _read_punctuation(self):
        token = None
        resulting_string = self._input.read(punct_pattern)
        if resulting_string != '':
            if resulting_string == '=':
                token = self._create_token(TOKEN.EQUALS, resulting_string)
            else:
                token = self._create_token(TOKEN.OPERATOR, resulting_string)

        return token

    __regexTokens = { TOKEN.COMMENT, TOKEN.START_EXPR, TOKEN.START_BLOCK,
        TOKEN.START, TOKEN.END_BLOCK, TOKEN.OPERATOR,
        TOKEN.EQUALS, TOKEN.EOF, TOKEN.SEMICOLON, TOKEN.COMMA }
    def allowRegExOrXML(self, previous_token):
        return (previous_token.type == TOKEN.RESERVED and previous_token.text in {'return', 'case', 'throw', 'else', 'do', 'typeof', 'yield'}) or \
            (previous_token.type == TOKEN.END_EXPR and previous_token.text == ')' and
                previous_token.opened.previous.type == TOKEN.RESERVED and previous_token.opened.previous.text in {'if', 'while', 'for'}) or \
            (previous_token.type in self.__regexTokens )

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
                    resulting_string = self.parse_string(
                        resulting_string, '}', allow_unescaped_newlines, '`')
                else:
                    resulting_string = self.parse_string(
                        resulting_string, '`', allow_unescaped_newlines, '${')

                if self._input.hasNext():
                    resulting_string += self._input.next()

        return resulting_string


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
