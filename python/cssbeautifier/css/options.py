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

from jsbeautifier.core.options import Options as BaseOptions


class BeautifierOptions(BaseOptions):
    def __init__(self, options=None):
        BaseOptions.__init__(self, options, "css")

        self.selector_separator_newline = self._get_boolean(
            "selector_separator_newline", True
        )
        self.newline_between_rules = self._get_boolean("newline_between_rules", True)

        brace_style_split = self._get_selection_list(
            "brace_style",
            ["collapse", "expand", "end-expand", "none", "preserve-inline"],
        )
        self.brace_style = "collapse"
        for bs in brace_style_split:
            if bs != "expand":
                # default to collapse, as only collapse|expand is implemented for now
                self.brace_style = "collapse"
            else:
                self.brace_style = bs

        # deprecated
        space_around_selector_separator = self._get_boolean(
            "space_around_selector_separator"
        )

        # Continue to accept deprecated option
        self.space_around_combinator = (
            self._get_boolean("space_around_combinator")
            or space_around_selector_separator
        )
