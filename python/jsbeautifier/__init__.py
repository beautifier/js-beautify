import sys
import getopt
import re
import string

#
# Originally written by Einar Lielmanis et al.,
# Conversion to python by Einar Lielmanis, einar@jsbeautifier.org,
# MIT licence, enjoy.
#
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
        self.max_preserve_newlines = 10.
        self.jslint_happy = False
        self.brace_style = 'collapse'
        self.keep_array_indentation = False
        self.keep_function_indentation = False
        self.eval_code = False
        self.unescape_strings = False
        self.break_chained_methods = False



    def __repr__(self):
        return \
"""indent_size = %d
indent_char = [%s]
preserve_newlines = %s
max_preserve_newlines = %d
jslint_happy = %s
indent_with_tabs = %s
brace_style = %s
keep_array_indentation = %s
eval_code = %s
unescape_strings = %s
""" % ( self.indent_size,
        self.indent_char,
        self.preserve_newlines,
        self.max_preserve_newlines,
        self.jslint_happy,
        self.indent_with_tabs,
        self.brace_style,
        self.keep_array_indentation,
        self.eval_code,
        self.unescape_strings,
        )


class BeautifierFlags:
    def __init__(self, mode):
        self.previous_mode = 'BLOCK'
        self.mode = mode
        self.var_line = False
        self.var_line_tainted = False
        self.var_line_reindented = False
        self.in_html_comment = False
        self.if_line = False
        self.chain_extra_indentation = 0
        self.in_case = False
        self.in_case_statement = False
        self.case_body = False
        self.eat_next_space = False
        self.indentation_level = 0
        self.ternary_depth = 0


def default_options():
    return BeautifierOptions()


def beautify(string, opts = default_options() ):
    b = Beautifier()
    return b.beautify(string, opts)

def beautify_file(file_name, opts = default_options() ):

    if file_name == '-': # stdin
        f = sys.stdin
    else:
        try:
            f = open(file_name)
        except Exception as ex:
            return 'The file could not be opened'

    b = Beautifier()
    return b.beautify(''.join(f.readlines()), opts)


def usage():

    print("""Javascript beautifier (http://jsbeautifier.org/)

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
 -j,  --jslint-happy               more jslint-compatible output
 -b,  --brace-style=collapse       brace style (collapse, expand, end-expand)
 -k,  --keep-array-indentation     keep array indentation.
 -o,  --outfile=FILE               specify a file to output to (default stdout)
 -f,  --keep-function-indentation  Do not re-indent function bodies defined in var lines.
 -x,  --unescape-strings          Decode printable chars encoded in \\xNN notation.

Rarely needed options:

 --eval-code                       evaluate code if a JS interpreter is
                                   installed. May be useful with some obfuscated
                                   script but poses a potential security issue.

 -l,  --indent-level=NUMBER        initial indentation level. (default 0).

 -h,  --help, --usage              prints this help statement.

""")






class Beautifier:

    def __init__(self, opts = default_options() ):

        self.opts = opts
        self.blank_state()

    def blank_state(self):

        # internal flags
        self.flags = BeautifierFlags('BLOCK')
        self.flag_store = []
        self.wanted_newline = False
        self.just_added_newline = False
        self.do_block_just_closed = False

        if self.opts.indent_with_tabs:
            self.indent_string = "\t"
        else:
            self.indent_string = self.opts.indent_char * self.opts.indent_size

        self.preindent_string = ''
        self.last_word = ''              # last TK_WORD seen
        self.last_type = 'TK_START_EXPR' # last token type
        self.last_text = ''              # last token text
        self.last_last_text = ''         # pre-last token text

        self.input = None
        self.output = []                 # formatted javascript gets built here

        self.whitespace = ["\n", "\r", "\t", " "]
        self.wordchar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$'
        self.digits = '0123456789'
        self.punct = '+ - * / % & ++ -- = += -= *= /= %= == === != !== > < >= <= >> << >>> >>>= >>= <<= && &= | || ! !! , : ? ^ ^= |= ::'
        self.punct += ' <?= <? ?> <%= <% %>'
        self.punct = self.punct.split(' ')


        # Words which always should start on a new line
        self.line_starters = 'continue,try,throw,return,var,if,switch,case,default,for,while,break,function'.split(',')
        self.set_mode('BLOCK')

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
        while True:
            token_text, token_type = self.get_next_token()
            #print (token_text, token_type, self.flags.mode)
            if token_type == 'TK_EOF':
                break

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

            handlers[token_type](token_text)

            self.last_last_text = self.last_text
            self.last_type = token_type
            self.last_text = token_text

        sweet_code = self.preindent_string + re.sub('[\n ]+$', '', ''.join(self.output))
        return sweet_code

    def unpack(self, source, evalcode=False):
        import jsbeautifier.unpackers as unpackers
        try:
            return unpackers.run(source, evalcode)
        except unpackers.UnpackingError as error:
            print('error:', error)
            return ''

    def trim_output(self, eat_newlines = False):
        while len(self.output) \
              and (
                  self.output[-1] == ' '\
                  or self.output[-1] == self.indent_string \
                  or self.output[-1] == self.preindent_string \
                  or (eat_newlines and self.output[-1] in ['\n', '\r'])):
            self.output.pop()

    def is_special_word(self, s):
        return s in ['case', 'return', 'do', 'if', 'throw', 'else'];

    def is_array(self, mode):
        return mode in ['[EXPRESSION]', '[INDENTED-EXPRESSION]']


    def is_expression(self, mode):
        return mode in ['[EXPRESSION]', '[INDENTED-EXPRESSION]', '(EXPRESSION)', '(FOR-EXPRESSION)', '(COND-EXPRESSION)']


    def append_newline_forced(self):
        old_array_indentation = self.opts.keep_array_indentation
        self.opts.keep_array_indentation = False
        self.append_newline()
        self.opts.keep_array_indentation = old_array_indentation

    def append_newline(self, ignore_repeated = True, reset_statement_flags = True):

        self.flags.eat_next_space = False

        if self.opts.keep_array_indentation and self.is_array(self.flags.mode):
            return

        if reset_statement_flags:
            self.flags.if_line = False
            self.flags.chain_extra_indentation = 0

        self.trim_output()

        if len(self.output) == 0:
            # no newline on start of file
            return

        if self.output[-1] != '\n' or not ignore_repeated:
            self.just_added_newline = True
            self.output.append('\n')

        if self.preindent_string:
            self.output.append(self.preindent_string)

        for i in range(self.flags.indentation_level + self.flags.chain_extra_indentation):
            self.output.append(self.indent_string)

        if self.flags.var_line and self.flags.var_line_reindented:
            self.output.append(self.indent_string)


    def append(self, s):
        if s == ' ':
            # do not add just a single space after the // comment, ever
            if self.last_type == 'TK_COMMENT':
                return self.append_newline()

            # make sure only single space gets drawn
            if self.flags.eat_next_space:
                self.flags.eat_next_space = False
            elif len(self.output) and self.output[-1] not in [' ', '\n', self.indent_string]:
                self.output.append(' ')
        else:
            self.just_added_newline = False
            self.flags.eat_next_space = False
            self.output.append(s)


    def indent(self):
        self.flags.indentation_level = self.flags.indentation_level + 1


    def remove_indent(self):
        if len(self.output) and self.output[-1] in [self.indent_string, self.preindent_string]:
            self.output.pop()


    def set_mode(self, mode):

        prev = BeautifierFlags('BLOCK')

        if self.flags:
            self.flag_store.append(self.flags)
            prev = self.flags

        self.flags = BeautifierFlags(mode)

        if len(self.flag_store) == 1:
            self.flags.indentation_level = 0
        else:
            self.flags.indentation_level = prev.indentation_level
            if prev.var_line and prev.var_line_reindented:
                self.flags.indentation_level = self.flags.indentation_level + 1
        self.flags.previous_mode = prev.mode


    def restore_mode(self):
        self.do_block_just_closed = self.flags.mode == 'DO_BLOCK'
        if len(self.flag_store) > 0:
            mode = self.flags.mode
            self.flags = self.flag_store.pop()
            self.flags.previous_mode = mode


    def get_next_token(self):

        self.n_newlines = 0

        if self.parser_pos >= len(self.input):
            return '', 'TK_EOF'

        self.wanted_newline = False
        c = self.input[self.parser_pos]
        self.parser_pos += 1

        keep_whitespace = self.opts.keep_array_indentation and self.is_array(self.flags.mode)

        if keep_whitespace:
            whitespace_count = 0
            while c in self.whitespace:
                if c == '\n':
                    self.trim_output()
                    self.output.append('\n')
                    self.just_added_newline = True
                    whitespace_count = 0
                elif c == '\t':
                    whitespace_count += 4
                elif c == '\r':
                    pass
                else:
                    whitespace_count += 1

                if self.parser_pos >= len(self.input):
                    return '', 'TK_EOF'

                c = self.input[self.parser_pos]
                self.parser_pos += 1

            if self.just_added_newline:
                for i in range(whitespace_count):
                    self.output.append(' ')

        else: # not keep_whitespace
            while c in self.whitespace:
                if c == '\n':
                    if self.opts.max_preserve_newlines == 0 or self.opts.max_preserve_newlines > self.n_newlines:
                        self.n_newlines += 1

                if self.parser_pos >= len(self.input):
                    return '', 'TK_EOF'

                c = self.input[self.parser_pos]
                self.parser_pos += 1

            if self.opts.preserve_newlines and self.n_newlines > 1:
                for i in range(self.n_newlines):
                    self.append_newline(i == 0)
                    self.just_added_newline = True

            self.wanted_newline = self.n_newlines > 0


        if c in self.wordchar:
            if self.parser_pos < len(self.input):
                while self.input[self.parser_pos] in self.wordchar:
                    c = c + self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos == len(self.input):
                        break

            # small and surprisingly unugly hack for 1E-10 representation
            if self.parser_pos != len(self.input) and self.input[self.parser_pos] in '+-' \
               and re.match('^[0-9]+[Ee]$', c):

                sign = self.input[self.parser_pos]
                self.parser_pos += 1
                t = self.get_next_token()
                c += sign + t[0]
                return c, 'TK_WORD'

            if c == 'in': # in is an operator, need to hack
                return c, 'TK_OPERATOR'

            if self.wanted_newline and \
               self.last_type != 'TK_OPERATOR' and\
               self.last_type != 'TK_EQUALS' and\
               not self.flags.if_line and \
               (self.opts.preserve_newlines or self.last_text != 'var'):
                self.append_newline()

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
                if self.wanted_newline:
                    self.append_newline()
                return comment, 'TK_COMMENT'



        if c == "'" or c == '"' or \
           (c == '/' and ((self.last_type == 'TK_WORD' and self.is_special_word(self.last_text)) or \
                          (self.last_type == 'TK_END_EXPR' and self.flags.previous_mode in ['(FOR-EXPRESSION)', '(COND-EXPRESSION)']) or \
                          (self.last_type in ['TK_COMMENT', 'TK_START_EXPR', 'TK_START_BLOCK', 'TK_END_BLOCK', 'TK_OPERATOR',
                                              'TK_EQUALS', 'TK_EOF', 'TK_SEMICOLON', 'TK_COMMA']))):
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
            if len(self.output) == 0 and len(self.input) > 1 and self.input[self.parser_pos] == '!':
                resulting_string = c
                while self.parser_pos < len(self.input) and c != '\n':
                    c = self.input[self.parser_pos]
                    resulting_string += c
                    self.parser_pos += 1
                self.output.append(resulting_string.strip() + "\n")
                self.append_newline()
                return self.get_next_token()


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
            if self.wanted_newline:
                self.append_newline()
            return '-->', 'TK_COMMENT'

        if c == '.':
            return c, 'TK_DOT'

        if c in self.punct:
            while self.parser_pos < len(self.input) and c + self.input[self.parser_pos] in self.punct:
                c += self.input[self.parser_pos]
                self.parser_pos += 1
                if self.parser_pos >= len(self.input):
                    break
            if c == '=':
                return c, 'TK_EQUALS'

            if c == ',':
                return c, 'TK_COMMA'
            return c, 'TK_OPERATOR'

        return c, 'TK_UNKNOWN'



    def handle_start_expr(self, token_text):
        if token_text == '[':
            if self.last_type == 'TK_WORD' or self.last_text == ')':
                if self.last_text in self.line_starters:
                    self.append(' ')
                self.set_mode('(EXPRESSION)')
                self.append(token_text)
                return

            if self.flags.mode in ['[EXPRESSION]', '[INDENTED-EXPRESSION]']:
                if self.last_last_text == ']' and self.last_text == ',':
                    # ], [ goes to a new line
                    if self.flags.mode == '[EXPRESSION]':
                        self.flags.mode = '[INDENTED-EXPRESSION]'
                        if not self.opts.keep_array_indentation:
                            self.indent()
                    self.set_mode('[EXPRESSION]')
                    if not self.opts.keep_array_indentation:
                        self.append_newline()
                elif self.last_text == '[':
                    if self.flags.mode == '[EXPRESSION]':
                        self.flags.mode = '[INDENTED-EXPRESSION]'
                        if not self.opts.keep_array_indentation:
                            self.indent()
                    self.set_mode('[EXPRESSION]')

                    if not self.opts.keep_array_indentation:
                        self.append_newline()
                else:
                    self.set_mode('[EXPRESSION]')
            else:
                self.set_mode('[EXPRESSION]')
        else:
            if self.last_text == 'for':
                self.set_mode('(FOR-EXPRESSION)')
            elif self.last_text in ['if', 'while']:
                self.set_mode('(COND-EXPRESSION)')
            else:
                self.set_mode('(EXPRESSION)')


        if self.last_text == ';' or self.last_type == 'TK_START_BLOCK':
            self.append_newline()
        elif self.last_type in ['TK_END_EXPR', 'TK_START_EXPR', 'TK_END_BLOCK'] or self.last_text == '.':
            # do nothing on (( and )( and ][ and ]( and .(
            if self.wanted_newline:
                self.append_newline();
        elif self.last_type not in ['TK_WORD', 'TK_OPERATOR']:
            self.append(' ')
        elif self.last_word == 'function' or self.last_word == 'typeof':
            # function() vs function (), typeof() vs typeof ()
            if self.opts.jslint_happy:
                self.append(' ')
        elif self.last_text in self.line_starters or self.last_text == 'catch':
            self.append(' ')

        self.append(token_text)


    def handle_end_expr(self, token_text):
        if token_text == ']':
            if self.opts.keep_array_indentation:
                if self.last_text == '}':
                    self.remove_indent()
                    self.append(token_text)
                    self.restore_mode()
                    return
            else:
                if self.flags.mode == '[INDENTED-EXPRESSION]':
                    if self.last_text == ']':
                        self.restore_mode()
                        self.append_newline()
                        self.append(token_text)
                        return
        self.restore_mode()
        self.append(token_text)


    def handle_start_block(self, token_text):
        if self.last_word == 'do':
            self.set_mode('DO_BLOCK')
        else:
            self.set_mode('BLOCK')

        if self.opts.brace_style == 'expand':
            if self.last_type != 'TK_OPERATOR':
                if self.last_text == '=' or (self.is_special_word(self.last_text) and self.last_text != 'else'):
                    self.append(' ')
                else:
                    self.append_newline(True)

            self.append(token_text)
            self.indent()
        else:
            if self.last_type not in ['TK_OPERATOR', 'TK_START_EXPR']:
                if self.last_type == 'TK_START_BLOCK':
                    self.append_newline()
                else:
                    self.append(' ')
            else:
                # if TK_OPERATOR or TK_START_EXPR
                if self.is_array(self.flags.previous_mode) and self.last_text == ',':
                    if self.last_last_text == '}':
                        self.append(' ')
                    else:
                        self.append_newline()
            self.indent()
            self.append(token_text)


    def handle_end_block(self, token_text):
        self.restore_mode()
        if self.opts.brace_style == 'expand':
            if self.last_text != '{':
                self.append_newline()
        else:
            if self.last_type == 'TK_START_BLOCK':
                if self.just_added_newline:
                    self.remove_indent()
                else:
                    # {}
                    self.trim_output()
            else:
                if self.is_array(self.flags.mode) and self.opts.keep_array_indentation:
                    self.opts.keep_array_indentation = False
                    self.append_newline()
                    self.opts.keep_array_indentation = True
                else:
                    self.append_newline()

        self.append(token_text)


    def handle_word(self, token_text):
        if self.do_block_just_closed:
            self.append(' ')
            self.append(token_text)
            self.append(' ')
            self.do_block_just_closed = False
            return

        if token_text == 'function':

            if self.flags.var_line and self.last_text != '=':
                self.flags.var_line_reindented = not self.opts.keep_function_indentation
            if (self.just_added_newline or self.last_text == ';') and self.last_text != '{':
                # make sure there is a nice clean space of at least one blank line
                # before a new function definition
                have_newlines = self.n_newlines
                if not self.just_added_newline:
                    have_newlines = 0
                if not self.opts.preserve_newlines:
                    have_newlines = 1
                for i in range(2 - have_newlines):
                    self.append_newline(False)

            if self.last_text in ['get', 'set', 'new'] or self.last_type == 'TK_WORD':
                self.append(' ')

            if self.last_type == 'TK_WORD':
                if self.last_text in ['get', 'set', 'new', 'return']:
                    self.append(' ')
                else:
                    self.append_newline()
            elif self.last_type == 'TK_OPERATOR' or self.last_text == '=':
                # foo = function
                self.append(' ')
            elif self.is_expression(self.flags.mode):
                # (function
                pass
            else:
                self.append_newline()

            self.append('function')
            self.last_word = 'function'
            return

        if token_text == 'case' or (token_text == 'default' and self.flags.in_case_statement):
            self.append_newline()
            if self.flags.case_body:
                self.remove_indent();
                self.flags.case_body = False
                self.flags.indentation_level -= 1;
            self.append(token_text)
            self.flags.in_case = True
            self.flags.in_case_statement = True
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
                    self.append(' ')
        elif self.last_type == 'TK_SEMICOLON' and self.flags.mode in ['BLOCK', 'DO_BLOCK']:
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_SEMICOLON' and self.is_expression(self.flags.mode):
            prefix = 'SPACE'
        elif self.last_type == 'TK_STRING':
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_WORD':
            if self.last_text == 'else':
                # eat newlines between ...else *** some_op...
                # won't preserve extra newlines in this place (if any), but don't care that much
                self.trim_output(True)
            prefix = 'SPACE'
        elif self.last_type == 'TK_START_BLOCK':
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_END_EXPR':
            self.append(' ')
            prefix = 'NEWLINE'

        if self.flags.if_line and self.last_type == 'TK_END_EXPR':
            self.flags.if_line = False

        if token_text in self.line_starters:
            if self.last_text == 'else':
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
                self.append(' ')
        elif prefix == 'NEWLINE':
            if self.is_special_word(self.last_text):
                # no newline between return nnn
                self.append(' ')
            elif self.last_type != 'TK_END_EXPR':
                if (self.last_type != 'TK_START_EXPR' or token_text != 'var') and self.last_text != ':':
                    # no need to force newline on VAR -
                    # for (var x = 0...
                    if token_text == 'if' and self.last_word == 'else' and self.last_text != '{':
                        self.append(' ')
                    else:
                        self.flags.var_line = False
                        self.flags.var_line_reindented = False
                        self.append_newline()
            elif token_text in self.line_starters and self.last_text != ')':
                self.flags.var_line = False
                self.flags.var_line_reindented = False
                self.append_newline()
        elif self.is_array(self.flags.mode) and self.last_text == ',' and self.last_last_text == '}':
            self.append_newline() # }, in lists get a newline
        elif prefix == 'SPACE':
            self.append(' ')


        self.append(token_text)
        self.last_word = token_text

        if token_text == 'var':
            self.flags.var_line = True
            self.flags.var_line_reindented = False
            self.flags.var_line_tainted = False


        if token_text == 'if':
            self.flags.if_line = True

        if token_text == 'else':
            self.flags.if_line = False


    def handle_semicolon(self, token_text):
        self.append(token_text)
        self.flags.var_line = False
        self.flags.var_line_reindented = False
        if self.flags.mode == 'OBJECT':
            # OBJECT mode is weird and doesn't get reset too well.
            self.flags.mode = 'BLOCK'


    def handle_string(self, token_text):
        if self.last_type == 'TK_END_EXPR' and self.flags.previous_mode in ['(COND-EXPRESSION)', '(FOR-EXPRESSION)']:
            self.append(' ')
        elif self.last_type == 'TK_WORD':
            self.append(' ')
        elif self.last_type in ['TK_COMMA', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR']:
            if self.opts.preserve_newlines and self.wanted_newline and self.flags.mode != 'OBJECT':
                self.append_newline()
                self.append(self.indent_string)
        else:
            self.append_newline()

        self.append(token_text)


    def handle_equals(self, token_text):
        if self.flags.var_line:
            # just got an '=' in a var-line, different line breaking rules will apply
            self.flags.var_line_tainted = True

        self.append(' ')
        self.append(token_text)
        self.append(' ')


    def handle_comma(self, token_text):


        if self.last_type == 'TK_COMMENT':
            self.append_newline();

        if self.flags.var_line:
            if self.is_expression(self.flags.mode) or self.last_type == 'TK_END_BLOCK':
                # do not break on comma, for ( var a = 1, b = 2
                self.flags.var_line_tainted = False
            if self.flags.var_line_tainted:
                self.append(token_text)
                self.flags.var_line_reindented = True
                self.flags.var_line_tainted = False
                self.append_newline()
                return
            else:
                self.flags.var_line_tainted = False

            self.append(token_text)
            self.append(' ');
            return

        if self.last_type == 'TK_END_BLOCK' and self.flags.mode != '(EXPRESSION)':
            self.append(token_text)
            if self.flags.mode == 'OBJECT' and self.last_text == '}':
                self.append_newline()
            else:
                self.append(' ')
        else:
            if self.flags.mode == 'OBJECT':
                self.append(token_text)
                self.append_newline()
            else:
                # EXPR or DO_BLOCK
                self.append(token_text)
                self.append(' ')


    def handle_operator(self, token_text):
        space_before = True
        space_after = True

        if self.is_special_word(self.last_text):
            # return had a special handling in TK_WORD
            self.append(' ')
            self.append(token_text)
            return

        # hack for actionscript's import .*;
        if token_text == '*' and self.last_type == 'TK_DOT' and not self.last_last_text.isdigit():
            self.append(token_text)
            return


        if token_text == ':' and self.flags.in_case:
            self.flags.case_body = True
            self.indent();
            self.append(token_text)
            self.append_newline()
            self.flags.in_case = False
            return

        if token_text == '::':
            # no spaces around the exotic namespacing syntax operator
            self.append(token_text)
            return


        if token_text in ['--', '++', '!'] \
                or (token_text in ['+', '-'] \
                    and (self.last_type in ['TK_START_BLOCK', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR'] \
                    or self.last_text in self.line_starters or self.last_text == ',')):

            space_before = False
            space_after = False

            if self.last_text == ';' and self.is_expression(self.flags.mode):
                # for (;; ++i)
                #         ^^
                space_before = True

            if self.last_type == 'TK_WORD' and self.last_text in self.line_starters:
                space_before = True

            if self.flags.mode == 'BLOCK' and self.last_text in ['{', ';']:
                # { foo: --i }
                # foo(): --bar
                self.append_newline()

        elif token_text == ':':
            if self.flags.ternary_depth == 0:
                if self.flags.mode == 'BLOCK':
                    self.flags.mode = 'OBJECT'
                space_before = False
            else:
                self.flags.ternary_depth -= 1
        elif token_text == '?':
            self.flags.ternary_depth += 1

        if space_before:
            self.append(' ')

        self.append(token_text)

        if space_after:
            self.append(' ')



    def handle_block_comment(self, token_text):

        lines = token_text.replace('\x0d', '').split('\x0a')
        # all lines start with an asterisk? that's a proper box comment
        if not any(l for l in lines[1:] if ( l.strip() == '' or (l.lstrip())[0] != '*')):
            self.append_newline()
            self.append(lines[0])
            for line in lines[1:]:
                self.append_newline()
                self.append(' ' + line.strip())
        else:
            # simple block comment: leave intact
            if len(lines) > 1:
                # multiline comment starts on a new line
                self.append_newline()
            else:
                # single line /* ... */ comment stays on the same line
                self.append(' ')
            for line in lines:
                self.append(line)
                self.append('\n')
        self.append_newline()


    def handle_inline_comment(self, token_text):
        self.append(' ')
        self.append(token_text)
        if self.is_expression(self.flags.mode):
            self.append(' ')
        else:
            self.append_newline_forced()


    def handle_comment(self, token_text):
        if self.last_text == ',' and not self.wanted_newline:
            self.trim_output(True)

        if self.last_type != 'TK_COMMENT':
            if self.wanted_newline:
                self.append_newline()
            else:
                self.append(' ')

        self.append(token_text)
        self.append_newline();


    def handle_dot(self, token_text):
        if self.is_special_word(self.last_text):
            self.append(' ')
        elif self.last_text == ')':
            if self.opts.break_chained_methods or self.wanted_newline:
                self.flags.chain_extra_indentation = 1;
                self.append_newline(True, False)
        self.append(token_text)

    def handle_unknown(self, token_text):
        self.append(token_text)





def main():

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:c:o:djbkil:xhtf", ['indent-size=','indent-char=','outfile=', 'disable-preserve-newlines',
                                                          'jslint-happy', 'brace-style=',
                                                          'keep-array-indentation', 'indent-level=', 'unescape-strings', 'help',
                                                          'usage', 'stdin', 'eval-code', 'indent-with-tabs', 'keep-function-indentation'])
    except getopt.GetoptError:
        return usage()

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
        elif opt in ('--disable-preserve_newlines', '-d'):
            js_options.preserve_newlines = False
        elif opt in ('--jslint-happy', '-j'):
            js_options.jslint_happy = True
        elif opt in ('--eval-code'):
            js_options.eval_code = True
        elif opt in ('--brace-style', '-b'):
            js_options.brace_style = arg
        elif opt in ('--unescape-strings', '-x'):
            js_options.unescape_strings = True
        elif opt in ('--stdin', '-i'):
            file = '-'
        elif opt in ('--help', '--usage', '-h'):
            return usage()

    if not file:
        return usage()
    else:
        if outfile == 'stdout':
            print(beautify_file(file, js_options))
        else:
            with open(outfile, 'w') as f:
                f.write(beautify_file(file, js_options) + '\n')
