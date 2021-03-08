from __future__ import print_function
import sys
import re
import copy
from .options import BeautifierOptions
from jsbeautifier.core.output import Output
from jsbeautifier.core.inputscanner import InputScanner
from jsbeautifier.core.directives import Directives
from cssbeautifier.__version__ import __version__

# This is not pretty, but given how we did the version import
# it is the only way to do this without having setup.py fail on a missing
# six dependency.
six = __import__("six")

#
# The MIT License (MIT)

# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


directives_core = Directives(r"/\*", r"\*/")

whitespaceChar = re.compile(r"\s")
whitespacePattern = re.compile(r"(?:\s|\n)+")

# WORD_RE = re.compile("[\w$\-_]")


def default_options():
    return BeautifierOptions()


def beautify(string, opts=default_options()):
    b = Beautifier(string, opts)
    return b.beautify()


def beautify_file(file_name, opts=default_options()):
    if file_name == "-":  # stdin
        stream = sys.stdin
    else:
        stream = open(file_name)
    content = "".join(stream.readlines())
    b = Beautifier(content, opts)
    return b.beautify()


def usage(stream=sys.stdout):

    print(
        "cssbeautifier.py@"
        + __version__
        + """

CSS beautifier (https://beautifier.io/)

""",
        file=stream,
    )
    if stream == sys.stderr:
        return 1
    else:
        return 0


class Beautifier:
    def __init__(self, source_text, opts=default_options()):
        # in javascript, these two differ
        # in python they are the same, different methods are called on them
        # IMPORTANT: This string must be run through six to handle \u chars
        self.lineBreak = re.compile(six.u(r"\r\n|[\n\r]"))
        self.allLineBreaks = self.lineBreak

        self.comment_pattern = re.compile(six.u(r"\/\/(?:[^\n\r\u2028\u2029]*)"))
        self.block_comment_pattern = re.compile(r"\/\*(?:[\s\S]*?)((?:\*\/)|$)")

        if not source_text:
            source_text = ""

        self.__source_text = source_text

        self._options = BeautifierOptions(opts)
        self._input = None
        self._ch = None

        self._indentLevel = 0
        self._nestedLevel = 0
        self._output = None

        # https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule
        # also in CONDITIONAL_GROUP_RULE below
        self.NESTED_AT_RULE = {
            "@page",
            "@font-face",
            "@keyframes",
            "@media",
            "@supports",
            "@document",
        }
        self.CONDITIONAL_GROUP_RULE = {"@media", "@supports", "@document"}

    def eatString(self, endChars):
        result = ""
        self._ch = self._input.next()
        while self._ch:
            result += self._ch
            if self._ch == "\\":
                result += self._input.next()
            elif self._ch in endChars or self._ch == "\n":
                break
            self._ch = self._input.next()
        return result

    # Skips any white space in the source text from the current position.
    # When allowAtLeastOneNewLine is true, will output new lines for each
    # newline character found; if the user has preserve_newlines off, only
    # the first newline will be output
    def eatWhitespace(self, allowAtLeastOneNewLine=False):
        result = whitespaceChar.search(self._input.peek() or "") is not None
        isFirstNewLine = True
        newline_count = 0
        while whitespaceChar.search(self._input.peek() or "") is not None:
            self._ch = self._input.next()
            if allowAtLeastOneNewLine and self._ch == "\n":
                if (
                    newline_count == 0
                    or newline_count < self._options.max_preserve_newlines
                ):
                    newline_count += 1
                    self._output.add_new_line(True)
        return result

    # Nested pseudo-class if we are insideRule
    # and the next special character found opens
    # a new block
    def foundNestedPseudoClass(self):
        openParen = 0
        i = 1
        ch = self._input.peek(i)
        while ch:
            if ch == "{":
                return True
            elif ch == "(":
                # pseudoclasses can contain ()
                openParen += 1
            elif ch == ")":
                if openParen == 0:
                    return False
                openParen -= 1
            elif ch == ";" or ch == "}":
                return False
            i += 1
            ch = self._input.peek(i)

        return False

    def indent(self):
        self._indentLevel += 1

    def outdent(self):
        if self._indentLevel > 0:
            self._indentLevel -= 1

    def preserveSingleSpace(self, isAfterSpace):
        if isAfterSpace:
            self._output.space_before_token = True

    def print_string(self, output_string):
        self._output.set_indent(self._indentLevel)
        self._output.non_breaking_space = True
        self._output.add_token(output_string)

    def beautify(self):
        if self._options.disabled:
            return self.__source_text

        source_text = self.__source_text

        if self._options.eol == "auto":
            self._options.eol = "\n"
            if self.lineBreak.search(source_text or ""):
                self._options.eol = self.lineBreak.search(source_text).group()

        # HACK: newline parsing inconsistent. This brute force normalizes the
        # input newlines.
        source_text = re.sub(self.allLineBreaks, "\n", source_text)
        baseIndentString = re.search("^[\t ]*", source_text).group(0)

        self._output = Output(self._options, baseIndentString)

        self._input = InputScanner(source_text)

        self._indentLevel = 0
        self._nestedLevel = 0

        self._ch = None
        parenLevel = 0

        insideRule = False
        insidePropertyValue = False
        enteringConditionalGroup = False
        insideAtExtend = False
        insideAtImport = False
        topCharacter = self._ch

        while True:
            whitespace = self._input.read(whitespacePattern)
            isAfterSpace = whitespace != ""
            previous_ch = topCharacter
            self._ch = self._input.next()
            if self._ch == "\\" and self._input.hasNext():
                self._ch += self._input.next()
            topCharacter = self._ch

            if not self._ch:
                break
            elif self._ch == "/" and self._input.peek() == "*":
                # /* css comment */
                # Always start block comments on a new line.
                # This handles scenarios where a block comment immediately
                # follows a property definition on the same line or where
                # minified code is being beautified.
                self._output.add_new_line()
                self._input.back()
                comment = self._input.read(self.block_comment_pattern)

                # handle ignore directive
                directives = directives_core.get_directives(comment)
                if directives and directives.get("ignore") == "start":
                    comment += directives_core.readIgnored(self._input)

                self.print_string(comment)

                # Ensures any new lines following the comment are preserved
                self.eatWhitespace(True)

                # Block comments are followed by a new line so they don't
                # share a line with other properties
                self._output.add_new_line()
            elif self._ch == "/" and self._input.peek() == "/":
                # // single line comment
                # Preserves the space before a comment
                # on the same line as a rule
                self._output.space_before_token = True
                self._input.back()
                self.print_string(self._input.read(self.comment_pattern))

                # Ensures any new lines following the comment are preserved
                self.eatWhitespace(True)
            elif self._ch == "@":
                self.preserveSingleSpace(isAfterSpace)

                # deal with less propery mixins @{...}
                if self._input.peek() == "{":
                    self.print_string(self._ch + self.eatString("}"))
                else:
                    self.print_string(self._ch)
                    # strip trailing space, for hash property check
                    variableOrRule = self._input.peekUntilAfter(
                        re.compile(r"[: ,;{}()[\]\/='\"]")
                    )

                    if variableOrRule[-1] in ": ":
                        # wwe have a variable or pseudo-class, add it and
                        # insert one space before continuing
                        variableOrRule = self.eatString(": ")
                        if variableOrRule[-1].isspace():
                            variableOrRule = variableOrRule[:-1]
                        self.print_string(variableOrRule)
                        self._output.space_before_token = True

                    if variableOrRule[-1].isspace():
                        variableOrRule = variableOrRule[:-1]

                    if variableOrRule == "extend":
                        insideAtExtend = True
                    elif variableOrRule == "import":
                        insideAtImport = True

                    # might be a nesting at-rule
                    if variableOrRule in self.NESTED_AT_RULE:
                        self._nestedLevel += 1
                        if variableOrRule in self.CONDITIONAL_GROUP_RULE:
                            enteringConditionalGroup = True
                    elif (
                        not insideRule and parenLevel == 0 and variableOrRule[-1] == ":"
                    ):
                        insidePropertyValue = True
                        self.indent()
            elif self._ch == "#" and self._input.peek() == "{":
                self.preserveSingleSpace(isAfterSpace)
                self.print_string(self._ch + self.eatString("}"))
            elif self._ch == "{":
                if insidePropertyValue:
                    insidePropertyValue = False
                    self.outdent()

                # when entering conditional groups, only rulesets are
                # allowed
                if enteringConditionalGroup:
                    enteringConditionalGroup = False
                    insideRule = self._indentLevel >= self._nestedLevel
                else:
                    # otherwise, declarations are also allowed
                    insideRule = self._indentLevel >= self._nestedLevel - 1

                if self._options.newline_between_rules and insideRule:
                    if (
                        self._output.previous_line
                        and not self._output.previous_line.is_empty()
                        and self._output.previous_line.item(-1) != "{"
                    ):
                        self._output.ensure_empty_line_above("/", ",")

                self._output.space_before_token = True

                # The difference in print_string and indent order
                # is necessary to indent the '{' correctly
                if self._options.brace_style == "expand":
                    self._output.add_new_line()
                    self.print_string(self._ch)
                    self.indent()
                    self._output.set_indent(self._indentLevel)
                else:
                    self.indent()
                    self.print_string(self._ch)

                self.eatWhitespace(True)
                self._output.add_new_line()
            elif self._ch == "}":
                self.outdent()
                self._output.add_new_line()
                if previous_ch == "{":
                    self._output.trim(True)
                insideAtExtend = False
                insideAtImport = False
                if insidePropertyValue:
                    self.outdent()
                    insidePropertyValue = False
                self.print_string(self._ch)
                insideRule = False
                if self._nestedLevel:
                    self._nestedLevel -= 1

                self.eatWhitespace(True)
                self._output.add_new_line()

                if (
                    self._options.newline_between_rules
                    and not self._output.just_added_blankline()
                ):
                    if self._input.peek() != "}":
                        self._output.add_new_line(True)
            elif self._ch == ":":
                if (
                    (insideRule or enteringConditionalGroup)
                    and not (self._input.lookBack("&") or self.foundNestedPseudoClass())
                    and not self._input.lookBack("(")
                    and not insideAtExtend
                    and parenLevel == 0
                ):
                    # 'property: value' delimiter
                    # which could be in a conditional group query
                    self.print_string(":")
                    if not insidePropertyValue:
                        insidePropertyValue = True
                        self._output.space_before_token = True
                        self.eatWhitespace(True)
                        self.indent()

                else:
                    # sass/less parent reference don't use a space
                    # sass nested pseudo-class don't use a space

                    # preserve space before pseudoclasses/pseudoelements,
                    # as it means "in any child"
                    if self._input.lookBack(" "):
                        self._output.space_before_token = True
                    if self._input.peek() == ":":
                        # pseudo-element
                        self._ch = self._input.next()
                        self.print_string("::")
                    else:
                        # pseudo-element
                        self.print_string(":")
            elif self._ch == '"' or self._ch == "'":
                self.preserveSingleSpace(isAfterSpace)
                self.print_string(self._ch + self.eatString(self._ch))
                self.eatWhitespace(True)
            elif self._ch == ";":
                if parenLevel == 0:
                    if insidePropertyValue:
                        self.outdent()
                        insidePropertyValue = False
                    insideAtExtend = False
                    insideAtImport = False
                    self.print_string(self._ch)
                    self.eatWhitespace(True)

                    # This maintains single line comments on the same
                    # line. Block comments are also affected, but
                    # a new line is always output before one inside
                    # that section
                    if self._input.peek() != "/":
                        self._output.add_new_line()
                else:
                    self.print_string(self._ch)
                    self.eatWhitespace(True)
                    self._output.space_before_token = True
            elif self._ch == "(":
                # may be a url
                if self._input.lookBack("url"):
                    self.print_string(self._ch)
                    self.eatWhitespace()
                    parenLevel += 1
                    self.indent()
                    self._ch = self._input.next()
                    if self._ch in {")", '"', "'"}:
                        self._input.back()
                    elif self._ch is not None:
                        self.print_string(self._ch + self.eatString(")"))
                        if parenLevel:
                            parenLevel -= 1
                            self.outdent()
                else:
                    self.preserveSingleSpace(isAfterSpace)
                    self.print_string(self._ch)
                    self.eatWhitespace()
                    parenLevel += 1
                    self.indent()
            elif self._ch == ")":
                if parenLevel:
                    parenLevel -= 1
                    self.outdent()
                self.print_string(self._ch)
            elif self._ch == ",":
                self.print_string(self._ch)
                self.eatWhitespace(True)
                if (
                    self._options.selector_separator_newline
                    and not insidePropertyValue
                    and parenLevel == 0
                    and not insideAtImport
                    and not insideAtExtend
                ):
                    self._output.add_new_line()
                else:
                    self._output.space_before_token = True
            elif (
                (self._ch == ">" or self._ch == "+" or self._ch == "~")
                and not insidePropertyValue
                and parenLevel == 0
            ):
                # handle combinator spacing
                if self._options.space_around_combinator:
                    self._output.space_before_token = True
                    self.print_string(self._ch)
                    self._output.space_before_token = True
                else:
                    self.print_string(self._ch)
                    self.eatWhitespace()
                    # squash extra whitespace
                    if self._ch and bool(whitespaceChar.search(self._ch)):
                        self._ch = ""
            elif self._ch == "]":
                self.print_string(self._ch)
            elif self._ch == "[":
                self.preserveSingleSpace(isAfterSpace)
                self.print_string(self._ch)
            elif self._ch == "=":
                # no whitespace before or after
                self.eatWhitespace()
                self.print_string("=")
                if bool(whitespaceChar.search(self._ch)):
                    self._ch = ""
            elif self._ch == "!" and not (self._input.lookBack("\\")):
                # !important
                self.print_string(" ")
                self.print_string(self._ch)
            else:
                self.preserveSingleSpace(isAfterSpace)
                self.print_string(self._ch)

        sweet_code = self._output.get_code(self._options.eol)

        return sweet_code
