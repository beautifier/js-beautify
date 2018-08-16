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

// function trim(s) {
//     return s.replace(/^\s+|\s+$/g, '');
// }

// function ltrim(s) {
//   return s.replace(/^\s+/g, '');
// }

// function rtrim(s) {
//   return s.replace(/\s+$/g, '');
// }


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

  this._output = new Output(this.indent_string, ''); // jshint unused:false

};

Printer.prototype.get_current_line_items = function() {
  return this._output.current_line._items;
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

Printer.prototype.print_token_raw = function(text) {
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

function Beautifier(html_source, options, js_beautify, css_beautify) {
  //Wrapper function to invoke all the necessary constructors and deal with the output.
  html_source = html_source || '';
  options = options || {};

  var multi_parser,
    indent_inner_html,
    indent_body_inner_html,
    indent_head_inner_html,
    indent_size,
    indent_character,
    wrap_line_length,
    inline_tags,
    unformatted,
    content_unformatted,
    preserve_newlines,
    max_preserve_newlines,
    indent_handlebars,
    wrap_attributes,
    wrap_attributes_indent_size,
    is_wrap_attributes_force,
    is_wrap_attributes_force_expand_multiline,
    is_wrap_attributes_force_aligned,
    is_wrap_attributes_aligned_multiple,
    end_with_newline,
    extra_liners,
    eol;

  // Allow the setting of language/file-type specific options
  // with inheritance of overall settings
  options = mergeOpts(options, 'html');

  // backwards compatibility to 1.3.4
  if ((options.wrap_line_length === undefined || parseInt(options.wrap_line_length, 10) === 0) &&
    (options.max_char !== undefined && parseInt(options.max_char, 10) !== 0)) {
    options.wrap_line_length = options.max_char;
  }

  indent_inner_html = (options.indent_inner_html === undefined) ? false : options.indent_inner_html;
  indent_body_inner_html = (options.indent_body_inner_html === undefined) ? true : options.indent_body_inner_html;
  indent_head_inner_html = (options.indent_head_inner_html === undefined) ? true : options.indent_head_inner_html;
  indent_size = (options.indent_size === undefined) ? 4 : parseInt(options.indent_size, 10);
  indent_character = (options.indent_char === undefined) ? ' ' : options.indent_char;
  wrap_line_length = parseInt(options.wrap_line_length, 10) === 0 ? 32786 : parseInt(options.wrap_line_length || 250, 10);
  inline_tags = options.inline || [
    // https://www.w3.org/TR/html5/dom.html#phrasing-content
    'a', 'abbr', 'area', 'audio', 'b', 'bdi', 'bdo', 'br', 'button', 'canvas', 'cite',
    'code', 'data', 'datalist', 'del', 'dfn', 'em', 'embed', 'i', 'iframe', 'img',
    'input', 'ins', 'kbd', 'keygen', 'label', 'map', 'mark', 'math', 'meter', 'noscript',
    'object', 'output', 'progress', 'q', 'ruby', 's', 'samp', /* 'script', */ 'select', 'small',
    'span', 'strong', 'sub', 'sup', 'svg', 'template', 'textarea', 'time', 'u', 'var',
    'video', 'wbr', 'text',
    // prexisting - not sure of full effect of removing, leaving in
    'acronym', 'address', 'big', 'dt', 'ins', 'strike', 'tt'
  ];
  unformatted = options.unformatted || [];
  content_unformatted = options.content_unformatted || [
    'pre', 'textarea'
  ];
  preserve_newlines = (options.preserve_newlines === undefined) ? true : options.preserve_newlines;
  max_preserve_newlines = preserve_newlines ?
    (isNaN(parseInt(options.max_preserve_newlines, 10)) ? 32786 : parseInt(options.max_preserve_newlines, 10)) :
    0;
  indent_handlebars = (options.indent_handlebars === undefined) ? false : options.indent_handlebars;
  wrap_attributes = (options.wrap_attributes === undefined) ? 'auto' : options.wrap_attributes;
  wrap_attributes_indent_size = (isNaN(parseInt(options.wrap_attributes_indent_size, 10))) ? indent_size : parseInt(options.wrap_attributes_indent_size, 10);
  is_wrap_attributes_force = wrap_attributes.substr(0, 'force'.length) === 'force';
  is_wrap_attributes_force_expand_multiline = (wrap_attributes === 'force-expand-multiline');
  is_wrap_attributes_force_aligned = (wrap_attributes === 'force-aligned');
  is_wrap_attributes_aligned_multiple = (wrap_attributes === 'aligned-multiple');
  end_with_newline = (options.end_with_newline === undefined) ? false : options.end_with_newline;
  extra_liners = (typeof options.extra_liners === 'object') && options.extra_liners ?
    options.extra_liners.concat() : (typeof options.extra_liners === 'string') ?
    options.extra_liners.split(',') : 'head,body,/html'.split(',');
  eol = options.eol ? options.eol : 'auto';

  if (options.indent_with_tabs) {
    indent_character = '\t';
    indent_size = 1;
  }

  if (eol === 'auto') {
    eol = '\n';
    if (html_source && lineBreak.test(html_source || '')) {
      eol = html_source.match(lineBreak)[0];
    }
  }

  eol = eol.replace(/\\r/, '\r').replace(/\\n/, '\n');

  // HACK: newline parsing inconsistent. This brute force normalizes the input.
  html_source = html_source.replace(allLineBreaks, '\n');

  this._tokens = null;

  this._options = {};
  this._options.indent_handlebars = indent_handlebars;
  this._options.unformatted = unformatted || [];
  this._options.content_unformatted = content_unformatted || [];




  function Parser() {

    this.tags = { //An object to hold tags, their position, and their parent-tags, initiated with default values
      parent: null,
      tag: '',
      indent_level: 0,
      parser_token: null
    };
    this.last_token = {
      text: '',
      type: ''
    };
    this.last_tag_token = {
      text: '',
      type: '',
      tag_name: '',
      tag_complete: true,
      is_start_tag: false,
      is_end_tag: false,
      is_inline_tag: false
    };

    this.indent_content = indent_inner_html;
    this.indent_body_inner_html = indent_body_inner_html;
    this.indent_head_inner_html = indent_head_inner_html;

    this.Utils = { //Uilities made available to the various functions
      whitespace: "\n\r\t ".split(''),

      single_token: options.void_elements || [
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
      ],
      extra_liners: extra_liners, //for tags that need a line of whitespace before them
      in_array: function(what, arr) {
        return arr.indexOf(what) !== -1;
      }
    };

    this.record_tag = function(tag, parser_token, indent_level) { //function to record a tag and its parent in this.tags Object
      var new_tag = {
        parent: this.tags,
        tag: tag,
        indent_level: indent_level,
        parser_token: parser_token
      };

      this.tags = new_tag;
    };

    this.retrieve_tag = function(tag, printer) { //function to retrieve the opening tag to the corresponding closer
      var parser_token = null;
      var temp_parent = this.tags;

      while (temp_parent) { //till we reach '' (the initial value);
        if (temp_parent.tag === tag) { //if this is it use it
          break;
        }
        temp_parent = temp_parent.parent;
      }


      if (temp_parent) {
        parser_token = temp_parent.parser_token;
        printer.indent_level = temp_parent.indent_level;
        this.tags = temp_parent.parent;

      }
      return parser_token;
    };

    this.indent_to_tag = function(tag_list, printer) {
      var temp_parent = this.tags;

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

    this.get_tag_open = function(raw_token, printer) { //function to get a full tag and parse its type
      var parser_token = {
        parent: this.tags.parser_token,
        text: '',
        type: '',
        tag_name: '',
        is_inline_tag: false,
        is_unformatted: false,
        is_content_unformatted: false,
        is_single_tag: false,
        is_start_tag: false,
        is_end_tag: false,
        multiline_content: false,
        custom_beautifier: false,
        start_tag_token: null,
        attr_count: 0,
        has_wrapped_attrs: false,
        alignment_size: wrap_attributes_indent_size,
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

      parser_token.is_end_tag = parser_token.tag_check.charAt(0) === '/';
      parser_token.is_single_tag = raw_token.type === TOKEN.COMMENT ||
        this.Utils.in_array(parser_token.tag_check, this.Utils.single_token) ||
        (raw_token.closed && raw_token.closed.text === '/>');
      parser_token.tag_name = parser_token.is_end_tag ? parser_token.tag_check.substr(1) : parser_token.tag_check;
      parser_token.is_inline_tag = this.Utils.in_array(parser_token.tag_name, inline_tags) || parser_token.tag_start_char === '{';
      parser_token.is_unformatted = !parser_token.tag_complete && this.Utils.in_array(parser_token.tag_check, unformatted);
      parser_token.is_content_unformatted = !parser_token.tag_complete && this.Utils.in_array(parser_token.tag_check, content_unformatted);

      printer.traverse_whitespace(raw_token);

      if (this.Utils.in_array(parser_token.tag_check, this.Utils.extra_liners)) { //check if this double needs an extra line
        printer.print_newline(false);
        if (!printer._output.just_added_blankline()) {
          printer.print_newline(true);
        }
      }

      if (parser_token.is_unformatted || parser_token.is_content_unformatted) {
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_single_tag = true;
        parser_token.is_end_tag = true;
      } else if ((parser_token.tag_check === 'script' || parser_token.tag_check === 'style') && uses_beautifier(parser_token.tag_check, raw_token)) {
        // By default, use the custom beautifiers for script and style
        parser_token.custom_beautifier = true;
        if (parser_token.tag_name === 'script') {
          parser_token.type = 'TK_TAG_SCRIPT';
        } else {
          parser_token.type = 'TK_TAG_STYLE';
        }
        printer.print_newline(false);

      } else if (parser_token.is_single_tag) { //if this tag name is a single tag type (either in the list or has a closing /)
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_end_tag = true;
      } else if (indent_handlebars && parser_token.tag_start_char === '{' && parser_token.tag_check === 'else') {
        this.indent_to_tag(['if', 'unless'], printer);
        parser_token.type = 'TK_TAG_HANDLEBARS_ELSE';
        this.indent_content = true;
        // Don't add a newline if opening {{#if}} tag is on the current line
        var foundIfOnCurrentLine = false;
        var items = printer.get_current_line_items();
        for (var lastCheckedOutput = items.length - 1; lastCheckedOutput >= 0; lastCheckedOutput--) {
          if (items[lastCheckedOutput].match(/{{#if/)) {
            foundIfOnCurrentLine = true;
            break;
          }
        }
        if (!foundIfOnCurrentLine) {
          printer.print_newline(false);
        }

      } else if (indent_handlebars && parser_token.tag_start_char === '{' && (raw_token.text.length < 3 || (/[^#\^\/]/.test(raw_token.text.charAt(2))))) {
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_single_tag = true;
        parser_token.is_end_tag = true;
      } else if (parser_token.tag_check.charAt(0) === '!') { //peek for <! comment
        // for comments content is already correct.
        parser_token.is_single_tag = true;
        parser_token.type = 'TK_TAG_SINGLE';
      } else if (parser_token.is_end_tag) { //this tag is a double tag so check for tag-ending
        parser_token.start_tag_token = this.retrieve_tag(parser_token.tag_check.substring(1), printer); //remove it and all ancestors
        parser_token.type = 'TK_TAG_END';

        if ((parser_token.start_tag_token && parser_token.start_tag_token.multiline_content) ||
          !(parser_token.is_inline_tag ||
            (this.last_tag_token.is_inline_tag) ||
            (this.last_token === this.last_tag_token && this.last_tag_token.is_start_tag &&
              parser_token.is_end_tag && this.last_tag_token.tag_name === parser_token.tag_name) ||
            (this.last_token.type === 'TK_CONTENT')
          )) {
          printer.print_newline(false);
        }

      } else { // it's a start-tag
        this.record_tag(parser_token.tag_check, parser_token, printer.indent_level); //push it on the tag stack
        if (parser_token.tag_check !== 'html') {
          this.indent_content = true;
        }
        parser_token.type = 'TK_TAG_START';
        parser_token.is_start_tag = true;
        if (!parser_token.is_inline_tag && this.last_token.type !== 'TK_CONTENT') {
          if (parser_token.parent) {
            parser_token.parent.multiline_content = true;
          }
          printer.print_newline(false);

        }
      }

      if (parser_token.type === 'TK_TAG_SINGLE') {
        // Don't add a newline before elements that should remain unformatted.
        if (parser_token.tag_name === '!--' && this.last_token.is_end_tag && parser_token.text.indexOf('\n') === -1) {
          //Do nothing. Leave comments on same line.
        } else if (!parser_token.is_inline_tag && !parser_token.is_unformatted) {
          printer.print_newline(false);
        }
      }
      this.last_tag_token = parser_token;

      return parser_token;
    };

    return this;
  }

  /*_____________________--------------------_____________________*/

  this.beautify = function() {
    multi_parser = new Parser(); //wrapping functions Parser
    printer = new Printer(indent_character, indent_size, wrap_line_length, max_preserve_newlines, preserve_newlines);
    this._tokens = new Tokenizer(html_source, this._options).tokenize();

    var parser_token = null;
    raw_token = this._tokens.next();
    while (raw_token.type !== TOKEN.EOF) {

      if (raw_token.type === TOKEN.TAG_CLOSE) {
        printer.alignment_size = 0;
        multi_parser.last_tag_token.tag_complete = true;

        printer.set_space_before_token(raw_token.newlines || raw_token.whitespace_before !== '');
        if (multi_parser.last_tag_token.is_unformatted) {
          printer.add_raw_token(raw_token);
        } else {
          if (multi_parser.last_tag_token.tag_start_char === '<') {
            printer.set_space_before_token(raw_token.text[0] === '/'); // space before />, no space before >
            if (is_wrap_attributes_force_expand_multiline && multi_parser.last_tag_token.has_wrapped_attrs) {
              printer.print_newline(false);
            }
          }
          printer.print_token(raw_token.text);
        }

        if (multi_parser.indent_content &&
          !(multi_parser.last_tag_token.is_unformatted || multi_parser.last_tag_token.is_content_unformatted)) {
          if (multi_parser.last_tag_token.tag_start_char === '{' ||
            ((multi_parser.indent_body_inner_html || multi_parser.last_tag_token.tag_name !== 'body') &&
              (multi_parser.indent_head_inner_html || multi_parser.last_tag_token.tag_name !== 'head'))) {

            printer.indent();
          }

          multi_parser.indent_content = false;
        }
      } else if ((raw_token.type === TOKEN.ATTRIBUTE || raw_token.type === TOKEN.EQUALS || raw_token.type === TOKEN.VALUE) ||
        (raw_token.type === TOKEN.TEXT && !multi_parser.last_tag_token.tag_complete)) {
        printer.set_space_before_token(raw_token.newlines || raw_token.whitespace_before !== '');
        if (multi_parser.last_tag_token.is_unformatted) {
          printer.add_raw_token(raw_token);
        } else {
          if (multi_parser.last_tag_token.tag_start_char === '<') {
            if (raw_token.type === TOKEN.ATTRIBUTE) {
              printer.set_space_before_token(true);
              multi_parser.last_tag_token.attr_count += 1;
            } else if (raw_token.type === TOKEN.EQUALS) { //no space before =
              printer.set_space_before_token(false);
            } else if (raw_token.type === TOKEN.VALUE && raw_token.previous.type === TOKEN.EQUALS) { //no space before value
              printer.set_space_before_token(false);
            }
          }

          if (printer._output.space_before_token && multi_parser.last_tag_token.tag_start_char === '<') {
            var wrapped = printer.print_space_or_wrap(raw_token.text);
            if (raw_token.type === TOKEN.ATTRIBUTE) {
              var indentAttrs = wrapped && !is_wrap_attributes_force;

              if (is_wrap_attributes_force) {
                var force_first_attr_wrap = false;
                if (is_wrap_attributes_force_expand_multiline && multi_parser.last_tag_token.attr_count === 1) {
                  var is_only_attribute = true;
                  var peek_index = 0;
                  var peek_token;
                  do {
                    peek_token = this._tokens.peek(peek_index);
                    if (peek_token.type === TOKEN.ATTRIBUTE) {
                      is_only_attribute = false;
                      break;
                    }
                    peek_index += 1;
                  } while (peek_index < 4 && peek_token.type !== TOKEN.EOF && peek_token.type !== TOKEN.TAG_CLOSE);

                  force_first_attr_wrap = !is_only_attribute;
                }

                if (multi_parser.last_tag_token.attr_count > 1 || force_first_attr_wrap) {
                  printer.print_newline(false);
                  indentAttrs = true;
                }
              }
              if (indentAttrs) {
                multi_parser.last_tag_token.has_wrapped_attrs = true;
              }
            }
          }
          printer.print_token(raw_token.text);
        }
      } else if (raw_token.type === TOKEN.TEXT) {
        parser_token = { text: raw_token.text, type: 'TK_CONTENT' };
        if (multi_parser.last_token.type === 'TK_TAG_SCRIPT' || multi_parser.last_token.type === 'TK_TAG_STYLE') { //check if we need to format javascript
          if (raw_token.text !== '') {
            printer.print_newline(false);
            var text = raw_token.text,
              _beautifier,
              script_indent_level = 1;
            if (multi_parser.last_token.type === 'TK_TAG_SCRIPT') {
              _beautifier = typeof js_beautify === 'function' && js_beautify;
            } else if (multi_parser.last_token.type === 'TK_TAG_STYLE') {
              _beautifier = typeof css_beautify === 'function' && css_beautify;
            }

            if (options.indent_scripts === "keep") {
              script_indent_level = 0;
            } else if (options.indent_scripts === "separate") {
              script_indent_level = -printer.indent_level;
            }

            var indentation = printer.get_full_indent(script_indent_level);
            if (_beautifier) {

              // call the Beautifier if avaliable
              var Child_options = function() {
                this.eol = '\n';
              };
              Child_options.prototype = options;
              var child_options = new Child_options();
              text = _beautifier(indentation + text, child_options);
            } else {
              // simply indent the string otherwise
              var white = text.match(/^\s*/)[0];
              var _level = white.match(/[^\n\r]*$/)[0].split(multi_parser.indent_string).length - 1;
              var reindent = multi_parser.get_full_indent(script_indent_level - _level);
              text = (indentation + text.trim())
                .replace(/\r\n|\r|\n/g, '\n' + reindent);
            }
            if (text) {
              printer.print_token_raw(text);
              printer.print_newline(true);
            }
          }
        } else if (multi_parser.last_tag_token.is_unformatted || multi_parser.last_tag_token.is_content_unformatted) {
          printer.add_raw_token(raw_token);
        } else {
          printer.traverse_whitespace(raw_token);
          printer.print_token(raw_token.text);
        }
      } else if (raw_token.type === TOKEN.TAG_OPEN || raw_token.type === TOKEN.COMMENT) {
        var previous = multi_parser.last_tag_token;
        parser_token = multi_parser.get_tag_open(raw_token, printer);

        if ((previous.is_unformatted || previous.is_content_unformatted) &&
          raw_token.type === TOKEN.TAG_OPEN && raw_token.text.indexOf('</') === 0) {
          printer.add_raw_token(raw_token);
        } else {
          printer.print_token(raw_token.text);
        }

        //indent attributes an auto, forced, aligned or forced-align line-wrap
        if (is_wrap_attributes_force_aligned || is_wrap_attributes_aligned_multiple) {
          parser_token.alignment_size = raw_token.text.length + 1;
        }


        if (!parser_token.tag_complete && !parser_token.is_unformatted) {
          printer.alignment_size = parser_token.alignment_size;
        }

      } else {
        // This should never happen, but if it does. Print the raw token
        printer.add_raw_token(token);
      }

      multi_parser.last_token = parser_token;

      raw_token = this._tokens.next();
    }
    var sweet_code = printer._output.get_code(end_with_newline, eol);

    return sweet_code;
  };
}

module.exports.Beautifier = Beautifier;