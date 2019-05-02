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


class MissingInputStreamError(Exception):
    pass

def default_options():
    return BeautifierOptions()


def beautify(string, opts=default_options()):
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
                js_options.wrap_line_length = int(
                    _ecoptions["max_line_length"])

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

    except EditorConfigError:
        # do not error on bad editor config
        print("Error loading EditorConfig.  Ignoring.", file=sys.stderr)

def beautify_file(file_name, opts=default_options()):
    input_string = ''
    if file_name == '-':  # stdin
        if sys.stdin.isatty():
            raise MissingInputStreamError()

        stream = sys.stdin
        if platform.platform().lower().startswith('windows'):
            if sys.version_info.major >= 3:
                # for python 3 on windows this prevents conversion
                stream = io.TextIOWrapper(sys.stdin.buffer, newline='')
            elif platform.architecture()[0] == '32bit':
                # for python 2 x86 on windows this prevents conversion
                import msvcrt
                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            else:
                raise 'Pipe to stdin not supported on Windows with Python 2.x 64-bit.'

        input_string = stream.read()

        # if you pipe an empty string, that is a failure
        if input_string == '':
            raise MissingInputStreamError()
    else:
        stream = io.open(file_name, 'rt', newline='')
        input_string = stream.read()

    return beautify(input_string, opts)


def usage(stream=sys.stdout):

    print("jsbeautifier.py@" + __version__ + """

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
 -r,  --replace                    Write output in-place, replacing input
 -o,  --outfile=FILE               Specify a file to output to (default stdout)
 -f,  --keep-function-indentation  Do not re-indent function bodies defined in var lines.
 -x,  --unescape-strings           Decode printable chars encoded in \\xNN notation.
 -X,  --e4x                        Pass E4X xml literals through untouched
 -C,  --comma-first                Put commas at the beginning of new line instead of end.
 -O,  --operator-position=STRING   Set operator position (before-newline, after-newline, preserve-newline)
 -w,  --wrap-line-length           Attempt to wrap line when it exceeds this length.
                                   NOTE: Line continues until next wrap point is found.
 -n,  --end-with-newline           End output with newline
 --indent-empty-lines              Keep indentation on empty lines
 --templating                      List of templating languages (auto,none,django,erb,handlebars,php) ["auto"] auto = none in JavaScript, all in html
 --editorconfig                    Enable setting configuration from EditorConfig

Rarely needed options:

 --eval-code                       evaluate code if a JS interpreter is
                                   installed. May be useful with some obfuscated
                                   script but poses a potential security issue.

 -l,  --indent-level=NUMBER        Initial indentation level. (default 0).

 -h,  --help, --usage              Prints this help statement.
 -v,  --version                    Show the version

""", file=stream)
    if stream == sys.stderr:
        return 1
    else:
        return 0


def mkdir_p(path):
    try:
        if path:
            os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise Exception()


def isFileDifferent(filepath, expected):
    try:
        return (
            ''.join(
                io.open(
                    filepath,
                    'rt',
                    newline='').readlines()) != expected)
    except BaseException:
        return True


def main():

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "f:s:c:e:o:rdEPjabkil:xhtvXnCO:w:",
                                   ['file=', 'indent-size=', 'indent-char=', 'eol=', 'outfile=', 'replace', 'disable-preserve-newlines',
                                    'space-in-paren', 'space-in-empty-paren', 'jslint-happy', 'space-after-anon-function',
                                    'brace-style=', 'indent-level=', 'unescape-strings',
                                    'help', 'usage', 'stdin', 'eval-code', 'indent-with-tabs', 'keep-function-indentation', 'version',
                                    'e4x', 'end-with-newline', 'comma-first', 'operator-position=', 'wrap-line-length', 'editorconfig', 'space-after-named-function',
                                    'keep-array-indentation', 'indent-empty-lines', 'templating'])
    except getopt.GetoptError as ex:
        print(ex, file=sys.stderr)
        return usage(sys.stderr)

    js_options = default_options()

    filepath_params = []
    filepath_params.extend(args)

    outfile_param = 'stdout'
    replace = False

    for opt, arg in opts:
        if opt in ('--file', '-f'):
            filepath_params.append(arg)
        elif opt in ('--keep-array-indentation', '-k'):
            js_options.keep_array_indentation = True
        elif opt in ('--keep-function-indentation'):
            js_options.keep_function_indentation = True
        elif opt in ('--outfile', '-o'):
            outfile_param = arg
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
        elif opt in ('--space_after_named_function'):
            js_options.space_after_named_function = True
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
            js_options.operator_position = arg
        elif opt in ('--wrap-line-length ', '-w'):
            js_options.wrap_line_length = int(arg)
        elif opt in ('--indent-empty-lines'):
            js_options.indent_empty_lines = True
        elif opt in ('--templating'):
            js_options.templating = arg.split(',')
        elif opt in ('--stdin', '-i'):
            # stdin is the default if no files are passed
            filepath_params = []
        elif opt in ('--editorconfig'):
            js_options.editorconfig = True
        elif opt in ('--version', '-v'):
            return print(__version__)
        elif opt in ('--help', '--usage', '-h'):
            return usage()

    try:
        filepaths = []
        if not filepath_params or (
                len(filepath_params) == 1 and filepath_params[0] == '-'):
            # default to stdin
            filepath_params = []
            filepaths.append('-')


        for filepath_param in filepath_params:
            # ignore stdin setting if files are specified
            if '-' == filepath_param:
                continue

            # Check if each literal filepath exists
            if os.path.isfile(filepath_param):
                filepaths.append(filepath_param)
            elif '*' in filepath_param or '?' in filepath_param:
                # handle globs
                # empty result is okay
                if sys.version_info.major == 2 or (
                        sys.version_info.major == 3 and
                        sys.version_info.minor <= 4):
                    if '**' in filepath_param:
                        raise 'Recursive globs not supported on Python <= 3.4.'
                    filepaths.extend(glob.glob(filepath_param))
                else:
                    filepaths.extend(glob.glob(filepath_param, recursive=True))
            else:
                # not a glob and not a file
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT),
                    filepath_param)

        if len(filepaths) > 1:
            replace = True
        elif filepaths and filepaths[0] == '-':
            replace = False

        # remove duplicates
        filepaths = set(filepaths)

        for filepath in filepaths:
            if not replace:
                outfile = outfile_param
            else:
                outfile = filepath

            # Editorconfig used only on files, not stdin
            if getattr(js_options, 'editorconfig'):
                editorconfig_filepath = filepath

                if editorconfig_filepath == '-':
                    if outfile != 'stdout':
                        editorconfig_filepath = outfile
                    else:
                        fileType = 'js'
                        editorconfig_filepath = 'stdin.' + fileType

                # debug("EditorConfig is enabled for ", editorconfig_filepath);
                js_options = copy.copy(js_options)
                set_file_editorconfig_opts(editorconfig_filepath, js_options)

            pretty = beautify_file(filepath, js_options)

            if outfile == 'stdout':
                stream = sys.stdout

                # python automatically converts newlines in text to "\r\n" when on windows
                # switch to binary to prevent this
                if platform.platform().lower().startswith('windows'):
                    if sys.version_info.major >= 3:
                        # for python 3 on windows this prevents conversion
                        stream = io.TextIOWrapper(sys.stdout.buffer, newline='')
                    elif platform.architecture()[0] == '32bit':
                        # for python 2 x86 on windows this prevents conversion
                        import msvcrt
                        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                    else:
                        raise 'Pipe to stdout not supported on Windows with Python 2.x 64-bit.'

                stream.write(pretty)
            else:
                if isFileDifferent(outfile, pretty):
                    mkdir_p(os.path.dirname(outfile))

                    # python automatically converts newlines in text to "\r\n" when on windows
                    # set newline to empty to prevent this
                    with io.open(outfile, 'wt', newline='') as f:
                        print('beautified ' + outfile, file=sys.stdout)
                        try:
                            f.write(pretty)
                        except TypeError:
                            # This is not pretty, but given how we did the version import
                            # it is the only way to do this without having setup.py
                            # fail on a missing six dependency.
                            six = __import__("six")
                            f.write(six.u(pretty))
                else:
                    print('beautified ' + outfile + ' - unchanged', file=sys.stdout)


    except MissingInputStreamError:
        print(
            "Must pipe input or define at least one file.\n",
            file=sys.stderr)
        usage(sys.stderr)
        return 1

    except UnicodeError as ex:
        print("Error while decoding input or encoding output:",
            file=sys.stderr)
        print(ex, file=sys.stderr)
        return 1

    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

    # Success
    return 0


if __name__ == "__main__":
    main()
