import re
import unittest
import jsbeautifier


class TestJSBeautifierIndentation(unittest.TestCase):
    def test_tabs(self):
        test_fragment = self.decodesto

        self.options.indent_with_tabs = 1
        test_fragment('{tabs()}', "{\n\ttabs()\n}")

    def test_function_indent(self):
        test_fragment = self.decodesto

        self.options.indent_with_tabs = 1
        self.options.keep_function_indentation = 1
        test_fragment(
            'var foo = function(){ bar() }();',
            "var foo = function() {\n\tbar()\n}();")

        self.options.tabs = 1
        self.options.keep_function_indentation = 0
        test_fragment(
            'var foo = function(){ baz() }();',
            "var foo = function() {\n\tbaz()\n}();")

    def decodesto(self, input, expectation=None):
        self.assertEqual(
            jsbeautifier.beautify(input, self.options), expectation or input)

    @classmethod
    def setUpClass(cls):
        options = jsbeautifier.default_options()
        options.indent_size = 4
        options.indent_char = ' '
        options.preserve_newlines = True
        options.jslint_happy = False
        options.keep_array_indentation = False
        options.brace_style = 'collapse'
        options.indent_level = 0

        cls.options = options
        cls.wrapregex = re.compile('^(.+)$', re.MULTILINE)


if __name__ == '__main__':
    unittest.main()
