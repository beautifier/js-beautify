from __future__ import print_function
import sys
import re
import copy
from .options import BeautifierOptions
from jsbeautifier.core.options import mergeOpts
from jsbeautifier.core.options import normalizeOpts
from jsbeautifier.core.output import Output
from jsbeautifier.core.inputscanner import InputScanner
from jsbeautifier.__version__ import __version__

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


whitespaceChar = re.compile(r"\s")
whitespacePattern = re.compile(r"(?:\s|\n)+")

# WORD_RE = re.compile("[\w$\-_]")


def default_options():
    return BeautifierOptions()


def beautify(string, opts=default_options()):
    b = Beautifier(string, opts)
    return b.beautify()


def beautify_file(file_name, opts=default_options()):
    if file_name == '-':  # stdin
        stream = sys.stdin
    else:
        stream = open(file_name)
    content = ''.join(stream.readlines())
    b = Beautifier(content, opts)
    return b.beautify()


def usage(stream=sys.stdout):

    print("cssbeautifier.py@" + __version__ + """

CSS beautifier (http://jsbeautifier.org/)

""", file=stream)
    if stream == sys.stderr:
        return 1
    else:
        return 0


class Printer:

    def __init__(self, indent_char, indent_size, default_indent=""):
        self.singleIndent = (indent_size) * indent_char
        self.indentLevel = 0
        self.nestedLevel = 0

        self.baseIndentString = default_indent
        self.output = Output(self.singleIndent, self.baseIndentString)

    def indent(self):
        self.indentLevel += 1

    def outdent(self):
        if self.indentLevel > 0:
            self.indentLevel -= 1

    def preserveSingleSpace(self, isAfterSpace):
        if isAfterSpace:
            self.output.space_before_token = True

    def print_string(self, output_string):
        if self.output.just_added_newline():
            self.output.set_indent(self.indentLevel)

        self.output.add_token(output_string)


class Beautifier:

    def __init__(self, source_text, opts=default_options()):
        import jsbeautifier.core.acorn as acorn
        self.lineBreak = acorn.lineBreak
        self.allLineBreaks = acorn.allLineBreaks
        self.comment_pattern = re.compile(
            acorn.six.u(r"\/\/(?:[^\n\r\u2028\u2029]*)"))
        self.block_comment_pattern = re.compile(
            r"\/\*(?:[\s\S]*?)((?:\*\/)|$)")

        if not source_text:
            source_text = ''

        self.__source_text = source_text

        opts = mergeOpts(opts, 'css')
        opts = normalizeOpts(opts)

        # Continue to accept deprecated option
        opts.space_around_combinator = opts.space_around_combinator or \
            opts.space_around_selector_separator

        self.opts = opts
        self.indentSize = opts.indent_size
        self.indentChar = opts.indent_char
        self.input = None
        self.ch = None

        if self.opts.indent_with_tabs:
            self.indentChar = "\t"
            self.indentSize = 1

        self.opts.eol = self.opts.eol.replace('\\r', '\r').replace('\\n', '\n')


        # https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule
        # also in CONDITIONAL_GROUP_RULE below
        self.NESTED_AT_RULE = {
            "@page",
            "@font-face",
            "@keyframes",
            "@media",
            "@supports",
            "@document"}
        self.CONDITIONAL_GROUP_RULE = {
            "@media",
            "@supports",
            "@document"}

    def eatString(self, endChars):
        result = ''
        self.ch = self.input.next()
        while self.ch:
            result += self.ch
            if self.ch == "\\":
                result += self.input.next()
            elif self.ch in endChars or self.ch == "\n":
                break
            self.ch = self.input.next()
        return result

    # Skips any white space in the source text from the current position.
    # When allowAtLeastOneNewLine is true, will output new lines for each
    # newline character found; if the user has preserve_newlines off, only
    # the first newline will be output
    def eatWhitespace(self, allowAtLeastOneNewLine=False):
        result = whitespaceChar.search(self.input.peek() or '') is not None
        isFirstNewLine = True

        while whitespaceChar.search(self.input.peek() or '') is not None:
            self.ch = self.input.next()
            if allowAtLeastOneNewLine and self.ch == "\n":
                if self.opts.preserve_newlines or isFirstNewLine:
                    isFirstNewLine = False
                    self.output.add_new_line(True)
        return result

    # Nested pseudo-class if we are insideRule
    # and the next special character found opens
    # a new block
    def foundNestedPseudoClass(self):
        openParen = 0
        i = 1
        ch = self.input.peek(i)
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
            ch = self.input.peek(i)

        return False

    def beautify(self):
        if self.opts.disabled:
            return self.__source_text

        source_text = self.__source_text

        if self.opts.eol == 'auto':
            self.opts.eol = '\n'
            if self.lineBreak.search(source_text or ''):
                self.opts.eol = self.lineBreak.search(source_text).group()


        # HACK: newline parsing inconsistent. This brute force normalizes the
        # input newlines.
        source_text = re.sub(self.allLineBreaks, '\n', source_text)

        m = re.search("^[\t ]*", source_text)
        self.baseIndentString = m.group(0)

        printer = Printer(
            self.indentChar,
            self.indentSize,
            self.baseIndentString)
        self.output = printer.output
        self.input = InputScanner(source_text)

        output = self.output
        input = self.input

        self.ch = None
        parenLevel = 0

        insideRule = False
        insidePropertyValue = False
        enteringConditionalGroup = False
        insideAtExtend = False
        insideAtImport = False
        topCharacter = self.ch

        while True:
            whitespace = input.read(whitespacePattern)
            isAfterSpace = whitespace != ''
            previous_ch = topCharacter
            self.ch = input.next()
            topCharacter = self.ch

            if not self.ch:
                break
            elif self.ch == '/' and input.peek() == '*':
                # /* css comment */
                # Always start block comments on a new line.
                # This handles scenarios where a block comment immediately
                # follows a property definition on the same line or where
                # minified code is being beautified.
                output.add_new_line()
                input.back()
                printer.print_string(
                    input.read(
                        self.block_comment_pattern))

                # Ensures any new lines following the comment are preserved
                self.eatWhitespace(True)

                # Block comments are followed by a new line so they don't
                # share a line with other properties
                output.add_new_line()
            elif self.ch == '/' and input.peek() == '/':
                # // single line comment
                # Preserves the space before a comment
                # on the same line as a rule
                output.space_before_token = True
                input.back()
                printer.print_string(input.read(self.comment_pattern))

                # Ensures any new lines following the comment are preserved
                self.eatWhitespace(True)
            elif self.ch == '@':
                printer.preserveSingleSpace(isAfterSpace)

                # deal with less propery mixins @{...}
                if input.peek() == '{':
                    printer.print_string(self.ch + self.eatString('}'))
                else:
                    printer.print_string(self.ch)
                    # strip trailing space, for hash property check
                    variableOrRule = input.peekUntilAfter(
                        re.compile(r"[: ,;{}()[\]\/='\"]"))

                    if variableOrRule[-1] in ": ":
                        # wwe have a variable or pseudo-class, add it and
                        # insert one space before continuing
                        variableOrRule = self.eatString(": ")
                        if variableOrRule[-1].isspace():
                            variableOrRule = variableOrRule[:-1]
                        printer.print_string(variableOrRule)
                        output.space_before_token = True

                    if variableOrRule[-1].isspace():
                        variableOrRule = variableOrRule[:-1]

                    if variableOrRule == "extend":
                        insideAtExtend = True
                    elif variableOrRule == "import":
                        insideAtImport = True

                    # might be a nesting at-rule
                    if variableOrRule in self.NESTED_AT_RULE:
                        printer.nestedLevel += 1
                        if variableOrRule in self.CONDITIONAL_GROUP_RULE:
                            enteringConditionalGroup = True
                    elif not insideRule and parenLevel == 0 and \
                            variableOrRule[-1] == ":":
                        insidePropertyValue = True
                        printer.indent()
            elif self.ch == '#' and input.peek() == '{':
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.ch + self.eatString('}'))
            elif self.ch == '{':
                if insidePropertyValue:
                    insidePropertyValue = False
                    printer.outdent()
                printer.indent()
                output.space_before_token = True
                printer.print_string(self.ch)

                # when entering conditional groups, only rulesets are
                # allowed
                if enteringConditionalGroup:
                    enteringConditionalGroup = False
                    insideRule = printer.indentLevel > printer.nestedLevel
                else:
                    # otherwise, declarations are also allowed
                    insideRule = printer.indentLevel >= printer.nestedLevel

                if self.opts.newline_between_rules and insideRule:
                    if output.previous_line and \
                            not output.previous_line.is_empty() and \
                            output.previous_line.item(-1) != '{':
                        output.ensure_empty_line_above('/', ',')
                self.eatWhitespace(True)
                output.add_new_line()
            elif self.ch == '}':
                printer.outdent()
                output.add_new_line()
                if previous_ch == '{':
                    output.trim(True)
                insideAtExtend = False
                insideAtImport = False
                if insidePropertyValue:
                    printer.outdent()
                    insidePropertyValue = False
                printer.print_string(self.ch)
                insideRule = False
                if printer.nestedLevel:
                    printer.nestedLevel -= 1

                self.eatWhitespace(True)
                output.add_new_line()

                if self.opts.newline_between_rules and \
                        not output.just_added_blankline():
                    if input.peek() != '}':
                        output.add_new_line(True)
            elif self.ch == ":":
                if (insideRule or enteringConditionalGroup) and \
                        not (input.lookBack('&') or
                             self.foundNestedPseudoClass()) and \
                        not input.lookBack('(') and not insideAtExtend:
                    # 'property: value' delimiter
                    # which could be in a conditional group query
                    printer.print_string(":")
                    if not insidePropertyValue:
                        insidePropertyValue = True
                        output.space_before_token = True
                        self.eatWhitespace(True)
                        printer.indent()

                else:
                    # sass/less parent reference don't use a space
                    # sass nested pseudo-class don't use a space

                    # preserve space before pseudoclasses/pseudoelements,
                    # as it means "in any child"
                    if input.lookBack(' '):
                        output.space_before_token = True
                    if input.peek() == ":":
                        # pseudo-element
                        self.ch = input.next()
                        printer.print_string("::")
                    else:
                        # pseudo-element
                        printer.print_string(":")
            elif self.ch == '"' or self.ch == '\'':
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.ch + self.eatString(self.ch))
                self.eatWhitespace(True)
            elif self.ch == ';':
                if insidePropertyValue:
                    printer.outdent()
                    insidePropertyValue = False
                insideAtExtend = False
                insideAtImport = False
                printer.print_string(self.ch)
                self.eatWhitespace(True)

                # This maintains single line comments on the same
                # line. Block comments are also affected, but
                # a new line is always output before one inside
                # that section
                if input.peek() is not '/':
                    output.add_new_line()
            elif self.ch == '(':
                # may be a url
                if input.lookBack("url"):
                    printer.print_string(self.ch)
                    self.eatWhitespace()
                    self.ch = input.next()
                    if self.ch in {')', '"', '\''}:
                        input.back()
                        parenLevel += 1
                    elif self.ch is not None:
                        printer.print_string(self.ch + self.eatString(')'))
                else:
                    parenLevel += 1
                    printer.preserveSingleSpace(isAfterSpace)
                    printer.print_string(self.ch)
                    self.eatWhitespace()
            elif self.ch == ')':
                printer.print_string(self.ch)
                parenLevel -= 1
            elif self.ch == ',':
                printer.print_string(self.ch)
                self.eatWhitespace(True)
                if self.opts.selector_separator_newline and \
                        not insidePropertyValue and parenLevel < 1 and \
                        not insideAtImport:
                    output.add_new_line()
                else:
                    output.space_before_token = True
            elif (self.ch == '>' or self.ch == '+' or self.ch == '~') and \
                    not insidePropertyValue and parenLevel < 1:
                # handle combinator spacing
                if self.opts.space_around_combinator:
                    output.space_before_token = True
                    printer.print_string(self.ch)
                    output.space_before_token = True
                else:
                    printer.print_string(self.ch)
                    self.eatWhitespace()
                    # squash extra whitespace
                    if self.ch and bool(whitespaceChar.search(self.ch)):
                        self.ch = ''
            elif self.ch == ']':
                printer.print_string(self.ch)
            elif self.ch == '[':
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.ch)
            elif self.ch == '=':
                # no whitespace before or after
                self.eatWhitespace()
                printer.print_string('=')
                if bool(whitespaceChar.search(self.ch)):
                    self.ch = ''
            elif self.ch == '!':  # !important
                printer.print_string(' ')
                printer.print_string(self.ch)
            else:
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.ch)

        sweet_code = output.get_code(self.opts.end_with_newline, self.opts.eol)

        return sweet_code
