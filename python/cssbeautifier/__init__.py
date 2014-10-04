from __future__ import print_function
import sys
import re
from cssbeautifier.__version__ import __version__

#
# The MIT License (MIT)

# Copyright (c) 2013 Einar Lielmanis and contributors.

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


class BeautifierOptions:
    def __init__(self):
        self.indent_size = 4
        self.indent_char = ' '
        self.selector_separator_newline = True
        self.end_with_newline = False

    def __repr__(self):
        return \
"""indent_size = %d
indent_char = [%s]
separate_selectors_newline = [%s]
end_with_newline = [%s]
""" % (self.indent_size, self.indent_char,
       self.separate_selectors, self.end_with_newline)


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

    def __init__(self, indent_char, indent_size, default_indent=""):
        self.indentSize = indent_size
        self.singleIndent = (indent_size) * indent_char
        self.indentLevel = 0
        self.nestedLevel = 0
 		
        self.baseIndentString = default_indent
        self.output = []
        if self.baseIndentString:
            self.push(self.baseIndentString)

    def __lastCharWhitespace(self):
        return len(self.output) > 0 and WHITE_RE.search(self.output[-1]) is not None

    def indent(self):
        self.indentLevel += 1
        self.baseIndentString += self.singleIndent

    def outdent(self):
        if self.indentLevel:
            self.indentLevel -= 1
            self.baseIndentString = self.baseIndentString[:-(len(self.singleIndent))]

    def push(self, string):
        self.output.append(string)

    def openBracket(self):
        self.singleSpace()
        self.output.append("{")
        self.newLine()

    def closeBracket(self):
        self.newLine()
        self.output.append("}")
        self.newLine()

    def semicolon(self):
        self.output.append(";")
        self.newLine()

    def comment(self, comment):
        self.output.append(comment)

    def newLine(self, keepWhitespace=False):
        if not keepWhitespace:
            self.trim()

        if len(self.output) > 0:
            self.output.append("\n")

        if len(self.baseIndentString) > 0:
            self.output.append(self.baseIndentString)

    def trim(self):
        while self.__lastCharWhitespace():
            self.output.pop()

    def singleSpace(self):
        if len(self.output) > 0 and not self.__lastCharWhitespace():
            self.output.append(" ")

    def result(self):
        return "".join(self.output)


class Beautifier:

    def __init__(self, source_text, opts=default_options()):
        self.source_text = source_text
        self.opts = opts
        self.indentSize = opts.indent_size
        self.indentChar = opts.indent_char
        self.pos = -1
        self.ch = None
        
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

    def eatWhitespace(self):
        result = ''
        while WHITE_RE.search(self.peek()) is not None:
            self.next()
            result += self.ch
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
        while i < len(self.source_text):
            ch = self.source_text[i]
            if ch == "{":
                return True
            elif ch == ";" or ch == "}" or ch == ")":
                return False
            i += 1;
            
        return False
        

    def beautify(self):
        m = re.search("^[\t ]*", self.source_text)
        baseIndentString = m.group(0)
        printer = Printer(self.indentChar, self.indentSize, baseIndentString)

        insideRule = False
        enteringConditionalGroup = False
        top_ch = '' 
        last_top_ch = '' 
        
        while True:
            whitespace = self.skipWhitespace();
            isAfterSpace = whitespace != ''
            isAfterNewline = '\n' in whitespace;
            last_top_ch = top_ch
            top_ch = self.ch
            
            if not self.ch:
                break
            elif self.ch == '/' and self.peek() == '*':
                printer.newLine()
                comment = self.eatComment()
                printer.comment(comment)
                printer.newLine()                
                header = self.lookBack("")
                if header:
                    printer.newLine(True)
            elif self.ch == '/' and self.peek() == '/':
                if not isAfterNewline and last_top_ch != '{':
                    printer.trim()
                    
                printer.singleSpace()
                printer.comment(self.eatComment())
                printer.newLine()
            elif self.ch == '@':
                # pass along the space we found as a separate item
                if isAfterSpace:
                    printer.singleSpace()
                printer.push(self.ch)

                # strip trailing space, if present, for hash property check
                variableOrRule = self.peekString(": ,;{}()[]/='\"")
                if variableOrRule[-1].isspace():
                    variableOrRule = variableOrRule[:-1]

                # might be a nesting at-rule
                if variableOrRule in self.NESTED_AT_RULE:
                    printer.nestedLevel += 1
                    if variableOrRule in self.CONDITIONAL_GROUP_RULE:
                        enteringConditionalGroup = True
                elif variableOrRule[-1] in ": ":
                    # we have a variable, add it and a space after
                    self.next()
                    variableOrRule = self.eatString(": ")
                    if variableOrRule[-1].isspace():
                        variableOrRule = variableOrRule[:-1]
                    printer.push(variableOrRule)
                    printer.singleSpace();


            elif self.ch == '{':
                if self.peek(True) == '}':
                    self.eatWhitespace()
                    self.next()
                    printer.singleSpace()
                    printer.push("{}")
                else:
                    printer.indent()
                    printer.openBracket()
                    # when entering conditional groups, only rulesets are allowed
                    if enteringConditionalGroup:
                        enteringConditionalGroup = False
                        insideRule = printer.indentLevel > printer.nestedLevel
                    else:
                        # otherwise, declarations are also allowed
                        insideRule = printer.indentLevel >= printer.nestedLevel
            elif self.ch == '}':
                printer.outdent()
                printer.closeBracket()
                insideRule = False
                if printer.nestedLevel:
                    printer.nestedLevel -= 1
            elif self.ch == ":":
                self.eatWhitespace()
                if (insideRule or enteringConditionalGroup) and \
                        not (self.lookBack('&') or self.foundNestedPseudoClass()):
                    # 'property: value' delimiter
                    # which could be in a conditional group query
                    printer.push(":")
                    printer.singleSpace()
                else:
                    # sass/less parent reference don't use a space
                    # sass nested pseudo-class don't use a space
                    if self.peek() == ":":
                        # pseudo-element
                        self.next()
                        printer.push("::")
                    else:
                        # pseudo-element
                        printer.push(":")                    
            elif self.ch == '"' or self.ch == '\'':
                if isAfterSpace:
                    printer.singleSpace()
                printer.push(self.eatString(self.ch))
            elif self.ch == ';':
                printer.semicolon()
            elif self.ch == '(':
                # may be a url
                if self.lookBack("url"):
                    printer.push(self.ch)
                    self.eatWhitespace()
                    if self.next():
                        if self.ch is not ')' and self.ch is not '"' \
                        and self.ch is not '\'':
                            printer.push(self.eatString(')'))
                        else:
                            self.pos = self.pos - 1
                else:
                    if isAfterSpace:
                        printer.singleSpace()
                    printer.push(self.ch)
                    self.eatWhitespace()
            elif self.ch == ')':
                printer.push(self.ch)
            elif self.ch == ',':
                printer.push(self.ch)
                self.eatWhitespace()
                if not insideRule and self.opts.selector_separator_newline:
                    printer.newLine()
                else:
                    printer.singleSpace()
            elif self.ch == ']':
                printer.push(self.ch)
            elif self.ch == '[':
                if isAfterSpace:
                    printer.singleSpace()
                printer.push(self.ch)
            elif self.ch == '=':
                # no whitespace before or after
                self.eatWhitespace()
                printer.push(self.ch)
            else:
                if isAfterSpace:
                    printer.singleSpace()

                printer.push(self.ch)

        sweet_code = re.sub('[\r\n\t ]+$', '', printer.result())

        # establish end_with_newline
        if self.opts.end_with_newline:
            sweet_code += "\n"

        return sweet_code