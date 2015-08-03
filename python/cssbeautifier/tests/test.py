#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import cssbeautifier


class CSSBeautifierTest(unittest.TestCase):

    def resetOptions(self):
        false = False
        true = True
        self.options = cssbeautifier.default_options()
        self.options.indent_size = 1
        self.options.indent_char = '\t'
        self.options.selector_separator_newline = true
        self.options.end_with_newline = false
        self.options.newline_between_rules = false

    def testGenerated(self):
        self.resetOptions()
        test_fragment = self.decodesto
        t = self.decodesto

        false = False
        true = True

        self.options.indent_size = 1
        self.options.indent_char = '\t'
        self.options.selector_separator_newline = true
        self.options.end_with_newline = false
        self.options.newline_between_rules = false

        # End With Newline - (eof = "\n")
        self.options.end_with_newline = true
        test_fragment('', '\n')
        test_fragment('   .tabs{}', '   .tabs {}\n')
        test_fragment('   \n\n.tabs{}\n\n\n\n', '   .tabs {}\n')
        test_fragment('\n')

        # End With Newline - (eof = "")
        self.options.end_with_newline = false
        test_fragment('')
        test_fragment('   .tabs{}', '   .tabs {}')
        test_fragment('   \n\n.tabs{}\n\n\n\n', '   .tabs {}')
        test_fragment('\n', '')

        # Empty braces
        t('.tabs{}', '.tabs {}')
        t('.tabs { }', '.tabs {}')
        t('.tabs    {    }', '.tabs {}')
        t('.tabs    \n{\n    \n  }', '.tabs {}')

        # 
        t('#cboxOverlay {\n\tbackground: url(images/overlay.png) repeat 0 0;\n\topacity: 0.9;\n\tfilter: alpha(opacity = 90);\n}', '#cboxOverlay {\n\tbackground: url(images/overlay.png) repeat 0 0;\n\topacity: 0.9;\n\tfilter: alpha(opacity=90);\n}')

        # Selector Separator - (separator = " ", separator1 = " ")
        self.options.selector_separator_newline = false
        self.options.selector_separator = " "
        t('#bla, #foo{color:green}', '#bla, #foo {\n\tcolor: green\n}')
        t('@media print {.tab{}}', '@media print {\n\t.tab {}\n}')
        t('@media print {.tab,.bat{}}', '@media print {\n\t.tab, .bat {}\n}')
        t('#bla, #foo{color:black}', '#bla, #foo {\n\tcolor: black\n}')
        t('a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}', 'a:first-child, a:first-child {\n\tcolor: red;\n\tdiv:first-child, div:hover {\n\t\tcolor: black;\n\t}\n}')

        # Selector Separator - (separator = " ", separator1 = " ")
        self.options.selector_separator_newline = false
        self.options.selector_separator = "  "
        t('#bla, #foo{color:green}', '#bla, #foo {\n\tcolor: green\n}')
        t('@media print {.tab{}}', '@media print {\n\t.tab {}\n}')
        t('@media print {.tab,.bat{}}', '@media print {\n\t.tab, .bat {}\n}')
        t('#bla, #foo{color:black}', '#bla, #foo {\n\tcolor: black\n}')
        t('a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}', 'a:first-child, a:first-child {\n\tcolor: red;\n\tdiv:first-child, div:hover {\n\t\tcolor: black;\n\t}\n}')

        # Selector Separator - (separator = "\n", separator1 = "\n\t")
        self.options.selector_separator_newline = true
        self.options.selector_separator = " "
        t('#bla, #foo{color:green}', '#bla,\n#foo {\n\tcolor: green\n}')
        t('@media print {.tab{}}', '@media print {\n\t.tab {}\n}')
        t('@media print {.tab,.bat{}}', '@media print {\n\t.tab,\n\t.bat {}\n}')
        t('#bla, #foo{color:black}', '#bla,\n#foo {\n\tcolor: black\n}')
        t('a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}', 'a:first-child,\na:first-child {\n\tcolor: red;\n\tdiv:first-child,\n\tdiv:hover {\n\t\tcolor: black;\n\t}\n}')

        # Selector Separator - (separator = "\n", separator1 = "\n\t")
        self.options.selector_separator_newline = true
        self.options.selector_separator = "  "
        t('#bla, #foo{color:green}', '#bla,\n#foo {\n\tcolor: green\n}')
        t('@media print {.tab{}}', '@media print {\n\t.tab {}\n}')
        t('@media print {.tab,.bat{}}', '@media print {\n\t.tab,\n\t.bat {}\n}')
        t('#bla, #foo{color:black}', '#bla,\n#foo {\n\tcolor: black\n}')
        t('a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}', 'a:first-child,\na:first-child {\n\tcolor: red;\n\tdiv:first-child,\n\tdiv:hover {\n\t\tcolor: black;\n\t}\n}')

        # Newline Between Rules - (separator = "\n")
        self.options.newline_between_rules = true
        t('.div {}\n.span {}', '.div {}\n\n.span {}')
        t('.div{}\n   \n.span{}', '.div {}\n\n.span {}')
        t('.div {}    \n  \n.span { } \n', '.div {}\n\n.span {}')
        t('.div {\n    \n} \n  .span {\n }  ', '.div {}\n\n.span {}')
        t('.selector1 {\n\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n.div{height:15px;}', '.selector1 {\n\tmargin: 0;\n\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n\n.div {\n\theight: 15px;\n}')
        t('.tabs{width:10px;//end of line comment\nheight:10px;//another\n}\n.div{height:15px;}', '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px; //another\n}\n\n.div {\n\theight: 15px;\n}')
        t('#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', '#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n\n.div {\n\theight: 15px;\n}')
        t('@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', '@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n\n.div {\n\theight: 15px;\n}')
        t('@font-face {\n\tfont-family: "Bitstream Vera Serif Bold";\n\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: "Helvetica Neue"\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}', '@font-face {\n\tfont-family: "Bitstream Vera Serif Bold";\n\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n\n@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: "Helvetica Neue"\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}')
        t('a:first-child{color:red;div:first-child{color:black;}}\n.div{height:15px;}', 'a:first-child {\n\tcolor: red;\n\tdiv:first-child {\n\t\tcolor: black;\n\t}\n}\n\n.div {\n\theight: 15px;\n}')
        t('a:first-child{color:red;div:not(.peq){color:black;}}\n.div{height:15px;}', 'a:first-child {\n\tcolor: red;\n\tdiv:not(.peq) {\n\t\tcolor: black;\n\t}\n}\n\n.div {\n\theight: 15px;\n}')

        # Newline Between Rules - (separator = "")
        self.options.newline_between_rules = false
        t('.div {}\n.span {}')
        t('.div{}\n   \n.span{}', '.div {}\n.span {}')
        t('.div {}    \n  \n.span { } \n', '.div {}\n.span {}')
        t('.div {\n    \n} \n  .span {\n }  ', '.div {}\n.span {}')
        t('.selector1 {\n\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n.div{height:15px;}', '.selector1 {\n\tmargin: 0;\n\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n.div {\n\theight: 15px;\n}')
        t('.tabs{width:10px;//end of line comment\nheight:10px;//another\n}\n.div{height:15px;}', '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px; //another\n}\n.div {\n\theight: 15px;\n}')
        t('#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', '#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div {\n\theight: 15px;\n}')
        t('@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', '@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div {\n\theight: 15px;\n}')
        t('@font-face {\n\tfont-family: "Bitstream Vera Serif Bold";\n\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: "Helvetica Neue"\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}')
        t('a:first-child{color:red;div:first-child{color:black;}}\n.div{height:15px;}', 'a:first-child {\n\tcolor: red;\n\tdiv:first-child {\n\t\tcolor: black;\n\t}\n}\n.div {\n\theight: 15px;\n}')
        t('a:first-child{color:red;div:not(.peq){color:black;}}\n.div{height:15px;}', 'a:first-child {\n\tcolor: red;\n\tdiv:not(.peq) {\n\t\tcolor: black;\n\t}\n}\n.div {\n\theight: 15px;\n}')

        # Functions braces
        t('.tabs(){}', '.tabs() {}')
        t('.tabs (){}', '.tabs () {}')
        t('.tabs (pa, pa(1,2)), .cols { }', '.tabs (pa, pa(1, 2)),\n.cols {}')
        t('.tabs(pa, pa(1,2)), .cols { }', '.tabs(pa, pa(1, 2)),\n.cols {}')
        t('.tabs (   )   {    }', '.tabs () {}')
        t('.tabs(   )   {    }', '.tabs() {}')
        t('.tabs  (t, t2)  \n{\n  key: val(p1  ,p2);  \n  }', '.tabs (t, t2) {\n\tkey: val(p1, p2);\n}')
        t('.box-shadow(@shadow: 0 1px 3px rgba(0, 0, 0, .25)) {\n\t-webkit-box-shadow: @shadow;\n\t-moz-box-shadow: @shadow;\n\tbox-shadow: @shadow;\n}')

        # Comments
        t('/* test */')
        t('.tabs{/* test */}', '.tabs {\n\t/* test */\n}')
        t('.tabs{/* test */}', '.tabs {\n\t/* test */\n}')
        t('/* header */.tabs {}', '/* header */\n\n.tabs {}')
        t('.tabs {\n/* non-header */\nwidth:10px;}', '.tabs {\n\t/* non-header */\n\twidth: 10px;\n}')
        t('/* header')
        t('// comment')
        t('.selector1 {\n\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}', '.selector1 {\n\tmargin: 0;\n\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n}')
        
        # single line comment support (less/sass)
        t('.tabs{\n// comment\nwidth:10px;\n}', '.tabs {\n\t// comment\n\twidth: 10px;\n}')
        t('.tabs{// comment\nwidth:10px;\n}', '.tabs {\n\t// comment\n\twidth: 10px;\n}')
        t('//comment\n.tabs{width:10px;}', '//comment\n.tabs {\n\twidth: 10px;\n}')
        t('.tabs{//comment\n//2nd single line comment\nwidth:10px;}', '.tabs {\n\t//comment\n\t//2nd single line comment\n\twidth: 10px;\n}')
        t('.tabs{width:10px;//end of line comment\n}', '.tabs {\n\twidth: 10px; //end of line comment\n}')
        t('.tabs{width:10px;//end of line comment\nheight:10px;}', '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px;\n}')
        t('.tabs{width:10px;//end of line comment\nheight:10px;//another\n}', '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px; //another\n}')

        # Psuedo-classes vs Variables
        t('@page :first {}')
        
        # Assume the colon goes with the @name. If we're in LESS, this is required regardless of the at-string.
        t('@page:first {}', '@page: first {}')
        t('@page: first {}')

        # SASS/SCSS
        
        # Basic Interpolation
        t('p {\n\t$font-size: 12px;\n\t$line-height: 30px;\n\tfont: #{$font-size}/#{$line-height};\n}')
        t('p.#{$name} {}')
        t(
            '@mixin itemPropertiesCoverItem($items, $margin) {\n' +
            '\twidth: calc((100% - ((#{$items} - 1) * #{$margin}rem)) / #{$items});\n' +
            '\tmargin: 1.6rem #{$margin}rem 1.6rem 0;\n' +
            '}')

        # 


    def testNewline(self):
        self.resetOptions()
        t = self.decodesto

        self.options.end_with_newline = True
        t("", "\n")
        t("\n", "\n")
        t(".tabs{}\n", ".tabs {}\n")
        t(".tabs{}", ".tabs {}\n")

    def testBasics(self):
        self.resetOptions()
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
        self.resetOptions()
        t = self.decodesto

        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}")
        t("a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")


    def testBlockNesting(self):
        self.resetOptions()
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
        self.resetOptions()
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
        self.resetOptions()
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
        input = input.replace('\n', '\r\n')
        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), expectation)
        self.options.eol = '\n'

if __name__ == '__main__':
    unittest.main()
