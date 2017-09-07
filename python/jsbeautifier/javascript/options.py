# The MIT License (MIT)
#
# Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.
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

class BeautifierOptions:
    def __init__(self):
        self.indent_size = 4
        self.indent_char = ' '
        self.indent_with_tabs = False
        self.eol = 'auto'
        self.preserve_newlines = True
        self.max_preserve_newlines = 10
        self.space_in_paren = False
        self.space_in_empty_paren = False
        self.e4x = False
        self.jslint_happy = False
        self.space_after_anon_function = False
        self.brace_style = 'collapse'
        self.keep_array_indentation = False
        self.keep_function_indentation = False
        self.eval_code = False
        self.unescape_strings = False
        self.wrap_line_length = 0
        self.unindent_chained_methods = False
        self.break_chained_methods = False
        self.end_with_newline = False
        self.comma_first = False
        self.operator_position = 'before-newline'

        self.css = None
        self.js = None
        self.html = None

        # For testing of beautify ignore:start directive
        self.test_output_raw = False
        self.editorconfig = False


    def __repr__(self):
        return \
"""indent_size = %d
indent_char = [%s]
preserve_newlines = %s
max_preserve_newlines = %d
space_in_paren = %s
jslint_happy = %s
space_after_anon_function = %s
indent_with_tabs = %s
brace_style = %s
keep_array_indentation = %s
eval_code = %s
wrap_line_length = %s
unescape_strings = %s
""" % ( self.indent_size,
        self.indent_char,
        self.preserve_newlines,
        self.max_preserve_newlines,
        self.space_in_paren,
        self.jslint_happy,
        self.space_after_anon_function,
        self.indent_with_tabs,
        self.brace_style,
        self.keep_array_indentation,
        self.eval_code,
        self.wrap_line_length,
        self.unescape_strings,
        )
