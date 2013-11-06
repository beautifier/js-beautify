from __future__ import print_function
import sys
import os
import getopt
import re
import string
import errno
from jsbeautifier.__version__ import __version__

#
# The MIT License (MIT)

# Copyright (c) 2007-2013 Einar Lielmanis and contributors.

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


class BeautifierOptions:
    def __init__(self):
        self.indent_size = 4
        self.indent_char = ' '
        self.indent_with_tabs = False
        self.preserve_newlines = True
        self.max_preserve_newlines = 10
        self.space_in_paren = False
        self.e4x = False
        self.jslint_happy = False
        self.brace_style = 'collapse'
        self.keep_array_indentation = False
        self.keep_function_indentation = False
        self.eval_code = False
        self.unescape_strings = False
        self.wrap_line_length = 0
        self.break_chained_methods = False



    def __repr__(self):
        return \
"""indent_size = %d
indent_char = [%s]
preserve_newlines = %s
max_preserve_newlines = %d
space_in_paren = %s
jslint_happy = %s
indent_with_tabs = %s
brace_style = %s
keep_array_indentation = %s
eval_code = %s
wrap_line_length = %s
unescape_strings = %s
""" % ( self.indent_size,
        self.indent_char,
        self.preserve_newlines,
        self.max_preserve_newlines,
        self.space_in_paren,
        self.jslint_happy,
        self.indent_with_tabs,
        self.brace_style,
        self.keep_array_indentation,
        self.eval_code,
        self.wrap_line_length,
        self.unescape_strings,
        )


class BeautifierFlags:
    def __init__(self, mode):
        self.mode = mode
        self.parent = None
        self.last_text = ''
        self.last_word = ''
        self.var_line = False
        self.var_line_tainted = False
        self.var_line_reindented = False
        self.in_html_comment = False
        self.multiline_frame = False
        self.if_block = False
        self.do_block = False
        self.do_while = False
        self.in_case = False
        self.in_case_statement = False
        self.case_body = False
        self.indentation_level = 0
        self.line_indent_level = 0
        self.start_line_index = 0
        self.ternary_depth = 0
        self.had_comment = False

    def apply_base(self, flags_base, added_newline):
        next_indent_level = flags_base.indentation_level;
        if flags_base.var_line and flags_base.var_line_reindented:
            next_indent_level += 1
        if not added_newline and \
            flags_base.line_indent_level > next_indent_level:
            next_indent_level = flags_base.line_indent_level;

        self.parent = flags_base;
        self.last_text = flags_base.last_text
        self.last_word = flags_base.last_word
        self.indentation_level = next_indent_level

# Using object instead of string to allow for later expansion of info about each line
class OutputLine:
    def __init__(self):
        self.text = []




def default_options():
    return BeautifierOptions()


def beautify(string, opts = default_options() ):
    b = Beautifier()
    return b.beautify(string, opts)

def beautify_file(file_name, opts = default_options() ):
    if file_name == '-': # stdin
        stream = sys.stdin
    else:
        stream = open(file_name)

    return beautify(''.join(stream.readlines()), opts);


def usage(stream=sys.stdout):

    print("jsbeautifier.py@" + __version__ + """

Javascript beautifier (http://jsbeautifier.org/)

Usage: jsbeautifier.py [options] <infile>

    <infile> can be "-", which means stdin.
    <outfile> defaults to stdout

Input options:

 -i,  --stdin                      read input from stdin

Output options:

 -s,  --indent-size=NUMBER         indentation size. (default 4).
 -c,  --indent-char=CHAR           character to indent with. (default space).
 -t,  --indent-with-tabs           Indent with tabs, overrides -s and -c
 -d,  --disable-preserve-newlines  do not preserve existing line breaks.
 -P,  --space-in-paren             add padding spaces within paren, ie. f( a, b )
 -j,  --jslint-happy               more jslint-compatible output
 -b,  --brace-style=collapse       brace style (collapse, expand, end-expand)
 -k,  --keep-array-indentation     keep array indentation.
 -o,  --outfile=FILE               specify a file to output to (default stdout)
 -f,  --keep-function-indentation  Do not re-indent function bodies defined in var lines.
 -x,  --unescape-strings           Decode printable chars encoded in \\xNN notation.
 -X,  --e4x                        Pass E4X xml literals through untouched
 -w,  --wrap-line-length                   Attempt to wrap line when it exceeds this length.
                                   NOTE: Line continues until next wrap point is found.

Rarely needed options:

 --eval-code                       evaluate code if a JS interpreter is
                                   installed. May be useful with some obfuscated
                                   script but poses a potential security issue.

 -l,  --indent-level=NUMBER        initial indentation level. (default 0).

 -h,  --help, --usage              prints this help statement.
 -v, --version                     Show the version

""", file=stream)
    if stream == sys.stderr:
        return 1
    else:
        return 0



class MODE:
      BlockStatement, Statement, ObjectLiteral, ArrayLiteral, \
      ForInitializer, Conditional, Expression = range(7)

class Beautifier:

    def __init__(self, opts = default_options() ):

        self.opts = opts
        self.blank_state()

    def blank_state(self):

        # internal flags
        self.flags = None
        self.previous_flags = None
        self.flag_store = []
        self.input_wanted_newline = False
        if self.opts.indent_with_tabs:
            self.opts.indent_char = "\t"
            self.opts.indent_size = 1

        self.indent_string = self.opts.indent_char * self.opts.indent_size

        self.preindent_string = ''
        self.last_type = 'TK_START_BLOCK' # last token type
        self.last_last_text = ''         # pre-last token text

        self.input = None
        self.output_lines = [ OutputLine() ]
        self.output_wrapped = False
        self.output_space_before_token = False
        self.whitespace_before_token = []

        self.whitespace = ["\n", "\r", "\t", " "]
        self.wordchar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$'
        self.digits = '0123456789'
        self.punct = '+ - * / % & ++ -- = += -= *= /= %= == === != !== > < >= <= >> << >>> >>>= >>= <<= && &= | || ! !! , : ? ^ ^= |= ::'
        self.punct += ' <?= <? ?> <%= <% %>'
        self.punct = self.punct.split(' ')


        # Words which always should start on a new line
        self.line_starters = 'continue,try,throw,return,var,if,switch,case,default,for,while,break,function'.split(',')

        self.set_mode(MODE.BlockStatement)

        self.parser_pos = 0


    def beautify(self, s, opts = None ):

        if opts != None:
            self.opts = opts

        if self.opts.brace_style not in ['expand', 'collapse', 'end-expand']:
            raise(Exception('opts.brace_style must be "expand", "collapse" or "end-expand".'))

        self.blank_state()

        while s and s[0] in [' ', '\t']:
            self.preindent_string += s[0]
            s = s[1:]

        self.input = self.unpack(s, self.opts.eval_code)

        self.parser_pos = 0
        handlers = {
            'TK_START_EXPR': self.handle_start_expr,
            'TK_END_EXPR': self.handle_end_expr,
            'TK_START_BLOCK': self.handle_start_block,
            'TK_END_BLOCK': self.handle_end_block,
            'TK_WORD': self.handle_word,
            'TK_SEMICOLON': self.handle_semicolon,
            'TK_STRING': self.handle_string,
            'TK_EQUALS': self.handle_equals,
            'TK_OPERATOR': self.handle_operator,
            'TK_COMMA': self.handle_comma,
            'TK_BLOCK_COMMENT': self.handle_block_comment,
            'TK_INLINE_COMMENT': self.handle_inline_comment,
            'TK_COMMENT': self.handle_comment,
            'TK_DOT': self.handle_dot,
            'TK_UNKNOWN': self.handle_unknown,
        }

        while True:
            self.token_text, token_type = self.get_next_token()

            #print (token_text, token_type, self.flags.mode)
            if token_type == 'TK_EOF':
                break

            keep_whitespace = self.opts.keep_array_indentation and self.is_array(self.flags.mode)
            self.input_wanted_newline = self.n_newlines > 0

            if keep_whitespace:
                 for i in range(self.n_newlines):
                        self.append_newline(i > 0)
            else: # not keep_whitespace
                if self.opts.max_preserve_newlines != 0 and self.n_newlines > self.opts.max_preserve_newlines:
                    self.n_newlines = self.opts.max_preserve_newlines

                if self.opts.preserve_newlines and self.n_newlines > 1:

                    for i in range(self.n_newlines):
                        self.append_newline(i != 0)

            handlers[token_type](self.token_text)

            # The cleanest handling of inline comments is to treat them as though they aren't there.
            # Just continue formatting and the behavior should be logical.
            if token_type != 'TK_INLINE_COMMENT' and token_type != 'TK_COMMENT' and token_type != 'TK_BLOCK_COMMENT' and token_type != 'TK_UNKNOWN':
                self.last_last_text = self.flags.last_text
                self.last_type = token_type
                self.flags.last_text = self.token_text
            self.flags.had_comment = token_type in ['TK_COMMENT', 'TK_INLINE_COMMENT', 'TK_BLOCK_COMMENT']

        sweet_code = ''.join(self.output_lines[0].text)
        if len(self.output_lines) > 1:
            for line_index in range(1, len(self.output_lines)):
                sweet_code += '\n' + ''.join(self.output_lines[line_index].text);

        sweet_code = re.sub('[\n ]+$', '', sweet_code)
        return sweet_code

    def unpack(self, source, evalcode=False):
        import jsbeautifier.unpackers as unpackers
        try:
            return unpackers.run(source, evalcode)
        except unpackers.UnpackingError as error:
            print('error:', error)
            return ''

    def trim_output(self, eat_newlines = False):
        self.trim_output_line(self.output_lines[-1])

        while eat_newlines and len(self.output_lines) > 1 and \
            len(self.output_lines[-1].text) == 0:
            self.output_lines.pop()
            self.trim_output_line(self.output_lines[-1])

    def trim_output_line(self, line):
        while len(line.text) \
              and (
                  line.text[-1] == ' '\
                  or line.text[-1] == self.indent_string \
                  or line.text[-1] == self.preindent_string):
            line.text.pop()

    def is_special_word(self, s):
        return s in ['case', 'return', 'do', 'if', 'throw', 'else']

    def is_array(self, mode):
        return mode == MODE.ArrayLiteral


    def is_expression(self, mode):
        return mode in [MODE.Expression, MODE.ForInitializer, MODE.Conditional]

    def just_added_newline(self):
        line = self.output_lines[-1]
        return len(line.text) == 0


    def just_added_blankline(self):
        if self.just_added_newline():
            if len(self.output_lines) == 1:
                return True

            line = self.output_lines[-2]
            return len(line.text) == 0

        return False

    def allow_wrap_or_preserved_newline(self, token_text, force_linewrap = False):
        if self.opts.wrap_line_length > 0 and not force_linewrap:
            line = self.output_lines[-1]

            # never wrap the first token of a line.
            if len(line.text) > 0:
                proposed_line_length = len(''.join(line.text)) + len(token_text)
                if self.output_space_before_token:
                    proposed_line_length += 1

                if proposed_line_length >= self.opts.wrap_line_length:
                    force_linewrap = True

        if ((self.opts.preserve_newlines and self.input_wanted_newline) or force_linewrap) and not self.just_added_newline():
            self.append_newline(preserve_statement_flags = True)

            # Expressions and array literals already indent their contents.
            if not (self.is_array(self.flags.mode) or self.is_expression(self.flags.mode)):
                self.output_wrapped = True


    def append_newline(self, force_newline = False, preserve_statement_flags = False):
        self.output_wrapped = False
        self.output_space_before_token = False

        if not preserve_statement_flags:
            if self.flags.last_text != ';':
                while self.flags.mode == MODE.Statement and not self.flags.if_block and not self.flags.do_block:
                    self.restore_mode();

        if len(self.output_lines) == 1 and self.just_added_newline():
            # no newline on start of file
            return

        if force_newline or not self.just_added_newline():
            self.flags.multiline_frame = True
            self.output_lines.append(OutputLine())


    def append_token_line_indentation(self):
        if self.just_added_newline():
            line = self.output_lines[-1]
            if self.opts.keep_array_indentation and self.is_array(self.flags.mode) and self.input_wanted_newline:
                # prevent removing of this whitespace as redundant
                line.text.append('');
                for item in self.whitespace_before_token:
                    line.text.append(item)

            else:
                if self.preindent_string != '':
                    line.text.append(self.preindent_string)

                level = self.flags.indentation_level;
                if self.flags.var_line and self.flags.var_line_reindented:
                    level += 1
                if self.output_wrapped:
                    level += 1

                self.append_indent_string(level)


    def append_indent_string(self, level):
        # Never indent your first output indent at the start of the file
        if len(self.output_lines) > 1:
            line = self.output_lines[-1]
            self.flags.line_indent_level = level
            for i in range(level):
                line.text.append(self.indent_string)


    def append_token_space_before(self):
        # make sure only single space gets drawn
        line = self.output_lines[-1]
        if self.output_space_before_token and len(line.text) and line.text[-1] not in [' ', self.indent_string]:
            line.text.append(' ')


    def append_token(self, s):
        self.append_token_line_indentation()
        self.output_wrapped = False
        self.append_token_space_before()
        self.output_space_before_token = False
        self.output_lines[-1].text.append(s)


    def indent(self):
        self.flags.indentation_level += 1

    def deindent(self):
        allow_deindent = self.flags.indentation_level > 0 and ((self.flags.parent == None) or self.flags.indentation_level > self.flags.parent.indentation_level)

        if allow_deindent:
            self.flags.indentation_level -= 1

    def remove_redundant_indentation(self, frame):
        # This implementation is effective but has some issues:
        #     - less than great performance due to array splicing
        #     - can cause line wrap to happen too soon due to indent removal
        #           after wrap points are calculated
        # These issues are minor compared to ugly indentation.

        if frame.multiline_frame:
            return

        # remove one indent from each line inside this section
        index = frame.start_line_index
        splice_index = 0
        while index < len(self.output_lines):
            line = self.output_lines[index]
            index += 1

            # skip empty lines
            if len(line.text) == 0:
                continue

            # skip the preindent string if present
            if self.preindent_string != '' and \
                    line.text[0] == self.preindent_string:
                splice_index = 1
            else:
                splice_index = 0

            # remove one indent, if present
            if line.text[splice_index] == self.indent_string:
                del line.text[splice_index]

    def set_mode(self, mode):
        if self.flags:
            self.flag_store.append(self.flags)
            self.previous_flags = self.flags
        else:
            self.previous_flags = BeautifierFlags(mode)

        self.flags = BeautifierFlags(mode)
        self.flags.apply_base(self.previous_flags, self.just_added_newline());
        self.flags.start_line_index = len(self.output_lines)

    def restore_mode(self):
        if len(self.flag_store) > 0:
            self.previous_flags = self.flags
            self.flags = self.flag_store.pop()

    def start_of_object_property(self):
        return self.flags.mode == MODE.ObjectLiteral and self.flags.last_text == ':' and \
            self.flags.ternary_depth == 0

    def start_of_statement(self):
        if (self.flags.last_text == 'do' \
                or (self.flags.last_text == 'else' and self.token_text != 'if' ) \
                or (self.last_type == 'TK_END_EXPR' and (self.previous_flags.mode == MODE.ForInitializer or self.previous_flags.mode == MODE.Conditional))):
            # Issue #276:
            # If starting a new statement with [if, for, while, do], push to a new line.
            # if (a) if (b) if(c) d(); else e(); else f();
            self.allow_wrap_or_preserved_newline(self.token_text, self.token_text in ['do', 'for', 'if', 'while']);

            self.set_mode(MODE.Statement);
            # Issue #275:
            # If starting on a newline, all of a statement should be indented.
            # if not, use line wrapping logic for indent.
            if self.just_added_newline():
                self.indent()
                self.output_wrapped = False

            return True
        else:
            return False

    def is_next(self, find):
        local_pos = self.parser_pos
        if local_pos >= len(self.input):
            return False
        c = self.input[local_pos]

        while (c in self.whitespace) and c != find:
            local_pos+= 1
            if local_pos >= len(self.input):
                return False
            c = self.input[local_pos]

        return c == find

    def get_next_token(self):

        self.n_newlines = 0

        if self.parser_pos >= len(self.input):
            return '', 'TK_EOF'

        self.input_wanted_newline = False
        self.whitespace_before_token = []

        c = self.input[self.parser_pos]
        self.parser_pos += 1

        while c in self.whitespace:
            if c == '\n':
                self.n_newlines += 1
                self.whitespace_before_token = []
            elif c == self.indent_string:
                self.whitespace_before_token.append(self.indent_string)
            elif c != '\r':
                self.whitespace_before_token.append(' ')

            if self.parser_pos >= len(self.input):
                return '', 'TK_EOF'

            c = self.input[self.parser_pos]
            self.parser_pos += 1


        if c in self.wordchar:
            if self.parser_pos < len(self.input):
                while self.input[self.parser_pos] in self.wordchar:
                    c = c + self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos == len(self.input):
                        break

            # small and surprisingly unugly hack for IE-10 representation
            if self.parser_pos != len(self.input) and self.input[self.parser_pos] in '+-' \
               and re.match('^[0-9]+[Ee]$', c):

                sign = self.input[self.parser_pos]
                self.parser_pos += 1
                t = self.get_next_token()
                c += sign + t[0]
                return c, 'TK_WORD'

            if c == 'in': # in is an operator, need to hack
                return c, 'TK_OPERATOR'

            return c, 'TK_WORD'

        if c in '([':
            return c, 'TK_START_EXPR'

        if c in ')]':
            return c, 'TK_END_EXPR'

        if c == '{':
            return c, 'TK_START_BLOCK'

        if c == '}':
            return c, 'TK_END_BLOCK'

        if c == ';':
            return c, 'TK_SEMICOLON'

        if c == '/':
            comment = ''
            inline_comment = True
            if self.input[self.parser_pos] == '*': # peek /* .. */ comment
                self.parser_pos += 1
                if self.parser_pos < len(self.input):
                    while not (self.input[self.parser_pos] == '*' and \
                               self.parser_pos + 1 < len(self.input) and \
                               self.input[self.parser_pos + 1] == '/')\
                          and self.parser_pos < len(self.input):
                        c = self.input[self.parser_pos]
                        comment += c
                        if c in '\r\n':
                            inline_comment = False
                        self.parser_pos += 1
                        if self.parser_pos >= len(self.input):
                            break
                self.parser_pos += 2
                if inline_comment and self.n_newlines == 0:
                    return '/*' + comment + '*/', 'TK_INLINE_COMMENT'
                else:
                    return '/*' + comment + '*/', 'TK_BLOCK_COMMENT'

            if self.input[self.parser_pos] == '/': # peek // comment
                comment = c
                while self.input[self.parser_pos] not in '\r\n':
                    comment += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos >= len(self.input):
                        break

                return comment, 'TK_COMMENT'

        if c == "'" or c == '"' or \
            ( \
                (c == '/') or \
                (self.opts.e4x and c == "<" and re.match('^<(!\[CDATA\[[\s\S]*?\]\]|[-a-zA-Z:0-9_.]+|\{[^{}]*\})\s*([-a-zA-Z:0-9_.]+=(\{[^{}]*\}|"[^"]*"|\'[^\']*\')\s*)*\/?\s*>', self.input[self.parser_pos - 1:])) \
            ) and ( \
                (self.last_type == 'TK_WORD' and self.is_special_word(self.flags.last_text)) or \
                (self.last_type == 'TK_END_EXPR' and self.previous_flags.mode in [MODE.Conditional, MODE.ForInitializer]) or \
                (self.last_type in ['TK_COMMENT', 'TK_START_EXPR', 'TK_START_BLOCK', 'TK_END_BLOCK', 'TK_OPERATOR', \
                                   'TK_EQUALS', 'TK_EOF', 'TK_SEMICOLON', 'TK_COMMA'])):
            sep = c
            esc = False
            esc1 = 0
            esc2 = 0
            resulting_string = c
            in_char_class = False

            if self.parser_pos < len(self.input):
                if sep == '/':
                    # handle regexp
                    in_char_class = False
                    while esc or in_char_class or self.input[self.parser_pos] != sep:
                        resulting_string += self.input[self.parser_pos]
                        if not esc:
                            esc = self.input[self.parser_pos] == '\\'
                            if self.input[self.parser_pos] == '[':
                                in_char_class = True
                            elif self.input[self.parser_pos] == ']':
                                in_char_class = False
                        else:
                            esc = False
                        self.parser_pos += 1
                        if self.parser_pos >= len(self.input):
                            # incomplete regex when end-of-file reached
                            # bail out with what has received so far
                            return resulting_string, 'TK_STRING'

                elif self.opts.e4x and sep == '<':
                    # handle e4x xml literals
                    xmlRegExp = re.compile('<(\/?)(!\[CDATA\[[\s\S]*?\]\]|[-a-zA-Z:0-9_.]+|\{[^{}]*\})\s*([-a-zA-Z:0-9_.]+=(\{[^{}]*\}|"[^"]*"|\'[^\']*\')\s*)*(\/?)\s*>')
                    xmlStr = self.input[self.parser_pos - 1:]
                    match = xmlRegExp.match(xmlStr)
                    if match:
                        rootTag = match.group(2)
                        depth = 0
                        while (match):
                            isEndTag = match.group(1)
                            tagName = match.group(2)
                            isSingletonTag = (match.groups()[-1] != "") or (match.group(2)[0:8] == "![CDATA[")
                            if tagName == rootTag and not isSingletonTag:
                                if isEndTag:
                                    depth -= 1
                                else:
                                    depth += 1

                            if depth <= 0:
                                break

                            match = xmlRegExp.search(xmlStr, match.end())

                        if match:
                            xmlLength = match.end() # + len(match.group())
                        else:
                            xmlLength = len(xmlStr)

                        self.parser_pos += xmlLength - 1
                        return xmlStr[:xmlLength], 'TK_STRING'

                else:
                    # handle string
                    while esc or self.input[self.parser_pos] != sep:
                        resulting_string += self.input[self.parser_pos]
                        if esc1 and esc1 >= esc2:
                            try:
                                esc1 = int(resulting_string[-esc2:], 16)
                            except Exception:
                                esc1 = False
                            if esc1 and esc1 >= 0x20 and esc1 <= 0x7e:
                                esc1 = chr(esc1)
                                resulting_string = resulting_string[:-2 - esc2]
                                if esc1 == sep or esc1 == '\\':
                                        resulting_string += '\\'
                                resulting_string += esc1
                            esc1 = 0
                        if esc1:
                            esc1 += 1
                        elif not esc:
                            esc = self.input[self.parser_pos] == '\\'
                        else:
                            esc = False
                            if self.opts.unescape_strings:
                                if self.input[self.parser_pos] == 'x':
                                    esc1 += 1
                                    esc2 = 2
                                elif self.input[self.parser_pos] == 'u':
                                    esc1 += 1
                                    esc2 = 4
                        self.parser_pos += 1
                        if self.parser_pos >= len(self.input):
                            # incomplete string when end-of-file reached
                            # bail out with what has received so far
                            return resulting_string, 'TK_STRING'


            self.parser_pos += 1
            resulting_string += sep
            if sep == '/':
                # regexps may have modifiers /regexp/MOD, so fetch those too
                while self.parser_pos < len(self.input) and self.input[self.parser_pos] in self.wordchar:
                    resulting_string += self.input[self.parser_pos]
                    self.parser_pos += 1
            return resulting_string, 'TK_STRING'

        if c == '#':

            # she-bang
            if len(self.output_lines) == 1 and len(self.output_lines[0].text) == 0 and \
                    len(self.input) > self.parser_pos and self.input[self.parser_pos] == '!':
                resulting_string = c
                while self.parser_pos < len(self.input) and c != '\n':
                    c = self.input[self.parser_pos]
                    resulting_string += c
                    self.parser_pos += 1
                return resulting_string.strip() + '\n', 'TK_UNKNOWN'


            # Spidermonkey-specific sharp variables for circular references
            # https://developer.mozilla.org/En/Sharp_variables_in_JavaScript
            # http://mxr.mozilla.org/mozilla-central/source/js/src/jsscan.cpp around line 1935
            sharp = '#'
            if self.parser_pos < len(self.input) and self.input[self.parser_pos] in self.digits:
                while True:
                    c = self.input[self.parser_pos]
                    sharp += c
                    self.parser_pos += 1
                    if self.parser_pos >= len(self.input)  or c == '#' or c == '=':
                        break
            if c == '#' or self.parser_pos >= len(self.input):
                pass
            elif self.input[self.parser_pos] == '[' and self.input[self.parser_pos + 1] == ']':
                sharp += '[]'
                self.parser_pos += 2
            elif self.input[self.parser_pos] == '{' and self.input[self.parser_pos + 1] == '}':
                sharp += '{}'
                self.parser_pos += 2
            return sharp, 'TK_WORD'

        if c == '<' and self.input[self.parser_pos - 1 : self.parser_pos + 3] == '<!--':
            self.parser_pos += 3
            c = '<!--'
            while self.parser_pos < len(self.input) and self.input[self.parser_pos] != '\n':
                c += self.input[self.parser_pos]
                self.parser_pos += 1
            self.flags.in_html_comment = True
            return c, 'TK_COMMENT'

        if c == '-' and self.flags.in_html_comment and self.input[self.parser_pos - 1 : self.parser_pos + 2] == '-->':
            self.flags.in_html_comment = False
            self.parser_pos += 2
            return '-->', 'TK_COMMENT'

        if c == '.':
            return c, 'TK_DOT'

        if c in self.punct:
            while self.parser_pos < len(self.input) and c + self.input[self.parser_pos] in self.punct:
                c += self.input[self.parser_pos]
                self.parser_pos += 1
                if self.parser_pos >= len(self.input):
                    break

            if c == ',':
                return c, 'TK_COMMA'
            if c == '=':
                return c, 'TK_EQUALS'

            return c, 'TK_OPERATOR'

        return c, 'TK_UNKNOWN'


    def handle_start_expr(self, token_text):
        if self.start_of_statement():
            # The conditional starts the statement if appropriate.
            pass

        next_mode = MODE.Expression

        if token_text == '[':
            if self.last_type == 'TK_WORD' or self.flags.last_text == ')':
                if self.flags.last_text in self.line_starters:
                    self.output_space_before_token = True
                self.set_mode(next_mode)
                self.append_token(token_text)
                self.indent()
                if self.opts.space_in_paren:
                    self.output_space_before_token = True
                return

            next_mode = MODE.ArrayLiteral

            if self.is_array(self.flags.mode):
                if self.flags.last_text == '[' or (
                    self.flags.last_text == ',' and (self.last_last_text == ']' or self.last_last_text == '}')):
                    # ], [ goes to a new line
                    # }, [ goes to a new line
                    if not self.opts.keep_array_indentation:
                        self.append_newline()

        else:
            if self.flags.last_text == 'for':
                next_mode = MODE.ForInitializer
            elif self.flags.last_text in ['if', 'while']:
                next_mode = MODE.Conditional
            else:
                next_mode = MODE.Expression


        if self.flags.last_text == ';' or self.last_type == 'TK_START_BLOCK':
            self.append_newline()
        elif self.last_type in ['TK_END_EXPR', 'TK_START_EXPR', 'TK_END_BLOCK'] or self.flags.last_text == '.':
            # do nothing on (( and )( and ][ and ]( and .(
            # TODO: Consider whether forcing this is required.  Review failing tests when removed.
            self.allow_wrap_or_preserved_newline(token_text, self.input_wanted_newline);
            self.output_wrapped = False;

        elif self.last_type not in ['TK_WORD', 'TK_OPERATOR']:
            self.output_space_before_token = True
        elif self.flags.last_word == 'function' or self.flags.last_word == 'typeof':
            # function() vs function (), typeof() vs typeof ()
            if self.opts.jslint_happy:
                self.output_space_before_token = True
        elif self.flags.last_text in self.line_starters or self.flags.last_text == 'catch':
            # TODO: option space_before_conditional
            self.output_space_before_token = True

        # Support of this kind of newline preservation:
        # a = (b &&
        #     (c || d));
        if self.last_type in ['TK_EQUALS', 'TK_OPERATOR']:
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(token_text)

        self.set_mode(next_mode)
        self.append_token(token_text)

        if self.opts.space_in_paren:
            self.output_space_before_token = True

        # In all cases, if we newline while inside an expression it should be indented.
        self.indent()



    def handle_end_expr(self, token_text):
        # statements inside expressions are not valid syntax, but...
        # statements must all be closed when their container closes
        while self.flags.mode == MODE.Statement:
            self.restore_mode()

        if self.token_text == ']' and self.is_array(self.flags.mode) and self.flags.multiline_frame and not self.opts.keep_array_indentation:
            self.append_newline()

        if self.flags.multiline_frame:
            self.allow_wrap_or_preserved_newline(token_text)

        if self.opts.space_in_paren:
            if self.last_type == 'TK_START_EXPR':
                # empty parens are always "()" and "[]", not "( )" or "[ ]"
                self.output_space_before_token = False
                self.trim_output()
            else:
                self.output_space_before_token = True

        if self.token_text == ']' and self.opts.keep_array_indentation:
            self.append_token(token_text)
            self.restore_mode()
        else:
            self.restore_mode()
            self.append_token(token_text)

        self.remove_redundant_indentation(self.previous_flags);

        # do {} while () // no statement required after
        if self.flags.do_while and self.previous_flags.mode == MODE.Conditional:
            self.previous_flags.mode = MODE.Expression
            self.flags.do_block = False
            self.flags.do_while = False

    def handle_start_block(self, token_text):
        self.set_mode(MODE.BlockStatement)

        empty_braces = self.is_next('}')
        empty_anonymous_function = empty_braces and self.flags.last_word == 'function' and \
            self.last_type == 'TK_END_EXPR'

        if self.opts.brace_style == 'expand':
            if self.last_type != 'TK_OPERATOR' and \
                (empty_anonymous_function or
                    self.last_type == 'TK_EQUALS' or
                    (self.is_special_word(self.flags.last_text) and self.flags.last_text != 'else')):
                self.output_space_before_token = True
            else:
                self.append_newline()
        else: # collapse
            if self.last_type not in ['TK_OPERATOR', 'TK_START_EXPR']:
                if self.last_type == 'TK_START_BLOCK':
                    self.append_newline()
                else:
                    self.output_space_before_token = True
            else:
                # if TK_OPERATOR or TK_START_EXPR
                if self.is_array(self.previous_flags.mode) and self.flags.last_text == ',':
                    if self.last_last_text == '}':
                        self.output_space_before_token = True
                    else:
                        self.append_newline()

        self.append_token(token_text)
        self.indent()


    def handle_end_block(self, token_text):
        # statements must all be closed when their container closes
        while self.flags.mode == MODE.Statement:
            self.restore_mode()

        empty_braces = self.last_type == 'TK_START_BLOCK';
        if self.opts.brace_style == 'expand':
            if not empty_braces:
                self.append_newline()
        else:
            # skip {}
            if not empty_braces:
                if self.is_array(self.flags.mode) and self.opts.keep_array_indentation:
                    self.opts.keep_array_indentation = False
                    self.append_newline()
                    self.opts.keep_array_indentation = True
                else:
                    self.append_newline()

        self.restore_mode()
        self.append_token(token_text)


    def handle_word(self, token_text):
        if self.start_of_statement():
            # The conditional starts the statement if appropriate.
            pass
        elif self.input_wanted_newline and \
                not self.is_expression(self.flags.mode) and \
                (self.last_type != 'TK_OPERATOR' or (self.flags.last_text == '--' or self.flags.last_text == '++')) and \
                self.last_type != 'TK_EQUALS' and \
                (self.opts.preserve_newlines or self.flags.last_text != 'var'):
            self.append_newline()

        if self.flags.do_block and not self.flags.do_while:
            if token_text == 'while':
                # do {} ## while ()
                self.output_space_before_token = True
                self.append_token(token_text)
                self.output_space_before_token = True
                self.flags.do_while = True
                return
            else:
                # do {} should always have while as the next word.
                # if we don't see the expected while, recover
                self.append_newline()
                self.flags.do_block = False

        # if may be followed by else, or not
        # Bare/inline ifs are tricky
        # Need to unwind the modes correctly: if (a) if (b) c(); else d(); else e();
        if self.flags.if_block:
            if token_text != 'else':
                while self.flags.mode == MODE.Statement:
                    self.restore_mode()

                self.flags.if_block = False;

        if token_text == 'case' or (token_text == 'default' and self.flags.in_case_statement):
            self.append_newline()
            if self.flags.case_body or self.opts.jslint_happy:
                self.flags.case_body = False
                self.deindent()
            self.append_token(token_text)
            self.flags.in_case = True
            self.flags.in_case_statement = True
            return

        if token_text == 'function':
            if self.flags.var_line and self.flags.last_text != '=':
                self.flags.var_line_reindented = not self.opts.keep_function_indentation

            if self.flags.last_text in ['}', ';'] or (self.just_added_newline() and not self.flags.last_text in ['{', ':', '=', ',']):
                # make sure there is a nice clean space of at least one blank line
                # before a new function definition, except in arrays
                if not self.just_added_blankline() and not self.flags.had_comment:
                    self.append_newline()
                    self.append_newline(True)

            if self.last_type == 'TK_WORD':
                if self.flags.last_text in ['get', 'set', 'new', 'return']:
                    self.output_space_before_token = True
                else:
                    self.append_newline()
            elif self.last_type == 'TK_OPERATOR' or self.flags.last_text == '=':
                # foo = function
                self.output_space_before_token = True
            elif self.is_expression(self.flags.mode):
                # (function
                pass
            else:
                self.append_newline()

        if self.last_type in ['TK_COMMA', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR']:
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(token_text)

        if token_text == 'function':
            self.append_token(token_text)
            self.flags.last_word = token_text
            return

        prefix = 'NONE'

        if self.last_type == 'TK_END_BLOCK':
            if token_text not in ['else', 'catch', 'finally']:
                prefix = 'NEWLINE'
            else:
                if self.opts.brace_style in ['expand', 'end-expand']:
                    prefix = 'NEWLINE'
                else:
                    prefix = 'SPACE'
                    self.output_space_before_token = True
        elif self.last_type == 'TK_SEMICOLON' and self.flags.mode == MODE.BlockStatement:
            # TODO: Should this be for STATEMENT as well?
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_SEMICOLON' and self.is_expression(self.flags.mode):
            prefix = 'SPACE'
        elif self.last_type == 'TK_STRING':
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_WORD':
            prefix = 'SPACE'
        elif self.last_type == 'TK_START_BLOCK':
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_END_EXPR':
            self.output_space_before_token = True
            prefix = 'NEWLINE'

        if token_text in self.line_starters:
            if self.flags.last_text == 'else':
                prefix = 'SPACE'
            else:
                prefix = 'NEWLINE'

        if token_text in ['else', 'catch', 'finally']:
            if self.last_type != 'TK_END_BLOCK' \
               or self.opts.brace_style == 'expand' \
               or self.opts.brace_style == 'end-expand':
                self.append_newline()
            else:
                self.trim_output(True)
                line = self.output_lines[-1]
                # If we trimmed and there's something other than a close block before us
                # put a newline back in.  Handles '} // comment' scenario.
                if line.text[-1] != '}':
                    self.append_newline()

                self.output_space_before_token = True

        elif prefix == 'NEWLINE':
            if self.is_special_word(self.flags.last_text):
                # no newline between return nnn
                self.output_space_before_token = True
            elif self.last_type != 'TK_END_EXPR':
                if (self.last_type != 'TK_START_EXPR' or token_text != 'var') and self.flags.last_text != ':':
                    # no need to force newline on VAR -
                    # for (var x = 0...
                    if token_text == 'if' and self.flags.last_word == 'else' and self.flags.last_text != '{':
                        self.output_space_before_token = True
                    else:
                        self.flags.var_line = False
                        self.flags.var_line_reindented = False
                        self.append_newline()
            elif token_text in self.line_starters and self.flags.last_text != ')':
                self.flags.var_line = False
                self.flags.var_line_reindented = False
                self.append_newline()
        elif self.is_array(self.flags.mode) and self.flags.last_text == ',' and self.last_last_text == '}':
            self.append_newline() # }, in lists get a newline
        elif prefix == 'SPACE':
            self.output_space_before_token = True


        self.append_token(token_text)
        self.flags.last_word = token_text

        if token_text == 'var':
            self.flags.var_line = True
            self.flags.var_line_reindented = False
            self.flags.var_line_tainted = False


        if token_text == 'do':
            self.flags.do_block = True

        if token_text == 'if':
            self.flags.if_block = True


    def handle_semicolon(self, token_text):
        if self.start_of_statement():
            # The conditional starts the statement if appropriate.
            # Semicolon can be the start (and end) of a statement
            self.output_space_before_token = False
        while self.flags.mode == MODE.Statement and not self.flags.if_block and not self.flags.do_block:
            self.restore_mode()

        self.append_token(token_text)
        self.flags.var_line = False
        self.flags.var_line_reindented = False
        if self.flags.mode == MODE.ObjectLiteral:
            # OBJECT mode is weird and doesn't get reset too well.
            self.flags.mode = MODE.BlockStatement


    def handle_string(self, token_text):
        if self.start_of_statement():
            # The conditional starts the statement if appropriate.
            # One difference - strings want at least a space before
            self.output_space_before_token = True
        elif self.last_type == 'TK_WORD':
            self.output_space_before_token = True
        elif self.last_type in ['TK_COMMA', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR']:
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(token_text)
        else:
            self.append_newline()

        self.append_token(token_text)


    def handle_equals(self, token_text):
        if self.flags.var_line:
            # just got an '=' in a var-line, different line breaking rules will apply
            self.flags.var_line_tainted = True

        self.output_space_before_token = True
        self.append_token(token_text)
        self.output_space_before_token = True


    def handle_comma(self, token_text):
        if self.flags.var_line:
            if self.is_expression(self.flags.mode) or self.last_type == 'TK_END_BLOCK':
                # do not break on comma, for ( var a = 1, b = 2
                self.flags.var_line_tainted = False

            if self.flags.var_line:
                self.flags.var_line_reindented = True

            self.append_token(token_text)

            if self.flags.var_line_tainted:
                self.flags.var_line_tainted = False
                self.append_newline()
            else:
                self.output_space_before_token = True

            return

        if self.last_type == 'TK_END_BLOCK' and self.flags.mode != MODE.Expression:
            self.append_token(token_text)
            if self.flags.mode == MODE.ObjectLiteral and self.flags.last_text == '}':
                self.append_newline()
            else:
                self.output_space_before_token = True
        else:
            if self.flags.mode == MODE.ObjectLiteral:
                self.append_token(token_text)
                self.append_newline()
            else:
                # EXPR or DO_BLOCK
                self.append_token(token_text)
                self.output_space_before_token = True


    def handle_operator(self, token_text):
        space_before = True
        space_after = True

        if self.is_special_word(self.flags.last_text):
            # return had a special handling in TK_WORD
            self.output_space_before_token = True
            self.append_token(token_text)
            return

        # hack for actionscript's import .*;
        if token_text == '*' and self.last_type == 'TK_DOT' and not self.last_last_text.isdigit():
            self.append_token(token_text)
            return


        if token_text == ':' and self.flags.in_case:
            self.flags.case_body = True
            self.indent()
            self.append_token(token_text)
            self.append_newline()
            self.flags.in_case = False
            return

        if token_text == '::':
            # no spaces around the exotic namespacing syntax operator
            self.append_token(token_text)
            return

        # http://www.ecma-international.org/ecma-262/5.1/#sec-7.9.1
        # if there is a newline between -- or ++ and anything else we should preserve it.
        if self.input_wanted_newline and (token_text == '--' or token_text == '++'):
            self.append_newline()


        if token_text in ['--', '++', '!'] \
                or (token_text in ['+', '-'] \
                    and (self.last_type in ['TK_START_BLOCK', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR'] \
                    or self.flags.last_text in self.line_starters or self.flags.last_text == ',')):

            space_before = False
            space_after = False

            if self.flags.last_text == ';' and self.is_expression(self.flags.mode):
                # for (;; ++i)
                #         ^^
                space_before = True

            if self.last_type == 'TK_WORD' and self.flags.last_text in self.line_starters:
                space_before = True

            if self.flags.mode == MODE.BlockStatement and self.flags.last_text in ['{', ';']:
                # { foo: --i }
                # foo(): --bar
                self.append_newline()

        elif token_text == ':':
            if self.flags.ternary_depth == 0:
                if self.flags.mode == MODE.BlockStatement:
                    self.flags.mode = MODE.ObjectLiteral
                space_before = False
            else:
                self.flags.ternary_depth -= 1
        elif token_text == '?':
            self.flags.ternary_depth += 1

        if space_before:
            self.output_space_before_token = True

        self.append_token(token_text)

        if space_after:
            self.output_space_before_token = True



    def handle_block_comment(self, token_text):
        lines = token_text.replace('\x0d', '').split('\x0a')
        javadoc = False

        # block comment starts with a new line
        self.append_newline(preserve_statement_flags = True)
        if  len(lines) > 1:
            if not any(l for l in lines[1:] if ( l.strip() == '' or (l.lstrip())[0] != '*')):
                javadoc = True

        # first line always indented
        self.append_token(lines[0])
        for line in lines[1:]:
            self.append_newline(preserve_statement_flags = True)
            if javadoc:
                # javadoc: reformat and re-indent
                self.append_token(' ' + line.strip())
            else:
                # normal comments output raw
                self.output_lines[-1].text.append(line)

        self.append_newline(preserve_statement_flags = True)

    def handle_inline_comment(self, token_text):
        self.output_space_before_token = True
        self.append_token(token_text)
        self.output_space_before_token = True


    def handle_comment(self, token_text):
        if self.input_wanted_newline:
            self.append_newline(preserve_statement_flags = True)

        if not self.input_wanted_newline:
            self.trim_output(True)

        self.output_space_before_token = True
        self.append_token(token_text)
        self.append_newline(preserve_statement_flags = True)


    def handle_dot(self, token_text):
        if self.is_special_word(self.flags.last_text):
            self.output_space_before_token = True
        else:
            # allow preserved newlines before dots in general
            # force newlines on dots after close paren when break_chained - for bar().baz()
            self.allow_wrap_or_preserved_newline(token_text,
                self.flags.last_text == ')' and self.opts.break_chained_methods)

        self.append_token(token_text)

    def handle_unknown(self, token_text):
        self.append_token(token_text)
        if token_text[len(token_text) - 1] == '\n':
            self.append_newline()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def main():

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:c:o:dPjbkil:xhtfvXw:",
            ['indent-size=','indent-char=','outfile=', 'disable-preserve-newlines',
            'space-in-paren', 'jslint-happy', 'brace-style=', 'keep-array-indentation',
            'indent-level=', 'unescape-strings', 'help', 'usage', 'stdin', 'eval-code',
            'indent-with-tabs', 'keep-function-indentation', 'version', 'e4x', 'wrap-line-length'])
    except getopt.GetoptError as ex:
        print(ex, file=sys.stderr)
        return usage(sys.stderr)

    js_options = default_options()

    file = None
    outfile = 'stdout'
    if len(args) == 1:
        file = args[0]

    for opt, arg in opts:
        if opt in ('--keep-array-indentation', '-k'):
            js_options.keep_array_indentation = True
        if opt in ('--keep-function-indentation','-f'):
            js_options.keep_function_indentation = True
        elif opt in ('--outfile', '-o'):
            outfile = arg
        elif opt in ('--indent-size', '-s'):
            js_options.indent_size = int(arg)
        elif opt in ('--indent-char', '-c'):
            js_options.indent_char = arg
        elif opt in ('--indent-with-tabs', '-t'):
            js_options.indent_with_tabs = True
        elif opt in ('--disable-preserve-newlines', '-d'):
            js_options.preserve_newlines = False
        elif opt in ('--space-in-paren', '-P'):
            js_options.space_in_paren = True
        elif opt in ('--jslint-happy', '-j'):
            js_options.jslint_happy = True
        elif opt in ('--eval-code'):
            js_options.eval_code = True
        elif opt in ('--brace-style', '-b'):
            js_options.brace_style = arg
        elif opt in ('--unescape-strings', '-x'):
            js_options.unescape_strings = True
        elif opt in ('--e4x', '-X'):
            js_options.e4x = True
        elif opt in ('--wrap-line-length ', '-w'):
            js_options.wrap_line_length = int(arg)
        elif opt in ('--stdin', '-i'):
            file = '-'
        elif opt in ('--version', '-v'):
            return print(__version__)
        elif opt in ('--help', '--usage', '-h'):
            return usage()


    if not file:
        print("Must define at least one file.", file=sys.stderr)
        return usage(sys.stderr)
    else:
        try:
            if outfile == 'stdout':
                print(beautify_file(file, js_options))
            else:
                mkdir_p(os.path.dirname(outfile))
                with open(outfile, 'w') as f:
                    f.write(beautify_file(file, js_options) + '\n')
        except Exception as ex:
            print(ex, file=sys.stderr)
            return 1

    # Success
    return 0
