import jsbeautifier
import json
import unittest


class TestWrapLineLength(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_wrap_line_does_not_create_invalid_json(self):
        options = jsbeautifier.default_options()
        options.indent_size = 4
        options.brace_style = "expand"
        options.wrap_line_length = 40
        obj = {
            "1234567891234567891234567891234": -4
        }
        # make sure exception is not raised due to bad json (line break after -):
        # {
        #   "1234567891234567891234567891234": -
        #   4
        # }
        # json.decoder.JSONDecodeError: Expecting value: line 2 column 40 (char 41)
        json.loads(jsbeautifier.beautify(json.dumps(obj), options))
