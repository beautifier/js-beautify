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


class TokenTypes:
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
    EOF = 'TK_EOF'

    def __init__(self):
        pass


TOKEN = TokenTypes()


class Tokenizer:

    number_pattern = re.compile(
        r'0[xX][0123456789abcdefABCDEF]*|0[oO][01234567]*|0[bB][01]*|\d+n|(?:\.\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?')
    digit = re.compile(r'[0-9]')

    startXmlRegExp = re.compile(
        r'<()([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')
    xmlRegExp = re.compile(
        r'[\s\S]*?<(\/?)([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{[\s\S]+?}))*\s*(/?)\s*>')

    positionable_operators = '!= !== % & && * ** + - / : < << <= == === > >= >> >>> ? ^ | ||'.split(
        ' ')
    punct = (positionable_operators +
             # non-positionable operators - these do not follow operator
             # position settings
             '! %= &= *= **= ++ += , -- -= /= :: <<= = => >>= >>>= ^= |= ~ ...'.split(' '))

    # Words which always should start on a new line
    line_starters = 'continue,try,throw,return,var,let,const,if,switch,case,default,for,while,break,function,import,export'.split(
        ',')
    reserved_words = line_starters + ['do',
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
                                      'as']

    def __init__(self, input_string, opts, indent_string):
        import jsbeautifier.core.acorn as acorn
        self.acorn = acorn

        self.input = InputScanner(input_string)
        self.opts = opts
        self.indent_string = indent_string
        #  /* ... */ comment ends with nearest */ or end of file
        self.block_comment_pattern = re.compile(r'([\s\S]*?)((?:\*\/)|$)')

        # comment ends just before nearest linefeed or end of file
        self.comment_pattern = re.compile(
            self.acorn.six.u(r'([^\n\r\u2028\u2029]*)'))

        self.directives_block_pattern = re.compile(
            r'\/\* beautify( \w+[:]\w+)+ \*\/')
        self.directive_pattern = re.compile(r' (\w+)[:](\w+)')
        self.directives_end_ignore_pattern = re.compile(
            r'([\s\S]*?)((?:\/\*\sbeautify\signore:end\s\*\/)|$)')

        self.template_pattern = re.compile(
            r'((<\?php|<\?=)[\s\S]*?\?>)|(<%[\s\S]*?%>)')

        self.whitespacePattern = re.compile(
            self.acorn.six.u(r'[\n\r\u2028\u2029\t ]+'))
        self.newlinePattern = re.compile(
            self.acorn.six.u(r'([\t ]*)(\r\n|[\n\r\u2028\u2029])?'))

    def tokenize(self):
        self.in_html_comment = False
        self.tokens = []

        next = None
        last = None
        open_token = None
        open_stack = []
        comments = []

        while not (last is not None and last.type == TOKEN.EOF):
            token_values = self.__tokenize_next()
            next = Token(
                token_values[1],
                token_values[0],
                self.n_newlines,
                self.whitespace_before_token)

            while next.type == TOKEN.COMMENT or next.type == TOKEN.BLOCK_COMMENT or next.type == TOKEN.UNKNOWN:
                if next.type == TOKEN.BLOCK_COMMENT:
                    next.directives = token_values[2]

                comments.append(next)
                token_values = self.__tokenize_next()
                next = Token(
                    token_values[1],
                    token_values[0],
                    self.n_newlines,
                    self.whitespace_before_token)

            if len(comments) > 0:
                next.comments_before = comments
                comments = []

            if next.type == TOKEN.START_BLOCK or next.type == TOKEN.START_EXPR:
                next.parent = last
                open_stack.append(open_token)
                open_token = next
            elif (next.type == TOKEN.END_BLOCK or next.type == TOKEN.END_EXPR) and \
                    (open_token is not None and (
                            (next.text == ']' and open_token.text == '[') or
                            (next.text == ')' and open_token.text == '(') or
                            (next.text == '}' and open_token.text == '{'))):
                next.parent = open_token.parent
                next.opened = open_token
                open_token = open_stack.pop()

            self.tokens.append(next)
            last = next
        return self.tokens

    def get_directives(self, text):
        if not self.directives_block_pattern.match(text):
            return None

        directives = {}
        directive_match = self.directive_pattern.search(text)
        while directive_match:
            directives[directive_match.group(1)] = directive_match.group(2)
            directive_match = self.directive_pattern.search(
                text, directive_match.end())

        return directives

    def __tokenize_next(self):

        self.n_newlines = 0
        self.whitespace_before_token = ''

        if len(self.tokens) > 0:
            last_token = self.tokens[-1]
        else:
            # For the sake of tokenizing we can pretend that there was on open
            # brace to start
            last_token = Token(TOKEN.START_BLOCK, '{')

        resulting_string = self.input.readWhile(self.whitespacePattern)
        if resulting_string != '':
            if resulting_string == ' ':
                self.whitespace_before_token = resulting_string
            else:
                for nextMatch in self.newlinePattern.findall(resulting_string):
                    if nextMatch[1] != '':
                        self.n_newlines += 1
                    else:
                        self.whitespace_before_token = nextMatch[0]
                        break

        resulting_string = self.input.readWhile(self.acorn.identifier)
        if resulting_string != '':
            if not (last_token.type == TOKEN.DOT or (
                    last_token.type == TOKEN.RESERVED and last_token.text in [
                        'set',
                        'get'])) and resulting_string in self.reserved_words:
                if resulting_string in ['in', 'of']:  # in and of are operators, need to hack
                    return resulting_string, TOKEN.OPERATOR

                return resulting_string, TOKEN.RESERVED

            return resulting_string, TOKEN.WORD

        resulting_string = self.input.readWhile(self.number_pattern)
        if resulting_string != '':
            return resulting_string, TOKEN.WORD

        c = self.input.next()

        if c is None:
            return '', TOKEN.EOF

        if c in '([':
            return c, TOKEN.START_EXPR

        if c in ')]':
            return c, TOKEN.END_EXPR

        if c == '{':
            return c, TOKEN.START_BLOCK

        if c == '}':
            return c, TOKEN.END_BLOCK

        if c == ';':
            return c, TOKEN.SEMICOLON

        if c == '/':
            comment = ''
            if self.input.peek() == '*':  # peek /* .. */ comment
                self.input.next()
                comment_match = self.input.match(self.block_comment_pattern)
                comment = '/*' + comment_match.group(0)

                directives = self.get_directives(comment)
                if directives and directives.get('ignore') == 'start':
                    comment_match = self.input.match(
                        self.directives_end_ignore_pattern)
                    comment += comment_match.group(0)
                comment = re.sub(self.acorn.allLineBreaks, '\n', comment)
                return comment, TOKEN.BLOCK_COMMENT, directives

            if self.input.peek() == '/':  # peek // comment
                self.input.next()
                comment_match = self.input.match(self.comment_pattern)
                comment = '//' + comment_match.group(0)
                return comment, TOKEN.COMMENT

        def allowRegExOrXML(self):
            return (last_token.type == TOKEN.RESERVED and last_token.text in ['return', 'case', 'throw', 'else', 'do', 'typeof', 'yield']) or \
                (last_token.type == TOKEN.END_EXPR and last_token.text == ')' and
                 last_token.parent and last_token.parent.type == TOKEN.RESERVED and last_token.parent.text in ['if', 'while', 'for']) or \
                (last_token.type in [TOKEN.COMMENT, TOKEN.START_EXPR, TOKEN.START_BLOCK, TOKEN.END_BLOCK, TOKEN.OPERATOR,
                                     TOKEN.EQUALS, TOKEN.EOF, TOKEN.SEMICOLON, TOKEN.COMMA])

        self.has_char_escapes = False

        isString = (c == '`' or c == "'" or c == '"')
        isRegExp = (c == '/' and allowRegExOrXML(self))
        isXML = (self.opts.e4x and c == "<" and self.input.test(
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
                while self.input.hasNext():
                    current_char = self.input.peek()
                    if not (esc or (current_char != delimiter and (
                            allow_unescaped_newlines or not bool(
                                self.acorn.newline.match(current_char))))):
                        break

                    # Handle \r\n linebreaks after escapes or in template
                    # strings
                    if (esc or allow_unescaped_newlines) and bool(
                            self.acorn.newline.match(current_char)):
                        if current_char == '\r' and self.input.peek(1) == '\n':
                            self.input.next()
                            current_char = self.input.peek()

                        resulting_string += '\n'
                    else:
                        resulting_string += current_char

                    if esc:
                        if current_char == 'x' or current_char == 'u':
                            self.has_char_escapes = True

                        esc = False
                    else:
                        esc = current_char == '\\'

                    self.input.next()

                    if start_sub and resulting_string.endswith(start_sub):
                        if delimiter == '`':
                            resulting_string = parse_string(
                                self, resulting_string, '}', allow_unescaped_newlines, '`')
                        else:
                            resulting_string = parse_string(
                                self, resulting_string, '`', allow_unescaped_newlines, '${')

                        if self.input.hasNext():
                            resulting_string += self.input.next()

                return resulting_string

            if sep == '`':
                resulting_string = parse_string(
                    self, resulting_string, '`', True, '${')
            else:
                resulting_string = parse_string(self, resulting_string, sep)
        elif isRegExp:
            # handle regexp
            in_char_class = False
            while self.input.hasNext() and \
                    (esc or in_char_class or self.input.peek() != sep) and \
                    not self.input.testChar(self.acorn.newline):
                resulting_string += self.input.peek()
                if not esc:
                    esc = self.input.peek() == '\\'
                    if self.input.peek() == '[':
                        in_char_class = True
                    elif self.input.peek() == ']':
                        in_char_class = False
                else:
                    esc = False
                self.input.next()

        elif isXML:
            # handle e4x xml literals
            self.input.back()
            xmlStr = ""
            match = self.input.match(self.xmlRegExp)
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

                    match = self.input.match(self.xmlRegExp)

                # if we didn't close correctly, keep unformatted.
                if not match:
                    xmlStr += self.input.match(re.compile(r'[\s\S]*')).group(0)

                xmlStr = re.sub(self.acorn.allLineBreaks, '\n', xmlStr)
                return xmlStr, TOKEN.STRING

        if isRegExp or isString:
            if self.has_char_escapes and self.opts.unescape_strings:
                resulting_string = self.unescape_string(resulting_string)

            if self.input.peek() == sep:
                resulting_string += self.input.next()

                if sep == '/':
                    # regexps may have modifiers /regexp/MOD, so fetch those too
                    # Only [gim] are valid, but if the user puts in garbage, do
                    # what we can to take it.
                    resulting_string += self.input.readWhile(
                        self.acorn.identifier)

            resulting_string = re.sub(
                self.acorn.allLineBreaks, '\n', resulting_string)

            return resulting_string, TOKEN.STRING

        if c == '#':

            # she-bang
            if len(self.tokens) == 0 and self.input.peek() == '!':
                resulting_string = c
                while self.input.hasNext() and c != '\n':
                    c = self.input.next()
                    resulting_string += c
                return resulting_string.strip() + '\n', TOKEN.UNKNOWN

            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp
            # around line 1935
            sharp = '#'
            if self.input.hasNext() and self.input.testChar(self.digit):
                while True:
                    c = self.input.next()
                    sharp += c
                    if (not self.input.hasNext()) or c == '#' or c == '=':
                        break
            if c == '#':
                pass
            elif self.input.peek() == '[' and self.input.peek(1) == ']':
                sharp += '[]'
                self.input.next()
                self.input.next()
            elif self.input.peek() == '{' and self.input.peek(1) == '}':
                sharp += '{}'
                self.input.next()
                self.input.next()
            return sharp, TOKEN.WORD

        if c == '<' and self.input.peek() in ['?', '%']:
            self.input.back()
            template_match = self.input.match(self.template_pattern)
            if template_match:
                c = template_match.group(0)
                c = re.sub(self.acorn.allLineBreaks, '\n', c)
                return c, TOKEN.STRING

        if c == '<' and self.input.match(re.compile(r'\!--')):
            c = '<!--'
            while self.input.hasNext() and not self.input.testChar(self.acorn.newline):
                c += self.input.next()

            self.in_html_comment = True
            return c, TOKEN.COMMENT

        if c == '-' and self.in_html_comment and self.input.match(
                re.compile('->')):
            self.in_html_comment = False
            return '-->', TOKEN.COMMENT

        if c == '.':
            if self.input.peek() == '.' and self.input.peek(1) == '.':
                c += self.input.next() + self.input.next()
                return c, TOKEN.OPERATOR

            return c, TOKEN.DOT

        if c in self.punct:
            while self.input.hasNext() and c + self.input.peek() in self.punct:
                c += self.input.next()
                if not self.input.hasNext():
                    break

            if c == ',':
                return c, TOKEN.COMMA
            if c == '=':
                return c, TOKEN.EQUALS

            return c, TOKEN.OPERATOR

        return c, TOKEN.UNKNOWN

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
