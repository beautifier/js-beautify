from __future__ import print_function
import sys
import os
import platform
import io
import getopt
import re
import string
import errno
import copy
import glob
from jsbeautifier.__version__ import __version__
from jsbeautifier.cli import *
from jsbeautifier.javascript.options import BeautifierOptions
from jsbeautifier.javascript.beautifier import Beautifier

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
#
# Originally written by Einar Lielmanis et al.,
# Conversion to python by Einar Lielmanis, einar@beautifier.io,
# Parsing improvement for brace-less and semicolon-less statements
#    by Liam Newman <bitwiseman@beautifier.io>
# Python is not my native language, feel free to push things around.
#
# Use either from command line (script displays its usage when run
# without any parameters),
#
#
# or, alternatively, use it as a module:
#
#   import jsbeautifier
#   res = jsbeautifier.beautify('your javascript string')
#   res = jsbeautifier.beautify_file('some_file.js')
#
#  you may specify some options:
#
#   opts = jsbeautifier.default_options()
#   opts.indent_size = 2
#   res = jsbeautifier.beautify('some javascript', opts)
#
#
# Here are the available options: (read source)

__all__ = [
    "default_options",
    "beautify",
    "beautify_file",
    "usage",
    "main",
]


def default_options():
    return BeautifierOptions()


def beautify(string, opts=default_options()):
    b = Beautifier()
    return b.beautify(string, opts)


def beautify_file(file_name, opts=default_options()):
    return process_file(file_name, opts, beautify)


def usage(stream=sys.stdout):

    print(
        "jsbeautifier.py@"
        + __version__
        + """

Javascript beautifier (https://beautifier.io/)

Usage: jsbeautifier.py [options] <infile>

    <infile> can be "-", which means stdin.

Input options:

 -i,  --stdin                      Read input from stdin

Output options:

 -s,  --indent-size=NUMBER         Indentation size. (default 4).
 -c,  --indent-char=CHAR           Character to indent with. (default space).
 -e,  --eol=STRING                 Character(s) to use as line terminators.
                                   (default first newline in file, otherwise "\\n")
 -t,  --indent-with-tabs           Indent with tabs, overrides -s and -c
 -d,  --disable-preserve-newlines  Do not preserve existing line breaks.
 -P,  --space-in-paren             Add padding spaces within paren, ie. f( a, b )
 -E,  --space-in-empty-paren       Add a single space inside empty paren, ie. f( )
 -j,  --jslint-happy               More jslint-compatible output
 -a,  --space-after-anon-function  Add a space before an anonymous function's parens, ie. function ()
 --space-after-named-function      Add a space before a named function's parens, i.e. function example ()
 -b,  --brace-style=collapse       Brace style (collapse, expand, end-expand, none)(,preserve-inline)
 -k,  --keep-array-indentation     Keep array indentation.
 --quiet                           Suppress info about a file if nothing was changed.
 -r,  --replace                    Write output in-place, replacing input
 -o,  --outfile=FILE               Specify a file to output to (default stdout)
 -f,  --keep-function-indentation  Do not re-indent function bodies defined in var lines.
 -x,  --unescape-strings           Decode printable chars encoded in \\xNN notation.
 -X,  --e4x                        Pass E4X xml literals through untouched
 -C,  --comma-first                Put commas at the beginning of new line instead of end.
 -m,
 --max-preserve-newlines=NUMBER    Number of line-breaks to be preserved in one chunk (default 10)
 -O,  --operator-position=STRING   Set operator position (before-newline, after-newline, preserve-newline)
 -w,  --wrap-line-length           Attempt to wrap line when it exceeds this length.
                                   NOTE: Line continues until next wrap point is found.
 -n,  --end-with-newline           End output with newline
 --indent-empty-lines              Keep indentation on empty lines
 --templating                      List of templating languages (auto,none,django,erb,handlebars,php,smarty) ["auto"] auto = none in JavaScript, all in html
 --editorconfig                    Enable setting configuration from EditorConfig

Rarely needed options:

 --eval-code                       evaluate code if a JS interpreter is
                                   installed. May be useful with some obfuscated
                                   script but poses a potential security issue.

 -l,  --indent-level=NUMBER        Initial indentation level. (default 0).

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
            "f:s:c:e:o:rdEPjab:kil:xhtvXnCO:w:m:",
            [
                "brace-style=",
                "comma-first",
                "disable-preserve-newlines",
                "e4x",
                "editorconfig",
                "end-with-newline",
                "eol=",
                "eval-code",
                "file=",
                "help",
                "indent-char=",
                "indent-empty-lines",
                "indent-level=",
                "indent-size=",
                "indent-with-tabs",
                "jslint-happy",
                "keep-array-indentation",
                "keep-function-indentation",
                "max-preserve-newlines=",
                "operator-position=",
                "outfile=",
                "quiet",
                "replace",
                "space-after-anon-function",
                "space-after-named-function",
                "space-in-empty-paren",
                "space-in-paren",
                "stdin",
                "templating",
                "unescape-strings",
                "usage",
                "version",
                "wrap-line-length",
            ],
        )
    except getopt.GetoptError as ex:
        print(ex, file=sys.stderr)
        return usage(sys.stderr)

    js_options = default_options()

    filepath_params = []
    filepath_params.extend(args)

    outfile_param = "stdout"
    replace = False

    for opt, arg in opts:
        if opt in ("--file", "-f"):
            filepath_params.append(arg)
        elif opt in ("--keep-array-indentation", "-k"):
            js_options.keep_array_indentation = True
        elif opt in ("--keep-function-indentation",):
            js_options.keep_function_indentation = True
        elif opt in ("--outfile", "-o"):
            outfile_param = arg
        elif opt in ("--replace", "-r"):
            replace = True
        elif opt in ("--indent-size", "-s"):
            js_options.indent_size = int(arg)
        elif opt in ("--indent-char", "-c"):
            js_options.indent_char = arg
        elif opt in ("--eol", "-e"):
            js_options.eol = arg
        elif opt in ("--indent-with-tabs", "-t"):
            js_options.indent_with_tabs = True
        elif opt in ("--disable-preserve-newlines", "-d"):
            js_options.preserve_newlines = False
        elif opt in ("--max-preserve-newlines", "-m"):
            js_options.max_preserve_newlines = int(arg)
        elif opt in ("--space-in-paren", "-P"):
            js_options.space_in_paren = True
        elif opt in ("--space-in-empty-paren", "-E"):
            js_options.space_in_empty_paren = True
        elif opt in ("--jslint-happy", "-j"):
            js_options.jslint_happy = True
        elif opt in ("--space-after-anon-function", "-a"):
            js_options.space_after_anon_function = True
        elif opt in ("--space-after-named-function",):
            js_options.space_after_named_function = True
        elif opt in ("--eval-code",):
            js_options.eval_code = True
        elif opt in ("--quiet",):
            js_options.keep_quiet = True
        elif opt in ("--brace-style", "-b"):
            js_options.brace_style = arg
        elif opt in ("--unescape-strings", "-x"):
            js_options.unescape_strings = True
        elif opt in ("--e4x", "-X"):
            js_options.e4x = True
        elif opt in ("--end-with-newline", "-n"):
            js_options.end_with_newline = True
        elif opt in ("--comma-first", "-C"):
            js_options.comma_first = True
        elif opt in ("--operator-position", "-O"):
            js_options.operator_position = arg
        elif opt in ("--wrap-line-length ", "-w"):
            js_options.wrap_line_length = int(arg)
        elif opt in ("--indent-empty-lines",):
            js_options.indent_empty_lines = True
        elif opt in ("--templating",):
            js_options.templating = arg.split(",")
        elif opt in ("--stdin", "-i"):
            # stdin is the default if no files are passed
            filepath_params = []
        elif opt in ("--editorconfig",):
            js_options.editorconfig = True
        elif opt in ("--version", "-v"):
            return print(__version__)
        elif opt in ("--help", "--usage", "-h"):
            return usage()

    try:
        filepaths, replace = get_filepaths_from_params(filepath_params, replace)
        for filepath in filepaths:
            if not replace:
                outfile = outfile_param
            else:
                outfile = filepath

            js_options = integrate_editorconfig_options(
                filepath, js_options, outfile, "js"
            )

            pretty = beautify_file(filepath, js_options)

            write_beautified_output(pretty, js_options, outfile)

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


if __name__ == "__main__":
    main()
