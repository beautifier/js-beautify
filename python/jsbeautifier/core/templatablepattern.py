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

import copy
from ..core.pattern import Pattern

__all__ = ["TemplatablePattern"]


class TemplateNames:
    def __init__(self):
        self.django = False
        self.erb = False
        self.handlebars = False
        self.php = False
        self.smarty = False


class TemplatePatterns:
    def __init__(self, input_scanner):
        pattern = Pattern(input_scanner)
        self.handlebars_comment = pattern.starting_with(r"{{!--").until_after(r"--}}")
        self.handlebars_unescaped = pattern.starting_with(r"{{{").until_after(r"}}}")
        self.handlebars = pattern.starting_with(r"{{").until_after(r"}}")
        self.php = pattern.starting_with(r"<\?(?:[= ]|php)").until_after(r"\?>")
        self.erb = pattern.starting_with(r"<%[^%]").until_after(r"[^%]%>")
        # django coflicts with handlebars a bit.
        self.django = pattern.starting_with(r"{%").until_after(r"%}")
        self.django_value = pattern.starting_with(r"{{").until_after(r"}}")
        self.django_comment = pattern.starting_with(r"{#").until_after(r"#}")
        self.smarty_value = pattern.starting_with(r"{(?=[^}{\s\n])").until_after(r"}")
        self.smarty_comment = pattern.starting_with(r"{\*").until_after(r"\*}")
        self.smarty_literal = pattern.starting_with(r"{literal}").until_after(
            r"{/literal}"
        )


class TemplatablePattern(Pattern):
    def __init__(self, input_scanner, parent=None):
        Pattern.__init__(self, input_scanner, parent)
        self.__template_pattern = None
        self._disabled = TemplateNames()
        self._excluded = TemplateNames()

        if parent is not None:
            self.__template_pattern = self._input.get_regexp(parent.__template_pattern)
            self._disabled = copy.copy(parent._disabled)
            self._excluded = copy.copy(parent._excluded)

        self.__patterns = TemplatePatterns(input_scanner)

    def _create(self):
        return TemplatablePattern(self._input, self)

    def _update(self):
        self.__set_templated_pattern()

    def read_options(self, options):
        result = self._create()
        for language in ["django", "erb", "handlebars", "php", "smarty"]:
            setattr(result._disabled, language, not (language in options.templating))
        result._update()
        return result

    def disable(self, language):
        result = self._create()
        setattr(result._disabled, language, True)
        result._update()
        return result

    def exclude(self, language):
        result = self._create()
        setattr(result._excluded, language, True)
        result._update()
        return result

    def read(self):
        result = ""
        if bool(self._match_pattern):
            result = self._input.read(self._starting_pattern)
        else:
            result = self._input.read(self._starting_pattern, self.__template_pattern)

        next = self._read_template()

        while bool(next):
            if self._match_pattern is not None:
                next += self._input.read(self._match_pattern)
            else:
                next += self._input.readUntil(self.__template_pattern)

            result += next
            next = self._read_template()

        if self._until_after:
            result += self._input.readUntilAfter(self._until_after)

        return result

    def __set_templated_pattern(self):
        items = list()

        if not self._disabled.php:
            items.append(self.__patterns.php._starting_pattern.pattern)

        if not self._disabled.handlebars:
            items.append(self.__patterns.handlebars._starting_pattern.pattern)

        if not self._disabled.erb:
            items.append(self.__patterns.erb._starting_pattern.pattern)

        if not self._disabled.django:
            items.append(self.__patterns.django._starting_pattern.pattern)
            # The starting pattern for django is more complex because it has different
            # patterns for value, comment, and other sections
            items.append(self.__patterns.django_value._starting_pattern.pattern)
            items.append(self.__patterns.django_comment._starting_pattern.pattern)

        if not self._disabled.smarty:
            items.append(self.__patterns.smarty._starting_pattern.pattern)

        if self._until_pattern:
            items.append(self._until_pattern.pattern)

        self.__template_pattern = self._input.get_regexp(r"(?:" + "|".join(items) + ")")

    def _read_template(self):
        resulting_string = ""
        c = self._input.peek()
        if c == "<":
            peek1 = self._input.peek(1)
            if not self._disabled.php and not self._excluded.php and peek1 == "?":
                resulting_string = resulting_string or self.__patterns.php.read()

            if not self._disabled.erb and not self._excluded.erb and peek1 == "%":
                resulting_string = resulting_string or self.__patterns.erb.read()
        elif c == "{":
            if not self._disabled.handlebars and not self._excluded.handlebars:
                resulting_string = (
                    resulting_string or self.__patterns.handlebars_comment.read()
                )
                resulting_string = (
                    resulting_string or self.__patterns.handlebars_unescaped.read()
                )
                resulting_string = resulting_string or self.__patterns.handlebars.read()
            if not self._disabled.django:
                # django coflicts with handlebars a bit.
                if not self._excluded.django and not self._excluded.handlebars:
                    resulting_string = (
                        resulting_string or self.__patterns.django_value.read()
                    )
                if not self._excluded.django:

                    resulting_string = (
                        resulting_string or self.__patterns.django_comment.read()
                    )
                    resulting_string = resulting_string or self.__patterns.django.read()
            if not self._disabled.smarty:
                # smarty cannot be enabled with django or handlebars enabled

                if self._disabled.django and self._disabled.handlebars:
                    resulting_string = (
                        resulting_string or self.__patterns.smarty_comment.read()
                    )
                    resulting_string = (
                        resulting_string or self.__patterns.smarty_literal.read()
                    )

                    resulting_string = resulting_string or self.__patterns.smarty.read()

        return resulting_string
