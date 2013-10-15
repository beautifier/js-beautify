import unittest
import cssbeautifier


class CSSBeautifierTest(unittest.TestCase):

    def resetOptions(self):
      self.options = cssbeautifier.default_options()
      self.options.indent_size = 1
      self.options.indent_char = '\t'
      self.options.selector_separator = '\n'
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

        t("/* test */", "/* test */\n")
        t(".tabs{/* test */}", ".tabs {\n\t/* test */\n}\n")
        t("/* header */.tabs {}", "/* header */\n.tabs {}\n")


    def testSeperateSelectors(self):
        self.resetOptions()
        t = self.decodesto

        t("#bla, #foo{color:red}", "#bla,\n#foo {\n\tcolor: red\n}\n")
        t("a, img {padding: 0.2px}", "a,\nimg {\n\tpadding: 0.2px\n}\n")


    def testOptions(self):
        self.resetOptions()
        self.options.indent_size = 2
        self.options.indent_char = ' '
        self.options.selector_separator = ' '
        t = self.decodesto

        t("#bla, #foo{color:green}", "#bla, #foo {\n  color: green\n}\n")
        t("@media print {.tab{}}", "@media print {\n  .tab {}\n}\n")
        t("#bla, #foo{color:black}", "#bla, #foo {\n  color: black\n}\n")

    def decodesto(self, input, expectation=None):
        self.assertEqual(
            cssbeautifier.beautify(input, self.options), expectation or input)

if __name__ == '__main__':
    unittest.main()
