from __future__ import print_function
import sys
import os
import io
import getopt
import re
import string
import errno
import copy
from jsbeautifier.__version__ import __version__
from jsbeautifier.javascript.options import BeautifierOptions
from jsbeautifier.javascript.beautifier import Beautifier

#
# The MIT License (MIT)

# Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

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
# Conversion to python by Einar Lielmanis, einar@jsbeautifier.org,
# Parsing improvement for brace-less and semicolon-less statements
#    by Liam Newman <bitwiseman@gmail.com>
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


def default_options():
    return BeautifierOptions()


def beautify(string, opts = default_options() ):
    b = Beautifier()
    return b.beautify(string, opts)

def set_file_editorconfig_opts(filename, js_options):
    from editorconfig import get_properties, EditorConfigError
    try:
        _ecoptions = get_properties(os.path.abspath(filename))

        if _ecoptions.get("indent_style") == "tab":
            js_options.indent_with_tabs = True
        elif _ecoptions.get("indent_style") == "space":
            js_options.indent_with_tabs = False

        if _ecoptions.get("indent_size"):
            js_options.indent_size = int(_ecoptions["indent_size"])

        if _ecoptions.get("max_line_length"):
            if _ecoptions.get("max_line_length") == "off":
                js_options.wrap_line_length = 0
            else:
                js_options.wrap_line_length = int(_ecoptions["max_line_length"])

        if _ecoptions.get("insert_final_newline") == 'true':
            js_options.end_with_newline = True
        elif _ecoptions.get("insert_final_newline") == 'false':
            js_options.end_with_newline = False

        if _ecoptions.get("end_of_line"):
            if _ecoptions["end_of_line"] == "cr":
                js_options.eol = '\r'
            elif _ecoptions["end_of_line"] == "lf":
                js_options.eol = '\n'
            elif _ecoptions["end_of_line"] == "crlf":
                js_options.eol = '\r\n'

    except EditorConfigError as ex:
        # do not error on bad editor config
        print("Error loading EditorConfig.  Ignoring.", file=sys.stderr)


def beautify_file(file_name, opts = default_options() ):
    input_string = ''
    if file_name == '-': # stdin
        try:
            if sys.stdin.isatty():
                raise Exception()

            stream = sys.stdin
            input_string = ''.join(stream.readlines())
        except Exception as ex:
            print("Must pipe input or define at least one file.", file=sys.stderr)
            usage(sys.stderr)
            raise Exception()
    else:
        stream = io.open(file_name, 'rt', newline='')
        input_string = ''.join(stream.readlines())

    return beautify(input_string, opts)


def usage(stream=sys.stdout):

    print("jsbeautifier.py@" + __version__ + """

Javascript beautifier (http://jsbeautifier.org/)

Usage: jsbeautifier.py [options] <infile>

    <infile> can be "-", which means stdin.
    <outfile> defaults to stdout

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
 -a,  --space_after_anon_function  Add a space before an anonymous function's parens, ie. function ()
 -b,  --brace-style=collapse       Brace style (collapse, expand, end-expand, none)(,preserve-inline)
 -k,  --keep-array-indentation     Keep array indentation.
 -r,  --replace                    Write output in-place, replacing input
 -o,  --outfile=FILE               Specify a file to output to (default stdout)
 -f,  --keep-function-indentation  Do not re-indent function bodies defined in var lines.
 -x,  --unescape-strings           Decode printable chars encoded in \\xNN notation.
 -X,  --e4x                        Pass E4X xml literals through untouched
 -w,  --wrap-line-length                   Attempt to wrap line when it exceeds this length.
                                   NOTE: Line continues until next wrap point is found.
 -n, --end_with_newline            End output with newline
 --editorconfig                    Enable setting configuration from EditorConfig

Rarely needed options:

 --eval-code                       evaluate code if a JS interpreter is
                                   installed. May be useful with some obfuscated
                                   script but poses a potential security issue.

 -l,  --indent-level=NUMBER        Initial indentation level. (default 0).

 -h,  --help, --usage              Prints this help statement.
 -v, --version                     Show the version

""", file=stream)
    if stream == sys.stderr:
        return 1
    else:
        return 0


def mkdir_p(path):
    try:
        if path:
            os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise Exception()




def isFileDifferent(filepath, expected):
    try:
        return (''.join(io.open(filepath, 'rt', newline='').readlines()) != expected)
    except:
        return True


def main():

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:c:e:o:rdEPjabkil:xhtfvXnCO:w:",
            ['indent-size=','indent-char=','eol=''outfile=', 'replace', 'disable-preserve-newlines',
            'space-in-paren', 'space-in-empty-paren', 'jslint-happy', 'space-after-anon-function',
            'brace-style=', 'keep-array-indentation', 'indent-level=', 'unescape-strings',
            'help', 'usage', 'stdin', 'eval-code', 'indent-with-tabs', 'keep-function-indentation', 'version',
            'e4x', 'end-with-newline','comma-first','operator-position=','wrap-line-length','editorconfig'])
    except getopt.GetoptError as ex:
        print(ex, file=sys.stderr)
        return usage(sys.stderr)

    js_options = default_options()

    file = None
    outfile = 'stdout'
    replace = False
    if len(args) == 1:
        file = args[0]

    for opt, arg in opts:
        if opt in ('--keep-array-indentation', '-k'):
            js_options.keep_array_indentation = True
        if opt in ('--keep-function-indentation','-f'):
            js_options.keep_function_indentation = True
        elif opt in ('--outfile', '-o'):
            outfile = arg
        elif opt in ('--replace', '-r'):
            replace = True
        elif opt in ('--indent-size', '-s'):
            js_options.indent_size = int(arg)
        elif opt in ('--indent-char', '-c'):
            js_options.indent_char = arg
        elif opt in ('--eol', '-e'):
            js_options.eol = arg
        elif opt in ('--indent-with-tabs', '-t'):
            js_options.indent_with_tabs = True
        elif opt in ('--disable-preserve-newlines', '-d'):
            js_options.preserve_newlines = False
        elif opt in ('--space-in-paren', '-P'):
            js_options.space_in_paren = True
        elif opt in ('--space-in-empty-paren', '-E'):
            js_options.space_in_empty_paren = True
        elif opt in ('--jslint-happy', '-j'):
            js_options.jslint_happy = True
        elif opt in ('--space_after_anon_function', '-a'):
            js_options.space_after_anon_function = True
        elif opt in ('--eval-code'):
            js_options.eval_code = True
        elif opt in ('--brace-style', '-b'):
            js_options.brace_style = arg
        elif opt in ('--unescape-strings', '-x'):
            js_options.unescape_strings = True
        elif opt in ('--e4x', '-X'):
            js_options.e4x = True
        elif opt in ('--end-with-newline', '-n'):
            js_options.end_with_newline = True
        elif opt in ('--comma-first', '-C'):
            js_options.comma_first = True
        elif opt in ('--operator-position', '-O'):
            js_options.operator_position = sanitizeOperatorPosition(arg)
        elif opt in ('--wrap-line-length ', '-w'):
            js_options.wrap_line_length = int(arg)
        elif opt in ('--stdin', '-i'):
            file = '-'
        elif opt in ('--editorconfig'):
            js_options.editorconfig = True
        elif opt in ('--version', '-v'):
            return print(__version__)
        elif opt in ('--help', '--usage', '-h'):
            return usage()


    if not file:
        file = '-'

    try:
        if outfile == 'stdout' and replace and not file == '-':
            outfile = file

        # Editorconfig used only on files, not stdin
        if getattr(js_options, 'editorconfig'):
            editorconfig_filepath = file

            if editorconfig_filepath == '-':
                if outfile != 'stdout':
                    editorconfig_filepath = outfile
                else:
                    fileType = 'js'
                    editorconfig_filepath = 'stdin.' + fileType

            # debug("EditorConfig is enabled for ", editorconfig_filepath);
            js_options = copy.copy(js_options)
            set_file_editorconfig_opts(editorconfig_filepath, js_options)

        pretty = beautify_file(file, js_options)

        if outfile == 'stdout':
            # python automatically converts newlines in text to "\r\n" when on windows
            # switch to binary to prevent this
            if sys.platform == "win32":
                import msvcrt
                msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

            sys.stdout.write(pretty)
        else:
            if isFileDifferent(outfile, pretty):
                mkdir_p(os.path.dirname(outfile))

                # python automatically converts newlines in text to "\r\n" when on windows
                # set newline to empty to prevent this
                with io.open(outfile, 'wt', newline='') as f:
                    print('writing ' + outfile, file=sys.stderr)
                    try:
                        f.write(pretty)
                    except TypeError:
                        # This is not pretty, but given how we did the version import
                        # it is the only way to do this without having setup.py fail on a missing six dependency.
                        six = __import__("six")
                        f.write(six.u(pretty))


    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

    # Success
    return 0
