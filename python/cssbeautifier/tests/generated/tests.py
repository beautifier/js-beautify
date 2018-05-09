#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    AUTO-GENERATED. DO NOT MODIFY.
    Script: test/generate-tests.js
    Template: test/data/css/python.mustache
    Data: test/data/css/tests.js

  The MIT License (MIT)

  Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

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
        false = False
        true = True

        default_options = cssbeautifier.default_options()
        default_options.indent_size = 1
        default_options.indent_char = '\t'
        default_options.selector_separator_newline = true
        default_options.end_with_newline = false
        default_options.newline_between_rules = false

        default_options.indent_size = 1
        default_options.indent_char = '\t'
        default_options.selector_separator_newline = true
        default_options.end_with_newline = false
        default_options.newline_between_rules = false
        default_options.space_around_combinator = false
        default_options.preserve_newlines = false
        default_options.space_around_selector_separator = false

        cls.default_options = default_options

    def reset_options(self):
        self.options = copy.copy(self.default_options)

    def testGenerated(self):
        self.reset_options()
        test_fragment = self.decodesto
        t = self.decodesto

        false = False
        true = True


        #============================================================
        # End With Newline - (eof = "\n")
        self.reset_options();
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

        # End With Newline - (eof = "")
        self.reset_options();
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
        # Empty braces
        self.reset_options();
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
        self.reset_options();
        t(
            '#cboxOverlay {\n' +
            '\tbackground: url(images/overlay.png) repeat 0 0;\n' +
            '\topacity: 0.9;\n' +
            '\tfilter: alpha(opacity = 90);\n' +
            '}',
            #  -- output --
            '#cboxOverlay {\n' +
            '\tbackground: url(images/overlay.png) repeat 0 0;\n' +
            '\topacity: 0.9;\n' +
            '\tfilter: alpha(opacity=90);\n' +
            '}')


        #============================================================
        # Support simple language specific option inheritance/overriding - (c = "     ")
        self.reset_options();
        self.options.indent_char = ' '
        self.options.indent_size = 4
        self.options.js = { 'indent_size': 3 }
        self.options.css = { 'indent_size': 5 }
        t(
            '.selector {\n' +
            '     font-size: 12px;\n' +
            '}')

        # Support simple language specific option inheritance/overriding - (c = "    ")
        self.reset_options();
        self.options.indent_char = ' '
        self.options.indent_size = 4
        self.options.html = { 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 } }
        t(
            '.selector {\n' +
            '    font-size: 12px;\n' +
            '}')

        # Support simple language specific option inheritance/overriding - (c = "   ")
        self.reset_options();
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
        # Space Around Combinator - (space = " ")
        self.reset_options();
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
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a ~ b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a + b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a + b > c {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')

        # Space Around Combinator - (space = "")
        self.reset_options();
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
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a~b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a+b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a+b>c {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')

        # Space Around Combinator - (space = " ")
        self.reset_options();
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
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a ~ b{width: calc(100% + 45px);}',
            #  -- output --
            'a ~ b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b{width: calc(100% + 45px);}',
            #  -- output --
            'a + b {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')
        t(
            'a + b > c{width: calc(100% + 45px);}',
            #  -- output --
            'a + b > c {\n' +
            '\twidth: calc(100% + 45px);\n' +
            '}')


        #============================================================
        # Selector Separator - (separator = " ", separator1 = " ")
        self.reset_options();
        self.options.selector_separator_newline = false
        self.options.selector_separator = " "
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '\tcolor: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab {}\n' +
            '}')
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab, .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla, #foo {\n' +
            '\tcolor: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child, a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child, div:hover {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}')

        # Selector Separator - (separator = " ", separator1 = " ")
        self.reset_options();
        self.options.selector_separator_newline = false
        self.options.selector_separator = "  "
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla, #foo {\n' +
            '\tcolor: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab {}\n' +
            '}')
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab, .bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla, #foo {\n' +
            '\tcolor: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child, a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child, div:hover {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}')

        # Selector Separator - (separator = "\n", separator1 = "\n\t")
        self.reset_options();
        self.options.selector_separator_newline = true
        self.options.selector_separator = " "
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '\tcolor: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab {}\n' +
            '}')
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab,\n\t.bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '\tcolor: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child,\n\tdiv:hover {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}')

        # Selector Separator - (separator = "\n", separator1 = "\n\t")
        self.reset_options();
        self.options.selector_separator_newline = true
        self.options.selector_separator = "  "
        t(
            '#bla, #foo{color:green}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '\tcolor: green\n' +
            '}')
        t(
            '@media print {.tab{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab {}\n' +
            '}')
        t(
            '@media print {.tab,.bat{}}',
            #  -- output --
            '@media print {\n' +
            '\t.tab,\n\t.bat {}\n' +
            '}')
        t(
            '#bla, #foo{color:black}',
            #  -- output --
            '#bla,\n#foo {\n' +
            '\tcolor: black\n' +
            '}')
        t(
            'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
            #  -- output --
            'a:first-child,\na:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child,\n\tdiv:hover {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}')


        #============================================================
        # Preserve Newlines - (separator_input = "\n\n", separator_output = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        t('.div {}\n\n.span {}')
        t(
            '#bla, #foo{\n' +
            '\tcolor:black;\n\n\tfont-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '\tcolor: black;\n\n\tfont-size: 12px;\n' +
            '}')

        # Preserve Newlines - (separator_input = "\n\n", separator_output = "\n")
        self.reset_options();
        self.options.preserve_newlines = false
        t('.div {}\n\n.span {}', '.div {}\n.span {}')
        t(
            '#bla, #foo{\n' +
            '\tcolor:black;\n\n\tfont-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '\tcolor: black;\n\tfont-size: 12px;\n' +
            '}')


        #============================================================
        # Preserve Newlines and newline_between_rules
        self.reset_options();
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
            '\tcolor:black;\n' +
            '\tfont-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '\tcolor: black;\n' +
            '\tfont-size: 12px;\n' +
            '}')
        t(
            '#bla, #foo{\n' +
            '\tcolor:black;\n' +
            '\n' +
            '\n' +
            '\tfont-size: 12px;\n' +
            '}',
            #  -- output --
            '#bla,\n' +
            '#foo {\n' +
            '\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\tfont-size: 12px;\n' +
            '}')
        t(
            '#bla,\n' +
            '\n' +
            '#foo {\n' +
            '\tcolor: black;\n' +
            '\tfont-size: 12px;\n' +
            '}')
        t(
            'a {\n' +
            '\tb: c;\n' +
            '\n' +
            '\n' +
            '\td: {\n' +
            '\t\te: f;\n' +
            '\t}\n' +
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
            '\ta: 1;\n' +
            '\n' +
            '\n' +
            '\tb: 2;\n' +
            '}\n' +
            '\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\ta: 1;\n' +
            '}')
        t(
            '.div {\n' +
            '\n' +
            '\n' +
            '\ta: 1;\n' +
            '\n' +
            '\n' +
            '\tb: 2;\n' +
            '}\n' +
            '\n' +
            '\n' +
            '\n' +
            '.span {\n' +
            '\ta: 1;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t.div {\n' +
            '\t\ta: 1;\n' +
            '\n' +
            '\n' +
            '\t\tb: 2;\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\n' +
            '\t.span {\n' +
            '\t\ta: 1;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {}\n' +
            '\n' +
            '.span {}')


        #============================================================
        # Preserve Newlines and add tabs
        self.reset_options();
        self.options.preserve_newlines = true
        t(
            '.tool-tip {\n' +
            '\tposition: relative;\n' +
            '\n' +
            '\t\t\n' +
            '\t.tool-tip-content {\n' +
            '\t\t&>* {\n' +
            '\t\t\tmargin-top: 0;\n' +
            '\t\t}\n' +
            '\t\t\n' +
            '\n' +
            '\t\t.mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n' +
            '\t\tpadding: 1rem;\n' +
            '\t\tposition: absolute;\n' +
            '\t\tz-index: 10;\n' +
            '\t}\n' +
            '}',
            #  -- output --
            '.tool-tip {\n' +
            '\tposition: relative;\n' +
            '\n' +
            '\n' +
            '\t.tool-tip-content {\n' +
            '\t\t&>* {\n' +
            '\t\t\tmargin-top: 0;\n' +
            '\t\t}\n' +
            '\n\n\t\t.mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n' +
            '\t\tpadding: 1rem;\n' +
            '\t\tposition: absolute;\n' +
            '\t\tz-index: 10;\n' +
            '\t}\n' +
            '}')


        #============================================================
        # Newline Between Rules - (new_rule = "\n\n")
        self.reset_options();
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
            '\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue"\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue"\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Newline Between Rules - (new_rule = "\n")
        self.reset_options();
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
            '\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue"\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}\n' +
            '.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')


        #============================================================
        # Functions braces
        self.reset_options();
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
            '\tkey: val(p1, p2);\n' +
            '}')
        t(
            '.box-shadow(@shadow: 0 1px 3px rgba(0, 0, 0, .25)) {\n' +
            '\t-webkit-box-shadow: @shadow;\n' +
            '\t-moz-box-shadow: @shadow;\n' +
            '\tbox-shadow: @shadow;\n' +
            '}')


        #============================================================
        # Comments - (i = "", i1 = "\n", o = "\n", new_rule = "\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo@2x.png);\t}\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\tfont-family: "Bitstream Vera Serif Bold";\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo.png);\t}\t@media screen and (min-device-pixel-ratio: 2) {\t\t@font-face {\t\t\tfont-family: "Helvetica Neue";\t\t}\t\t#foo:hover {\t\t\tbackground-image: url(foo@2x.png);\t\t}\t}}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\n\n", i1 = "\n\n\n", o = "\n", new_rule = "\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
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
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
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
            '\t// comment\n' +
            '\twidth: 10px;\n' +
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
            '\t// comment\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px;\n' +
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
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
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
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '\t\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
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
            '\ttext-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\t\t\n    \n", i1 = "\n\t\t\t\n   \n", o = "\n", new_rule = "\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '/* test */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\t\t\n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\t\t\n' +
            '    \n' +
            '/* non-header */\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\t\t\n' +
            '    \n' +
            'margin: 0;\n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '//2nd single line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;\n' +
            '\t\t\t\n' +
            '   \n' +
            '\t\t// comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\t\t\n' +
            '    \n' +
            '/* another comment */\n' +
            '\t\t\n' +
            '    \n' +
            'body{}\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align:left;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\t\n' +
            '   \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '//\n' +
            '.div {}\n' +
            '//\n' +
            '.span {}')
        t(
            '.selector1 {\n' +
            '\t\t\n' +
            '    \n' +
            'margin: 0; \n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\t\t\n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:not(.peq){\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "", i1 = "\n", o = "\n", new_rule = "\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo@2x.png);\t}\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\tfont-family: "Bitstream Vera Serif Bold";\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo.png);\t}\t@media screen and (min-device-pixel-ratio: 2) {\t\t@font-face {\t\t\tfont-family: "Helvetica Neue";\t\t}\t\t#foo:hover {\t\t\tbackground-image: url(foo@2x.png);\t\t}\t}}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n", i1 = "\n", o = "\n", new_rule = "\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '/* test */\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            'width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            'width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
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
            '\ttext-align: left;\n' +
            '}\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            'background-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\t\t\n    \n", i1 = "\n\t\t\t\n   \n", o = "\n\n\n", new_rule = "\n\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '/* test */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t/* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\t\t\n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\t\t\n' +
            '    \n' +
            '/* non-header */\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t/* non-header */\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\t\t\n' +
            '    \n' +
            'margin: 0;\n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '//2nd single line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t//comment\n' +
            '\n' +
            '\n' +
            '\t//2nd single line comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;\n' +
            '\t\t\t\n' +
            '   \n' +
            '\t\t// comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\t\t\n' +
            '    \n' +
            '/* another comment */\n' +
            '\t\t\n' +
            '    \n' +
            'body{}\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '\ttext-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align:left;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '\ttext-align: left;\n' +
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
            '\ttext-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\t\n' +
            '   \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'margin: 0; \n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '\t\t\n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:first-child {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:not(.peq){\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:not(.peq) {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (i = "\n\n\n", i1 = "\n\n\n", o = "\n\n\n", new_rule = "\n\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = false
        t('/* header comment newlines on */')
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
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
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
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px;\n' +
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
            '\t//comment\n' +
            '\n' +
            '\n' +
            '\t//2nd single line comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another nl\n' +
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
            '\twidth: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
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
            '\t\t// comment follows rule\n' +
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
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '\ttext-align: right;\n' +
            '\n' +
            '\n' +
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
            '\ttext-align: left;\n' +
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
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:first-child {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:not(.peq) {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (i = "", i1 = "\n", o = "\n", new_rule = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo@2x.png);\t}\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\tfont-family: "Bitstream Vera Serif Bold";\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo.png);\t}\t@media screen and (min-device-pixel-ratio: 2) {\t\t@font-face {\t\t\tfont-family: "Helvetica Neue";\t\t}\t\t#foo:hover {\t\t\tbackground-image: url(foo@2x.png);\t\t}\t}}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\n\n", i1 = "\n\n\n", o = "\n", new_rule = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
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
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
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
            '\t// comment\n' +
            '\twidth: 10px;\n' +
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
            '\t// comment\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px;\n' +
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
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
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
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\n' +
            '\n' +
            'width: 10px;\n' +
            '\n' +
            '\n' +
            '\t\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '// another comment new line\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
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
            '\ttext-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\n' +
            '\n' +
            'background-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\t\t\n    \n", i1 = "\n\t\t\t\n   \n", o = "\n", new_rule = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = false
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '/* test */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\t\t\n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\t\t\n' +
            '    \n' +
            '/* non-header */\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\t\t\n' +
            '    \n' +
            'margin: 0;\n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '//2nd single line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;\n' +
            '\t\t\t\n' +
            '   \n' +
            '\t\t// comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\t\t\n' +
            '    \n' +
            '/* another comment */\n' +
            '\t\t\n' +
            '    \n' +
            'body{}\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align:left;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\t\n' +
            '   \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'margin: 0; \n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            '\t\t\n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:not(.peq){\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "", i1 = "\n", o = "\n", new_rule = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '.tabs{/* test */}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {margin: 0;/* This is a comment including an url http://domain.com/path/to/file.ext */}',
            #  -- output --
            '.selector1 {\n' +
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{// comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{width:10px;}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
            '}')
        t(
            '.demoa2 {text-align:left;}//demob instructions for LESS note visibility only\n' +
            '.demob {text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\ttext-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '.tabs{width:10px;//end of line comment\n' +
            'height:10px;//another\n' +
            '}.div{height:15px;}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {background-image: url(foo@2x.png);\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo@2x.png);\t}\t@font-face {\t\tfont-family: "Bitstream Vera Serif Bold";\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\t}}.div{height:15px;}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\tfont-family: "Bitstream Vera Serif Bold";\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");}\n' +
            '@media screen {\t#foo:hover {\t\tbackground-image: url(foo.png);\t}\t@media screen and (min-device-pixel-ratio: 2) {\t\t@font-face {\t\t\tfont-family: "Helvetica Neue";\t\t}\t\t#foo:hover {\t\t\tbackground-image: url(foo@2x.png);\t\t}\t}}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}')
        t(
            'a:first-child{color:red;div:first-child{color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            'a:first-child{color:red;div:not(.peq){color:black;}}.div{height:15px;}',
            #  -- output --
            'a:first-child {\n' +
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n", i1 = "\n", o = "\n", new_rule = "\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '/* test */\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '// comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t// comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '//comment\n' +
            '.tabs{\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '//comment\n' +
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            '//comment\n' +
            '//2nd single line comment\n' +
            'width:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\t//comment\n' +
            '\t//2nd single line comment\n' +
            '\twidth: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px;\n' +
            '}')
        t(
            '.tabs{\n' +
            'width:10px;//end of line comment\n' +
            'height:10px;//another nl\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another nl\n' +
            '}')
        t(
            '.tabs{\n' +
            'width: 10px;   // comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\t// another comment new line\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            'width: 10px;\n' +
            '\t\t// comment follows rule\n' +
            '// another comment new line\n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\twidth: 10px;\n' +
            '\t// comment follows rule\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '}\n' +
            '\n' +
            '.demob {\n' +
            '\ttext-align: right;\n' +
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
            '\ttext-align: left;\n' +
            '}\n' +
            '\n' +
            '//demob instructions for LESS note visibility only\n' +
            '.demob {\n' +
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\theight: 10px; //another\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '#foo {\n' +
            'background-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '.div{\n' +
            'height:15px;\n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t}\n' +
            '\t@font-face {\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')
        t(
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '}\n' +
            '\n' +
            '@media screen {\n' +
            '\t#foo:hover {\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t}\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t@font-face {\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t}\n' +
            '\t\t#foo:hover {\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t}\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:first-child {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\tdiv:not(.peq) {\n' +
            '\t\tcolor: black;\n' +
            '\t}\n' +
            '}\n' +
            '\n' +
            '.div {\n' +
            '\theight: 15px;\n' +
            '}')

        # Comments - (i = "\n\n\n", i1 = "\n\n\n", o = "\n\n\n", new_rule = "\n\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
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
            '\t/* test */\n' +
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
            '\t/* non-header */\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
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
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px;\n' +
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
            '\t//comment\n' +
            '\n' +
            '\n' +
            '\t//2nd single line comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another nl\n' +
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
            '\twidth: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
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
            '\t\t// comment follows rule\n' +
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
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
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
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '\ttext-align: right;\n' +
            '\n' +
            '\n' +
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
            '\ttext-align: left;\n' +
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
            '\ttext-align: right\n' +
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
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
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
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:first-child {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
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
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:not(.peq) {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')

        # Comments - (i = "\n\t\t\n    \n", i1 = "\n\t\t\t\n   \n", o = "\n\n\n", new_rule = "\n\n\n")
        self.reset_options();
        self.options.preserve_newlines = true
        self.options.newline_between_rules = true
        t('/* header comment newlines on */')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '/* test */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t/* test */\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1185
        t(
            '/* header */\n' +
            '\t\t\n' +
            '    \n' +
            '.tabs{}',
            #  -- output --
            '/* header */\n' +
            '\n' +
            '\n' +
            '.tabs {}')
        t(
            '.tabs {\n' +
            '\t\t\n' +
            '    \n' +
            '/* non-header */\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t/* non-header */\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t('/* header')
        t('// comment')
        t('/*')
        t('//')
        t(
            '.selector1 {\n' +
            '\t\t\n' +
            '    \n' +
            'margin: 0;\n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}')
        
        # single line comment support (less/sass)
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '// comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t// comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '//comment\n' +
            '\n' +
            '\n' +
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            '//comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '//2nd single line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'width:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\t//comment\n' +
            '\n' +
            '\n' +
            '\t//2nd single line comment\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another nl\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another nl\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;   // comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; // comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #1165
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width: 10px;\n' +
            '\t\t\t\n' +
            '   \n' +
            '\t\t// comment follows rule\n' +
            '\t\t\t\n' +
            '   \n' +
            '// another comment new line\n' +
            '\t\t\t\n' +
            '   \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px;\n' +
            '\n' +
            '\n' +
            '\t// comment follows rule\n' +
            '\n' +
            '\n' +
            '\t// another comment new line\n' +
            '\n' +
            '\n' +
            '}')
        
        # #736
        t(
            '/*\n' +
            ' * comment\n' +
            ' */\n' +
            '\t\t\n' +
            '    \n' +
            '/* another comment */\n' +
            '\t\t\n' +
            '    \n' +
            'body{}\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'text-align:left; //demoa1 instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.demoa1 {\n' +
            '\n' +
            '\n' +
            '\ttext-align: left; //demoa1 instructions for LESS note visibility only\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.demob {\n' +
            '\n' +
            '\n' +
            '\ttext-align: right;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.demoa2 {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align:left;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '//demob instructions for LESS note visibility only\n' +
            '\t\t\t\n' +
            '   \n' +
            '.demob {\n' +
            '\t\t\n' +
            '    \n' +
            'text-align: right}',
            #  -- output --
            '.demoa2 {\n' +
            '\n' +
            '\n' +
            '\ttext-align: left;\n' +
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
            '\ttext-align: right\n' +
            '}')
        
        # new lines between rules - #531 and #857
        t(
            '.div{}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.div {}\n' +
            '\n' +
            '\n' +
            '.span {}')
        t(
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '/**/\n' +
            '\t\t\n' +
            '    \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\t\n' +
            '   \n' +
            '.div{}\n' +
            '\t\t\n' +
            '    \n' +
            '//\n' +
            '\t\t\t\n' +
            '   \n' +
            '.span {\n' +
            '\t\t\n' +
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
            '\t\t\n' +
            '    \n' +
            'margin: 0; \n' +
            '\t\t\n' +
            '    \n' +
            '/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.selector1 {\n' +
            '\n' +
            '\n' +
            '\tmargin: 0;\n' +
            '\n' +
            '\n' +
            '\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '.tabs{\n' +
            '\t\t\n' +
            '    \n' +
            'width:10px;//end of line comment\n' +
            '\t\t\t\n' +
            '   \n' +
            'height:10px;//another\n' +
            '\t\t\t\n' +
            '   \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '.tabs {\n' +
            '\n' +
            '\n' +
            '\twidth: 10px; //end of line comment\n' +
            '\n' +
            '\n' +
            '\theight: 10px; //another\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '#foo {\n' +
            '\t\t\n' +
            '    \n' +
            'background-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '#foo {\n' +
            '\n' +
            '\n' +
            '\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            '@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\t\t\n' +
            '    \n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\t\n' +
            '   \n' +
            '@media screen {\n' +
            '\t\t\n' +
            '    \n' +
            '\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t@font-face {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t#foo:hover {\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\t\t\n' +
            '    \n' +
            '\t\t}\n' +
            '\t\t\n' +
            '    \n' +
            '\t}\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            '@font-face {\n' +
            '\n' +
            '\n' +
            '\tfont-family: "Bitstream Vera Serif Bold";\n' +
            '\n' +
            '\n' +
            '\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '@media screen {\n' +
            '\n' +
            '\n' +
            '\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\tbackground-image: url(foo.png);\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '\t@media screen and (min-device-pixel-ratio: 2) {\n' +
            '\n' +
            '\n' +
            '\t\t@font-face {\n' +
            '\n' +
            '\n' +
            '\t\t\tfont-family: "Helvetica Neue";\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t\t#foo:hover {\n' +
            '\n' +
            '\n' +
            '\t\t\tbackground-image: url(foo@2x.png);\n' +
            '\n' +
            '\n' +
            '\t\t}\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:first-child {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')
        t(
            'a:first-child{\n' +
            '\t\t\n' +
            '    \n' +
            'color:red;\n' +
            '\t\t\n' +
            '    \n' +
            'div:not(.peq){\n' +
            '\t\t\n' +
            '    \n' +
            'color:black;\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '}\n' +
            '\t\t\n' +
            '    \n' +
            '.div{\n' +
            '\t\t\n' +
            '    \n' +
            'height:15px;\n' +
            '\t\t\n' +
            '    \n' +
            '}',
            #  -- output --
            'a:first-child {\n' +
            '\n' +
            '\n' +
            '\tcolor: red;\n' +
            '\n' +
            '\n' +
            '\tdiv:not(.peq) {\n' +
            '\n' +
            '\n' +
            '\t\tcolor: black;\n' +
            '\n' +
            '\n' +
            '\t}\n' +
            '\n' +
            '\n' +
            '}\n' +
            '\n' +
            '\n' +
            '.div {\n' +
            '\n' +
            '\n' +
            '\theight: 15px;\n' +
            '\n' +
            '\n' +
            '}')


        #============================================================
        # Handle LESS property name interpolation
        self.reset_options();
        t(
            'tag {\n' +
            '\t@{prop}: none;\n' +
            '}')
        t(
            'tag{@{prop}:none;}',
            #  -- output --
            'tag {\n' +
            '\t@{prop}: none;\n' +
            '}')
        t(
            'tag{ @{prop}: none;}',
            #  -- output --
            'tag {\n' +
            '\t@{prop}: none;\n' +
            '}')
        
        # can also be part of property name
        t(
            'tag {\n' +
            '\tdynamic-@{prop}: none;\n' +
            '}')
        t(
            'tag{dynamic-@{prop}:none;}',
            #  -- output --
            'tag {\n' +
            '\tdynamic-@{prop}: none;\n' +
            '}')
        t(
            'tag{ dynamic-@{prop}: none;}',
            #  -- output --
            'tag {\n' +
            '\tdynamic-@{prop}: none;\n' +
            '}')


        #============================================================
        # Handle LESS property name interpolation, test #631
        self.reset_options();
        t(
            '.generate-columns(@n, @i: 1) when (@i =< @n) {\n' +
            '\t.column-@{i} {\n' +
            '\t\twidth: (@i * 100% / @n);\n' +
            '\t}\n' +
            '\t.generate-columns(@n, (@i + 1));\n' +
            '}')
        t(
            '.generate-columns(@n,@i:1) when (@i =< @n){.column-@{i}{width:(@i * 100% / @n);}.generate-columns(@n,(@i + 1));}',
            #  -- output --
            '.generate-columns(@n, @i: 1) when (@i =< @n) {\n' +
            '\t.column-@{i} {\n' +
            '\t\twidth: (@i * 100% / @n);\n' +
            '\t}\n' +
            '\t.generate-columns(@n, (@i + 1));\n' +
            '}')


        #============================================================
        # Handle LESS function parameters
        self.reset_options();
        t(
            'div{.px2rem(width,12);}',
            #  -- output --
            'div {\n' +
            '\t.px2rem(width, 12);\n' +
            '}')
        t(
            'div {\n' +
            '\tbackground: url("//test.com/dummy.png");\n' +
            '\t.px2rem(width, 12);\n' +
            '}')


        #============================================================
        # Psuedo-classes vs Variables
        self.reset_options();
        t('@page :first {}')
        
        # Assume the colon goes with the @name. If we're in LESS, this is required regardless of the at-string.
        t('@page:first {}', '@page: first {}')
        t('@page: first {}')


        #============================================================
        # SASS/SCSS
        self.reset_options();
        
        # Basic Interpolation
        t(
            'p {\n' +
            '\t$font-size: 12px;\n' +
            '\t$line-height: 30px;\n' +
            '\tfont: #{$font-size}/#{$line-height};\n' +
            '}')
        t('p.#{$name} {}')
        t(
            '@mixin itemPropertiesCoverItem($items, $margin) {\n' +
            '\twidth: calc((100% - ((#{$items} - 1) * #{$margin}rem)) / #{$items});\n' +
            '\tmargin: 1.6rem #{$margin}rem 1.6rem 0;\n' +
            '}')
        
        # Multiple filed issues in LESS due to not(:blah)
        t('&:first-of-type:not(:last-child) {}')
        t(
            'div {\n' +
            '\t&:not(:first-of-type) {\n' +
            '\t\tbackground: red;\n' +
            '\t}\n' +
            '}')


        #============================================================
        # Proper handling of colon in selectors
        self.reset_options();
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
            '\tcolor: #87D1FF;\n' +
            '}')
        t(
            'div [attr] :not(.class) {\n' +
            '\tcolor: red;\n' +
            '}')


        #============================================================
        # Regresssion Tests
        self.reset_options();
        self.options.selector_separator_newline = false
        t(
            '@media(min-width:768px) {\n' +
            '\t.selector::after {\n' +
            '\t\t/* property: value */\n' +
            '\t}\n' +
            '\t.other-selector {\n' +
            '\t\t/* property: value */\n' +
            '\t}\n' +
            '}')
        t(
            '.fa-rotate-270 {\n' +
            '\tfilter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);\n' +
            '}')


        #============================================================
        # Important 
        self.reset_options();
        t(
            'a {\n' +
            '\tcolor: blue  !important;\n' +
            '}',
            #  -- output --
            'a {\n' +
            '\tcolor: blue !important;\n' +
            '}')
        t(
            'a {\n' +
            '\tcolor: blue!important;\n' +
            '}',
            #  -- output --
            'a {\n' +
            '\tcolor: blue !important;\n' +
            '}')
        t(
            'a {\n' +
            '\tcolor: blue !important;\n' +
            '}')


        #============================================================
        # 
        self.reset_options();



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

        t("", "")
        t("\n", "")
        t(".tabs{}\n", ".tabs {}")
        t(".tabs{}", ".tabs {}")
        t(".tabs{color:red}", ".tabs {\n\tcolor: red\n}")
        t(".tabs{color:rgb(255, 255, 0)}", ".tabs {\n\tcolor: rgb(255, 255, 0)\n}")
        t(".tabs{background:url('back.jpg')}", ".tabs {\n\tbackground: url('back.jpg')\n}")
        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}")
        t("@media print {.tab{}}", "@media print {\n\t.tab {}\n}")
        t("@media print {.tab{background-image:url(foo@2x.png)}}", "@media print {\n\t.tab {\n\t\tbackground-image: url(foo@2x.png)\n\t}\n}")

        t("a:before {\n" +
            "\tcontent: 'a{color:black;}\"\"\\'\\'\"\\n\\n\\na{color:black}\';\n" +
            "}");

        # may not eat the space before "["
        t('html.js [data-custom="123"] {\n\topacity: 1.00;\n}')
        t('html.js *[data-custom="123"] {\n\topacity: 1.00;\n}')

        # lead-in whitespace determines base-indent.
        # lead-in newlines are stripped.
        t("\n\na, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")
        t("   a, img {padding: 0.2px}", "   a,\n   img {\n   \tpadding: 0.2px\n   }")
        t(" \t \na, img {padding: 0.2px}", " \t a,\n \t img {\n \t \tpadding: 0.2px\n \t }")
        t("\n\n     a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")

    def testSeperateSelectors(self):
        self.reset_options()
        t = self.decodesto

        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}")
        t("a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")


    def testBlockNesting(self):
        self.reset_options()
        t = self.decodesto

        t("#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: 'Bitstream Vera Serif Bold';\n\t\tsrc: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n\t}\n}")
        t("@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: 'Bitstream Vera Serif Bold';\n\t\tsrc: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n\t}\n}")

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
        t("@font-face {\n\tfont-family: 'Bitstream Vera Serif Bold';\n\tsrc: url('http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf');\n}\n@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: 'Helvetica Neue'\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}")


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

        t('.well{   \n    @well-bg:@bg-color;@well-fg:@fg-color;}','.well {\n\t@well-bg: @bg-color;\n\t@well-fg: @fg-color;\n}')
        t('.well {&.active {\nbox-shadow: 0 1px 1px @border-color, 1px 0 1px @border-color;}}',
            '.well {\n' +
            '\t&.active {\n' +
            '\t\tbox-shadow: 0 1px 1px @border-color, 1px 0 1px @border-color;\n' +
            '\t}\n' +
            '}')
        t('a {\n' +
            '\tcolor: blue;\n' +
            '\t&:hover {\n' +
            '\t\tcolor: green;\n' +
            '\t}\n' +
            '\t& & &&&.active {\n' +
            '\t\tcolor: green;\n' +
            '\t}\n' +
            '}')

        # Not sure if this is sensible
        # but I believe it is correct to not remove the space in "&: hover".
        t('a {\n' +
            '\t&: hover {\n' +
            '\t\tcolor: green;\n' +
            '\t}\n' +
            '}');

        # import
        t('@import "test";');

        # don't break nested pseudo-classes
        t("a:first-child{color:red;div:first-child{color:black;}}",
            "a:first-child {\n\tcolor: red;\n\tdiv:first-child {\n\t\tcolor: black;\n\t}\n}");

        # handle SASS/LESS parent reference
        t("div{&:first-letter {text-transform: uppercase;}}",
            "div {\n\t&:first-letter {\n\t\ttext-transform: uppercase;\n\t}\n}");

        # nested modifiers (&:hover etc)
        t(".tabs{&:hover{width:10px;}}", ".tabs {\n\t&:hover {\n\t\twidth: 10px;\n\t}\n}")
        t(".tabs{&.big{width:10px;}}", ".tabs {\n\t&.big {\n\t\twidth: 10px;\n\t}\n}")
        t(".tabs{&>big{width:10px;}}", ".tabs {\n\t&>big {\n\t\twidth: 10px;\n\t}\n}")
        t(".tabs{&+.big{width:10px;}}", ".tabs {\n\t&+.big {\n\t\twidth: 10px;\n\t}\n}")

        # nested rules
        t(".tabs{.child{width:10px;}}", ".tabs {\n\t.child {\n\t\twidth: 10px;\n\t}\n}")

        # variables
        t("@myvar:10px;.tabs{width:10px;}", "@myvar: 10px;\n.tabs {\n\twidth: 10px;\n}")
        t("@myvar:10px; .tabs{width:10px;}", "@myvar: 10px;\n.tabs {\n\twidth: 10px;\n}")

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
        self.options.eol = '\r\\n';
        expectation = expectation.replace('\n', '\r\n')
        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), expectation)
        if input.find('\n') != -1:
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
