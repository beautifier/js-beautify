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

class BeautifierOptions:
    def __init__(self):
        self.indent_size = 4
        self.indent_char = ' '
        self.indent_with_tabs = False
        self.preserve_newlines = False
        self.selector_separator_newline = True
        self.end_with_newline = False
        self.newline_between_rules = True
        self.space_around_combinator = False
        self.eol = 'auto'

        self.css = None
        self.js = None
        self.html = None

        # deprecated
        self.space_around_selector_separator = False

    def __repr__(self):
        return \
"""indent_size = %d
indent_char = [%s]
indent_with_tabs = [%s]
preserve_newlines = [%s]
separate_selectors_newline = [%s]
end_with_newline = [%s]
newline_between_rules = [%s]
space_around_combinator = [%s]
""" % (self.indent_size, self.indent_char, self.indent_with_tabs, self.preserve_newlines,
    self.selector_separator_newline, self.end_with_newline, self.newline_between_rules,
    self.space_around_combinator)
