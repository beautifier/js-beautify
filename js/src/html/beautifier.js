/*jshint curly:true, eqeqeq:true, laxbreak:true, noempty:false */
/*

  The MIT License (MIT)

  Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation files
  (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*/

var mergeOpts = require('../core/options').mergeOpts;
var acorn = require('../core/acorn');
var Output = require('../core/output').Output;
var Tokenizer = require('../html/tokenizer').Tokenizer;
var TOKEN = require('../html/tokenizer').TOKEN;

var lineBreak = acorn.lineBreak;
var allLineBreaks = acorn.allLineBreaks;

var Printer = function(indent_character, indent_size, wrap_line_length, max_preserve_newlines, preserve_newlines) { //handles input/output and some other printing functions

  this.indent_character = indent_character;
  this.indent_string = '';
  this.indent_size = indent_size;
  this.indent_level = 0;
  this.alignment_size = 0;
  this.wrap_line_length = wrap_line_length;
  this.max_preserve_newlines = max_preserve_newlines;
  this.preserve_newlines = preserve_newlines;

  for (var i = 0; i < this.indent_size; i++) {
    this.indent_string += this.indent_character;
  }

  this._output = new Output(this.indent_string, '');

};

Printer.prototype.current_line_has_match = function(pattern) {
  return this._output.current_line.has_match(pattern);
};

Printer.prototype.set_space_before_token = function(value) {
  this._output.space_before_token = value;
};

Printer.prototype.add_raw_token = function(token) {
  this._output.add_raw_token(token);
};

Printer.prototype.traverse_whitespace = function(raw_token) {
  if (raw_token.whitespace_before || raw_token.newlines) {
    var newlines = 0;

    if (raw_token.type !== TOKEN.TEXT && raw_token.previous.type !== TOKEN.TEXT) {
      newlines = raw_token.newlines ? 1 : 0;
    }

    if (this.preserve_newlines) {
      newlines = raw_token.newlines < this.max_preserve_newlines + 1 ? raw_token.newlines : this.max_preserve_newlines + 1;
    }

    if (newlines) {
      for (var n = 0; n < newlines; n++) {
        this.print_newline(n > 0);
      }
    } else {
      this._output.space_before_token = true;
      this.print_space_or_wrap(raw_token.text);
    }
    return true;
  }
  return false;
};

// Append a space to the given content (string array) or, if we are
// at the wrap_line_length, append a newline/indentation.
// return true if a newline was added, false if a space was added
Printer.prototype.print_space_or_wrap = function(text) {
  if (this._output.current_line.get_character_count() + text.length + 1 >= this.wrap_line_length) { //insert a line when the wrap_line_length is reached
    if (this._output.add_new_line()) {
      return true;
    }
  }
  return false;
};

Printer.prototype.print_newline = function(force) {
  this._output.add_new_line(force);
};

Printer.prototype.print_token = function(text) {
  if (text) {
    if (this._output.current_line.is_empty()) {
      this._output.set_indent(this.indent_level, this.alignment_size);
    }

    this._output.add_token(text);
  }
};

Printer.prototype.print_raw_text = function(text) {
  this._output.current_line.push_raw(text);
};

Printer.prototype.indent = function() {
  this.indent_level++;
};

Printer.prototype.unindent = function() {
  if (this.indent_level > 0) {
    this.indent_level--;
  }
};

Printer.prototype.get_full_indent = function(level) {
  level = this.indent_level + (level || 0);
  if (level < 1) {
    return '';
  }

  return this._output.get_indent_string(level);
};


var uses_beautifier = function(tag_check, start_token) {
  var raw_token = start_token.next;
  if (!start_token.closed) {
    return false;
  }

  while (raw_token.type !== TOKEN.EOF && raw_token.closed !== start_token) {
    if (raw_token.type === TOKEN.ATTRIBUTE && raw_token.text === 'type') {
      // For script and style tags that have a type attribute, only enable custom beautifiers for matching values
      var peekEquals = raw_token.next ? raw_token.next : raw_token;
      var peekValue = peekEquals.next ? peekEquals.next : peekEquals;
      if (peekEquals.type === TOKEN.EQUALS && peekValue.type === TOKEN.VALUE) {
        return (tag_check === 'style' && peekValue.text.search('text/css') > -1) ||
          (tag_check === 'script' && peekValue.text.search(/(text|application|dojo)\/(x-)?(javascript|ecmascript|jscript|livescript|(ld\+)?json|method|aspect)/) > -1);
      }
      return false;
    }
    raw_token = raw_token.next;
  }

  return true;
};

function in_array(what, arr) {
  return arr.indexOf(what) !== -1;
}


function TagFrame(parent, tag, parser_token, indent_level) {
  this.parent = parent || null;
  this.tag = tag || '';
  this.indent_level = indent_level || 0;
  this.parser_token = parser_token || null;
}

TagFrame.prototype.record_tag = function(tag, parser_token, indent_level) { //function to record a tag and its parent in this.tags Object
  var new_parent = new TagFrame(this.parent, this.tag, this.parser_token, this.indent_level);
  this.parent = new_parent;
  this.tag = tag;
  this.indent_level = indent_level;
  this.parser_token = parser_token;
};

TagFrame.prototype.retrieve_tag = function(tag, printer) { //function to retrieve the opening tag to the corresponding closer
  var parser_token = null;
  var temp_parent = this;

  while (temp_parent) { //till we reach '' (the initial value);
    if (temp_parent.tag === tag) { //if this is it use it
      break;
    }
    temp_parent = temp_parent.parent;
  }


  if (temp_parent) {
    parser_token = temp_parent.parser_token;
    printer.indent_level = temp_parent.indent_level;
    temp_parent = temp_parent.parent ? temp_parent.parent : temp_parent;
    this.parent = temp_parent.parent;
    this.tag = temp_parent.tag;
    this.indent_level = temp_parent.indent_level;
    this.parser_token = temp_parent.parser_token;
  }

  return parser_token;
};

TagFrame.prototype.indent_to_tag = function(tag_list, printer) {
  var temp_parent = this;

  while (temp_parent) { //till we reach '' (the initial value);
    if (tag_list.indexOf(temp_parent.tag) !== -1) { //if this is it use it
      break;
    }
    temp_parent = temp_parent.parent;
  }

  if (temp_parent) {
    printer.indent_level = temp_parent.indent_level;
  }
};

function get_array(input, default_list) {
  var result = default_list || [];
  if (typeof input === 'object') {
    if (input !== null && typeof input.concat === 'function') {
      result = input.concat();
    }
  } else if (typeof input === 'string') {
    result = input.trim().replace(/\s*,\s*/g, ',').split(',');
  }
  return result;
}

function Beautifier(source_text, options, js_beautify, css_beautify) {
  //Wrapper function to invoke all the necessary constructors and deal with the output.
  this._source_text = source_text || '';
  options = options || {};
  this._js_beautify = js_beautify;
  this._css_beautify = css_beautify;
  this._tag_stack = null;

  // Allow the setting of language/file-type specific options
  // with inheritance of overall settings
  options = mergeOpts(options, 'html');

  // backwards compatibility to 1.3.4
  if ((options.wrap_line_length === undefined || parseInt(options.wrap_line_length, 10) === 0) &&
    (options.max_char !== undefined && parseInt(options.max_char, 10) !== 0)) {
    options.wrap_line_length = options.max_char;
  }

  this._options = Object.assign({}, options);

  this._options.indent_inner_html = (options.indent_inner_html === undefined) ? true : options.indent_inner_html;
  this._options.indent_body_inner_html = (options.indent_body_inner_html === undefined) ? true : options.indent_body_inner_html;
  this._options.indent_head_inner_html = (options.indent_head_inner_html === undefined) ? true : options.indent_head_inner_html;
  this._options.indent_size = (options.indent_size === undefined) ? 4 : parseInt(options.indent_size, 10);
  this._options.indent_character = (options.indent_char === undefined) ? ' ' : options.indent_char;
  this._options.wrap_line_length = parseInt(options.wrap_line_length, 10) === 0 ? 32786 : parseInt(options.wrap_line_length || 250, 10);
  this._options.preserve_newlines = (options.preserve_newlines === undefined) ? true : options.preserve_newlines;
  this._options.max_preserve_newlines = this._options.preserve_newlines ?
    (isNaN(parseInt(options.max_preserve_newlines, 10)) ? 32786 : parseInt(options.max_preserve_newlines, 10)) :
    0;
  this._options.indent_handlebars = (options.indent_handlebars === undefined) ? false : options.indent_handlebars;
  this._options.wrap_attributes = (options.wrap_attributes === undefined) ? 'auto' : options.wrap_attributes;
  this._options.wrap_attributes_indent_size = (isNaN(parseInt(options.wrap_attributes_indent_size, 10))) ? this._options.indent_size : parseInt(options.wrap_attributes_indent_size, 10);
  this._options.end_with_newline = (options.end_with_newline === undefined) ? false : options.end_with_newline;
  this._options.extra_liners = get_array(options.extra_liners, ['head', 'body', '/html']);
  this._options.eol = options.eol ? options.eol : 'auto';

  if (options.indent_with_tabs) {
    this._options.indent_character = '\t';
    this._options.indent_size = 1;
  }

  // Support passing the source text back with no change
  this._options.disabled = (options.disabled === undefined) ? false : options.disabled;

  this._options.eol = this._options.eol.replace(/\\r/, '\r').replace(/\\n/, '\n');

  this._options.inline_tags = get_array(options.inline, [
    // https://www.w3.org/TR/html5/dom.html#phrasing-content
    'a', 'abbr', 'area', 'audio', 'b', 'bdi', 'bdo', 'br', 'button', 'canvas', 'cite',
    'code', 'data', 'datalist', 'del', 'dfn', 'em', 'embed', 'i', 'iframe', 'img',
    'input', 'ins', 'kbd', 'keygen', 'label', 'map', 'mark', 'math', 'meter', 'noscript',
    'object', 'output', 'progress', 'q', 'ruby', 's', 'samp', /* 'script', */ 'select', 'small',
    'span', 'strong', 'sub', 'sup', 'svg', 'template', 'textarea', 'time', 'u', 'var',
    'video', 'wbr', 'text',
    // prexisting - not sure of full effect of removing, leaving in
    'acronym', 'address', 'big', 'dt', 'ins', 'strike', 'tt'
  ]);
  this._options.void_elements = get_array(options.void_elements, [
    // HTLM void elements - aka self-closing tags - aka singletons
    // https://www.w3.org/html/wg/drafts/html/master/syntax.html#void-elements
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
    'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr',
    // NOTE: Optional tags - are not understood.
    // https://www.w3.org/TR/html5/syntax.html#optional-tags
    // The rules for optional tags are too complex for a simple list
    // Also, the content of these tags should still be indented in many cases.
    // 'li' is a good exmple.

    // Doctype and xml elements
    '!doctype', '?xml',
    // ?php and ?= tags
    '?php', '?=',
    // other tags that were in this list, keeping just in case
    'basefont', 'isindex'
  ]);
  this._options.unformatted = get_array(options.unformatted, []);
  this._options.content_unformatted = get_array(options.content_unformatted, [
    'pre', 'textarea'
  ]);


  this._is_wrap_attributes_force = this._options.wrap_attributes.substr(0, 'force'.length) === 'force';
  this._is_wrap_attributes_force_expand_multiline = (this._options.wrap_attributes === 'force-expand-multiline');
  this._is_wrap_attributes_force_aligned = (this._options.wrap_attributes === 'force-aligned');
  this._is_wrap_attributes_aligned_multiple = (this._options.wrap_attributes === 'aligned-multiple');
}

Beautifier.prototype.beautify = function() {

  // if disabled, return the input unchanged.
  if (this._options.disabled) {
    return this._source_text;
  }

  var source_text = this._source_text;
  var eol = this._options.eol;
  if (this._options.eol === 'auto') {
    eol = '\n';
    if (source_text && lineBreak.test(source_text)) {
      eol = source_text.match(lineBreak)[0];
    }
  }

  // HACK: newline parsing inconsistent. This brute force normalizes the input.
  source_text = source_text.replace(allLineBreaks, '\n');

  this._tag_stack = new TagFrame();
  last_token = {
    text: '',
    type: ''
  };
  var last_tag_token = {
    text: '',
    type: '',
    tag_name: '',
    indent_content: false,
    tag_complete: true,
    is_start_tag: false,
    is_end_tag: false,
    is_inline_tag: false
  };

  printer = new Printer(this._options.indent_character, this._options.indent_size,
    this._options.wrap_line_length, this._options.max_preserve_newlines, this._options.preserve_newlines);
  var tokens = new Tokenizer(source_text, this._options).tokenize();

  var parser_token = null;
  raw_token = tokens.next();
  while (raw_token.type !== TOKEN.EOF) {

    if (raw_token.type === TOKEN.TAG_OPEN || raw_token.type === TOKEN.COMMENT) {
      parser_token = this._handle_tag_open(printer, raw_token, last_tag_token, last_token);
      last_tag_token = parser_token;
    } else if ((raw_token.type === TOKEN.ATTRIBUTE || raw_token.type === TOKEN.EQUALS || raw_token.type === TOKEN.VALUE) ||
      (raw_token.type === TOKEN.TEXT && !last_tag_token.tag_complete)) {
      parser_token = this._handle_inside_tag(printer, raw_token, last_tag_token, tokens);
    } else if (raw_token.type === TOKEN.TAG_CLOSE) {
      parser_token = this._handle_tag_close(printer, raw_token, last_tag_token);
    } else if (raw_token.type === TOKEN.TEXT) {
      parser_token = this._handle_text(printer, raw_token, last_tag_token);
    } else {
      // This should never happen, but if it does. Print the raw token
      printer.add_raw_token(token);
    }

    last_token = parser_token;

    raw_token = tokens.next();
  }
  var sweet_code = printer._output.get_code(this._options.end_with_newline, eol);

  return sweet_code;
};

Beautifier.prototype._handle_tag_close = function(printer, raw_token, last_tag_token) {
  parser_token = { text: raw_token.text, type: raw_token.type };
  printer.alignment_size = 0;
  last_tag_token.tag_complete = true;

  printer.set_space_before_token(raw_token.newlines || raw_token.whitespace_before !== '');
  if (last_tag_token.is_unformatted) {
    printer.add_raw_token(raw_token);
  } else {
    if (last_tag_token.tag_start_char === '<') {
      printer.set_space_before_token(raw_token.text[0] === '/'); // space before />, no space before >
      if (this._is_wrap_attributes_force_expand_multiline && last_tag_token.has_wrapped_attrs) {
        printer.print_newline(false);
      }
    }
    printer.print_token(raw_token.text);
  }

  if (last_tag_token.indent_content &&
    !(last_tag_token.is_unformatted || last_tag_token.is_content_unformatted)) {
    if (last_tag_token.tag_start_char === '{' ||
      ((this._options.indent_body_inner_html || last_tag_token.tag_name !== 'body') &&
        (this._options.indent_head_inner_html || last_tag_token.tag_name !== 'head'))) {

      printer.indent();
    }

    // only indent once per opened tag
    last_tag_token.indent_content = false;
  }
  return parser_token;
};

Beautifier.prototype._handle_inside_tag = function(printer, raw_token, last_tag_token, tokens) {
  parser_token = { text: raw_token.text, type: raw_token.type };
  printer.set_space_before_token(raw_token.newlines || raw_token.whitespace_before !== '');
  if (last_tag_token.is_unformatted) {
    printer.add_raw_token(raw_token);
  } else {
    if (last_tag_token.tag_start_char === '<') {
      if (raw_token.type === TOKEN.ATTRIBUTE) {
        printer.set_space_before_token(true);
        last_tag_token.attr_count += 1;
      } else if (raw_token.type === TOKEN.EQUALS) { //no space before =
        printer.set_space_before_token(false);
      } else if (raw_token.type === TOKEN.VALUE && raw_token.previous.type === TOKEN.EQUALS) { //no space before value
        printer.set_space_before_token(false);
      }
    }

    if (printer._output.space_before_token && last_tag_token.tag_start_char === '<') {
      var wrapped = printer.print_space_or_wrap(raw_token.text);
      if (raw_token.type === TOKEN.ATTRIBUTE) {
        var indentAttrs = wrapped && !this._is_wrap_attributes_force;

        if (this._is_wrap_attributes_force) {
          var force_first_attr_wrap = false;
          if (this._is_wrap_attributes_force_expand_multiline && last_tag_token.attr_count === 1) {
            var is_only_attribute = true;
            var peek_index = 0;
            var peek_token;
            do {
              peek_token = tokens.peek(peek_index);
              if (peek_token.type === TOKEN.ATTRIBUTE) {
                is_only_attribute = false;
                break;
              }
              peek_index += 1;
            } while (peek_index < 4 && peek_token.type !== TOKEN.EOF && peek_token.type !== TOKEN.TAG_CLOSE);

            force_first_attr_wrap = !is_only_attribute;
          }

          if (last_tag_token.attr_count > 1 || force_first_attr_wrap) {
            printer.print_newline(false);
            indentAttrs = true;
          }
        }
        if (indentAttrs) {
          last_tag_token.has_wrapped_attrs = true;
        }
      }
    }
    printer.print_token(raw_token.text);
  }
  return parser_token;
};

Beautifier.prototype._handle_text = function(printer, raw_token, last_tag_token) {
  parser_token = { text: raw_token.text, type: 'TK_CONTENT' };
  if (last_tag_token.type === 'TK_TAG_SCRIPT' || last_tag_token.type === 'TK_TAG_STYLE') { //check if we need to format javascript
    if (raw_token.text !== '') {
      printer.print_newline(false);
      var text = raw_token.text,
        _beautifier,
        script_indent_level = 1;
      if (last_tag_token.type === 'TK_TAG_SCRIPT') {
        _beautifier = typeof this._js_beautify === 'function' && this._js_beautify;
      } else if (last_tag_token.type === 'TK_TAG_STYLE') {
        _beautifier = typeof this._css_beautify === 'function' && this._css_beautify;
      }

      if (this._options.indent_scripts === "keep") {
        script_indent_level = 0;
      } else if (this._options.indent_scripts === "separate") {
        script_indent_level = -printer.indent_level;
      }

      var indentation = printer.get_full_indent(script_indent_level);

      // if there is at least one empty line at the end of this text, strip it
      // we'll be adding one back after the text but before the containing tag.
      text = text.replace(/\n[ \t]*$/, '');

      if (_beautifier) {

        // call the Beautifier if avaliable
        var Child_options = function() {
          this.eol = '\n';
        };
        Child_options.prototype = this._options;
        var child_options = new Child_options();
        text = _beautifier(indentation + text, child_options);
      } else {
        // simply indent the string otherwise
        var white = text.match(/^\s*/)[0];
        var _level = white.match(/[^\n\r]*$/)[0].split(this._indent_string).length - 1;
        var reindent = this._get_full_indent(script_indent_level - _level);
        text = (indentation + text.trim())
          .replace(/\r\n|\r|\n/g, '\n' + reindent);
      }
      if (text) {
        printer.print_raw_text(text);
        printer.print_newline(true);
      }
    }
  } else if (last_tag_token.is_unformatted || last_tag_token.is_content_unformatted) {
    printer.add_raw_token(raw_token);
  } else {
    printer.traverse_whitespace(raw_token);
    printer.print_token(raw_token.text);
  }
  return parser_token;
};

Beautifier.prototype._handle_tag_open = function(printer, raw_token, last_tag_token, last_token) {
  var parser_token = this._get_tag_open(this._tag_stack.parser_token, raw_token);
  printer.traverse_whitespace(raw_token);

  this._set_tag_position(printer, parser_token, last_tag_token, last_token);

  if ((last_tag_token.is_unformatted || last_tag_token.is_content_unformatted) &&
    raw_token.type === TOKEN.TAG_OPEN && raw_token.text.indexOf('</') === 0) {
    printer.add_raw_token(raw_token);
  } else {
    printer.print_token(raw_token.text);
  }

  //indent attributes an auto, forced, aligned or forced-align line-wrap
  if (this._is_wrap_attributes_force_aligned || this._is_wrap_attributes_aligned_multiple) {
    parser_token.alignment_size = raw_token.text.length + 1;
  }


  if (!parser_token.tag_complete && !parser_token.is_unformatted) {
    printer.alignment_size = parser_token.alignment_size;
  }

  return parser_token;
};

Beautifier.prototype._get_tag_open = function(parent, raw_token) { //function to get a full tag and parse its type
  var parser_token = {
    parent: parent,
    text: '',
    type: '',
    tag_name: '',
    is_inline_tag: false,
    is_unformatted: false,
    is_content_unformatted: false,
    is_single_tag: false,
    is_start_tag: false,
    is_end_tag: false,
    indent_content: false,
    multiline_content: false,
    custom_beautifier: false,
    start_tag_token: null,
    attr_count: 0,
    has_wrapped_attrs: false,
    alignment_size: this._options.wrap_attributes_indent_size,
    tag_complete: false,
    tag_start_char: '',
    tag_check: ''
  };

  var tag_check_match;
  parser_token.tag_start_char = raw_token.text[0];

  if (parser_token.tag_start_char === '<') {
    tag_check_match = raw_token.text.match(/^<([^\s>]*)/);
    parser_token.tag_check = tag_check_match ? tag_check_match[1] : '';
  } else {
    tag_check_match = raw_token.text.match(/^{{\#?([^\s}]+)/);
    parser_token.tag_check = tag_check_match ? tag_check_match[1] : '';
  }
  parser_token.tag_check = parser_token.tag_check.toLowerCase();

  if (raw_token.type === TOKEN.COMMENT) {
    parser_token.tag_complete = true;
  }
  parser_token.text = raw_token.text;

  parser_token.is_start_tag = parser_token.tag_check.charAt(0) !== '/';
  parser_token.tag_name = !parser_token.is_start_tag ? parser_token.tag_check.substr(1) : parser_token.tag_check;
  parser_token.is_end_tag = !parser_token.is_start_tag ||
    (raw_token.closed && raw_token.closed.text === '/>');

  // handlebars tags that don't start with # or ^ are single_tags, and so also start and end.
  parser_token.is_end_tag = parser_token.is_end_tag ||
    (parser_token.tag_start_char === '{' && (parser_token.text.length < 3 || (/[^#\^]/.test(parser_token.text.charAt(2)))));

  parser_token.is_unformatted = !parser_token.tag_complete && in_array(parser_token.tag_check, this._options.unformatted);
  parser_token.is_content_unformatted = !parser_token.tag_complete && in_array(parser_token.tag_check, this._options.content_unformatted);
  parser_token.is_inline_tag = in_array(parser_token.tag_name, this._options.inline_tags) || parser_token.tag_start_char === '{';

  parser_token.is_single_tag = raw_token.type === TOKEN.COMMENT ||
    in_array(parser_token.tag_check, this._options.void_elements) ||
    (parser_token.is_start_tag && parser_token.is_end_tag) ||
    (parser_token.is_unformatted || parser_token.is_content_unformatted);

  if (parser_token.is_single_tag) {
    parser_token.type = 'TK_TAG_SINGLE';
  } else if (parser_token.is_end_tag) { //this tag is a double tag so check for tag-ending
    parser_token.start_tag_token = this._tag_stack.retrieve_tag(parser_token.tag_name, printer); //remove it and all ancestors
    parser_token.type = 'TK_TAG_END';
  } else { // it's a start-tag
    this._tag_stack.record_tag(parser_token.tag_name, parser_token, printer.indent_level); //push it on the tag stack
    parser_token.type = 'TK_TAG_START';

    if ((parser_token.tag_name === 'script' || parser_token.tag_name === 'style') &&
      uses_beautifier(parser_token.tag_check, raw_token)) {
      parser_token.custom_beautifier = true;
      if (parser_token.tag_name === 'script') {
        parser_token.type = 'TK_TAG_SCRIPT';
      } else {
        parser_token.type = 'TK_TAG_STYLE';
      }
    }
  }


  return parser_token;
};

Beautifier.prototype._set_tag_position = function(printer, parser_token, last_tag_token, last_token) {

  if (in_array(parser_token.tag_check, this._options.extra_liners)) { //check if this double needs an extra line
    printer.print_newline(false);
    if (!printer._output.just_added_blankline()) {
      printer.print_newline(true);
    }
  }

  if (parser_token.is_single_tag) { //if this tag name is a single tag type (either in the list or has a closing /)

    if (parser_token.tag_start_char === '{' && parser_token.tag_check === 'else') {
      this._tag_stack.indent_to_tag(['if', 'unless'], printer);
      parser_token.indent_content = true;
      // Don't add a newline if opening {{#if}} tag is on the current line
      var foundIfOnCurrentLine = printer.current_line_has_match(/{{#if/);
      if (!foundIfOnCurrentLine) {
        printer.print_newline(false);
      }
    }

    // Don't add a newline before elements that should remain where they are.
    if (parser_token.tag_name === '!--' && last_token.type === TOKEN.TAG_CLOSE &&
      last_tag_token.is_end_tag && parser_token.text.indexOf('\n') === -1) {
      //Do nothing. Leave comments on same line.
    } else if (!parser_token.is_inline_tag && !parser_token.is_unformatted) {
      printer.print_newline(false);
    }

  } else if (parser_token.is_end_tag) { //this tag is a double tag so check for tag-ending
    if ((parser_token.start_tag_token && parser_token.start_tag_token.multiline_content) ||
      !(parser_token.is_inline_tag ||
        (last_tag_token.is_inline_tag) ||
        (last_token.type === TOKEN.TAG_CLOSE &&
          parser_token.start_tag_token === last_tag_token) ||
        (last_token.type === 'TK_CONTENT')
      )) {
      printer.print_newline(false);
    }
  } else if (parser_token.custom_beautifier) {
    printer.print_newline(false);
  } else { // it's a start-tag
    if (parser_token.tag_check !== 'html') {
      parser_token.indent_content = true;
    }

    if (!parser_token.is_inline_tag && last_token.type !== 'TK_CONTENT') {
      if (parser_token.parent) {
        parser_token.parent.multiline_content = true;
      }
      printer.print_newline(false);
    }
  }
};

module.exports.Beautifier = Beautifier;