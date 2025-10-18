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

# Copyright (c) 2007-2020 Einar Lielmanis, Liam Newman, and contributors.

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

__all__ = [
    "MissingInputStreamError",
    "process_file",
    "get_filepaths_from_params",
    "integrate_editorconfig_options",
    "write_beautified_output",
]


class MissingInputStreamError(Exception):
    pass


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

        if _ecoptions.get("insert_final_newline") == "true":
            js_options.end_with_newline = True
        elif _ecoptions.get("insert_final_newline") == "false":
            js_options.end_with_newline = False

        if _ecoptions.get("end_of_line"):
            if _ecoptions["end_of_line"] == "cr":
                js_options.eol = "\r"
            elif _ecoptions["end_of_line"] == "lf":
                js_options.eol = "\n"
            elif _ecoptions["end_of_line"] == "crlf":
                js_options.eol = "\r\n"

    except EditorConfigError:
        # do not error on bad editor config
        print("Error loading EditorConfig.  Ignoring.", file=sys.stderr)


def process_file(file_name, opts, beautify_code):
    input_string = ""
    if file_name == "-":  # stdin
        if sys.stdin.isatty():
            raise MissingInputStreamError()

        stream = sys.stdin
        if platform.platform().lower().startswith("windows"):
            if sys.version_info.major >= 3:
                # for python 3 on windows this prevents conversion
                stream = io.TextIOWrapper(sys.stdin.buffer, newline="")
            elif platform.architecture()[0] == "32bit":
                # for python 2 x86 on windows this prevents conversion
                import msvcrt

                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            else:
                raise Exception(
                    "Pipe to stdin not supported on Windows with Python 2.x 64-bit."
                )

        input_string = stream.read()

        # if you pipe an empty string, that is a failure
        if input_string == "":
            raise MissingInputStreamError()
    else:
        stream = io.open(file_name, "rt", newline="", encoding="UTF-8")
        input_string = stream.read()

    return beautify_code(input_string, opts)


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
        return "".join(io.open(filepath, "rt", newline="").readlines()) != expected
    except BaseException:
        return True


def get_filepaths_from_params(filepath_params, replace):
    filepaths = []
    if not filepath_params or (len(filepath_params) == 1 and filepath_params[0] == "-"):
        # default to stdin
        filepath_params = []
        filepaths.append("-")

    for filepath_param in filepath_params:
        # ignore stdin setting if files are specified
        if "-" == filepath_param:
            continue

        # Check if each literal filepath exists
        if os.path.isfile(filepath_param):
            filepaths.append(filepath_param)
        elif "*" in filepath_param or "?" in filepath_param:
            # handle globs
            # empty result is okay
            if sys.version_info.major == 2 or (
                sys.version_info.major == 3 and sys.version_info.minor <= 4
            ):
                if "**" in filepath_param:
                    raise Exception("Recursive globs not supported on Python <= 3.4.")
                filepaths.extend(glob.glob(filepath_param))
            else:
                filepaths.extend(glob.glob(filepath_param, recursive=True))
        else:
            # not a glob and not a file
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), filepath_param)

    if len(filepaths) > 1:
        replace = True
    elif filepaths and filepaths[0] == "-":
        replace = False

    # remove duplicates
    filepaths = set(filepaths)

    return filepaths, replace


def integrate_editorconfig_options(filepath, local_options, outfile, default_file_type):
    # Editorconfig used only on files, not stdin
    if getattr(local_options, "editorconfig"):
        editorconfig_filepath = filepath

        if editorconfig_filepath == "-":
            if outfile != "stdout":
                editorconfig_filepath = outfile
            else:
                fileType = default_file_type
                editorconfig_filepath = "stdin." + fileType

        # debug("EditorConfig is enabled for ", editorconfig_filepath);
        local_options = copy.copy(local_options)
        set_file_editorconfig_opts(editorconfig_filepath, local_options)

    return local_options


def write_beautified_output(pretty, local_options, outfile):
    if outfile == "stdout":
        stream = sys.stdout

        # python automatically converts newlines in text to "\r\n" when on windows
        # switch to binary to prevent this
        if platform.platform().lower().startswith("windows"):
            if sys.version_info.major >= 3:
                # for python 3 on windows this prevents conversion
                stream = io.TextIOWrapper(sys.stdout.buffer, newline="")
            elif platform.architecture()[0] == "32bit":
                # for python 2 x86 on windows this prevents conversion
                import msvcrt

                msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
            else:
                raise Exception(
                    "Pipe to stdout not supported on Windows with Python 2.x 64-bit."
                )

        stream.write(pretty)
    else:
        if isFileDifferent(outfile, pretty):
            mkdir_p(os.path.dirname(outfile))

            # python automatically converts newlines in text to "\r\n" when on windows
            # set newline to empty to prevent this
            with io.open(outfile, "wt", newline="", encoding="UTF-8") as f:
                if not local_options.keep_quiet:
                    print("beautified " + outfile, file=sys.stdout)

                try:
                    f.write(pretty)
                except TypeError:
                    # This is not pretty, but given how we did the version import
                    # it is the only way to do this without having setup.py
                    # fail on a missing six dependency.
                    six = __import__("six")
                    f.write(six.u(pretty))
        elif not local_options.keep_quiet:
            print("beautified " + outfile + " - unchanged", file=sys.stdout)
