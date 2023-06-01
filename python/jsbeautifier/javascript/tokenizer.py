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
from ..core.tokenizer import TokenizerPatterns as BaseTokenizerPatterns
from ..core.directives import Directives

from ..core.pattern import Pattern
from ..core.templatablepattern import TemplatablePattern


__all__ = ["TOKEN", "Tokenizer", "TokenTypes"]


class TokenTypes(BaseTokenTypes):
    START_EXPR = "TK_START_EXPR"
    END_EXPR = "TK_END_EXPR"
    START_BLOCK = "TK_START_BLOCK"
    END_BLOCK = "TK_END_BLOCK"
    WORD = "TK_WORD"
    RESERVED = "TK_RESERVED"
    SEMICOLON = "TK_SEMICOLON"
    STRING = "TK_STRING"
    EQUALS = "TK_EQUALS"
    OPERATOR = "TK_OPERATOR"
    COMMA = "TK_COMMA"
    BLOCK_COMMENT = "TK_BLOCK_COMMENT"
    COMMENT = "TK_COMMENT"
    DOT = "TK_DOT"
    UNKNOWN = "TK_UNKNOWN"

    def __init__(self):
        pass


TOKEN = TokenTypes()

dot_pattern = re.compile(r"[^\d\.]")

number_pattern = re.compile(
    r"0[xX][0123456789abcdefABCDEF_]*n?|0[oO][01234567_]*n?|0[bB][01_]*n?|\d[\d_]*n|(?:\.\d[\d_]*|\d[\d_]*\.?[\d_]*)(?:[eE][+-]?[\d_]+)?"
)
digit = re.compile(r"[0-9]")


positionable_operators = frozenset(
    (
        ">>> === !== &&= ??= ||= "
        + "<< && >= ** != == <= >> || ?? |> "
        + "< / - + > : & % ? ^ | *"
    ).split(" ")
)

punct = (
    ">>>= "
    + "... >>= <<= === >>> !== **= &&= ??= ||= "
    + "=> ^= :: /= << <= == && -= >= >> != -- += ** || ?? ++ %= &= *= |= |> "
    + "= ! ? > < : / ^ - + * & % ~ |"
)

punct = re.compile(r"([-[\]{}()*+?.,\\^$|#])").sub(r"\\\1", punct)
# ?. but not if followed by a number
punct = "\\?\\.(?!\\d) " + punct
punct = punct.replace(" ", "|")

punct_pattern = re.compile(punct)

# Words which always should start on a new line
line_starters = frozenset(
    (
        "continue,try,throw,return,var,let,const,if,switch,case,default,for,"
        + "while,break,function,import,export"
    ).split(",")
)
reserved_words = line_starters | frozenset(
    [
        "do",
        "in",
        "of",
        "else",
        "get",
        "set",
        "new",
        "catch",
        "finally",
        "typeof",
        "yield",
        "async",
        "await",
        "from",
        "as",
        "class",
        "extends",
    ]
)

reserved_word_pattern = re.compile(r"^(?:" + "|".join(reserved_words) + r")$")

directives_core = Directives(r"/\*", r"\*/")

xmlRegExp = re.compile(
    r'[\s\S]*?<(\/?)([-a-zA-Z:0-9_.]+|{[^}]+?}|!\[CDATA\[[^\]]*?\]\]|)(\s*{[^}]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*(\'[^\']*\'|"[^"]*"|{([^{}]|{[^}]+?})+?}))*\s*(\/?)\s*>'
)


class TokenizerPatterns(BaseTokenizerPatterns):
    def __init__(self, input_scanner, acorn, options):
        BaseTokenizerPatterns.__init__(self, input_scanner)

        # This is not pretty, but given how we did the version import
        # it is the only way to do this without having setup.py fail on a missing
        # six dependency.
        six = __import__("six")

        # IMPORTANT: This string must be run through six to handle \u chars
        self.whitespace = self.whitespace.matching(
            six.u(r"\u00A0\u1680\u180e\u2000-\u200a\u202f\u205f\u3000\ufeff"),
            six.u(r"\u2028\u2029"),
        )

        pattern = Pattern(input_scanner)
        templatable = TemplatablePattern(input_scanner).read_options(options)

        self.identifier = templatable.starting_with(acorn.identifier).matching(
            acorn.identifierMatch
        )
        self.number = pattern.matching(number_pattern)
        self.punct = pattern.matching(punct_pattern)
        self.comment = pattern.starting_with(r"//").until(six.u(r"[\n\r\u2028\u2029]"))
        self.block_comment = pattern.starting_with(r"/\*").until_after(r"\*/")
        self.html_comment_start = pattern.matching(r"<!--")
        self.html_comment_end = pattern.matching(r"-->")
        self.include = pattern.starting_with(r"#include").until_after(acorn.lineBreak)
        self.shebang = pattern.starting_with(r"#!").until_after(acorn.lineBreak)

        self.xml = pattern.matching(xmlRegExp)

        self.single_quote = templatable.until(six.u(r"['\\\n\r\u2028\u2029]"))
        self.double_quote = templatable.until(six.u(r'["\\\n\r\u2028\u2029]'))
        self.template_text = templatable.until(r"[`\\$]")
        self.template_expression = templatable.until(r"[`}\\]")


class Tokenizer(BaseTokenizer):
    positionable_operators = positionable_operators
    line_starters = line_starters

    def __init__(self, input_string, opts):
        BaseTokenizer.__init__(self, input_string, opts)

        import jsbeautifier.javascript.acorn as acorn

        self.acorn = acorn

        self.in_html_comment = False
        self.has_char_escapes = False

        self._patterns = TokenizerPatterns(self._input, self.acorn, opts)

    def _reset(self):
        self.in_html_comment = False

    def _is_comment(self, current_token):
        return (
            current_token.type == TOKEN.COMMENT
            or current_token.type == TOKEN.BLOCK_COMMENT
            or current_token.type == TOKEN.UNKNOWN
        )

    def _is_opening(self, current_token):
        return (
            current_token.type == TOKEN.START_BLOCK
            or current_token.type == TOKEN.START_EXPR
        )

    def _is_closing(self, current_token, open_token):
        return (
            current_token.type == TOKEN.END_BLOCK
            or current_token.type == TOKEN.END_EXPR
        ) and (
            open_token is not None
            and (
                (current_token.text == "]" and open_token.text == "[")
                or (current_token.text == ")" and open_token.text == "(")
                or (current_token.text == "}" and open_token.text == "{")
            )
        )

    def _get_next_token(self, previous_token, open_token):
        token = None
        self._readWhitespace()

        c = self._input.peek()
        if c is None:
            token = self._create_token(TOKEN.EOF, "")

        token = token or self._read_non_javascript(c)
        token = token or self._read_string(c)
        token = token or self._read_pair(
            c, self._input.peek(1)
        )  # Issue #2062 hack for record type '#{'
        token = token or self._read_word(previous_token)
        token = token or self._read_singles(c)
        token = token or self._read_comment(c)
        token = token or self._read_regexp(c, previous_token)
        token = token or self._read_xml(c, previous_token)
        token = token or self._read_punctuation()
        token = token or self._create_token(TOKEN.UNKNOWN, self._input.next())

        return token

    def _read_singles(self, c):
        token = None

        if c == "(" or c == "[":
            token = self._create_token(TOKEN.START_EXPR, c)
        elif c == ")" or c == "]":
            token = self._create_token(TOKEN.END_EXPR, c)
        elif c == "{":
            token = self._create_token(TOKEN.START_BLOCK, c)
        elif c == "}":
            token = self._create_token(TOKEN.END_BLOCK, c)
        elif c == ";":
            token = self._create_token(TOKEN.SEMICOLON, c)
        elif (
            c == "."
            and self._input.peek(1) is not None
            and bool(dot_pattern.match(self._input.peek(1)))
        ):
            token = self._create_token(TOKEN.DOT, c)
        elif c == ",":
            token = self._create_token(TOKEN.COMMA, c)

        if token is not None:
            self._input.next()

        return token

    def _read_pair(self, c, d):
        token = None

        if c == "#" and d == "{":
            token = self._create_token(TOKEN.START_BLOCK, c + d)

        if token is not None:
            self._input.next()
            self._input.next()

        return token

    def _read_word(self, previous_token):
        resulting_string = self._patterns.identifier.read()

        if bool(resulting_string):
            resulting_string = re.sub(self.acorn.allLineBreaks, "\n", resulting_string)
            if not (
                previous_token.type == TOKEN.DOT
                or (
                    previous_token.type == TOKEN.RESERVED
                    and (previous_token.text == "set" or previous_token.text == "get")
                )
            ) and reserved_word_pattern.match(resulting_string):
                if (resulting_string == "in" or resulting_string == "of") and (
                    previous_token.type == TOKEN.WORD
                    or previous_token.type == TOKEN.STRING
                ):
                    # in and of are operators, need to hack
                    return self._create_token(TOKEN.OPERATOR, resulting_string)

                return self._create_token(TOKEN.RESERVED, resulting_string)

            return self._create_token(TOKEN.WORD, resulting_string)

        resulting_string = self._patterns.number.read()
        if resulting_string != "":
            return self._create_token(TOKEN.WORD, resulting_string)

    def _read_comment(self, c):
        token = None
        if c == "/":
            comment = ""
            if self._input.peek(1) == "*":  # peek /* .. */ comment
                comment = self._patterns.block_comment.read()

                directives = directives_core.get_directives(comment)
                if directives and directives.get("ignore") == "start":
                    comment += directives_core.readIgnored(self._input)
                comment = re.sub(self.acorn.allLineBreaks, "\n", comment)
                token = self._create_token(TOKEN.BLOCK_COMMENT, comment)
                token.directives = directives

            elif self._input.peek(1) == "/":  # peek // comment
                comment = self._patterns.comment.read()
                token = self._create_token(TOKEN.COMMENT, comment)

        return token

    def _read_string(self, c):
        if c == "`" or c == "'" or c == '"':
            resulting_string = self._input.next()
            self.has_char_escapes = False

            if c == "`":
                resulting_string += self.parse_string("`", True, "${")
            else:
                resulting_string += self.parse_string(c)

            if self.has_char_escapes and self._options.unescape_strings:
                resulting_string = self.unescape_string(resulting_string)

            if self._input.peek() == c:
                resulting_string += self._input.next()

            resulting_string = re.sub(self.acorn.allLineBreaks, "\n", resulting_string)

            return self._create_token(TOKEN.STRING, resulting_string)

        return None

    def _read_regexp(self, c, previous_token):
        if c == "/" and self.allowRegExOrXML(previous_token):
            # handle regexp
            resulting_string = self._input.next()
            esc = False

            in_char_class = False
            while (
                self._input.hasNext()
                and (esc or in_char_class or self._input.peek() != c)
                and not self._input.testChar(self.acorn.newline)
            ):
                resulting_string += self._input.peek()
                if not esc:
                    esc = self._input.peek() == "\\"
                    if self._input.peek() == "[":
                        in_char_class = True
                    elif self._input.peek() == "]":
                        in_char_class = False
                else:
                    esc = False
                self._input.next()

            if self._input.peek() == c:
                resulting_string += self._input.next()

                if c == "/":
                    # regexps may have modifiers /regexp/MOD, so fetch those too
                    # Only [gim] are valid, but if the user puts in garbage, do
                    # what we can to take it.
                    resulting_string += self._input.read(self.acorn.identifier)

            return self._create_token(TOKEN.STRING, resulting_string)

        return None

    def _read_xml(self, c, previous_token):
        if self._options.e4x and c == "<" and self.allowRegExOrXML(previous_token):
            # handle e4x xml literals
            xmlStr = ""
            match = self._patterns.xml.read_match()
            if match and not match.group(1):
                rootTag = match.group(2)
                rootTag = re.sub(r"^{\s+", "{", re.sub(r"\s+}$", "}", rootTag))
                isCurlyRoot = rootTag.startswith("{")
                depth = 0
                while bool(match):
                    isEndTag = match.group(1)
                    tagName = match.group(2)
                    isSingletonTag = (match.groups()[-1] != "") or (
                        match.group(2)[0:8] == "![CDATA["
                    )
                    if not isSingletonTag and (
                        tagName == rootTag
                        or (
                            isCurlyRoot
                            and re.sub(r"^{\s+", "{", re.sub(r"\s+}$", "}", tagName))
                        )
                    ):
                        if isEndTag:
                            depth -= 1
                        else:
                            depth += 1

                    xmlStr += match.group(0)
                    if depth <= 0:
                        break

                    match = self._patterns.xml.read_match()

                # if we didn't close correctly, keep unformatted.
                if not match:
                    xmlStr += self._input.match(re.compile(r"[\s\S]*")).group(0)

                xmlStr = re.sub(self.acorn.allLineBreaks, "\n", xmlStr)
                return self._create_token(TOKEN.STRING, xmlStr)

        return None

    def _read_non_javascript(self, c):
        resulting_string = ""

        if c == "#":
            # she-bang
            if self._is_first_token():
                resulting_string = self._patterns.shebang.read()
                if resulting_string:
                    return self._create_token(
                        TOKEN.UNKNOWN, resulting_string.strip() + "\n"
                    )

            # handles extendscript #includes
            resulting_string = self._patterns.include.read()

            if resulting_string:
                return self._create_token(
                    TOKEN.UNKNOWN, resulting_string.strip() + "\n"
                )

            c = self._input.next()

            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp
            # around line 1935
            sharp = "#"
            if self._input.hasNext() and self._input.testChar(digit):
                while True:
                    c = self._input.next()
                    sharp += c
                    if (not self._input.hasNext()) or c == "#" or c == "=":
                        break
                if c == "#":
                    pass
                elif self._input.peek() == "[" and self._input.peek(1) == "]":
                    sharp += "[]"
                    self._input.next()
                    self._input.next()
                elif self._input.peek() == "{" and self._input.peek(1) == "}":
                    sharp += "{}"
                    self._input.next()
                    self._input.next()

                return self._create_token(TOKEN.WORD, sharp)

            self._input.back()

        elif c == "<" and self._is_first_token():
            if self._patterns.html_comment_start.read():
                c = "<!--"
                while self._input.hasNext() and not self._input.testChar(
                    self.acorn.newline
                ):
                    c += self._input.next()

                self.in_html_comment = True
                return self._create_token(TOKEN.COMMENT, c)

        elif (
            c == "-" and self.in_html_comment and self._patterns.html_comment_end.read()
        ):
            self.in_html_comment = False
            return self._create_token(TOKEN.COMMENT, "-->")

        return None

    def _read_punctuation(self):
        token = None
        resulting_string = self._patterns.punct.read()
        if resulting_string != "":
            if resulting_string == "=":
                token = self._create_token(TOKEN.EQUALS, resulting_string)
            elif resulting_string == "?.":
                token = self._create_token(TOKEN.DOT, resulting_string)
            else:
                token = self._create_token(TOKEN.OPERATOR, resulting_string)

        return token

    __regexTokens = {
        TOKEN.COMMENT,
        TOKEN.START_EXPR,
        TOKEN.START_BLOCK,
        TOKEN.START,
        TOKEN.END_BLOCK,
        TOKEN.OPERATOR,
        TOKEN.EQUALS,
        TOKEN.EOF,
        TOKEN.SEMICOLON,
        TOKEN.COMMA,
    }

    def allowRegExOrXML(self, previous_token):
        return (
            (
                previous_token.type == TOKEN.RESERVED
                and previous_token.text
                in {"return", "case", "throw", "else", "do", "typeof", "yield"}
            )
            or (
                previous_token.type == TOKEN.END_EXPR
                and previous_token.text == ")"
                and previous_token.opened.previous.type == TOKEN.RESERVED
                and previous_token.opened.previous.text in {"if", "while", "for"}
            )
            or (previous_token.type in self.__regexTokens)
        )

    def parse_string(self, delimiter, allow_unescaped_newlines=False, start_sub=None):
        if delimiter == "'":
            pattern = self._patterns.single_quote
        elif delimiter == '"':
            pattern = self._patterns.double_quote
        elif delimiter == "`":
            pattern = self._patterns.template_text
        elif delimiter == "}":
            pattern = self._patterns.template_expression
        resulting_string = pattern.read()
        next = ""
        while self._input.hasNext():
            next = self._input.next()
            if next == delimiter or (
                not allow_unescaped_newlines and self.acorn.newline.match(next)
            ):
                self._input.back()
                break
            elif next == "\\" and self._input.hasNext():
                current_char = self._input.peek()
                if current_char == "x" or current_char == "u":
                    self.has_char_escapes = True
                elif current_char == "\r" and self._input.peek(1) == "\n":
                    self._input.next()

                next += self._input.next()
            elif start_sub is not None:
                if start_sub == "${" and next == "$" and self._input.peek() == "{":
                    next += self._input.next()

                if start_sub == next:
                    if delimiter == "`":
                        next += self.parse_string("}", allow_unescaped_newlines, "`")
                    else:
                        next += self.parse_string("`", allow_unescaped_newlines, "${")

                    if self._input.hasNext():
                        next += self._input.next()

            next += pattern.read()
            resulting_string += next
        return resulting_string

    def unescape_string(self, s):
        # You think that a regex would work for this
        # return s.replace(/\\x([0-9a-f]{2})/gi, function(match, val) {
        #         return String.fromCharCode(parseInt(val, 16));
        #     })
        # However, dealing with '\xff', '\\xff', '\\\xff' makes this more fun.
        out = self.acorn.six.u("")
        escaped = 0

        input_scan = InputScanner(s)
        matched = None

        while input_scan.hasNext():
            # Keep any whitespace, non-slash characters
            # also keep slash pairs.
            matched = input_scan.match(re.compile(r"([\s]|[^\\]|\\\\)+"))

            if matched:
                out += matched.group(0)

            if input_scan.peek() != "\\":
                continue

            input_scan.next()
            if input_scan.peek() == "x":
                matched = input_scan.match(re.compile(r"x([0-9A-Fa-f]{2})"))
            elif input_scan.peek() == "u":
                matched = input_scan.match(re.compile(r"u([0-9A-Fa-f]{4})"))
            else:
                out += "\\"
                if input_scan.hasNext():
                    out += input_scan.next()
                continue

            # If there's some error decoding, return the original string
            if not matched:
                return s

            escaped = int(matched.group(1), 16)

            if escaped > 0x7E and escaped <= 0xFF and matched.group(0).startswith("x"):
                # we bail out on \x7f..\xff,
                # leaving whole string escaped,
                # as it's probably completely binary
                return s
            elif escaped >= 0x00 and escaped < 0x20:
                # leave 0x00...0x1f escaped
                out += "\\" + matched.group(0)
                continue
            elif escaped == 0x22 or escaped == 0x27 or escaped == 0x5C:
                # single-quote, apostrophe, backslash - escape these
                out += "\\" + chr(escaped)
            else:
                out += self.acorn.six.unichr(escaped)

        return out
