import unittest
from types import SimpleNamespace

from ...core.output import Output


def make_output(**overrides):
    options = SimpleNamespace(
        indent_size=4,
        indent_char=" ",
        indent_with_tabs=False,
        indent_level=0,
        end_with_newline=False,
        wrap_line_length=0,
        indent_empty_lines=False,
    )

    for key, value in overrides.items():
        setattr(options, key, value)

    return Output(options)


class TestOutput(unittest.TestCase):
    def test_ensure_empty_line_above_inserts_blank_line(self):
        output = make_output()

        output.add_token("alpha")
        output.add_new_line()
        output.add_token("beta")
        output.add_new_line()
        output.add_token("gamma")

        output.ensure_empty_line_above("skip", "end")

        self.assertEqual(output.get_code("\n"), "alpha\nbeta\n\ngamma")

    def test_ensure_empty_line_above_skips_matching_prefix(self):
        output = make_output()

        output.add_token("skip-this")
        output.add_new_line()
        output.add_token("gamma")

        output.ensure_empty_line_above("skip", "end")

        self.assertEqual(output.get_code("\n"), "skip-this\ngamma")

    def test_ensure_empty_line_above_skips_matching_suffix(self):
        output = make_output()

        output.add_token("end")
        output.add_new_line()
        output.add_token("gamma")

        output.ensure_empty_line_above("skip", "end")

        self.assertEqual(output.get_code("\n"), "end\ngamma")


if __name__ == "__main__":
    unittest.main()
