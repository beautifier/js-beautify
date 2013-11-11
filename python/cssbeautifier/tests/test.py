import unittest
import cssbeautifier


class CSSBeautifierTest(unittest.TestCase):

    def resetOptions(self):
      self.options = cssbeautifier.default_options()
      self.options.indent_size = 1
      self.options.indent_char = '\t'
      self.options.selector_separator_newline = True
      self.options.end_with_newline = True

    def testBasics(self):
        self.resetOptions()
        t = self.decodesto

        t("", "\n")
        t(".tabs{}", ".tabs {}\n")
        t(".tabs{color:red}", ".tabs {\n\tcolor: red\n}\n")
        t(".tabs{color:rgb(255, 255, 0)}", ".tabs {\n\tcolor: rgb(255, 255, 0)\n}\n")
        t(".tabs{background:url('back.jpg')}", ".tabs {\n\tbackground: url('back.jpg')\n}\n")
        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}\n")
        t("@media print {.tab{}}", "@media print {\n\t.tab {}\n}\n")


    def testComments(self):
        self.resetOptions()
        t = self.decodesto

        t("/* test */", "/* test */\n\n")
        t(".tabs{/* test */}", ".tabs {\n\t/* test */\n}\n")
        t("/* header */.tabs {}", "/* header */\n\n.tabs {}\n")

        #single line comment support (less/sass)
        t(".tabs{\n// comment\nwidth:10px;\n}", ".tabs {\n\t// comment\n\twidth: 10px;\n}\n")
        t(".tabs{// comment\nwidth:10px;\n}", ".tabs {\n\t// comment\n\twidth: 10px;\n}\n")
        t("//comment\n.tabs{width:10px;}", "//comment\n.tabs {\n\twidth: 10px;\n}\n")
        t(".tabs{//comment\n//2nd single line comment\nwidth:10px;}", ".tabs {\n\t//comment\n\t//2nd single line comment\n\twidth: 10px;\n}\n")
        t(".tabs{width:10px;//end of line comment\n}", ".tabs {\n\twidth: 10px;//end of line comment\n}\n")
        t(".tabs{width:10px;//end of line comment\nheight:10px;}", ".tabs {\n\twidth: 10px;//end of line comment\n\theight: 10px;\n}\n")
        t(".tabs{width:10px;//end of line comment\nheight:10px;//another\n}", ".tabs {\n\twidth: 10px;//end of line comment\n\theight: 10px;//another\n}\n")


    def testSeperateSelectors(self):
        self.resetOptions()
        t = self.decodesto

        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}\n")
        t("a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}\n")


    def testOptions(self):
        self.resetOptions()
        self.options.indent_size = 2
        self.options.indent_char = ' '
        self.options.selector_separator_newline = False
        t = self.decodesto

        t("#bla, #foo{color:green}", "#bla, #foo {\n  color: green\n}\n")
        t("@media print {.tab{}}", "@media print {\n  .tab {}\n}\n")
        t("#bla, #foo{color:black}", "#bla, #foo {\n  color: black\n}\n")

    def decodesto(self, input, expectation=None):
        self.assertEqual(
            cssbeautifier.beautify(input, self.options), expectation or input)

if __name__ == '__main__':
    unittest.main()
