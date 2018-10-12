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


from ..core.options import Options as BaseOptions

OPERATOR_POSITION = [
    'before-newline',
    'after-newline',
    'preserve-newline'
]

class BeautifierOptions(BaseOptions):
    def __init__(self, options=None):
        BaseOptions.__init__(self, options, 'js')

        self.css = None
        self.js = None
        self.html = None

        # compatibility, re

        raw_brace_style = getattr(self.raw_options, 'brace_style', None)
        if raw_brace_style == "expand-strict": # graceful handling of deprecated option
            setattr(self.raw_options, 'brace_style', "expand")
        elif raw_brace_style == "collapse-preserve-inline": # graceful handling of deprecated option
            setattr(self.raw_options, 'brace_style', "collapse,preserve-inline")
        # elif bool(self.raw_options.braces_on_own_line): # graceful handling of deprecated option
        #     raw_brace_style = "expand": "collapse"
        # elif raw_brace_style is None: # Nothing exists to set it
        #     setattr(self.raw_options, 'brace_style', "collapse")

        # preserve-inline in delimited string will trigger brace_preserve_inline, everything
        # else is considered a brace_style and the last one only will have an effect

        brace_style_split = self._get_selection_list('brace_style', ['collapse', 'expand', 'end-expand', 'none', 'preserve-inline'])

        # preserve-inline in delimited string will trigger brace_preserve_inline
        # Everything else is considered a brace_style and the last one only will
        # have an effect
        # specify defaults in case one half of meta-option is missing
        self.brace_preserve_inline = False
        self.brace_style = "collapse"

        for bs in brace_style_split:
            if bs == "preserve-inline":
                self.brace_preserve_inline = True
            else:
                self.brace_style = bs

        self.unindent_chained_methods = self._get_boolean('unindent_chained_methods')
        self.break_chained_methods = self._get_boolean('break_chained_methods')
        self.space_in_paren = self._get_boolean('space_in_paren')
        self.space_in_empty_paren = self._get_boolean('space_in_empty_paren')
        self.jslint_happy = self._get_boolean('jslint_happy')
        self.space_after_anon_function = self._get_boolean('space_after_anon_function')
        self.space_after_named_function = self._get_boolean('space_after_named_function')
        self.keep_array_indentation = self._get_boolean('keep_array_indentation')
        self.space_before_conditional = self._get_boolean('space_before_conditional', True)
        self.unescape_strings = self._get_boolean('unescape_strings')
        self.e4x = self._get_boolean('e4x')
        self.comma_first = self._get_boolean('comma_first')
        self.operator_position = self._get_selection('operator_position', OPERATOR_POSITION)

        # For testing of beautify preserve:start directive
        self.test_output_raw = False
        self.editorconfig = False

        # force opts.space_after_anon_function to true if opts.jslint_happy
        if self.jslint_happy:
            self.space_after_anon_function = True

        self.eval_code = False
