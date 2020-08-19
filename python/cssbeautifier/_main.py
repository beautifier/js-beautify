#
# The MIT License (MIT)

# Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
import sys
import os
import io
import re
import copy
import getopt
from cssbeautifier.__version__ import __version__
from jsbeautifier.cli import *
from cssbeautifier.css.options import BeautifierOptions
from cssbeautifier.css.beautifier import Beautifier

__all__ = ["default_options", "beautify", "beautify_file", "usage", "main"]


def default_options():
    return BeautifierOptions()


def beautify(string, opts=None):
    b = Beautifier(string, opts)
    return b.beautify()


def beautify_file(file_name, opts=None):
    return process_file(file_name, opts, beautify)


def usage(stream=sys.stdout):

    print(
        "cssbeautifier.py@"
        + __version__
        + """

CSS beautifier (https://beautifier.io/)

Usage: cssbeautifier.py [options] <infile>

    <infile> can be "-", which means stdin.

Input options:

 -i,  --stdin                      Read input from stdin

Output options:

 -s,  --indent-size=NUMBER         Indentation size. (default 4).
 -c,  --indent-char=CHAR           Character to indent with. (default space).
 -e,  --eol=STRING                 Character(s) to use as line terminators.
                                   (default first newline in file, otherwise "\\n")
 -t,  --indent-with-tabs           Indent with tabs, overrides -s and -c
      --preserve-newlines          Preserve existing line breaks.
      --disable-selector-separator-newline
                                   Do not print each selector on a separate line.
 -b,  --brace-style=collapse       Brace style (collapse, expand)
 -n,  --end-with-newline           End output with newline
      --disable-newline-between-rules
                                   Do not print empty line between rules.
      --space-around-combinator    Print spaces around combinator.
      --indent-empty-lines         Keep indentation on empty lines
 -r,  --replace                    Write output in-place, replacing input
 -o,  --outfile=FILE               Specify a file to output to (default stdout)

Rarely needed options:

 -h,  --help, --usage              Prints this help statement.
 -v,  --version                    Show the version

""",
        file=stream,
    )
    if stream == sys.stderr:
        return 1
    else:
        return 0


def main():

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(
            argv,
            "hvio:rs:c:e:tnb:",
            [
                "editorconfig",
                "help",
                "usage",
                "version",
                "stdin",
                "outfile=",
                "replace",
                "indent-size=",
                "indent-char=",
                "eol=",
                "indent-with-tabs",
                "preserve-newlines",
                "brace-style=",
                "disable-selector-separator-newline",
                "end-with-newline",
                "disable-newline-between-rules",
                "space-around-combinator",
                "indent-empty-lines",
            ],
        )
    except getopt.GetoptError as ex:
        print(ex, file=sys.stderr)
        return usage(sys.stderr)

    css_options = default_options()

    filepath_params = []
    filepath_params.extend(args)

    outfile_param = "stdout"
    replace = False

    for opt, arg in opts:
        if opt in ("--stdin", "-i"):
            file = "-"
        elif opt in ("--outfile", "-o"):
            outfile = arg
        elif opt in ("--replace", "-r"):
            replace = True
        elif opt in ("--version", "-v"):
            return print(__version__)
        elif opt in ("--help", "--usage", "-h"):
            return usage()

        elif opt in ("--indent-size", "-s"):
            css_options.indent_size = int(arg)
        elif opt in ("--indent-char", "-c"):
            css_options.indent_char = arg
        elif opt in ("--eol", "-e"):
            css_options.eol = arg
        elif opt in ("--indent-with-tabs", "-t"):
            css_options.indent_with_tabs = True
        elif opt in ("--preserve-newlines"):
            css_options.preserve_newlines = True
        elif opt in ("--disable-selector-separator-newline"):
            css_options.selector_separator_newline = False
        elif opt in ("--brace-style", "-b"):
            css_options.brace_style = arg
        elif opt in ("--end-with-newline", "-n"):
            css_options.end_with_newline = True
        elif opt in ("--disable-newline-between-rules"):
            css_options.newline_between_rules = False
        elif opt in ("--space-around-combinator"):
            css_options.space_around_combinator = True
        elif opt in ("--indent-empty-lines"):
            css_options.indent_empty_lines = True
        elif opt in ("--editorconfig"):
            css_options.editorconfig = True

    try:
        filepaths, replace = get_filepaths_from_params(filepath_params, replace)
        for filepath in filepaths:
            if not replace:
                outfile = outfile_param
            else:
                outfile = filepath

            css_options = integrate_editorconfig_options(
                filepath, css_options, outfile, "js"
            )

            pretty = beautify_file(filepath, css_options)

            write_beautified_output(pretty, css_options, outfile)

    except MissingInputStreamError:
        print("Must pipe input or define at least one file.\n", file=sys.stderr)
        usage(sys.stderr)
        return 1

    except UnicodeError as ex:
        print("Error while decoding input or encoding output:", file=sys.stderr)
        print(ex, file=sys.stderr)
        return 1

    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

    # Success
    return 0
