import unittest
import cssbeautifier


class CSSBeautifierTest(unittest.TestCase):

    def resetOptions(self):
      self.options = cssbeautifier.default_options()
      self.options.indent_size = 1
      self.options.indent_char = '\t'
      self.options.selector_separator_newline = True
      self.options.end_with_newline = False

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

        # may not eat the space before "["
        t('html.js [data-custom="123"] {\n\topacity: 1.00;\n}')
        t('html.js *[data-custom="123"] {\n\topacity: 1.00;\n}')

        # lead-in whitespace determines base-indent.
        # lead-in newlines are stripped.
        t("\n\na, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")
        t("   a, img {padding: 0.2px}", "   a,\n   img {\n   \tpadding: 0.2px\n   }")
        t(" \t \na, img {padding: 0.2px}", " \t a,\n \t img {\n \t \tpadding: 0.2px\n \t }")
        t("\n\n     a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}")


    def testComments(self):
        self.resetOptions()
        t = self.decodesto

        t("/* test */", "/* test */")
        t(".tabs{/* test */}", ".tabs {\n\t/* test */\n}")
        t("/* header */.tabs {}", "/* header */\n\n.tabs {}")

        #single line comment support (less/sass)
        t(".tabs{\n// comment\nwidth:10px;\n}", ".tabs {\n\t// comment\n\twidth: 10px;\n}")
        t(".tabs{// comment\nwidth:10px;\n}", ".tabs {\n\t// comment\n\twidth: 10px;\n}")
        t("//comment\n.tabs{width:10px;}", "//comment\n.tabs {\n\twidth: 10px;\n}")
        t(".tabs{//comment\n//2nd single line comment\nwidth:10px;}", ".tabs {\n\t//comment\n\t//2nd single line comment\n\twidth: 10px;\n}")
        t(".tabs{width:10px;//end of line comment\n}", ".tabs {\n\twidth: 10px;//end of line comment\n}")
        t(".tabs{width:10px;//end of line comment\nheight:10px;}", ".tabs {\n\twidth: 10px;//end of line comment\n\theight: 10px;\n}")
        t(".tabs{width:10px;//end of line comment\nheight:10px;//another\n}", ".tabs {\n\twidth: 10px;//end of line comment\n\theight: 10px;//another\n}")


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

        t("#bla, #foo{color:green}", "#bla, #foo {\n  color: green\n}")
        t("@media print {.tab{}}", "@media print {\n  .tab {}\n}")
        t("@media print {.tab,.bat{}}", "@media print {\n  .tab, .bat {}\n}")
        t("#bla, #foo{color:black}", "#bla, #foo {\n  color: black\n}")

        # pseudo-classes and pseudo-elements
        t("#foo:hover {\n  background-image: url(foo@2x.png)\n}")
        t("#foo *:hover {\n  color: purple\n}")
        t("::selection {\n  color: #ff0000;\n}")

        # TODO: don't break nested pseduo-classes
        t("@media screen {.tab,.bat:hover {color:red}}", "@media screen {\n  .tab, .bat:hover {\n    color: red\n  }\n}")

        # particular edge case with braces and semicolons inside tags that allows custom text
        t(  "a:not(\"foobar\\\";{}omg\"){\ncontent: 'example\\';{} text';\ncontent: \"example\\\";{} text\";}",
            "a:not(\"foobar\\\";{}omg\") {\n  content: 'example\\';{} text';\n  content: \"example\\\";{} text\";\n}")

    def decodesto(self, input, expectation=None):
        if expectation == None:
            expectation = input

        self.assertMultiLineEqual(
            cssbeautifier.beautify(input, self.options), expectation)

        # if the expected is different from input, run it again
        # expected output should be unchanged when run twice.
        if not expectation == None:
            self.assertMultiLineEqual(
                cssbeautifier.beautify(expectation, self.options), expectation)
                
if __name__ == '__main__':
    unittest.main()
