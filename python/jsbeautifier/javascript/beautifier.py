# The MIT License (MIT)
#
# Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import string
import copy
from .tokenizer import Tokenizer
from .options import BeautifierOptions
from ..core.options import mergeOpts
from ..core.output import Output

def default_options():
    return BeautifierOptions()

class BeautifierFlags:
    def __init__(self, mode):
        self.mode = mode
        self.parent = None
        self.last_text = ''
        self.last_word = ''
        self.declaration_statement = False
        self.declaration_assignment = False
        self.multiline_frame = False
        self.inline_frame = False
        self.if_block = False
        self.else_block = False
        self.do_block = False
        self.do_while = False
        self.import_block = False
        self.in_case = False
        self.in_case_statement = False
        self.case_body = False
        self.indentation_level = 0
        self.line_indent_level = 0
        self.start_line_index = 0
        self.ternary_depth = 0

    def apply_base(self, flags_base, added_newline):
        next_indent_level = flags_base.indentation_level
        if not added_newline and \
            flags_base.line_indent_level > next_indent_level:
            next_indent_level = flags_base.line_indent_level

        self.parent = flags_base
        self.last_text = flags_base.last_text
        self.last_word = flags_base.last_word
        self.indentation_level = next_indent_level


OPERATOR_POSITION = {
    'before_newline': 'before-newline',
    'after_newline': 'after-newline',
    'preserve_newline': 'preserve-newline'
}
OPERATOR_POSITION_BEFORE_OR_PRESERVE = [OPERATOR_POSITION['before_newline'], OPERATOR_POSITION['preserve_newline']];

def sanitizeOperatorPosition(opPosition):
    if not opPosition:
        return OPERATOR_POSITION['before_newline']
    elif opPosition not in OPERATOR_POSITION.values():
        raise ValueError("Invalid Option Value: The option 'operator_position' must be one of the following values\n" +
            str(OPERATOR_POSITION.values()) +
            "\nYou passed in: '" + opPosition + "'")

    return opPosition

class MODE:
      BlockStatement, Statement, ObjectLiteral, ArrayLiteral, \
      ForInitializer, Conditional, Expression = range(7)


def remove_redundant_indentation(output, frame):
    # This implementation is effective but has some issues:
    #     - can cause line wrap to happen too soon due to indent removal
    #           after wrap points are calculated
    # These issues are minor compared to ugly indentation.

    if frame.multiline_frame or frame.mode == MODE.ForInitializer or frame.mode == MODE.Conditional:
        return

    # remove one indent from each line inside this section
    index = frame.start_line_index
    while index < len(output.lines):
        output.lines[index].remove_indent()
        index += 1


class Beautifier:

    def __init__(self, opts = default_options() ):
        import jsbeautifier.core.acorn as acorn
        self.acorn = acorn
        self.opts = copy.copy(opts)
        self.blank_state()

    def blank_state(self, js_source_text = None):

        # internal flags
        self.flags = None
        self.previous_flags = None
        self.flag_store = []
        self.tokens = []
        self.token_pos = 0


        # force opts.space_after_anon_function to true if opts.jslint_happy
        if self.opts.jslint_happy:
            self.opts.space_after_anon_function = True

        if self.opts.indent_with_tabs:
            self.opts.indent_char = "\t"
            self.opts.indent_size = 1

        if self.opts.eol == 'auto':
            self.opts.eol = '\n'
            if self.acorn.lineBreak.search(js_source_text or ''):
                self.opts.eol = self.acorn.lineBreak.search(js_source_text).group()

        self.opts.eol = self.opts.eol.replace('\\r', '\r').replace('\\n', '\n')

        self.indent_string = self.opts.indent_char * self.opts.indent_size

        self.baseIndentString = ''
        self.last_type = 'TK_START_BLOCK' # last token type
        self.last_last_text = ''         # pre-last token text

        preindent_index = 0;
        if not js_source_text == None and len(js_source_text) > 0:
            while preindent_index < len(js_source_text) and \
                    js_source_text[preindent_index] in [' ', '\t'] :
                self.baseIndentString += js_source_text[preindent_index]
                preindent_index += 1
            js_source_text = js_source_text[preindent_index:]

        self.output = Output(self.indent_string, self.baseIndentString)
        # If testing the ignore directive, start with output disable set to true
        self.output.raw = self.opts.test_output_raw;

        self.set_mode(MODE.BlockStatement)
        return js_source_text



    def beautify(self, s, opts = None ):

        if opts != None:
            opts = mergeOpts(opts, 'js')
            self.opts = copy.copy(opts)


        #Compat with old form
        if self.opts.brace_style == 'collapse-preserve-inline':
            self.opts.brace_style = 'collapse,preserve-inline'

        split = re.compile("[^a-zA-Z0-9_\-]+").split(self.opts.brace_style)
        self.opts.brace_style = split[0]
        self.opts.brace_preserve_inline = (True if bool(split[1] == 'preserve-inline') else None) if len(split) > 1 else False

        if self.opts.brace_style not in ['expand', 'collapse', 'end-expand', 'none']:
            raise(Exception('opts.brace_style must be "expand", "collapse", "end-expand", or "none".'))

        if self.opts.brace_preserve_inline == None:
            raise(Exception('opts.brace_style second item must be "preserve-inline"'))

        s = self.blank_state(s)

        input = self.unpack(s, self.opts.eval_code)

        self.handlers = {
            'TK_START_EXPR': self.handle_start_expr,
            'TK_END_EXPR': self.handle_end_expr,
            'TK_START_BLOCK': self.handle_start_block,
            'TK_END_BLOCK': self.handle_end_block,
            'TK_WORD': self.handle_word,
            'TK_RESERVED': self.handle_word,
            'TK_SEMICOLON': self.handle_semicolon,
            'TK_STRING': self.handle_string,
            'TK_EQUALS': self.handle_equals,
            'TK_OPERATOR': self.handle_operator,
            'TK_COMMA': self.handle_comma,
            'TK_BLOCK_COMMENT': self.handle_block_comment,
            'TK_COMMENT': self.handle_comment,
            'TK_DOT': self.handle_dot,
            'TK_UNKNOWN': self.handle_unknown,
            'TK_EOF': self.handle_eof
        }

        self.tokens = Tokenizer(input, self.opts, self.indent_string).tokenize()
        self.token_pos = 0

        current_token = self.get_token()
        while current_token != None:
            self.handlers[current_token.type](current_token)

            self.last_last_text = self.flags.last_text
            self.last_type = current_token.type
            self.flags.last_text = current_token.text
            self.token_pos += 1
            current_token = self.get_token()


        sweet_code = self.output.get_code(self.opts.end_with_newline, self.opts.eol)

        return sweet_code


    def handle_whitespace_and_comments(self, local_token, preserve_statement_flags = False):
        newlines = local_token.newlines
        keep_whitespace = self.opts.keep_array_indentation and self.is_array(self.flags.mode)

        for comment_token in local_token.comments_before:
            # The cleanest handling of inline comments is to treat them as though they aren't there.
            # Just continue formatting and the behavior should be logical.
            # Also ignore unknown tokens.  Again, this should result in better behavior.
            self.handle_whitespace_and_comments(comment_token, preserve_statement_flags)
            self.handlers[comment_token.type](comment_token, preserve_statement_flags)


        if keep_whitespace:
             for i in range(newlines):
                    self.print_newline(i > 0, preserve_statement_flags)
        else: # not keep_whitespace
            if self.opts.max_preserve_newlines != 0 and newlines > self.opts.max_preserve_newlines:
                newlines = self.opts.max_preserve_newlines

            if self.opts.preserve_newlines and newlines > 1:
                self.print_newline(False, preserve_statement_flags)
                for i in range(1, newlines):
                    self.print_newline(True, preserve_statement_flags)


    def unpack(self, source, evalcode=False):
        import jsbeautifier.unpackers as unpackers
        try:
            return unpackers.run(source, evalcode)
        except unpackers.UnpackingError as error:
            return source

    def is_special_word(self, s):
        return s in ['case', 'return', 'do', 'if', 'throw', 'else']

    def is_array(self, mode):
        return mode == MODE.ArrayLiteral


    def is_expression(self, mode):
        return mode in [MODE.Expression, MODE.ForInitializer, MODE.Conditional]


    _newline_restricted_tokens = ['break','continue','return', 'throw', 'yield']
    def allow_wrap_or_preserved_newline(self, current_token, force_linewrap = False):
        # never wrap the first token of a line.
        if self.output.just_added_newline():
            return

        shouldPreserveOrForce = (self.opts.preserve_newlines and current_token.wanted_newline) or force_linewrap
        operatorLogicApplies = self.flags.last_text in Tokenizer.positionable_operators or current_token.text in Tokenizer.positionable_operators

        if operatorLogicApplies:
            shouldPrintOperatorNewline = (self.flags.last_text in Tokenizer.positionable_operators and self.opts.operator_position in OPERATOR_POSITION_BEFORE_OR_PRESERVE) \
                or current_token.text in Tokenizer.positionable_operators
            shouldPreserveOrForce = shouldPreserveOrForce and shouldPrintOperatorNewline

        if shouldPreserveOrForce:
            self.print_newline(preserve_statement_flags = True)
        elif self.opts.wrap_line_length > 0:
            if self.last_type == 'TK_RESERVED' and self.flags.last_text in self._newline_restricted_tokens:
                # These tokens should never have a newline inserted between
                # them and the following expression.
                return
            proposed_line_length = self.output.current_line.get_character_count() + len(current_token.text)
            if self.output.space_before_token:
                proposed_line_length += 1

            if proposed_line_length >= self.opts.wrap_line_length:
                self.print_newline(preserve_statement_flags = True)


    def print_newline(self, force_newline = False, preserve_statement_flags = False):
        if not preserve_statement_flags:
            if self.flags.last_text != ';' and self.flags.last_text != ',' and self.flags.last_text != '=' and self.last_type != 'TK_OPERATOR':
                next_token = self.get_token(1)
                while (self.flags.mode == MODE.Statement and
                        not (self.flags.if_block and next_token and next_token.type == 'TK_RESERVED' and next_token.text == 'else') and
                        not self.flags.do_block):
                    self.restore_mode()

        if self.output.add_new_line(force_newline):
            self.flags.multiline_frame = True

    def print_token_line_indentation(self, current_token):
        if self.output.just_added_newline():
            line = self.output.current_line
            if self.opts.keep_array_indentation and self.is_array(self.flags.mode) and current_token.wanted_newline:
                line.push(current_token.whitespace_before)
                self.output.space_before_token = False
            elif self.output.set_indent(self.flags.indentation_level):
                self.flags.line_indent_level = self.flags.indentation_level


    def print_token(self, current_token, s=None):
        if self.output.raw:
            self.output.add_raw_token(current_token)
            return

        if self.opts.comma_first and self.last_type == 'TK_COMMA' and self.output.just_added_newline():
            if self.output.previous_line.last() == ',':
                # if the comma was already at the start of the line,
                # pull back onto that line and reprint the indentation
                popped = self.output.previous_line.pop()
                if  self.output.previous_line.is_empty():
                     self.output.previous_line.push(popped)
                     self.output.trim(True)
                     self.output.current_line.pop()
                     self.output.trim()

                # add the comma in front of the next token
                self.print_token_line_indentation(current_token)
                self.output.add_token(',')
                self.output.space_before_token = True

        if s == None:
            s = current_token.text

        self.print_token_line_indentation(current_token)
        self.output.add_token(s);


    def indent(self):
        self.flags.indentation_level += 1

    def deindent(self):
        allow_deindent = self.flags.indentation_level > 0 and ((self.flags.parent == None) or self.flags.indentation_level > self.flags.parent.indentation_level)

        if allow_deindent:
            self.flags.indentation_level -= 1

    def set_mode(self, mode):
        if self.flags:
            self.flag_store.append(self.flags)
            self.previous_flags = self.flags
        else:
            self.previous_flags = BeautifierFlags(mode)

        self.flags = BeautifierFlags(mode)
        self.flags.apply_base(self.previous_flags, self.output.just_added_newline())
        self.flags.start_line_index = self.output.get_line_number();

    def restore_mode(self):
        if len(self.flag_store) > 0:
            self.previous_flags = self.flags
            self.flags = self.flag_store.pop()
            if self.previous_flags.mode == MODE.Statement and not self.opts.unindent_chained_methods:
                remove_redundant_indentation(self.output, self.previous_flags)


    def start_of_object_property(self):
        return self.flags.parent.mode == MODE.ObjectLiteral and self.flags.mode == MODE.Statement and \
                ((self.flags.last_text == ':' and self.flags.ternary_depth == 0) or (self.last_type == 'TK_RESERVED' and self.flags.last_text in ['get', 'set']))

    def start_of_statement(self, current_token):
        if (
            (self.last_type == 'TK_RESERVED' and self.flags.last_text in ['var', 'let', 'const'] and current_token.type == 'TK_WORD') \
                or (self.last_type == 'TK_RESERVED' and self.flags.last_text== 'do') \
                or (self.last_type == 'TK_RESERVED' and self.flags.last_text in self._newline_restricted_tokens and not current_token.wanted_newline) \
                or (self.last_type == 'TK_RESERVED' and self.flags.last_text == 'else' \
                    and not (current_token.type == 'TK_RESERVED' and current_token.text == 'if' and not len(current_token.comments_before))) \
                or (self.last_type == 'TK_END_EXPR' and (self.previous_flags.mode == MODE.ForInitializer or self.previous_flags.mode == MODE.Conditional)) \
                or (self.last_type == 'TK_WORD' and self.flags.mode == MODE.BlockStatement \
                    and not self.flags.in_case
                    and not (current_token.text == '--' or current_token.text == '++')
                    and self.last_last_text != 'function'
                    and current_token.type != 'TK_WORD' and current_token.type != 'TK_RESERVED') \
                or (self.flags.mode == MODE.ObjectLiteral and \
                    ((self.flags.last_text == ':' and self.flags.ternary_depth == 0) or (self.last_type == 'TK_RESERVED' and self.flags.last_text in ['get', 'set'])))
                ):

            self.set_mode(MODE.Statement)
            if not self.opts.unindent_chained_methods:
                self.indent()

            self.handle_whitespace_and_comments(current_token, True);

            # Issue #276:
            # If starting a new statement with [if, for, while, do], push to a new line.
            # if (a) if (b) if(c) d(); else e(); else f();
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(current_token, current_token.type == 'TK_RESERVED' and current_token.text in ['do', 'for', 'if', 'while'])

            return True
        else:
            return False

    def get_token(self, offset = 0):
        index = self.token_pos + offset
        if index < 0 or index >= len(self.tokens):
            return None
        else:
            return self.tokens[index]


    def handle_start_expr(self, current_token):
        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            pass
        else:
            self.handle_whitespace_and_comments(current_token)

        next_mode = MODE.Expression

        if current_token.text == '[':
            if self.last_type == 'TK_WORD' or self.flags.last_text == ')':
                if self.last_type == 'TK_RESERVED' and self.flags.last_text in Tokenizer.line_starters:
                    self.output.space_before_token = True
                self.set_mode(next_mode)
                self.print_token(current_token)
                self.indent()
                if self.opts.space_in_paren:
                    self.output.space_before_token = True
                return

            next_mode = MODE.ArrayLiteral

            if self.is_array(self.flags.mode):
                if self.flags.last_text == '[' or (
                    self.flags.last_text == ',' and (self.last_last_text == ']' or self.last_last_text == '}')):
                    # ], [ goes to a new line
                    # }, [ goes to a new line
                    if not self.opts.keep_array_indentation:
                        self.print_newline()

        else:
            if self.last_type == 'TK_RESERVED' and self.flags.last_text == 'for':
                next_mode = MODE.ForInitializer
            elif self.last_type == 'TK_RESERVED' and self.flags.last_text in ['if', 'while']:
                next_mode = MODE.Conditional
            else:
                next_mode = MODE.Expression


        if self.flags.last_text == ';' or self.last_type == 'TK_START_BLOCK':
            self.print_newline()
        elif self.last_type in ['TK_END_EXPR', 'TK_START_EXPR', 'TK_END_BLOCK'] or self.flags.last_text == '.':
            # do nothing on (( and )( and ][ and ]( and .(
            # TODO: Consider whether forcing this is required.  Review failing tests when removed.
            self.allow_wrap_or_preserved_newline(current_token, current_token.wanted_newline)

        elif not (self.last_type == 'TK_RESERVED' and current_token.text == '(') and self.last_type not in ['TK_WORD', 'TK_OPERATOR']:
            self.output.space_before_token = True
        elif (self.last_type == 'TK_RESERVED' and (self.flags.last_word == 'function' or self.flags.last_word == 'typeof')) or \
            (self.flags.last_text == '*' and (
                self.last_last_text in ['function', 'yield'] or
                (self.flags.mode == MODE.ObjectLiteral and self.last_last_text in ['{', ',']))):
            # function() vs function (), typeof() vs typeof ()
            # function*() vs function* (), yield*() vs yield* ()
            if self.opts.space_after_anon_function:
                self.output.space_before_token = True
        elif self.last_type == 'TK_RESERVED' and (self.flags.last_text in Tokenizer.line_starters or self.flags.last_text == 'catch'):
            # TODO: option space_before_conditional
            self.output.space_before_token = True

        elif current_token.text == '(' and self.last_type == 'TK_RESERVED' and self.flags.last_word == 'await':
            self.output.space_before_token = True


        # Support of this kind of newline preservation:
        # a = (b &&
        #     (c || d));
        if self.last_type in ['TK_EQUALS', 'TK_OPERATOR']:
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(current_token)


        # Support preserving wrapped arrow function expressions
        # a.b('c',
        #     () => d.e
        # )
        if current_token.text == '(' and self.last_type not in ['TK_WORD', 'TK_RESERVED']:
            self.allow_wrap_or_preserved_newline(current_token)


        self.set_mode(next_mode)
        self.print_token(current_token)

        if self.opts.space_in_paren:
            self.output.space_before_token = True

        # In all cases, if we newline while inside an expression it should be indented.
        self.indent()



    def handle_end_expr(self, current_token):
        # statements inside expressions are not valid syntax, but...
        # statements must all be closed when their container closes
        while self.flags.mode == MODE.Statement:
            self.restore_mode()

        self.handle_whitespace_and_comments(current_token)

        if self.flags.multiline_frame:
            self.allow_wrap_or_preserved_newline(current_token, current_token.text == ']' and self.is_array(self.flags.mode) and not self.opts.keep_array_indentation)

        if self.opts.space_in_paren:
            if self.last_type == 'TK_START_EXPR' and not self.opts.space_in_empty_paren:
                # empty parens are always "()" and "[]", not "( )" or "[ ]"
                self.output.space_before_token = False
                self.output.trim()
            else:
                self.output.space_before_token = True

        if current_token.text == ']' and self.opts.keep_array_indentation:
            self.print_token(current_token)
            self.restore_mode()
        else:
            self.restore_mode()
            self.print_token(current_token)

        remove_redundant_indentation(self.output, self.previous_flags)

        # do {} while () // no statement required after
        if self.flags.do_while and self.previous_flags.mode == MODE.Conditional:
            self.previous_flags.mode = MODE.Expression
            self.flags.do_block = False
            self.flags.do_while = False

    def handle_start_block(self, current_token):
        self.handle_whitespace_and_comments(current_token)

        # Check if this is a BlockStatement that should be treated as a ObjectLiteral
        next_token = self.get_token(1)
        second_token = self.get_token(2)
        if second_token != None and \
            ((second_token.text in [':', ','] and next_token.type in ['TK_STRING', 'TK_WORD', 'TK_RESERVED']) \
                or (next_token.text in ['get', 'set', '...'] and second_token.type in ['TK_WORD', 'TK_RESERVED'])):
            # We don't support TypeScript,but we didn't break it for a very long time.
            # We'll try to keep not breaking it.
            if not self.last_last_text in ['class','interface']:
                self.set_mode(MODE.ObjectLiteral)
            else:
                self.set_mode(MODE.BlockStatement)
        elif self.last_type == 'TK_OPERATOR' and self.flags.last_text == '=>':
            # arrow function: (param1, paramN) => { statements }
            self.set_mode(MODE.BlockStatement)
        elif self.last_type in ['TK_EQUALS', 'TK_START_EXPR', 'TK_COMMA', 'TK_OPERATOR'] or \
            (self.last_type == 'TK_RESERVED' and self.flags.last_text in ['return', 'throw', 'import', 'default']):
            # Detecting shorthand function syntax is difficult by scanning forward,
            #     so check the surrounding context.
            # If the block is being returned, imported, export default, passed as arg,
            #     assigned with = or assigned in a nested object, treat as an ObjectLiteral.
            self.set_mode(MODE.ObjectLiteral)
        else:
            self.set_mode(MODE.BlockStatement)

        empty_braces = (not next_token == None) and len(next_token.comments_before) == 0 and next_token.text == '}'
        empty_anonymous_function = empty_braces and self.flags.last_word == 'function' and \
            self.last_type == 'TK_END_EXPR'

        if self.opts.brace_preserve_inline: # check for inline, set inline_frame if so
            # search forward for newline wanted inside this block
            index = 0
            check_token = None
            self.flags.inline_frame = True
            do_loop = True
            while (do_loop):
                index += 1
                check_token = self.get_token(index)
                if check_token.wanted_newline:
                    self.flags.inline_frame = False

                do_loop = (check_token.type != 'TK_EOF' and
                      not (check_token.type == 'TK_END_BLOCK' and check_token.opened == current_token))

        if (self.opts.brace_style == 'expand' or \
            (self.opts.brace_style == 'none' and current_token.wanted_newline)) and \
            not self.flags.inline_frame:
            if self.last_type != 'TK_OPERATOR' and \
                (empty_anonymous_function or
                    self.last_type == 'TK_EQUALS' or
                    (self.last_type == 'TK_RESERVED' and self.is_special_word(self.flags.last_text) and self.flags.last_text != 'else')):
                self.output.space_before_token = True
            else:
                self.print_newline(preserve_statement_flags = True)
        else: # collapse || inline_frame
            if self.is_array(self.previous_flags.mode) and (self.last_type == 'TK_START_EXPR' or self.last_type == 'TK_COMMA'):
                # if we're preserving inline,
                # allow newline between comma and next brace.
                if self.flags.inline_frame:
                    self.allow_wrap_or_preserved_newline(current_token)
                    self.flags.inline_frame = True
                    self.previous_flags.multiline_frame = self.previous_flags.multiline_frame or self.flags.multiline_frame
                    self.flags.multiline_frame = False
                elif self.last_type == 'TK_COMMA':
                    self.output.space_before_token = True

            elif self.last_type not in ['TK_OPERATOR', 'TK_START_EXPR']:
                if self.last_type == 'TK_START_BLOCK' and not self.flags.inline_frame:
                    self.print_newline()
                else:
                    self.output.space_before_token = True

        self.print_token(current_token)
        self.indent()


    def handle_end_block(self, current_token):
        # statements must all be closed when their container closes
        self.handle_whitespace_and_comments(current_token)

        while self.flags.mode == MODE.Statement:
            self.restore_mode()

        empty_braces = self.last_type == 'TK_START_BLOCK'

        if self.flags.inline_frame and not empty_braces: # try inline_frame (only set if opt.braces-preserve-inline) first
            self.output.space_before_token = True;
        elif self.opts.brace_style == 'expand':
            if not empty_braces:
                self.print_newline()
        else:
            # skip {}
            if not empty_braces:
                if self.is_array(self.flags.mode) and self.opts.keep_array_indentation:
                    self.opts.keep_array_indentation = False
                    self.print_newline()
                    self.opts.keep_array_indentation = True
                else:
                    self.print_newline()

        self.restore_mode()
        self.print_token(current_token)


    def handle_word(self, current_token):
        if current_token.type == 'TK_RESERVED':
            if current_token.text in ['set', 'get'] and self.flags.mode != MODE.ObjectLiteral:
                current_token.type = 'TK_WORD'
            elif current_token.text in ['as', 'from'] and not self.flags.import_block:
                current_token.type = 'TK_WORD'
            elif self.flags.mode == MODE.ObjectLiteral:
                next_token = self.get_token(1)
                if next_token.text == ':':
                    current_token.type = 'TK_WORD'

        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            if self.last_type == 'TK_RESERVED' and self.flags.last_text in ['var', 'let', 'const'] and current_token.type == 'TK_WORD':
                self.flags.declaration_statement = True

        elif current_token.wanted_newline and \
                not self.is_expression(self.flags.mode) and \
                (self.last_type != 'TK_OPERATOR' or (self.flags.last_text == '--' or self.flags.last_text == '++')) and \
                self.last_type != 'TK_EQUALS' and \
                (self.opts.preserve_newlines or not (self.last_type == 'TK_RESERVED' and self.flags.last_text in ['var', 'let', 'const', 'set', 'get'])):
            self.handle_whitespace_and_comments(current_token)
            self.print_newline()
        else:
            self.handle_whitespace_and_comments(current_token)


        if self.flags.do_block and not self.flags.do_while:
            if current_token.type == 'TK_RESERVED' and current_token.text == 'while':
                # do {} ## while ()
                self.output.space_before_token = True
                self.print_token(current_token)
                self.output.space_before_token = True
                self.flags.do_while = True
                return
            else:
                # do {} should always have while as the next word.
                # if we don't see the expected while, recover
                self.print_newline()
                self.flags.do_block = False

        # if may be followed by else, or not
        # Bare/inline ifs are tricky
        # Need to unwind the modes correctly: if (a) if (b) c(); else d(); else e();
        if self.flags.if_block:
            if (not self.flags.else_block) and (current_token.type == 'TK_RESERVED' and current_token.text == 'else'):
                self.flags.else_block = True
            else:
                while self.flags.mode == MODE.Statement:
                    self.restore_mode()

                self.flags.if_block = False

        if current_token.type == 'TK_RESERVED' and (current_token.text == 'case' or (current_token.text == 'default' and self.flags.in_case_statement)):
            self.print_newline()
            if self.flags.case_body or self.opts.jslint_happy:
                self.flags.case_body = False
                self.deindent()
            self.print_token(current_token)
            self.flags.in_case = True
            self.flags.in_case_statement = True
            return

        if self.last_type in ['TK_COMMA', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR']:
            if not self.start_of_object_property():
                self.allow_wrap_or_preserved_newline(current_token)

        if current_token.type == 'TK_RESERVED' and current_token.text == 'function':
            if (self.flags.last_text in ['}', ';'] or
                (self.output.just_added_newline() and not (self.flags.last_text in ['(', '[', '{', ':', '=', ','] or self.last_type == 'TK_OPERATOR'))):
                # make sure there is a nice clean space of at least one blank line
                # before a new function definition, except in arrays
                if not self.output.just_added_blankline() and len(current_token.comments_before) == 0:
                    self.print_newline()
                    self.print_newline(True)

            if self.last_type == 'TK_RESERVED' or self.last_type == 'TK_WORD':
                if self.last_type == 'TK_RESERVED' and (
                    self.flags.last_text in ['get', 'set', 'new', 'export', 'async'] or
                    self.flags.last_text in self._newline_restricted_tokens
                ):
                    self.output.space_before_token = True
                elif self.last_type == 'TK_RESERVED' and self.flags.last_text == 'default' and self.last_last_text == 'export':
                    self.output.space_before_token = True
                else:
                    self.print_newline()
            elif self.last_type == 'TK_OPERATOR' or self.flags.last_text == '=':
                # foo = function
                self.output.space_before_token = True
            elif not self.flags.multiline_frame and (self.is_expression(self.flags.mode) or self.is_array(self.flags.mode)):
                # (function
                pass
            else:
                self.print_newline()

            self.print_token(current_token)
            self.flags.last_word = current_token.text
            return

        prefix = 'NONE'

        if self.last_type == 'TK_END_BLOCK':
            if self.previous_flags.inline_frame:
                prefix = 'SPACE'
            elif not (current_token.type == 'TK_RESERVED' and current_token.text in ['else', 'catch', 'finally', 'from']):
                prefix = 'NEWLINE'
            else:
                if self.opts.brace_style in ['expand', 'end-expand'] or \
                    (self.opts.brace_style == 'none' and current_token.wanted_newline):
                    prefix = 'NEWLINE'
                else:
                    prefix = 'SPACE'
                    self.output.space_before_token = True
        elif self.last_type == 'TK_SEMICOLON' and self.flags.mode == MODE.BlockStatement:
            # TODO: Should this be for STATEMENT as well?
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_SEMICOLON' and self.is_expression(self.flags.mode):
            prefix = 'SPACE'
        elif self.last_type == 'TK_STRING':
            prefix = 'NEWLINE'
        elif self.last_type == 'TK_RESERVED' or self.last_type == 'TK_WORD' or \
            (self.flags.last_text == '*' and (
                self.last_last_text in ['function', 'yield'] or
                (self.flags.mode == MODE.ObjectLiteral and self.last_last_text in ['{', ',']))):
            prefix = 'SPACE'
        elif self.last_type == 'TK_START_BLOCK':
            if self.flags.inline_frame:
                prefix = 'SPACE'
            else:
                prefix = 'NEWLINE'
        elif self.last_type == 'TK_END_EXPR':
            self.output.space_before_token = True
            prefix = 'NEWLINE'

        if current_token.type == 'TK_RESERVED' and current_token.text in Tokenizer.line_starters and self.flags.last_text != ')':
            if self.flags.inline_frame or self.flags.last_text == 'else ' or self.flags.last_text == 'export':
                prefix = 'SPACE'
            else:
                prefix = 'NEWLINE'

        if current_token.type == 'TK_RESERVED' and current_token.text in ['else', 'catch', 'finally']:
            if ((not (self.last_type == 'TK_END_BLOCK' and self.previous_flags.mode == MODE.BlockStatement)) \
               or self.opts.brace_style == 'expand' \
               or self.opts.brace_style == 'end-expand' \
               or (self.opts.brace_style == 'none' and current_token.wanted_newline)) \
               and not self.flags.inline_frame:
                self.print_newline()
            else:
                self.output.trim(True)
                # If we trimmed and there's something other than a close block before us
                # put a newline back in.  Handles '} // comment' scenario.
                if self.output.current_line.last() != '}':
                    self.print_newline()

                self.output.space_before_token = True

        elif prefix == 'NEWLINE':
            if self.last_type == 'TK_RESERVED' and self.is_special_word(self.flags.last_text):
                # no newline between return nnn
                self.output.space_before_token = True
            elif self.last_type != 'TK_END_EXPR':
                if (self.last_type != 'TK_START_EXPR' or not (current_token.type == 'TK_RESERVED' and current_token.text in ['var', 'let', 'const'])) and self.flags.last_text != ':':
                    # no need to force newline on VAR -
                    # for (var x = 0...
                    if current_token.type == 'TK_RESERVED' and current_token.text == 'if' and self.flags.last_text == 'else':
                        self.output.space_before_token = True
                    else:
                        self.print_newline()
            elif current_token.type == 'TK_RESERVED' and current_token.text in Tokenizer.line_starters and self.flags.last_text != ')':
                self.print_newline()
        elif self.flags.multiline_frame and self.is_array(self.flags.mode) and self.flags.last_text == ',' and self.last_last_text == '}':
            self.print_newline() # }, in lists get a newline
        elif prefix == 'SPACE':
            self.output.space_before_token = True


        self.print_token(current_token)
        self.flags.last_word = current_token.text

        if current_token.type == 'TK_RESERVED':
            if current_token.text == 'do':
                self.flags.do_block = True
            elif current_token.text == 'if':
                self.flags.if_block = True
            elif current_token.text == 'import':
                self.flags.import_block = True
            elif current_token.text == 'from' and self.flags.import_block:
                self.flags.import_block = False


    def handle_semicolon(self, current_token):
        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            # Semicolon can be the start (and end) of a statement
            self.output.space_before_token = False
        else:
            self.handle_whitespace_and_comments(current_token)

        next_token = self.get_token(1)
        while (self.flags.mode == MODE.Statement and
                not (self.flags.if_block and next_token and next_token.type == 'TK_RESERVED' and next_token.text == 'else') and
                not self.flags.do_block):
            self.restore_mode()

        if self.flags.import_block:
            self.flags.import_block = False

        self.print_token(current_token)


    def handle_string(self, current_token):
        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            # One difference - strings want at least a space before
            self.output.space_before_token = True
        else:
            self.handle_whitespace_and_comments(current_token)

            if self.last_type == 'TK_RESERVED' or self.last_type == 'TK_WORD' or self.flags.inline_frame:
                self.output.space_before_token = True
            elif self.last_type in ['TK_COMMA', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR']:
                if not self.start_of_object_property():
                    self.allow_wrap_or_preserved_newline(current_token)
            else:
                self.print_newline()

        self.print_token(current_token)


    def handle_equals(self, current_token):
        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            pass
        else:
            self.handle_whitespace_and_comments(current_token)


        if self.flags.declaration_statement:
            # just got an '=' in a var-line, different line breaking rules will apply
            self.flags.declaration_assignment = True

        self.output.space_before_token = True
        self.print_token(current_token)
        self.output.space_before_token = True


    def handle_comma(self, current_token):
        self.handle_whitespace_and_comments(current_token, True)

        self.print_token(current_token)
        self.output.space_before_token = True

        if self.flags.declaration_statement:
            if self.is_expression(self.flags.parent.mode):
                # do not break on comma, for ( var a = 1, b = 2
                self.flags.declaration_assignment = False

            if self.flags.declaration_assignment:
                self.flags.declaration_assignment = False
                self.print_newline(preserve_statement_flags = True)
            elif self.opts.comma_first:
                # for comma-first, we want to allow a newline before the comma
                # to turn into a newline after the comma, which we will fixup later
                self.allow_wrap_or_preserved_newline(current_token)

        elif self.flags.mode == MODE.ObjectLiteral \
            or (self.flags.mode == MODE.Statement and self.flags.parent.mode ==  MODE.ObjectLiteral):
            if self.flags.mode == MODE.Statement:
                self.restore_mode()

            if not self.flags.inline_frame:
                self.print_newline()
        elif self.opts.comma_first:
            # EXPR or DO_BLOCK
            # for comma-first, we want to allow a newline before the comma
            # to turn into a newline after the comma, which we will fixup later
            self.allow_wrap_or_preserved_newline(current_token)


    def handle_operator(self, current_token):
        isGeneratorAsterisk = current_token.text == '*' and \
            ((self.last_type == 'TK_RESERVED' and self.flags.last_text in ['function', 'yield']) or
                (self.last_type in ['TK_START_BLOCK', 'TK_COMMA', 'TK_END_BLOCK', 'TK_SEMICOLON']))
        isUnary = current_token.text in ['+', '-'] \
            and (self.last_type in ['TK_START_BLOCK', 'TK_START_EXPR', 'TK_EQUALS', 'TK_OPERATOR'] \
            or self.flags.last_text in Tokenizer.line_starters or self.flags.last_text == ',')

        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            pass
        else:
            preserve_statement_flags = not isGeneratorAsterisk
            self.handle_whitespace_and_comments(current_token, preserve_statement_flags)

        if self.last_type == 'TK_RESERVED' and self.is_special_word(self.flags.last_text):
            # return had a special handling in TK_WORD
            self.output.space_before_token = True
            self.print_token(current_token)
            return

        # hack for actionscript's import .*;
        if current_token.text == '*' and self.last_type == 'TK_DOT':
            self.print_token(current_token)
            return

        if current_token.text == '::':
            # no spaces around the exotic namespacing syntax operator
            self.print_token(current_token)
            return

        # Allow line wrapping between operators when operator_position is
        #   set to before or preserve
        if self.last_type == 'TK_OPERATOR' and self.opts.operator_position in OPERATOR_POSITION_BEFORE_OR_PRESERVE:
            self.allow_wrap_or_preserved_newline(current_token)

        if current_token.text == ':' and self.flags.in_case:
            self.flags.case_body = True
            self.indent()
            self.print_token(current_token)
            self.print_newline()
            self.flags.in_case = False
            return

        space_before = True
        space_after = True
        in_ternary = False

        if current_token.text == ':':
            if self.flags.ternary_depth == 0:
                # Colon is invalid javascript outside of ternary and object, but do our best to guess what was meant.
                space_before = False
            else:
                self.flags.ternary_depth -= 1
                in_ternary = True
        elif current_token.text == '?':
            self.flags.ternary_depth += 1

        # let's handle the operator_position option prior to any conflicting logic
        if (not isUnary) and (not isGeneratorAsterisk) and \
            self.opts.preserve_newlines and current_token.text in Tokenizer.positionable_operators:

            isColon = current_token.text == ':'
            isTernaryColon = isColon and in_ternary
            isOtherColon = isColon and not in_ternary

            if self.opts.operator_position == OPERATOR_POSITION['before_newline']:
                # if the current token is : and it's not a ternary statement then we set space_before to false
                self.output.space_before_token = not isOtherColon

                self.print_token(current_token)

                if (not isColon) or isTernaryColon:
                    self.allow_wrap_or_preserved_newline(current_token)

                self.output.space_before_token = True

                return

            elif self.opts.operator_position == OPERATOR_POSITION['after_newline']:
                # if the current token is anything but colon, or (via deduction) it's a colon and in a ternary statement,
                #   then print a newline.
                self.output.space_before_token = True

                if (not isColon) or isTernaryColon:
                    if self.get_token(1).wanted_newline:
                        self.print_newline(preserve_statement_flags = True)
                    else:
                        self.allow_wrap_or_preserved_newline(current_token)
                else:
                    self.output.space_before_token = False

                self.print_token(current_token)

                self.output.space_before_token = True
                return

            elif self.opts.operator_position == OPERATOR_POSITION['preserve_newline']:
                if not isOtherColon:
                    self.allow_wrap_or_preserved_newline(current_token)

                # if we just added a newline, or the current token is : and it's not a ternary statement,
                #   then we set space_before to false
                self.output.space_before_token = not (self.output.just_added_newline() or isOtherColon)

                self.print_token(current_token)

                self.output.space_before_token = True
                return

        if isGeneratorAsterisk:
            self.allow_wrap_or_preserved_newline(current_token)
            space_before = False
            next_token = self.get_token(1)
            space_after = next_token and next_token.type in ['TK_WORD','TK_RESERVED']
        elif current_token.text == '...':
            self.allow_wrap_or_preserved_newline(current_token)
            space_before = self.last_type == 'TK_START_BLOCK'
            space_after = False
        elif current_token.text in ['--', '++', '!', '~'] or isUnary:
            space_before = False
            space_after = False

            # http://www.ecma-international.org/ecma-262/5.1/#sec-7.9.1
            # if there is a newline between -- or ++ and anything else we should preserve it.
            if current_token.wanted_newline and (current_token.text == '--' or current_token.text == '++'):
                self.print_newline(preserve_statement_flags = True)

            if self.flags.last_text == ';' and self.is_expression(self.flags.mode):
                # for (;; ++i)
                #         ^^
                space_before = True

            if self.last_type == 'TK_RESERVED':
                space_before = True
            elif self.last_type == 'TK_END_EXPR':
                space_before = not (self.flags.last_text == ']' and current_token.text in ['--', '++'])
            elif self.last_type == 'TK_OPERATOR':
                # a++ + ++b
                # a - -b
                space_before = current_token.text in ['--', '-','++', '+'] and self.flags.last_text in ['--', '-','++', '+']
                # + and - are not unary when preceeded by -- or ++ operator
                # a-- + b
                # a * +b
                # a - -b
                if current_token.text in ['-', '+'] and self.flags.last_text in ['--', '++']:
                    space_after = True

            if (((self.flags.mode == MODE.BlockStatement and not self.flags.inline_frame) or self.flags.mode == MODE.Statement)
                    and self.flags.last_text in ['{', ';']):
                # { foo: --i }
                # foo(): --bar
                self.print_newline()

        if space_before:
            self.output.space_before_token = True

        self.print_token(current_token)

        if space_after:
            self.output.space_before_token = True



    def handle_block_comment(self, current_token, preserve_statement_flags):
        if self.output.raw:
            self.output.add_raw_token(current_token)
            if current_token.directives and current_token.directives.get('preserve') == 'end':
                # If we're testing the raw output behavior, do not allow a directive to turn it off.
                self.output.raw = self.opts.test_output_raw
            return

        if current_token.directives:
            self.print_newline(preserve_statement_flags = preserve_statement_flags)
            self.print_token(current_token)
            if current_token.directives.get('preserve') == 'start':
                self.output.raw = True

            self.print_newline(preserve_statement_flags = True)
            return

        # inline block
        if not self.acorn.newline.search(current_token.text) and not current_token.wanted_newline:
            self.output.space_before_token = True
            self.print_token(current_token)
            self.output.space_before_token = True
            return

        lines = self.acorn.allLineBreaks.split(current_token.text)
        javadoc = False
        starless = False
        last_indent = current_token.whitespace_before
        last_indent_length = len(last_indent)

        # block comment starts with a new line
        self.print_newline(preserve_statement_flags = preserve_statement_flags)
        if  len(lines) > 1:
            javadoc = not any(l for l in lines[1:] if ( l.strip() == '' or (l.lstrip())[0] != '*'))
            starless = all(l.startswith(last_indent) or l.strip() == '' for l in lines[1:])

        # first line always indented
        self.print_token(current_token, lines[0])
        for line in lines[1:]:
            self.print_newline(preserve_statement_flags = True)
            if javadoc:
                # javadoc: reformat and re-indent
                self.print_token(current_token, ' ' + line.lstrip())
            elif starless and len(line) > last_indent_length:
                # starless: re-indent non-empty content, avoiding trim
                self.print_token(current_token, line[last_indent_length:])
            else:
                # normal comments output raw
                self.output.add_token(line)

        self.print_newline(preserve_statement_flags = preserve_statement_flags)

    def handle_comment(self, current_token, preserve_statement_flags):
        if current_token.wanted_newline:
            self.print_newline(preserve_statement_flags = preserve_statement_flags)

        if not current_token.wanted_newline:
            self.output.trim(True)

        self.output.space_before_token = True
        self.print_token(current_token)
        self.print_newline(preserve_statement_flags = preserve_statement_flags)


    def handle_dot(self, current_token):
        if self.start_of_statement(current_token):
            # The conditional starts the statement if appropriate.
            pass
        else:
            self.handle_whitespace_and_comments(current_token, True)

        if self.last_type == 'TK_RESERVED' and self.is_special_word(self.flags.last_text):
            self.output.space_before_token = True
        else:
            # allow preserved newlines before dots in general
            # force newlines on dots after close paren when break_chained - for bar().baz()
            self.allow_wrap_or_preserved_newline(current_token,
                self.flags.last_text == ')' and self.opts.break_chained_methods)

        self.print_token(current_token)

    def handle_unknown(self, current_token, preserve_statement_flags):
        self.print_token(current_token)
        if current_token.text[-1] == '\n':
            self.print_newline(preserve_statement_flags = preserve_statement_flags)

    def handle_eof(self, current_token):
        # Unwind any open statements
        while self.flags.mode == MODE.Statement:
            self.restore_mode()

        self.handle_whitespace_and_comments(current_token)
