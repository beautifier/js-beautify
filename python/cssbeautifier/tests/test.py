import unittest
import cssbeautifier


class CSSBeautifierTest(unittest.TestCase):

    options = cssbeautifier.default_options()
    options.indent_size = 1
    options.indent_char = '\t'
    options.end_with_newline = True

    def testBasics(self):
        t = self.decodesto

        t("", "\n")
        t(".tabs{}", ".tabs {}\n")
        t(".tabs{color:red}", ".tabs {\n\tcolor: red\n}\n")
        t(".tabs{background:url('back.jpg')}", ".tabs {\n\tbackground: url('back.jpg')\n}\n")
        t("#bla, #foo{color:red}", "#bla, #foo {\n\tcolor: red\n}\n")
        t("@media print {.tab{}}", "@media print {\n\t.tab {}\n}\n")


    def testComments(self):
        t = self.decodesto

        t("/* test */", "/* test */\n")
        t(".tabs{/* test */}", ".tabs {\n\t/* test */\n}\n")
        t("/* header */.tabs {}", "/* header */\n.tabs {}\n")

    def testLeadingZero(self):
        t = self.decodesto

        t(".tabs{opacity: 0.9}", ".tabs {\n\topacity: .9\n}\n")
        t(".tabs{opacity:0.9}", ".tabs {\n\topacity: .9\n}\n")
        t(".tabs{padding: 10.3px}", ".tabs {\n\tpadding: 10.3px\n}\n")


    def testSpaceIndent(self):
        t = self.decodesto

        self.options.indent_size = 2
        self.options.indent_char = ' '

        t("#bla, #foo{color:red}", "#bla, #foo {\n  color: red\n}\n")
        t("@media print {.tab{}}", "@media print {\n  .tab {}\n}\n")

    def decodesto(self, input, expectation=None):
        self.assertEqual(
            cssbeautifier.beautify(input, self.options), expectation or input)

if __name__ == '__main__':
    unittest.main()
