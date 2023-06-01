#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    AUTO-GENERATED. DO NOT MODIFY.
    Script: test/generate-tests.js
    Template: test/data/css/python.mustache
    Data: test/data/css/tests.js

  The MIT License (MIT)

  Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation files
  (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
'''

import unittest
import cssbeautifier
import copy

class CSSBeautifierTest(unittest.TestCase):

    options = None

    @classmethod
    def setUpClass(cls):
        pass

    def reset_options(self):
        false = False
        true = True

        default_options = cssbeautifier.default_options()
        default_options.indent_size = 4
        default_options.indent_char = ' '
        default_options.selector_separator_newline = true
        default_options.end_with_newline = false
        default_options.newline_between_rules = false

        default_options.indent_size = 4
        default_options.indent_char = ' '
        default_options.selector_separator_newline = true
        default_options.brace_style = 'collapse'
        default_options.end_with_newline = false
        default_options.newline_between_rules = false
        default_options.space_around_combinator = false
        default_options.preserve_newlines = false
        default_options.space_around_selector_separator = false

        self.options = copy.copy(default_options)

    def testGenerated(self):
        self.reset_options()
        test_fragment = self.decodesto
        t = self.decodesto

        false = False
        true = True


        #============================================================
        # End With Newline - (end_with_newline = "true")
        self.reset_options()
        self.options.end_with_newline = true
        test_fragment('', '\n')
        test_fragment('   .tabs{}', '   .tabs {}\n')
        test_fragment(
            '   \n' +
            '\n' +
            '.tabs{}\n' +
            '\n' +
            '\n' +
            '\n',
            #  -- output --
            '   .tabs {}\n')
        test_fragment('\n')

        # End With Newline - (end_with_newline = "false")
        self.reset_options()
        self.options.end_with_newline = false
        test_fragment('')
        test_fragment('   .tabs{}', '   .tabs {}')
        test_fragment(
            '   \n' +
            '\n' +
            '.tabs{}\n' +
            '\n' +
            '\n' +
            '\n',
            #  -- output --
            '   .tabs {}')
        test_fragment('\n', '')


        #============================================================
        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "false")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = false
        test_fragment('   a')
        test_fragment(
            '   .a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '   .a {\n' +
            '       text-align: right;\n' +
            '   }')
        test_fragment(
            '   // This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '   // This is a random comment\n' +
            '   .a {\n' +
            '       text-align: right;\n' +
            '   }')

        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "false", indent_level = "0")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = false
        self.options.indent_level = 0
        test_fragment('   a')
        test_fragment(
            '   .a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '   .a {\n' +
            '       text-align: right;\n' +
            '   }')
        test_fragment(
            '   // This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '   // This is a random comment\n' +
            '   .a {\n' +
            '       text-align: right;\n' +
            '   }')

        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "false", indent_level = "1")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = false
        self.options.indent_level = 1
        test_fragment('   a', '    a')
        test_fragment(
            '   .a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '    .a {\n' +
            '        text-align: right;\n' +
            '    }')
        test_fragment(
            '   // This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '    // This is a random comment\n' +
            '    .a {\n' +
            '        text-align: right;\n' +
            '    }')

        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "false", indent_level = "2")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = false
        self.options.indent_level = 2
        test_fragment('a', '        a')
        test_fragment(
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '        .a {\n' +
            '            text-align: right;\n' +
            '        }')
        test_fragment(
            '// This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '        // This is a random comment\n' +
            '        .a {\n' +
            '            text-align: right;\n' +
            '        }')

        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "true", indent_level = "2")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = true
        self.options.indent_level = 2
        test_fragment('a', '\t\ta')
        test_fragment(
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '\t\t.a {\n' +
            '\t\t\ttext-align: right;\n' +
            '\t\t}')
        test_fragment(
            '// This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '\t\t// This is a random comment\n' +
            '\t\t.a {\n' +
            '\t\t\ttext-align: right;\n' +
            '\t\t}')

        # Support Indent Level Options and Base Indent Autodetection - (indent_size = "4", indent_char = "" "", indent_with_tabs = "false", indent_level = "0")
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.indent_with_tabs = false
        self.options.indent_level = 0
        test_fragment('\t   a')
        test_fragment(
            '\t   .a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '\t   .a {\n' +
            '\t       text-align: right;\n' +
            '\t   }')
        test_fragment(
            '\t   // This is a random comment\n' +
            '.a {\n' +
            '  text-align: right;\n' +
            '}',
            #  -- output --
            '\t   // This is a random comment\n' +
            '\t   .a {\n' +
            '\t       text-align: right;\n' +
            '\t   }')


        #============================================================
        # Empty braces
        self.reset_options()
        t('.tabs{}', '.tabs {}')
        t('.tabs { }', '.tabs {}')
        t('.tabs    {    }', '.tabs {}')
        t(
            '.tabs    \n' +
            '{\n' +
            '    \n' +
            '  }',
            #  -- output --
            '.tabs {}')


        #============================================================
        # 
        self.reset_options()
        t(
            '#cboxOverlay {\n' +
            '    background: url(images/overlay.png) repeat 0 0;\n' +
            '    opacity: 0.9;\n' +
            '    filter: alpha(opacity = 90);\n' +
            '}',
            #  -- output --
            '#cboxOverlay {\n' +
            '    background: url(images/overlay.png) repeat 0 0;\n' +
            '    opacity: 0.9;\n' +
            '    filter: alpha(opacity=90);\n' +
            '}')
        
        # simple data uri base64 test
        t(
            'a { background: url(data:image/gif;base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=); }',
            #  -- output --
            'a {\n' +
            '    background: url(data:image/gif;base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=);\n' +
            '}')
        
        # non-base64 data
        t(
            'a { background: url(data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E); }',
            #  -- output --
            'a {\n' +
            '    background: url(data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E);\n' +
            '}')
        
        # Beautifier does not fix or mitigate bad data uri
        t(
            'a { background: url(data:  image/gif   base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=); }',
            #  -- output --
            'a {\n' +
            '    background: url(data:  image/gif   base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=);\n' +
            '}')


        #============================================================
        # Support simple language specific option inheritance/overriding - (indent_char = "" "", indent_size = "4", js = "{ "indent_size": 3 }", css = "{ "indent_size": 5 }")
        self.reset_options()
        self.options.indent_char = ' '
        self.options.indent_size = 4
        self.options.js = { 'indent_size': 3 }
        self.options.css = { 'indent_size': 5 }
        t(
            '.selector {\n' +
            '     font-size: 12px;\n' +
            '}')

        # Support simple language specific option inheritance/overriding - (indent_char = "" "", indent_size = "4", html = "{ "js": { "indent_size": 3 }, "css": { "indent_size": 5 } }")
        self.reset_options()
        self.options.indent_char = ' '
        self.options.indent_size = 4
        self.options.html = { 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 } }
        t(
            '.selector {\n' +
            '    font-size: 12px;\n' +
            '}')

        # Support simple language specific option inheritance/overriding - (indent_char = "" "", indent_size = "9", html = "{ "js": { "indent_size": 3 }, "css": { "indent_size": 8 }, "indent_size": 2}", js = "{ "indent_size": 5 }", css = "{ "indent_size": 3 }")
        self.reset_options()
        self.options.indent_char = ' '
        self.options.indent_size = 9
        self.options.html = { 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 8 }, 'indent_size': 2}
        self.options.js = { 'indent_size': 5 }
        self.options.css = { 'indent_size': 3 }
        t(
            '.selector {\n' +
            '   font-size: 12px;\n' +
            '}')


        #============================================================
        # Space Around Combinator - (space_around_combinator = "true")
        self.reset_options()
        self.options.space_around_combinator = true
        t('a>b{}', 'a > b {}')
        t('a~b{}', 'a ~ b {}')
        t('a+b{}', 'a + b {}')
        t('a+b>c{}', 'a + b > c {}')
        t('a > b{}', 'a > b {}')
        t('a ~ b{}', 'a ~ b {}')
        t('a + b{}', 'a + b {}')
        t('a + b > c{}', 'a + b > c {}')
        t(
            'a > b{width: calc(100% + 45px);}',
            #  -- output --
            'a > b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a ~ b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a + b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a + b > c {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')

        # Space Around Combinator - (space_around_combinator = "false")
        self.reset_options()
        self.options.space_around_combinator = false
        t('a>b{}', 'a>b {}')
        t('a~b{}', 'a~b {}')
        t('a+b{}', 'a+b {}')
        t('a+b>c{}', 'a+b>c {}')
        t('a > b{}', 'a>b {}')
        t('a ~ b{}', 'a~b {}')
        t('a + b{}', 'a+b {}')
        t('a + b > c{}', 'a+b>c {}')
        t(
            'a > b{width: calc(100% + 45px);}',
            #  -- output --
            'a>b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a~b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a+b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a+b>c {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')

        # Space Around Combinator - (space_around_selector_separator = "true")
        self.reset_options()
        self.options.space_around_selector_separator = true
        t('a>b{}', 'a > b {}')
        t('a~b{}', 'a ~ b {}')
        t('a+b{}', 'a + b {}')
        t('a+b>c{}', 'a + b > c {}')
        t('a > b{}', 'a > b {}')
        t('a ~ b{}', 'a ~ b {}')
        t('a + b{}', 'a + b {}')
        t('a + b > c{}', 'a + b > c {}')
        t(
            'a > b{width: calc(100% + 45px);}',
            #  -- output --
            'a > b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a ~ b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a + b {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a + b > c {\n' +
            '    width: calc(100% + 45px);\n' +
            '}')


        #============================================================
        # Issue 1373 -- Correct spacing around [attribute~=value]
        self.reset_options()
        t('header>div[class~="div-all"]')


        #============================================================
        # Selector Separator - (selector_separator_newline = "false", selector_separator = "" "", newline_between_rules = "true")
        self.reset_options()
        self.options.selector_separator_newline = false
        self.options.selector_separator = " "
        self.options.newline_between_rules = true
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}\n' +
            '\n' +
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab, .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "false", selector_separator = "" "", newline_between_rules = "false")
        self.reset_options()
        self.options.selector_separator_newline = false
        self.options.selector_separator = " "
        self.options.newline_between_rules = false
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}\n' +
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab, .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "false", selector_separator = ""  "", newline_between_rules = "false")
        self.reset_options()
        self.options.selector_separator_newline = false
        self.options.selector_separator = "  "
        self.options.newline_between_rules = false
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}\n' +
            '#bla, #foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab, .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla, #foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            'a:first-child, a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child, div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "true", selector_separator = "" "", newline_between_rules = "true")
        self.reset_options()
        self.options.selector_separator_newline = true
        self.options.selector_separator = " "
        self.options.newline_between_rules = true
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}\n' +
            '\n' +
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\n' +
            '    .tab,\n    .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "true", selector_separator = "" "", newline_between_rules = "false")
        self.reset_options()
        self.options.selector_separator_newline = true
        self.options.selector_separator = " "
        self.options.newline_between_rules = false
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}\n' +
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab,\n    .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "true", selector_separator = ""  "", newline_between_rules = "false")
        self.reset_options()
        self.options.selector_separator_newline = true
        self.options.selector_separator = "  "
        self.options.newline_between_rules = false
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}\n' +
            '#bla,\n#foo {\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    .tab,\n    .bat {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print {\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            'a:first-child,\na:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')

        # Selector Separator - (selector_separator_newline = "true", selector_separator = ""  "", brace_style = ""expand"", newline_between_rules = "false")
        self.reset_options()
        self.options.selector_separator_newline = true
        self.options.selector_separator = "  "
        self.options.brace_style = "expand"
        self.options.newline_between_rules = false
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo\n{\n' +
            '    color: green\n' +
            '}')
        t(
            '#bla, #foo{color:green}\n' +
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo\n{\n' +
            '    color: green\n' +
            '}\n' +
            '#bla,\n#foo\n{\n' +
            '    color: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print\n{\n' +
            '    .tab\n    {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print\n{\n' +
            '    .tab,\n    .bat\n    {}\n' +
            '}')
        
        # This is bug #1489
        t(
            '@media print {// comment\n' +
            '//comment 2\n' +
            '.bat{}}',
            #  -- output --
            '@media print\n{\n' +
            '    // comment\n' +
            '    //comment 2\n' +
            '    .bat\n    {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo\n{\n' +
            '    color: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\n' +
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child\n{\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover\n    {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            'a:first-child,\na:first-child\n{\n' +
            '    color: red;\n' +
            '    div:first-child,\n    div:hover\n    {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Preserve Newlines - (preserve_newlines = "true")
        self.reset_options()
        self.options.preserve_newlines = true
        t('.div {}\n\n.span {}')
        t(
            '#bla, #foo{\n' +
            '    color:black;\n\n    font-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '    color: black;\n\n    font-size: 12px;\n' +
            '}')

        # Preserve Newlines - (preserve_newlines = "false")
        self.reset_options()
        self.options.preserve_newlines = false
        t('.div {}\n\n.span {}', '.div {}\n.span {}')
        t(
            '#bla, #foo{\n' +
            '    color:black;\n\n    font-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '    color: black;\n    font-size: 12px;\n' +
            '}')


        #============================================================
        # Preserve Newlines and newline_between_rules
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t(
            '.div {}.span {}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '#bla, #foo{\n' +
            '    color:black;\n' +
            '    font-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '    color: black;\n' +
            '    font-size: 12px;\n' +
            '}')
        t(
            '#bla, #foo{\n' +
            '    color:black;\n' +
            '\n' +
            '\n' +
            '    font-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '    color: black;\n' +
            '\n' +
            '\n' +
            '    font-size: 12px;\n' +
            '}')
        t(
            '#bla,\n' +
            '\n' +
            '#foo {\n' +
            '    color: black;\n' +
            '    font-size: 12px;\n' +
            '}')
        t(
            'a {\n' +
            '    b: c;\n' +
            '\n' +
            '\n' +
            '    d: {\n' +
            '        e: f;\n' +
            '    }\n' +
            '}')
        t(
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            'html {}\n' +
            '\n' +
            '/*this is a comment*/')
        t(
            '.div {\n' +
            '    a: 1;\n' +
            '\n' +
            '\n' +
            '    b: 2;\n' +
            '}\n' +
            '\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '    a: 1;\n' +
            '}')
        t(
            '.div {\n' +
            '\n' +
            '\n' +
            '    a: 1;\n' +
            '\n' +
            '\n' +
            '    b: 2;\n' +
            '}\n' +
            '\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '    a: 1;\n' +
            '}')
        t(
            '@media screen {\n' +
            '    .div {\n' +
            '        a: 1;\n' +
            '\n' +
            '\n' +
            '        b: 2;\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '\n' +
            '    .span {\n' +
            '        a: 1;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '.span {}')


        #============================================================
        # Preserve Newlines and add tabs
        self.reset_options()
        self.options.preserve_newlines = true
        t(
            '.tool-tip {\n' +
            '    position: relative;\n' +
            '\n' +
            '        \n' +
            '    .tool-tip-content {\n' +
            '        &>* {\n' +
            '            margin-top: 0;\n' +
            '        }\n' +
            '        \n' +
            '\n' +
            '        .mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n' +
            '        padding: 1rem;\n' +
            '        position: absolute;\n' +
            '        z-index: 10;\n' +
            '    }\n' +
            '}',
            #  -- output --
            '.tool-tip {\n' +
            '    position: relative;\n' +
            '\n' +
            '\n' +
            '    .tool-tip-content {\n' +
            '        &>* {\n' +
            '            margin-top: 0;\n' +
            '        }\n' +
            '\n\n        .mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n' +
            '        padding: 1rem;\n' +
            '        position: absolute;\n' +
            '        z-index: 10;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Issue #1338 -- Preserve Newlines within CSS rules
        self.reset_options()
        self.options.preserve_newlines = true
        t(
            'body {\n' +
            '    grid-template-areas:\n' +
            '        "header header"\n' +
            '        "main   sidebar"\n' +
            '        "footer footer";\n' +
            '}')


        #============================================================
        # Newline Between Rules - (newline_between_rules = "true")
        self.reset_options()
        self.options.newline_between_rules = true
        t(
            '.div {}\n' +
            '.span {}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '.div{}\n' +
            '   \n' +
            '.span{}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '.div {}    \n' +
            '  \n' +
            '.span { } \n',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '.div {\n' +
            '    \n' +
            '} \n' +
            '  .span {\n' +
            ' }  ',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '    margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue"\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue"\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '    }\n' +
            '\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {}\n' +
            '\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    .list-group-icon {}\n' +
            '\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    //this is my pre-comment\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    //this is a comment\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    //this is also a comment\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    //this is my pre-comment\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    //this is a comment\n' +
            '    .list-group-icon {}\n' +
            '\n' +
            '    //this is also a comment\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            'color: #38a0e5;\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            'color: #38a0e5;\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    color: #38a0e5;\n' +
            '\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    color: #38a0e5;\n' +
            '\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '\n' +
            '    color: #38a0e5;\n' +
            '\n' +
            '    .list-group-icon {}\n' +
            '\n' +
            '    color: #38a0e5;\n' +
            '\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '\n' +
            'color: #38a0e5;\n' +
            '\n' +
            '.list-group-condensed {}')
        t(
            '@media only screen and (max-width: 40em) {\n' +
            'header {\n' +
            '    margin: 0 auto;\n' +
            '    padding: 10px;\n' +
            '    background: red;\n' +
            '    }\n' +
            'main {\n' +
            '    margin: 20px auto;\n' +
            '    padding: 4px;\n' +
            '    background: blue;\n' +
            '    }\n' +
            '}',
            #  -- output --
            '@media only screen and (max-width: 40em) {\n' +
            '    header {\n' +
            '        margin: 0 auto;\n' +
            '        padding: 10px;\n' +
            '        background: red;\n' +
            '    }\n' +
            '\n' +
            '    main {\n' +
            '        margin: 20px auto;\n' +
            '        padding: 4px;\n' +
            '        background: blue;\n' +
            '    }\n' +
            '}')
        t(
            '.preloader {\n' +
            '    height: 20px;\n' +
            '    .line {\n' +
            '        width: 1px;\n' +
            '        height: 12px;\n' +
            '        background: #38a0e5;\n' +
            '        margin: 0 1px;\n' +
            '        display: inline-block;\n' +
            '        &.line-1 {\n' +
            '            animation-delay: 800ms;\n' +
            '        }\n' +
            '        &.line-2 {\n' +
            '            animation-delay: 600ms;\n' +
            '        }\n' +
            '    }\n' +
            '    div {\n' +
            '        color: #38a0e5;\n' +
            '        font-family: "Arial", sans-serif;\n' +
            '        font-size: 10px;\n' +
            '        margin: 5px 0;\n' +
            '    }\n' +
            '}',
            #  -- output --
            '.preloader {\n' +
            '    height: 20px;\n' +
            '\n' +
            '    .line {\n' +
            '        width: 1px;\n' +
            '        height: 12px;\n' +
            '        background: #38a0e5;\n' +
            '        margin: 0 1px;\n' +
            '        display: inline-block;\n' +
            '\n' +
            '        &.line-1 {\n' +
            '            animation-delay: 800ms;\n' +
            '        }\n' +
            '\n' +
            '        &.line-2 {\n' +
            '            animation-delay: 600ms;\n' +
            '        }\n' +
            '    }\n' +
            '\n' +
            '    div {\n' +
            '        color: #38a0e5;\n' +
            '        font-family: "Arial", sans-serif;\n' +
            '        font-size: 10px;\n' +
            '        margin: 5px 0;\n' +
            '    }\n' +
            '}')

        # Newline Between Rules - (newline_between_rules = "false")
        self.reset_options()
        self.options.newline_between_rules = false
        t(
            '.div {}\n' +
            '.span {}')
        t(
            '.div{}\n' +
            '   \n' +
            '.span{}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '.div {}    \n' +
            '  \n' +
            '.span { } \n',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '.div {\n' +
            '    \n' +
            '} \n' +
            '  .span {\n' +
            ' }  ',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '    margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue"\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '    }\n' +
            '\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {}\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    .list-group-icon {}\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    //this is my pre-comment\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    //this is a comment\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    //this is also a comment\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    //this is my pre-comment\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    //this is a comment\n' +
            '    .list-group-icon {}\n' +
            '    //this is also a comment\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            '.list-group-condensed {}')
        t(
            '.list-group {\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a:1\n' +
            '    }\n' +
            'color: #38a0e5;\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-icon {\n' +
            '    }\n' +
            '}\n' +
            'color: #38a0e5;\n' +
            '.list-group-condensed {\n' +
            '}',
            #  -- output --
            '.list-group {\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-item {\n' +
            '        a: 1\n' +
            '    }\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-icon {}\n' +
            '    color: #38a0e5;\n' +
            '    .list-group-icon {}\n' +
            '}\n' +
            'color: #38a0e5;\n' +
            '.list-group-condensed {}')
        t(
            '@media only screen and (max-width: 40em) {\n' +
            'header {\n' +
            '    margin: 0 auto;\n' +
            '    padding: 10px;\n' +
            '    background: red;\n' +
            '    }\n' +
            'main {\n' +
            '    margin: 20px auto;\n' +
            '    padding: 4px;\n' +
            '    background: blue;\n' +
            '    }\n' +
            '}',
            #  -- output --
            '@media only screen and (max-width: 40em) {\n' +
            '    header {\n' +
            '        margin: 0 auto;\n' +
            '        padding: 10px;\n' +
            '        background: red;\n' +
            '    }\n' +
            '    main {\n' +
            '        margin: 20px auto;\n' +
            '        padding: 4px;\n' +
            '        background: blue;\n' +
            '    }\n' +
            '}')
        t(
            '.preloader {\n' +
            '    height: 20px;\n' +
            '    .line {\n' +
            '        width: 1px;\n' +
            '        height: 12px;\n' +
            '        background: #38a0e5;\n' +
            '        margin: 0 1px;\n' +
            '        display: inline-block;\n' +
            '        &.line-1 {\n' +
            '            animation-delay: 800ms;\n' +
            '        }\n' +
            '        &.line-2 {\n' +
            '            animation-delay: 600ms;\n' +
            '        }\n' +
            '    }\n' +
            '    div {\n' +
            '        color: #38a0e5;\n' +
            '        font-family: "Arial", sans-serif;\n' +
            '        font-size: 10px;\n' +
            '        margin: 5px 0;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Functions braces
        self.reset_options()
        t('.tabs(){}', '.tabs() {}')
        t('.tabs (){}', '.tabs () {}')
        t(
            '.tabs (pa, pa(1,2)), .cols { }',
            #  -- output --
            '.tabs (pa, pa(1, 2)),\n' +
            '.cols {}')
        t(
            '.tabs(pa, pa(1,2)), .cols { }',
            #  -- output --
            '.tabs(pa, pa(1, 2)),\n' +
            '.cols {}')
        t('.tabs (   )   {    }', '.tabs () {}')
        t('.tabs(   )   {    }', '.tabs() {}')
        t(
            '.tabs  (t, t2)  \n' +
            '{\n' +
            '  key: val(p1  ,p2);  \n' +
            '  }',
            #  -- output --
            '.tabs (t, t2) {\n' +
            '    key: val(p1, p2);\n' +
            '}')
        t(
            '.box-shadow(@shadow: 0 1px 3px rgba(0, 0, 0, .25)) {\n' +
            '    -webkit-box-shadow: @shadow;\n' +
            '    -moz-box-shadow: @shadow;\n' +
            '    box-shadow: @shadow;\n' +
            '}')


        #============================================================
        # Beautify preserve formatting
        self.reset_options()
        self.options.indent_size = 4
        self.options.indent_char = ' '
        self.options.preserve_newlines = true
        
        # Directive: ignore
        t(
            '/* beautify ignore:start */\n' +
            '/* beautify ignore:end */')
        t(
            '/* beautify ignore:start */\n' +
            '   var a,,,{ 1;\n' +
            ' .div {}/* beautify ignore:end */')
        t(
            '.div {}\n' +
            '\n' +
            '/* beautify ignore:start */\n' +
            '   .div {}var a = 1;\n' +
            '/* beautify ignore:end */')
        
        # ignore starts _after_ the start comment, ends after the end comment
        t('/* beautify ignore:start */     {asdklgh;y;+++;dd2d}/* beautify ignore:end */')
        t('/* beautify ignore:start */  {asdklgh;y;+++;dd2d}    /* beautify ignore:end */')
        t(
            '.div {}/* beautify ignore:start */\n' +
            '   .div {}var a,,,{ 1;\n' +
            '/*beautify ignore:end*/',
            #  -- output --
            '.div {}\n' +
            '/* beautify ignore:start */\n' +
            '   .div {}var a,,,{ 1;\n' +
            '/*beautify ignore:end*/')
        t(
            '.div {}\n' +
            '  /* beautify ignore:start */\n' +
            '   .div {}var a,,,{ 1;\n' +
            '/* beautify ignore:end */',
            #  -- output --
            '.div {}\n' +
            '/* beautify ignore:start */\n' +
            '   .div {}var a,,,{ 1;\n' +
            '/* beautify ignore:end */')
        t(
            '.div {\n' +
            '    /* beautify ignore:start */\n' +
            '    one   :  1\n' +
            '    two   :  2,\n' +
            '    three :  {\n' +
            '    ten   : 10\n' +
            '    /* beautify ignore:end */\n' +
            '}')
        t(
            '.div {\n' +
            '/* beautify ignore:start */\n' +
            '    one   :  1\n' +
            '    two   :  2,\n' +
            '    three :  {\n' +
            '    ten   : 10\n' +
            '/* beautify ignore:end */\n' +
            '}',
            #  -- output --
            '.div {\n' +
            '    /* beautify ignore:start */\n' +
            '    one   :  1\n' +
            '    two   :  2,\n' +
            '    three :  {\n' +
            '    ten   : 10\n' +
            '/* beautify ignore:end */\n' +
            '}')
        t(
            '.div {\n' +
            '/* beautify ignore:start */\n' +
            '    one   :  1\n' +
            ' /* beautify ignore:end */\n' +
            '    two   :  2,\n' +
            '/* beautify ignore:start */\n' +
            '    three :  {\n' +
            '    ten   : 10\n' +
            '/* beautify ignore:end */\n' +
            '}',
            #  -- output --
            '.div {\n' +
            '    /* beautify ignore:start */\n' +
            '    one   :  1\n' +
            ' /* beautify ignore:end */\n' +
            '    two : 2,\n' +
            '    /* beautify ignore:start */\n' +
            '    three :  {\n' +
            '    ten   : 10\n' +
            '/* beautify ignore:end */\n' +
            '}')


        #============================================================
        # Comments - (preserve_newlines = "false", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {/* non-header */width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' *//* another comment */body{}',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}.demob {text-align: right;}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**//**///\n' +
            '/**/.div{}/**//**///\n' +
            '/**/.span {}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}//\n' +
            '.span {}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {    #foo:hover {        background-image: url(foo@2x.png);    }    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {    font-family: "Bitstream Vera Serif Bold";    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {    #foo:hover {        background-image: url(foo.png);    }    @media screen and (min-device-pixel-ratio: 2) {        @font-face {            font-family: "Helvetica Neue";        }        #foo:hover {            background-image: url(foo@2x.png);        }    }}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "false", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '/* test */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\n' +
            '\n' +
            '/* non-header */\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0;\n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '//comment\n' +
            '\n' +
            '\n' +
            '//2nd single line comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another nl\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;   // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '        // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body{}\n' +
            '\n' +
            '\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            'text-align:left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0; \n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:first-child{\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:not(.peq){\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "false", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '        \n' +
            '    \n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '/* test */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '        \n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '        \n' +
            '    \n' +
            '/* non-header */\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0;\n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '            \n' +
            '   \n' +
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '//comment\n' +
            '            \n' +
            '   \n' +
            '//2nd single line comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;\n' +
            '            \n' +
            '   \n' +
            '        // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '        \n' +
            '    \n' +
            '/* another comment */\n' +
            '        \n' +
            '    \n' +
            'body{}\n' +
            '        \n' +
            '    \n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '            \n' +
            '   \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0; \n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '        \n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '        \n' +
            '    \n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        \n' +
            '    \n' +
            '        @font-face {\n' +
            '        \n' +
            '    \n' +
            '            font-family: "Helvetica Neue";\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '        #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '            background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:not(.peq){\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {/* non-header */width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' *//* another comment */body{}',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}.demob {text-align: right;}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**//**///\n' +
            '/**/.div{}/**//**///\n' +
            '/**/.span {}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}//\n' +
            '.span {}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {    #foo:hover {        background-image: url(foo@2x.png);    }    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {    font-family: "Bitstream Vera Serif Bold";    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {    #foo:hover {        background-image: url(foo.png);    }    @media screen and (min-device-pixel-ratio: 2) {        @font-face {            font-family: "Helvetica Neue";        }        #foo:hover {            background-image: url(foo@2x.png);        }    }}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '/* test */\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '/* non-header */\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            'margin: 0;\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            'width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            'width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body{}\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            'text-align: right;\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            'text-align:left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div{}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}\n' +
            '//\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            'margin: 0; \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            'background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            'color:red;\n' +
            'div:first-child{\n' +
            'color:black;\n' +
            '}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            'color:red;\n' +
            'div:not(.peq){\n' +
            'color:black;\n' +
            '}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '        \n' +
            '    \n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '/* test */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '        \n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '        \n' +
            '    \n' +
            '/* non-header */\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* non-header */\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0;\n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '            \n' +
            '   \n' +
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '//comment\n' +
            '            \n' +
            '   \n' +
            '//2nd single line comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    //comment\n' +
            '\n' +
            '\n' +
            '    //2nd single line comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;\n' +
            '            \n' +
            '   \n' +
            '        // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '    // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '        \n' +
            '    \n' +
            '/* another comment */\n' +
            '        \n' +
            '    \n' +
            'body{}\n' +
            '        \n' +
            '    \n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '    text-align: left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '//\n' +
            '            \n' +
            '   \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0; \n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '        \n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '        \n' +
            '    \n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        \n' +
            '    \n' +
            '        @font-face {\n' +
            '        \n' +
            '    \n' +
            '            font-family: "Helvetica Neue";\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '        #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '            background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:first-child {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:not(.peq){\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "false")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '/* test */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\n' +
            '\n' +
            '/* non-header */\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* non-header */\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0;\n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '//comment\n' +
            '\n' +
            '\n' +
            '//2nd single line comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    //comment\n' +
            '\n' +
            '\n' +
            '    //2nd single line comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another nl\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;   // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '        // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '    // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body{}\n' +
            '\n' +
            '\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            'text-align:left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '    text-align: left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '//\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0; \n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:first-child{\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:first-child {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:not(.peq){\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (preserve_newlines = "false", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {/* non-header */width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' *//* another comment */body{}',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}.demob {text-align: right;}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**//**///\n' +
            '/**/.div{}/**//**///\n' +
            '/**/.span {}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}//\n' +
            '.span {}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {    #foo:hover {        background-image: url(foo@2x.png);    }    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {    font-family: "Bitstream Vera Serif Bold";    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {    #foo:hover {        background-image: url(foo.png);    }    @media screen and (min-device-pixel-ratio: 2) {        @font-face {            font-family: "Helvetica Neue";        }        #foo:hover {            background-image: url(foo@2x.png);        }    }}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "false", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '/* test */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\n' +
            '\n' +
            '/* non-header */\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0;\n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '//comment\n' +
            '\n' +
            '\n' +
            '//2nd single line comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another nl\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;   // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '        // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body{}\n' +
            '\n' +
            '\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            'text-align:left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0; \n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:first-child{\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:not(.peq){\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "false", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '        \n' +
            '    \n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '/* test */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '        \n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '        \n' +
            '    \n' +
            '/* non-header */\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0;\n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '            \n' +
            '   \n' +
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '//comment\n' +
            '            \n' +
            '   \n' +
            '//2nd single line comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;\n' +
            '            \n' +
            '   \n' +
            '        // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '        \n' +
            '    \n' +
            '/* another comment */\n' +
            '        \n' +
            '    \n' +
            'body{}\n' +
            '        \n' +
            '    \n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '            \n' +
            '   \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0; \n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '        \n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '        \n' +
            '    \n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        \n' +
            '    \n' +
            '        @font-face {\n' +
            '        \n' +
            '    \n' +
            '            font-family: "Helvetica Neue";\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '        #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '            background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:not(.peq){\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {/* non-header */width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' *//* another comment */body{}',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}.demob {text-align: right;}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**//**///\n' +
            '/**/.div{}/**//**///\n' +
            '/**/.span {}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}//\n' +
            '.span {}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {    #foo:hover {        background-image: url(foo@2x.png);    }    @font-face {        font-family: "Bitstream Vera Serif Bold";        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");    }}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {    font-family: "Bitstream Vera Serif Bold";    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {    #foo:hover {        background-image: url(foo.png);    }    @media screen and (min-device-pixel-ratio: 2) {        @font-face {            font-family: "Helvetica Neue";        }        #foo:hover {            background-image: url(foo@2x.png);        }    }}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '/* test */\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '/* non-header */\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    /* non-header */\n' +
            '    width: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            'margin: 0;\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    // comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    //comment\n' +
            '    //2nd single line comment\n' +
            '    width: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            'width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            'width: 10px;\n' +
            '        // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px;\n' +
            '    // comment follows rule\n' +
            '    // another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body{}\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '/* another comment */\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            'text-align: right;\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '    text-align: right;\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            'text-align:left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '    text-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div{}\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.div {}\n' +
            '\n' +
            '/**/\n' +
            '/**/\n' +
            '//\n' +
            '/**/\n' +
            '.span {}')
        t(
            '//\n' +
            '.div{}\n' +
            '//\n' +
            '.span {\n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            'margin: 0; \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '    margin: 0;\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '    width: 10px; //end of line comment\n' +
            '    height: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            'background-image: url(foo@2x.png);\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo@2x.png);\n' +
            '    }\n' +
            '\n' +
            '    @font-face {\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '    #foo:hover {\n' +
            '        background-image: url(foo.png);\n' +
            '    }\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        @font-face {\n' +
            '            font-family: "Helvetica Neue";\n' +
            '        }\n' +
            '\n' +
            '        #foo:hover {\n' +
            '            background-image: url(foo@2x.png);\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            'a:first-child{\n' +
            'color:red;\n' +
            'div:first-child{\n' +
            'color:black;\n' +
            '}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:first-child {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            'color:red;\n' +
            'div:not(.peq){\n' +
            'color:black;\n' +
            '}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '    color: red;\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '        color: black;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '    height: 15px;\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '/* test */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\n' +
            '\n' +
            '/* non-header */\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* non-header */\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0;\n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '// comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            '//comment\n' +
            '\n' +
            '\n' +
            '//2nd single line comment\n' +
            '\n' +
            '\n' +
            'width:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    //comment\n' +
            '\n' +
            '\n' +
            '    //2nd single line comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another nl\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;   // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '        // comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '    // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body{}\n' +
            '\n' +
            '\n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            'text-align:left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '    text-align: left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '//\n' +
            '\n' +
            '\n' +
            '.div{}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '//\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '\n' +
            '\n' +
            'margin: 0; \n' +
            '\n' +
            '\n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width:10px;//end of line comment\n' +
            '\n' +
            '\n' +
            'height:10px;//another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:first-child{\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:first-child {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\n' +
            '\n' +
            'color:red;\n' +
            '\n' +
            '\n' +
            'div:not(.peq){\n' +
            '\n' +
            '\n' +
            'color:black;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div{\n' +
            '\n' +
            '\n' +
            'height:15px;\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (preserve_newlines = "true", newline_between_rules = "true")
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '@import "custom.css";\n' +
            '        \n' +
            '    \n' +
            '.rule{}',
            #  -- output --
            '@import "custom.css";\n' +
            '\n' +
            '\n' +
            '.rule {}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '/* test */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '        \n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '        \n' +
            '    \n' +
            '/* non-header */\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    /* non-header */\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0;\n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '// comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    // comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '            \n' +
            '   \n' +
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            '//comment\n' +
            '            \n' +
            '   \n' +
            '//2nd single line comment\n' +
            '            \n' +
            '   \n' +
            'width:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    //comment\n' +
            '\n' +
            '\n' +
            '    //2nd single line comment\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width: 10px;\n' +
            '            \n' +
            '   \n' +
            '        // comment follows rule\n' +
            '            \n' +
            '   \n' +
            '// another comment new line\n' +
            '            \n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px;\n' +
            '\n' +
            '\n' +
            '    // comment follows rule\n' +
            '\n' +
            '\n' +
            '    // another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '        \n' +
            '    \n' +
            '/* another comment */\n' +
            '        \n' +
            '    \n' +
            'body{}\n' +
            '        \n' +
            '    \n',
            #  -- output --
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\n' +
            '\n' +
            '/* another comment */\n' +
            '\n' +
            '\n' +
            'body {}')
        
        # #1348
        t(
            '.demoa1 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '    text-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1440
        t(
            '#search-text {\n' +
            '  width: 43%;\n' +
            '  // height: 100%;\n' +
            '  border: none;\n' +
            '}',
            #  -- output --
            '#search-text {\n' +
            '    width: 43%;\n' +
            '    // height: 100%;\n' +
            '    border: none;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '        \n' +
            '    \n' +
            'text-align:left;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '            \n' +
            '   \n' +
            '.demob {\n' +
            '        \n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '    text-align: left;\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '    text-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '/**/\n' +
            '        \n' +
            '    \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '/**/\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '//\n' +
            '            \n' +
            '   \n' +
            '.div{}\n' +
            '        \n' +
            '    \n' +
            '//\n' +
            '            \n' +
            '   \n' +
            '.span {\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '//\n' +
            '\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '\n' +
            '//\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '        \n' +
            '    \n' +
            'margin: 0; \n' +
            '        \n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '    margin: 0;\n' +
            '\n' +
            '\n' +
            '    /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '        \n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '            \n' +
            '   \n' +
            'height:10px;//another\n' +
            '            \n' +
            '   \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '    width: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '    height: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '        \n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '    background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @font-face {\n' +
            '        \n' +
            '    \n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @font-face {\n' +
            '\n' +
            '\n' +
            '        font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '        \n' +
            '    \n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '        \n' +
            '    \n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '            \n' +
            '   \n' +
            '@media screen {\n' +
            '        \n' +
            '    \n' +
            '    #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '        background-image: url(foo.png);\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '        \n' +
            '    \n' +
            '        @font-face {\n' +
            '        \n' +
            '    \n' +
            '            font-family: "Helvetica Neue";\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '        #foo:hover {\n' +
            '        \n' +
            '    \n' +
            '            background-image: url(foo@2x.png);\n' +
            '        \n' +
            '    \n' +
            '        }\n' +
            '        \n' +
            '    \n' +
            '    }\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\n' +
            '\n' +
            '    font-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '    #foo:hover {\n' +
            '\n' +
            '\n' +
            '        background-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '    @media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '        @font-face {\n' +
            '\n' +
            '\n' +
            '            font-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '        #foo:hover {\n' +
            '\n' +
            '\n' +
            '            background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '        }\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:first-child {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '        \n' +
            '    \n' +
            'color:red;\n' +
            '        \n' +
            '    \n' +
            'div:not(.peq){\n' +
            '        \n' +
            '    \n' +
            'color:black;\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '}\n' +
            '        \n' +
            '    \n' +
            '.div{\n' +
            '        \n' +
            '    \n' +
            'height:15px;\n' +
            '        \n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '    color: red;\n' +
            '\n' +
            '\n' +
            '    div:not(.peq) {\n' +
            '\n' +
            '\n' +
            '        color: black;\n' +
            '\n' +
            '\n' +
            '    }\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '    height: 15px;\n' +
            '\n' +
            '\n' +
            '}')


        #============================================================
        # Handle LESS property name interpolation
        self.reset_options()
        t(
            'tag {\n' +
            '    @{prop}: none;\n' +
            '}')
        t(
            'tag{@{prop}:none;}',
            #  -- output --
            'tag {\n' +
            '    @{prop}: none;\n' +
            '}')
        t(
            'tag{ @{prop}: none;}',
            #  -- output --
            'tag {\n' +
            '    @{prop}: none;\n' +
            '}')
        
        # can also be part of property name
        t(
            'tag {\n' +
            '    dynamic-@{prop}: none;\n' +
            '}')
        t(
            'tag{dynamic-@{prop}:none;}',
            #  -- output --
            'tag {\n' +
            '    dynamic-@{prop}: none;\n' +
            '}')
        t(
            'tag{ dynamic-@{prop}: none;}',
            #  -- output --
            'tag {\n' +
            '    dynamic-@{prop}: none;\n' +
            '}')


        #============================================================
        # Handle LESS property name interpolation, test #631
        self.reset_options()
        t(
            '.generate-columns(@n, @i: 1) when (@i =< @n) {\n' +
            '    .column-@{i} {\n' +
            '        width: (@i * 100% / @n);\n' +
            '    }\n' +
            '    .generate-columns(@n, (@i + 1));\n' +
            '}')
        t(
            '.generate-columns(@n,@i:1) when (@i =< @n){.column-@{i}{width:(@i * 100% / @n);}.generate-columns(@n,(@i + 1));}',
            #  -- output --
            '.generate-columns(@n, @i: 1) when (@i =< @n) {\n' +
            '    .column-@{i} {\n' +
            '        width: (@i * 100% / @n);\n' +
            '    }\n' +
            '    .generate-columns(@n, (@i + 1));\n' +
            '}')


        #============================================================
        # Handle LESS function parameters
        self.reset_options()
        t(
            'div{.px2rem(width,12);}',
            #  -- output --
            'div {\n' +
            '    .px2rem(width, 12);\n' +
            '}')
        t(
            'div {\n' +
            '    background: url("//test.com/dummy.png");\n' +
            '    .px2rem(width, 12);\n' +
            '}')


        #============================================================
        # Psuedo-classes vs Variables
        self.reset_options()
        t('@page :first {}')
        
        # Assume the colon goes with the @name. If we're in LESS, this is required regardless of the at-string.
        t('@page:first {}', '@page: first {}')
        t('@page: first {}')


        #============================================================
        # Issue 1411 -- LESS Variable Assignment Spacing
        self.reset_options()
        t(
            '@set: {\n' +
            '    one: blue;\n' +
            '    two: green;\n' +
            '    three: red;\n' +
            '}\n' +
            '.set {\n' +
            '    each(@set, {\n' +
            '        @{key}-@{index}: @value;\n' +
            '    });\n' +
            '}')
        t('@light-blue: @nice-blue + #111;')


        #============================================================
        # SASS/SCSS
        self.reset_options()
        
        # Basic Interpolation
        t(
            'p {\n' +
            '    $font-size: 12px;\n' +
            '    $line-height: 30px;\n' +
            '    font: #{$font-size}/#{$line-height};\n' +
            '}')
        t('p.#{$name} {}')
        t(
            '@mixin itemPropertiesCoverItem($items, $margin) {\n' +
            '    width: calc((100% - ((#{$items} - 1) * #{$margin}rem)) / #{$items});\n' +
            '    margin: 1.6rem #{$margin}rem 1.6rem 0;\n' +
            '}')
        
        # Multiple filed issues in LESS due to not(:blah)
        t('&:first-of-type:not(:last-child) {}')
        
        # #1236 - maps standard
        t(
            '$theme-colors: (\n' +
            '    primary: $blue,\n' +
            '    secondary: "gray-600"\n' +
            ');')
        
        # #1236 - maps single line
        t(
            '$theme-colors:(primary: $blue,     secondary: "$gray-600");',
            #  -- output --
            '$theme-colors: (\n' +
            '    primary: $blue,\n' +
            '    secondary: "$gray-600"\n' +
            ');')
        
        # #1236 - maps with functions
        t(
            '$maps:(x: 80px,     y: "something",    \n' +
            'z: calc(10 + 10)\n' +
            ');',
            #  -- output --
            '$maps: (\n' +
            '    x: 80px,\n' +
            '    y: "something",\n' +
            '    z: calc(10 + 10)\n' +
            ');')
        t(
            'div {\n' +
            '    &:not(:first-of-type) {\n' +
            '        background: red;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Proper handling of colon in selectors
        self.reset_options()
        self.options.selector_separator_newline = false
        t('a :b {}')
        t('a ::b {}')
        t('a:b {}')
        t('a::b {}')
        t(
            'a {}, a::b {}, a   ::b {}, a:b {}, a   :b {}',
            #  -- output --
            'a {}\n' +
            ', a::b {}\n' +
            ', a ::b {}\n' +
            ', a:b {}\n' +
            ', a :b {}')
        t(
            '.card-blue ::-webkit-input-placeholder {\n' +
            '    color: #87D1FF;\n' +
            '}')
        t(
            'div [attr] :not(.class) {\n' +
            '    color: red;\n' +
            '}')
        
        # Issue #1233
        t(
            '.one {\n' +
            '    color: #FFF;\n' +
            '    // pseudo-element\n' +
            '    span:not(*::selection) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}\n' +
            '.two {\n' +
            '    color: #000;\n' +
            '    // pseudo-class\n' +
            '    span:not(*:active) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Regresssion Tests
        self.reset_options()
        self.options.selector_separator_newline = false
        t(
            '@media(min-width:768px) {\n' +
            '    .selector::after {\n' +
            '        /* property: value */\n' +
            '    }\n' +
            '    .other-selector {\n' +
            '        /* property: value */\n' +
            '    }\n' +
            '}')
        
        # #1236 - SCSS/SASS Maps with selector_separator_newline = false
        t('$font-weights: ("regular": 400, "medium": 500, "bold": 700);')
        t(
            '.fa-rotate-270 {\n' +
            '    filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);\n' +
            '}')
        
        # #2056 - Extra space before !important added
        t(
            '.x {\n' +
            '    $d: a !default;\n' +
            '}')
        t(
            '.x {\n' +
            '    $d: a !default;\n' +
            '    @if $x !=0 {\n' +
            '        color: $var !important;\n' +
            '    }\n' +
            '}')
        
        # #2051 - css format removes space after quoted value
        t(
            'q {\n' +
            '    quotes: \'"\' \'"\' "\'" "\'";\n' +
            '    quotes: "some" \'thing\' "different";\n' +
            '    quotes: \'some\' "thing" \'different\';\n' +
            '}')


        #============================================================
        # Regression tests - with default options
        self.reset_options()
        
        # Issue #1798 - space after strings in preserved
        t('@use "variables" as *;')
        
        # Issue #1976 - support the new @forwards syntax
        t(
            '@forwards "a" with (\n' +
            '   $a: 2\n' +
            ');',
            #  -- output --
            '@forwards "a" with ($a: 2);')


        #============================================================
        # Issue #1817
        self.reset_options()
        
        # ensure that properties that are expected to have multiline values persist new lines
        t(
            '.grid {\n' +
            '    grid-template:\n' +
            '        "top-bar top-bar" 100px\n' +
            '        "left-bar center" 100px;\n' +
            '}')
        
        # property values that have string followed by other identifiers should persist spacing
        t(
            '.grid {grid-template: "top-bar" 100px;}',
            #  -- output --
            '.grid {\n' +
            '    grid-template: "top-bar" 100px;\n' +
            '}')
        t(
            'div {\n' +
            'grid-template-areas: "a"\n' +
            ' "b" \n' +
            '                    "c";\n' +
            '}',
            #  -- output --
            'div {\n' +
            '    grid-template-areas: "a"\n' +
            '        "b"\n' +
            '        "c";\n' +
            '}')
        t(
            'div {\n' +
            'grid-template: "a a a" 20%\n' +
            ' [main-top] "b b b" 1fr\n' +
            '                    "b b b" auto;\n' +
            '}',
            #  -- output --
            'div {\n' +
            '    grid-template: "a a a" 20%\n' +
            '        [main-top] "b b b" 1fr\n' +
            '        "b b b" auto;\n' +
            '}')


        #============================================================
        # Issue #645, #1233
        self.reset_options()
        self.options.selector_separator_newline = true
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t(
            '/* Comment above first rule */\n' +
            '\n' +
            'body {\n' +
            '    display: none;\n' +
            '}\n' +
            '\n' +
            '/* Comment between rules */\n' +
            '\n' +
            'ul,\n' +
            '\n' +
            '/* Comment between selectors */\n' +
            '\n' +
            'li {\n' +
            '    display: none;\n' +
            '}\n' +
            '\n' +
            '/* Comment after last rule */')
        t(
            '.one  {\n' +
            '    color: #FFF;\n' +
            '    // pseudo-element\n' +
            '    span:not(*::selection) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}\n' +
            '.two {\n' +
            '    color: #000;\n' +
            '    // pseudo-class\n' +
            '    span:not(*:active) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}',
            #  -- output --
            '.one {\n' +
            '    color: #FFF;\n' +
            '\n' +
            '    // pseudo-element\n' +
            '    span:not(*::selection) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}\n' +
            '\n' +
            '.two {\n' +
            '    color: #000;\n' +
            '\n' +
            '    // pseudo-class\n' +
            '    span:not(*:active) {\n' +
            '        margin-top: 0;\n' +
            '    }\n' +
            '}')


        #============================================================
        # Extend Tests
        self.reset_options()
        t(
            '.btn-group-radios {\n' +
            '    .btn:hover {\n' +
            '        &:hover,\n' +
            '        &:focus {\n' +
            '            @extend .btn-blue:hover;\n' +
            '        }\n' +
            '    }\n' +
            '}')
        t(
            '.item-warning {\n' +
            '    @extend btn-warning:hover;\n' +
            '}\n' +
            '.item-warning-wrong {\n' +
            '    @extend btn-warning: hover;\n' +
            '}')
        t(
            '.item-warning {\n' +
            '    @extend .color1, .hover2;\n' +
            '}')


        #============================================================
        # Import Tests
        self.reset_options()
        t(
            '@import "custom.css";.rule{}\n' +
            'a, p {}',
            #  -- output --
            '@import "custom.css";\n' +
            '.rule {}\n' +
            'a,\n' +
            'p {}')
        t(
            '@import url("bluish.css") projection,tv;.rule{}\n' +
            'a, p {}',
            #  -- output --
            '@import url("bluish.css") projection, tv;\n' +
            '.rule {}\n' +
            'a,\n' +
            'p {}')


        #============================================================
        # Important
        self.reset_options()
        t(
            'a {\n' +
            '    color: blue  !important;\n' +
            '}',
            #  -- output --
            'a {\n' +
            '    color: blue !important;\n' +
            '}')
        t(
            'a {\n' +
            '    color: blue!important;\n' +
            '}',
            #  -- output --
            'a {\n' +
            '    color: blue !important;\n' +
            '}')
        t(
            'a {\n' +
            '    color: blue !important;\n' +
            '}')
        t(
            '.blue\\! {\n' +
            '    color: blue !important;\n' +
            '}')


        #============================================================
        # Escape
        self.reset_options()
        t(
            'a:not(.color\\:blue) {\n' +
            '    color: blue !important;\n' +
            '}')
        t(
            '.blue\\:very {\n' +
            '    color: blue !important;\n' +
            '}')
        test_fragment('a:not(.color\\')
        test_fragment('a:not\\')


        #============================================================
        # indent_empty_lines true
        self.reset_options()
        self.options.indent_empty_lines = true
        self.options.preserve_newlines = true
        test_fragment(
            'a {\n' +
            '\n' +
            'width: auto;\n' +
            '\n' +
            'height: auto;\n' +
            '\n' +
            '}',
            #  -- output --
            'a {\n' +
            '    \n' +
            '    width: auto;\n' +
            '    \n' +
            '    height: auto;\n' +
            '    \n' +
            '}')


        #============================================================
        # indent_empty_lines false
        self.reset_options()
        self.options.indent_empty_lines = false
        self.options.preserve_newlines = true
        test_fragment(
            'a {\n' +
            '\n' +
            '    width: auto;\n' +
            '\n' +
            '    height: auto;\n' +
            '\n' +
            '}')


        #============================================================
        # brace_style = expand - (brace_style = ""expand"", selector_separator_newline = "false", newline_between_rules = "true")
        self.reset_options()
        self.options.brace_style = 'expand'
        self.options.selector_separator_newline = false
        self.options.newline_between_rules = true
        t(
            'a, b, .c {\n' +
            '    width: auto;\n' +
            '  \n' +
            '    height: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '    width: auto;\n' +
            '    height: auto;\n' +
            '}')
        
        # edge case - empty line after { should not be indented without indent_empty_lines
        t(
            'a, b, .c {\n' +
            '\n' +
            '    width: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '    width: auto;\n' +
            '}')
        
        # mixins call with object notation, and brace_style="expand"
        t(
            '.example({\n' +
            '    color:red;\n' +
            '});',
            #  -- output --
            '.example(\n' +
            '    {\n' +
            '        color:red;\n' +
            '    }\n' +
            ');')
        
        # integration test of newline_between_rules, imports, and brace_style="expand"
        t(
            '.a{} @import "custom.css";.rule{}',
            #  -- output --
            '.a\n' +
            '{}\n' +
            '\n' +
            '@import "custom.css";\n' +
            '\n' +
            '.rule\n' +
            '{}')

        # brace_style = expand - (brace_style = ""expand"", indent_empty_lines = "true", selector_separator_newline = "false", preserve_newlines = "true")
        self.reset_options()
        self.options.brace_style = 'expand'
        self.options.indent_empty_lines = true
        self.options.selector_separator_newline = false
        self.options.preserve_newlines = true
        t(
            'a, b, .c {\n' +
            '    width: auto;\n' +
            '  \n' +
            '    height: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '    width: auto;\n' +
            '    \n    height: auto;\n' +
            '}')
        
        # edge case - empty line after { should not be indented without indent_empty_lines
        t(
            'a, b, .c {\n' +
            '\n' +
            '    width: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '    \n    width: auto;\n' +
            '}')
        
        # mixins call with object notation, and brace_style="expand"
        t(
            '.example({\n' +
            '    color:red;\n' +
            '});',
            #  -- output --
            '.example(\n' +
            '    {\n' +
            '        color:red;\n' +
            '    }\n' +
            ');')
        
        # integration test of newline_between_rules, imports, and brace_style="expand"
        t(
            '.a{} @import "custom.css";.rule{}',
            #  -- output --
            '.a\n' +
            '{}\n' +
            '@import "custom.css";\n' +
            '.rule\n' +
            '{}')

        # brace_style = expand - (brace_style = ""expand"", indent_empty_lines = "false", selector_separator_newline = "false", preserve_newlines = "true")
        self.reset_options()
        self.options.brace_style = 'expand'
        self.options.indent_empty_lines = false
        self.options.selector_separator_newline = false
        self.options.preserve_newlines = true
        t(
            'a, b, .c {\n' +
            '    width: auto;\n' +
            '  \n' +
            '    height: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '    width: auto;\n' +
            '\n    height: auto;\n' +
            '}')
        
        # edge case - empty line after { should not be indented without indent_empty_lines
        t(
            'a, b, .c {\n' +
            '\n' +
            '    width: auto;\n' +
            '}',
            #  -- output --
            'a, b, .c\n' +
            '{\n' +
            '\n    width: auto;\n' +
            '}')
        
        # mixins call with object notation, and brace_style="expand"
        t(
            '.example({\n' +
            '    color:red;\n' +
            '});',
            #  -- output --
            '.example(\n' +
            '    {\n' +
            '        color:red;\n' +
            '    }\n' +
            ');')
        
        # integration test of newline_between_rules, imports, and brace_style="expand"
        t(
            '.a{} @import "custom.css";.rule{}',
            #  -- output --
            '.a\n' +
            '{}\n' +
            '@import "custom.css";\n' +
            '.rule\n' +
            '{}')


        #============================================================
        # LESS mixins
        self.reset_options()
        t(
            '.btn {\n' +
            '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);\n' +
            '}\n' +
            '.mymixin(@color: #ccc; @border-width: 1px) {\n' +
            '    border: @border-width solid @color;\n' +
            '}\n' +
            'strong {\n' +
            '    &:extend(a:hover);\n' +
            '}')
        t(
            '.test {\n' +
            '    .example({\n' +
            '        color:red;\n' +
            '    });\n' +
            '}')
        t(
            '.example2({\n' +
            '    display:none;\n' +
            '});')
        t(
            '.aa {\n' +
            '    .mq-medium(a, {\n' +
            '        background: red;\n' +
            '    });\n' +
            '}')
        t(
            '@selectors: blue, green, red;\n' +
            'each(@selectors, {\n' +
            '    .sel-@{value} {\n' +
            '        a: b;\n' +
            '    }\n' +
            '});')
        
        # Ensure simple closing parens do not break behavior
        t(
            'strong {\n' +
            '    &:extend(a:hover));\n' +
            '}\n' +
            '.btn {\n' +
            '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);\n' +
            '}\n' +
            '.mymixin(@color: #ccc; @border-width: 1px) {\n' +
            '    border: @border-width solid @color;\n' +
            '}\n' +
            'strong {\n' +
            '    &:extend(a:hover);\n' +
            '}')
        
        # indent multi-line parens
        t(
            '.btn {\n' +
            '    .generate-animation(@mykeyframes, 1.4s,\n' +
            '        .5s, 1, ease-out);\n' +
            '}\n' +
            '.mymixin(@color: #ccc;\n' +
            '    @border-width: 1px) {\n' +
            '    border: @border-width solid @color;\n' +
            '}')
        
        # format inside mixin parens
        t(
            '.btn {\n' +
            '    .generate-animation(@mykeyframes,1.4s,.5s,1,ease-out);\n' +
            '}\n' +
            '.mymixin(@color:#ccc;@border-width:1px) {\n' +
            '    border:@border-width solid @color;\n' +
            '}',
            #  -- output --
            '.btn {\n' +
            '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);\n' +
            '}\n' +
            '.mymixin(@color: #ccc; @border-width: 1px) {\n' +
            '    border: @border-width solid @color;\n' +
            '}')


        #============================================================
        # Preserve Newlines and max number of new lines
        self.reset_options()
        self.options.preserve_newlines = true
        self.options.max_preserve_newlines = 2
        t(
            'p {\n' +
            '\n' +
            '\n' +
            '\n' +
            '    color: blue;\n' +
            '}',
            #  -- output --
            'p {\n' +
            '\n' +
            '    color: blue;\n' +
            '}')
        t(
            'p {\n' +
            '\n' +
            '    color: blue;\n' +
            '}')
        t(
            'p {\n' +
            '    color: blue;\n' +
            '}')


        #============================================================
        # Issue #2012, #2147
        self.reset_options()
        t('@extend .btn-blue:hover;')
        t('@import url("chrome://communicator/skin/");')
        t('@apply w-4 lg:w-10 space-y-3 lg:space-x-12;')
        t(
            'h3 {\n' +
            '    @apply flex flex-col lg:flex-row space-y-3 lg:space-x-12 items-start;\n' +
            '}')


        #============================================================
        # 
        self.reset_options()



    def testNewline(self):
        self.reset_options()
        t = self.decodesto

        self.options.end_with_newline = True
        t("", "\n")
        t("\n", "\n")
        t(".tabs{}\n", ".tabs {}\n")
        t(".tabs{}", ".tabs {}\n")

    def testBasics(self):
        self.reset_options()
        t = self.decodesto

        self.reset_options()
        #============================================================
        t(None, "")

        self.reset_options()
        #============================================================
        # Test user pebkac protection, converts dash names to underscored names
        setattr(self.options, 'end-with-newline', True)
        t(None, '\n')
        
        self.reset_options()
        #============================================================

        t("", "")
        t("\n", "")
        t(".tabs{}\n", ".tabs {}")
        t(".tabs{}", ".tabs {}")
        t(".tabs{color:red}", ".tabs {\n    color: red\n}")
        t(".tabs{color:rgb(255, 255, 0)}", ".tabs {\n    color: rgb(255, 255, 0)\n}")
        t(".tabs{background:url('back.jpg')}", ".tabs {\n    background: url('back.jpg')\n}")
        t("#bla, #foo{color:red}", "#bla,\n#foo {\n    color: red\n}")
        t("@media print {.tab{}}", "@media print {\n    .tab {}\n}")
        t("@media print {.tab{background-image:url(foo@2x.png)}}", "@media print {\n    .tab {\n        background-image: url(foo@2x.png)\n    }\n}")

        t("a:before {\n" +
            "    content: 'a{color:black;}\"\"\\'\\'\"\\n\\n\\na{color:black}\';\n" +
            "}")

        # may not eat the space before "["
        t('html.js [data-custom="123"] {\n    opacity: 1.00;\n}')
        t('html.js *[data-custom="123"] {\n    opacity: 1.00;\n}')

        # lead-in whitespace determines base-indent.
        # lead-in newlines are stripped.
        t("\n\na, img {padding: 0.2px}", "a,\nimg {\n    padding: 0.2px\n}")
        t("   a, img {padding: 0.2px}", "   a,\n   img {\n       padding: 0.2px\n   }")
        t("      \na, img {padding: 0.2px}", "      a,\n      img {\n          padding: 0.2px\n      }")
        t("\n\n     a, img {padding: 0.2px}", "a,\nimg {\n    padding: 0.2px\n}")

    def testSeperateSelectors(self):
        self.reset_options()
        t = self.decodesto

        t("#bla, #foo{color:red}", "#bla,\n#foo {\n    color: red\n}")
        t("a, img {padding: 0.2px}", "a,\nimg {\n    padding: 0.2px\n}")


    def testBlockNesting(self):
        self.reset_options()
        t = self.decodesto

        t("#foo {\n    background-image: url(foo@2x.png);\n    @font-face {\n        font-family: 'Bitstream Vera Serif Bold';\n        src: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n    }\n}")
        t("@media screen {\n    #foo:hover {\n        background-image: url(foo@2x.png);\n    }\n    @font-face {\n        font-family: 'Bitstream Vera Serif Bold';\n        src: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n    }\n}")

# @font-face {
#     font-family: 'Bitstream Vera Serif Bold';
#     src: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');
# }
# @media screen {
#     #foo:hover {
#         background-image: url(foo.png);
#     }
#     @media screen and (min-device-pixel-ratio: 2) {
#         @font-face {
#             font-family: 'Helvetica Neue'
#         }
#         #foo:hover {
#             background-image: url(foo@2x.png);
#         }
#     }
# }
        t("@font-face {\n    font-family: 'Bitstream Vera Serif Bold';\n    src: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n}\n@media screen {\n    #foo:hover {\n        background-image: url(foo.png);\n    }\n    @media screen and (min-device-pixel-ratio: 2) {\n        @font-face {\n            font-family: 'Helvetica Neue'\n        }\n        #foo:hover {\n            background-image: url(foo@2x.png);\n        }\n    }\n}")


    def testOptions(self):
        self.reset_options()
        self.options.indent_size = 2
        self.options.indent_char = ' '
        self.options.selector_separator_newline = False
        t = self.decodesto

        # pseudo-classes and pseudo-elements
        t("#foo:hover {\n  background-image: url(foo@2x.png)\n}")
        t("#foo *:hover {\n  color: purple\n}")
        t("::selection {\n  color: #ff0000;\n}")

        # TODO: don't break nested pseduo-classes
        t("@media screen {.tab,.bat:hover {color:red}}", "@media screen {\n  .tab, .bat:hover {\n    color: red\n  }\n}")

        # particular edge case with braces and semicolons inside tags that allows custom text
        t(  "a:not(\"foobar\\\";{}omg\"){\ncontent: 'example\\';{} text';\ncontent: \"example\\\";{} text\";}",
            "a:not(\"foobar\\\";{}omg\") {\n  content: 'example\\';{} text';\n  content: \"example\\\";{} text\";\n}")

    def testLessCss(self):
        self.reset_options()
        t = self.decodesto

        t('.well{   \n    @well-bg:@bg-color;@well-fg:@fg-color;}','.well {\n    @well-bg: @bg-color;\n    @well-fg: @fg-color;\n}')
        t('.well {&.active {\nbox-shadow: 0 1px 1px @border-color, 1px 0 1px @border-color;}}',
            '.well {\n' +
            '    &.active {\n' +
            '        box-shadow: 0 1px 1px @border-color, 1px 0 1px @border-color;\n' +
            '    }\n' +
            '}')
        t('a {\n' +
            '    color: blue;\n' +
            '    &:hover {\n' +
            '        color: green;\n' +
            '    }\n' +
            '    & & &&&.active {\n' +
            '        color: green;\n' +
            '    }\n' +
            '}')

        # Not sure if this is sensible
        # but I believe it is correct to not remove the space in "&: hover".
        t('a {\n' +
            '    &: hover {\n' +
            '        color: green;\n' +
            '    }\n' +
            '}')

        # import
        t('@import "test";')

        # don't break nested pseudo-classes
        t("a:first-child{color:red;div:first-child{color:black;}}",
            "a:first-child {\n    color: red;\n    div:first-child {\n        color: black;\n    }\n}")

        # handle SASS/LESS parent reference
        t("div{&:first-letter {text-transform: uppercase;}}",
            "div {\n    &:first-letter {\n        text-transform: uppercase;\n    }\n}")

        # nested modifiers (&:hover etc)
        t(".tabs{&:hover{width:10px;}}", ".tabs {\n    &:hover {\n        width: 10px;\n    }\n}")
        t(".tabs{&.big{width:10px;}}", ".tabs {\n    &.big {\n        width: 10px;\n    }\n}")
        t(".tabs{&>big{width:10px;}}", ".tabs {\n    &>big {\n        width: 10px;\n    }\n}")
        t(".tabs{&+.big{width:10px;}}", ".tabs {\n    &+.big {\n        width: 10px;\n    }\n}")

        # nested rules
        t(".tabs{.child{width:10px;}}", ".tabs {\n    .child {\n        width: 10px;\n    }\n}")

        # variables
        t("@myvar:10px;.tabs{width:10px;}", "@myvar: 10px;\n.tabs {\n    width: 10px;\n}")
        t("@myvar:10px; .tabs{width:10px;}", "@myvar: 10px;\n.tabs {\n    width: 10px;\n}")

    def decodesto(self, input, expectation=None):
        if expectation == None:
            expectation = input

        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), expectation)

        # if the expected is different from input, run it again
        # expected output should be unchanged when run twice.
        if not expectation != input:
            self.assertMultiLineEqual(
                cssbeautifier.beautify(expectation, self.options), expectation)

        # Everywhere we do newlines, they should be replaced with opts.eol
        self.options.eol = '\r\\n'
        expectation = expectation.replace('\n', '\r\n')
        self.options.disabled = True
        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), input or '')
        self.assertMultiLineEqual(
            cssbeautifier.beautify('\n\n' + expectation, self.options), '\n\n' + expectation)
        self.options.disabled = False;
        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), expectation)
        if input and input.find('\n') != -1:
            input = input.replace('\n', '\r\n')
            self.assertMultiLineEqual(
                cssbeautifier.beautify(input, self.options), expectation)
            # Ensure support for auto eol detection
            self.options.eol = 'auto'
            self.assertMultiLineEqual(
                cssbeautifier.beautify(input, self.options), expectation)
        self.options.eol = '\n'

if __name__ == '__main__':
    unittest.main()
