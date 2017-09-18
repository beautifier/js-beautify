from __future__ import print_function
import sys
import re
import copy
from .options import BeautifierOptions
from jsbeautifier.core.options import mergeOpts
from jsbeautifier.core.output import Output
from jsbeautifier.__version__ import __version__

#
# The MIT License (MIT)

# Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

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

WHITE_RE = re.compile("^\s+$")
WORD_RE = re.compile("[\w$\-_]")


class Printer:

    def __init__(self, beautifier, indent_char, indent_size, default_indent=""):
        self.beautifier = beautifier
        self.newlines_from_last_ws_eat = 0
        self.indentSize = indent_size
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

    def preserveSingleSpace(self,isAfterSpace):
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

        if not source_text:
            source_text = ''

        opts = mergeOpts(opts, 'css')

        # Continue to accept deprecated option
        opts.space_around_combinator = opts.space_around_combinator or opts.space_around_selector_separator

        self.opts = opts
        self.indentSize = opts.indent_size
        self.indentChar = opts.indent_char
        self.pos = -1
        self.ch = None

        if self.opts.indent_with_tabs:
            self.indentChar = "\t"
            self.indentSize = 1

        if self.opts.eol == 'auto':
            self.opts.eol = '\n'
            if self.lineBreak.search(source_text or ''):
                self.opts.eol = self.lineBreak.search(source_text).group()

        self.opts.eol = self.opts.eol.replace('\\r', '\r').replace('\\n', '\n')

        # HACK: newline parsing inconsistent. This brute force normalizes the input newlines.
        self.source_text = re.sub(self.allLineBreaks, '\n', source_text)

        # https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule
        # also in CONDITIONAL_GROUP_RULE below
        self.NESTED_AT_RULE = [ \
            "@page", \
            "@font-face", \
            "@keyframes", \
            "@media", \
            "@supports", \
            "@document"]
        self.CONDITIONAL_GROUP_RULE = [ \
            "@media", \
            "@supports", \
            "@document"]

        m = re.search("^[\t ]*", self.source_text)
        self.baseIndentString = m.group(0)

    def next(self):
        self.pos = self.pos + 1
        if self.pos < len(self.source_text):
            self.ch = self.source_text[self.pos]
        else:
            self.ch = ''
        return self.ch

    def peek(self,skipWhitespace=False):
        start = self.pos
        if skipWhitespace:
            self.eatWhitespace()
        result = ""
        if self.pos + 1 < len(self.source_text):
            result = self.source_text[self.pos + 1]
        if skipWhitespace:
            self.pos = start - 1
            self.next()

        return result

    def eatString(self, endChars):
        start = self.pos
        while self.next():
            if self.ch == "\\":
                self.next()
            elif self.ch in endChars:
                break
            elif self.ch == "\n":
                break
        return self.source_text[start:self.pos] + self.ch

    def peekString(self, endChar):
        start = self.pos
        st = self.eatString(endChar)
        self.pos = start - 1
        self.next()
        return st

    def eatWhitespace(self, preserve_newlines_local=False):
        result = 0
        while WHITE_RE.search(self.peek()) is not None:
            self.next()
            if self.ch == "\n" and preserve_newlines_local and self.opts.preserve_newlines:
                self.output.add_new_line(True)
                result += 1
        self.newlines_from_last_ws_eat = result
        return result

    def skipWhitespace(self):
        result = ''
        if self.ch and WHITE_RE.search(self.ch):
            result = self.ch

        while WHITE_RE.search(self.next()) is not None:
            result += self.ch
        return result

    def eatComment(self):
        start = self.pos
        singleLine = self.peek() == "/"
        self.next()
        while self.next():
            if not singleLine and self.ch == "*" and self.peek() == "/":
                self.next()
                break
            elif singleLine and self.ch == "\n":
                return self.source_text[start:self.pos]
        return self.source_text[start:self.pos] + self.ch

    def lookBack(self, string):
        past = self.source_text[self.pos - len(string):self.pos]
        return past.lower() == string

    # Nested pseudo-class if we are insideRule
    # and the next special character found opens
    # a new block
    def foundNestedPseudoClass(self):
        i = self.pos + 1
        openParen = 0
        while i < len(self.source_text):
            ch = self.source_text[i]
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

        return False

    def beautify(self):
        printer = Printer(self, self.indentChar, self.indentSize, self.baseIndentString)
        self.output = printer.output
        output = self.output

        self.pos = -1
        self.ch = None

        insideRule = False
        insidePropertyValue = False
        enteringConditionalGroup = False
        top_ch = ''
        last_top_ch = ''
        parenLevel = 0

        while True:
            whitespace = self.skipWhitespace()
            isAfterSpace = whitespace != ''
            isAfterNewline = '\n' in whitespace
            last_top_ch = top_ch
            top_ch = self.ch

            if not self.ch:
                break
            elif self.ch == '/' and self.peek() == '*':
                header = printer.indentLevel == 0

                if not isAfterNewline or header:
                    output.add_new_line()

                printer.print_string(self.eatComment())
                output.add_new_line()
                if header:
                    output.add_new_line(True)
            elif self.ch == '/' and self.peek() == '/':
                if not isAfterNewline and last_top_ch != '{':
                    output.trim(True)

                output.space_before_token = True
                printer.print_string(self.eatComment())
                output.add_new_line()
            elif self.ch == '@':
                printer.preserveSingleSpace(isAfterSpace)

                # deal with less propery mixins @{...}
                if self.peek(True) == '{':
                    printer.print_string(self.eatString('}'));
                else:
                    printer.print_string(self.ch)
                    # strip trailing space, if present, for hash property check
                    variableOrRule = self.peekString(": ,;{}()[]/='\"")

                    if variableOrRule[-1] in ": ":
                        # wwe have a variable or pseudo-class, add it and insert one space before continuing
                        self.next()
                        variableOrRule = self.eatString(": ")
                        if variableOrRule[-1].isspace():
                            variableOrRule = variableOrRule[:-1]
                        printer.print_string(variableOrRule)
                        output.space_before_token = True

                    if variableOrRule[-1].isspace():
                        variableOrRule = variableOrRule[:-1]

                    # might be a nesting at-rule
                    if variableOrRule in self.NESTED_AT_RULE:
                        printer.nestedLevel += 1
                        if variableOrRule in self.CONDITIONAL_GROUP_RULE:
                            enteringConditionalGroup = True
            elif self.ch == '#' and self.peek() == '{':
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.eatString('}'));
            elif self.ch == '{':
                if self.peek(True) == '}':
                    self.eatWhitespace()
                    self.next()
                    output.space_before_token = True
                    printer.print_string("{}")
                    if self.eatWhitespace(True) == 0:
                        output.add_new_line()

                    if self.newlines_from_last_ws_eat < 2 and self.opts.newline_between_rules and printer.indentLevel == 0:
                        output.add_new_line(True)
                else:
                    printer.indent()
                    output.space_before_token = True
                    printer.print_string(self.ch)
                    if self.eatWhitespace(True) == 0:
                        output.add_new_line()

                    # when entering conditional groups, only rulesets are allowed
                    if enteringConditionalGroup:
                        enteringConditionalGroup = False
                        insideRule = printer.indentLevel > printer.nestedLevel
                    else:
                        # otherwise, declarations are also allowed
                        insideRule = printer.indentLevel >= printer.nestedLevel
            elif self.ch == '}':
                printer.outdent()
                output.add_new_line()
                printer.print_string(self.ch)
                insideRule = False
                insidePropertyValue = False
                if printer.nestedLevel:
                    printer.nestedLevel -= 1

                if self.eatWhitespace(True) == 0:
                    output.add_new_line()


                if self.newlines_from_last_ws_eat < 2 and self.opts.newline_between_rules and printer.indentLevel == 0:
                    output.add_new_line(True)
            elif self.ch == ":":
                self.eatWhitespace()
                if (insideRule or enteringConditionalGroup) and \
                        not (self.lookBack('&') or self.foundNestedPseudoClass()) and \
                        not self.lookBack('('):
                    # 'property: value' delimiter
                    # which could be in a conditional group query
                    printer.print_string(":")
                    if not insidePropertyValue:
                        insidePropertyValue = True
                        output.space_before_token = True

                else:
                    # sass/less parent reference don't use a space
                    # sass nested pseudo-class don't use a space

                    # preserve space before pseudoclasses/pseudoelements, as it means "in any child"
                    if self.lookBack(' '):
                        output.space_before_token = True
                    if self.peek() == ":":
                        # pseudo-element
                        self.next()
                        printer.print_string("::")
                    else:
                        # pseudo-element
                        printer.print_string(":")
            elif self.ch == '"' or self.ch == '\'':
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.eatString(self.ch))
            elif self.ch == ';':
                insidePropertyValue = False
                printer.print_string(self.ch)
                if self.eatWhitespace(True) == 0:
                    output.add_new_line()
            elif self.ch == '(':
                # may be a url
                if self.lookBack("url"):
                    printer.print_string(self.ch)
                    self.eatWhitespace()
                    if self.next():
                        if self.ch is not ')' and self.ch is not '"' \
                        and self.ch is not '\'':
                            printer.print_string(self.eatString(')'))
                        else:
                            self.pos = self.pos - 1
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
                if self.eatWhitespace(True) == 0 and not insidePropertyValue and self.opts.selector_separator_newline and parenLevel < 1:
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
                    if self.ch and WHITE_RE.search(self.ch):
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
                if WHITE_RE.search(self.ch):
                    self.ch = ''
            else:
                printer.preserveSingleSpace(isAfterSpace)
                printer.print_string(self.ch)

        sweet_code = output.get_code(self.opts.end_with_newline, self.opts.eol)

        return sweet_code
