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
var InputScanner = require('../core/inputscanner').InputScanner;
var Tokenizer = require('../html/tokenizer').Tokenizer;
var TOKEN = require('../html/tokenizer').TOKEN;

var lineBreak = acorn.lineBreak;
var allLineBreaks = acorn.allLineBreaks;

// function trim(s) {
//     return s.replace(/^\s+|\s+$/g, '');
// }

function ltrim(s) {
  return s.replace(/^\s+/g, '');
}

function rtrim(s) {
  return s.replace(/\s+$/g, '');
}

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
    brace_style,
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
  brace_style = (options.brace_style === undefined) ? 'collapse' : options.brace_style;
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

    this.parser_token = '';
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
    this.token_text = '';
    this.newlines = 0;
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

    this.record_tag = function(tag, parser_token) { //function to record a tag and its parent in this.tags Object
      var new_tag = {
        parent: this.tags,
        tag: tag,
        indent_level: this.indent_level,
        parser_token: parser_token
      };

      this.tags = new_tag;
    };

    this.retrieve_tag = function(tag) { //function to retrieve the opening tag to the corresponding closer
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
        this.indent_level = temp_parent.indent_level;
        this.tags = temp_parent.parent;

      }
      return parser_token;
    };

    this.indent_to_tag = function(tag) {
      var temp_parent = this.tags;

      while (temp_parent) { //till we reach '' (the initial value);
        if (temp_parent.tag === tag) { //if this is it use it
          break;
        }
        temp_parent = temp_parent.parent;
      }

      if (temp_parent) {
        this.indent_level = temp_parent.indent_level;
      }
    };

    this.get_tag = function(raw_token) { //function to get a full tag and parse its type
      var parser_token = {
          parent: this.tags.parser_token,
          text: '',
          type: '',
          tag_name: '',
          is_inline_tag: false,
          is_unformatted: false,
          is_content_unformatted: false,
          is_opening_tag: false,
          is_closing_tag: false,
          multiline_content: false,
          start_tag_token: null
        },
        content = [],
        space = false,
        attr_count = 0,
        has_wrapped_attrs = false,
        tag_reading_finished = false,
        tag_start_char,
        tag_check = '',
        alignment_size = wrap_attributes_indent_size,
        alignment_string = '',
        custom_beautifier = false;

      tag_start_char = raw_token.text[0];
      if (tag_start_char === '<') {
        tag_check = raw_token.text.match(/^<([^\s>]*)/)[1];
      } else {
        tag_check = raw_token.text.match(/^{{\#?([^\s}]+)/)[1];
      }
      tag_check = tag_check.toLowerCase();

      if (raw_token.type === TOKEN.COMMENT) {
        tag_reading_finished = true;
      } else if (raw_token.type === TOKEN.TAG_OPEN) {
        space = tag_start_char === '<' || this._tokens.peek().type !== TOKEN.TAG_CLOSE;
      } else {
        throw "Unhandled token!";
      }

      parser_token.is_closing_tag = tag_check.charAt(0) === '/';
      parser_token.tag_name = parser_token.is_closing_tag ? tag_check.substr(1) : tag_check;
      parser_token.is_inline_tag = this.Utils.in_array(parser_token.tag_name, inline_tags) || tag_start_char === '{';
      parser_token.is_unformatted = this.Utils.in_array(tag_check, unformatted);
      parser_token.is_content_unformatted = this.Utils.in_array(tag_check, content_unformatted);

      if (parser_token.is_unformatted || parser_token.is_content_unformatted) {
        // do not assign type to unformatted yet.
      } else if (this.Utils.in_array(tag_check, this.Utils.single_token)) { //if this tag name is a single tag type (either in the list or has a closing /)
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_closing_tag = true;
      } else if (indent_handlebars && tag_start_char === '{' && tag_check === 'else') {
        this.indent_to_tag('if');
        parser_token.type = 'TK_TAG_HANDLEBARS_ELSE';
        this.indent_content = true;
      } else if (indent_handlebars && tag_start_char === '{' && (/[^#\^\/]/.test(raw_token.text.charAt(2)))) {
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_closing_tag = true;
      } else if (parser_token.is_unformatted || parser_token.is_content_unformatted) {
        // do not reformat the "unformatted" or "content_unformatted" tags
        if (this._tokens.peek().type === TOKEN.TEXT) {
          this.add_raw_token(content, this._tokens.next());
        }

        if (this._tokens.peek().type === TOKEN.TAG_OPEN) {
          this.add_raw_token(content, this._tokens.next());
          if (this._tokens.peek().type === TOKEN.TAG_CLOSE) {
            this.add_raw_token(content, this._tokens.next());
          }
        }
        parser_token.type = 'TK_TAG_SINGLE';
        parser_token.is_closing_tag = true;
      } else if (tag_check.charAt(0) === '!') { //peek for <! comment
        // for comments content is already correct.
        parser_token.type = 'TK_TAG_SINGLE';
      } else if (parser_token.is_closing_tag) { //this tag is a double tag so check for tag-ending
        parser_token.start_tag_token = this.retrieve_tag(tag_check.substring(1)); //remove it and all ancestors
        parser_token.type = 'TK_TAG_END';
      }

      this.traverse_whitespace(raw_token);

      if (this.Utils.in_array(tag_check, this.Utils.extra_liners)) { //check if this double needs an extra line
        this.print_newline(false, this.output);
        if (this.output.length && this.output[this.output.length - 2] !== '\n') {
          this.print_newline(true, this.output);
        }
      }

      this.print_indentation(this.output);

      this.add_text_item(content, raw_token.text);

      if (!tag_reading_finished && this._tokens.peek().type !== TOKEN.EOF) {
        //indent attributes an auto, forced, aligned or forced-align line-wrap
        if (is_wrap_attributes_force_aligned || is_wrap_attributes_aligned_multiple) {
          alignment_size = raw_token.text.length + 1;
        }

        // only ever further indent with spaces since we're trying to align characters
        alignment_string = Array(alignment_size + 1).join(' ');

        // By default, use the custom beautifiers for script and style
        custom_beautifier = tag_check === 'script' || tag_check === 'style';

        raw_token = this._tokens.next();
        while (raw_token.type !== TOKEN.EOF) {

          if (parser_token.is_unformatted) {
            this.add_raw_token(content, raw_token);
            if (raw_token.type === TOKEN.TAG_CLOSE || this._tokens.peek().type === TOKEN.EOF) {
              break;
            }

            raw_token = this._tokens.next();
            continue;
          }

          if (tag_start_char === '<') {
            if (raw_token.type === TOKEN.ATTRIBUTE) {
              space = true;
              attr_count += 1;

              if ((tag_check === 'script' || tag_check === 'style') && raw_token.text === 'type') {
                // For script and style tags that have a type attribute, only enable custom beautifiers for matching values
                custom_beautifier = false;
                var peekEquals = this._tokens.peek();
                var peekValue = this._tokens.peek(1);
                if (peekEquals && peekEquals.type === TOKEN.EQUALS && peekValue && peekValue.type === TOKEN.VALUE) {
                  custom_beautifier = custom_beautifier ||
                    (tag_check === 'script' && peekValue.text.search(/(text|application|dojo)\/(x-)?(javascript|ecmascript|jscript|livescript|(ld\+)?json|method|aspect)/) > -1) ||
                    (tag_check === 'style' && peekValue.text.search('text/css') > -1);
                }
              } else if (raw_token.type === TOKEN.EQUALS) { //no space before =
                space = false;
              } else if (raw_token.type === TOKEN.VALUE && raw_token.previous.type === TOKEN.EQUALS) { //no space before value
                space = false;
              }
            } else if (raw_token.type === TOKEN.TEXT) {
              space = true;
            } else if (raw_token.type === TOKEN.TAG_CLOSE) {
              space = raw_token.text[0] === '/'; // space before />, no space before >
            } else {
              space = raw_token.newlines || raw_token.whitespace_before !== '';
            }

            if (is_wrap_attributes_force_expand_multiline && has_wrapped_attrs && raw_token.type === TOKEN.TAG_CLOSE) {
              space = false;
              this.print_newline(false, content);
              this.print_indentation(content);
            }

          }

          if (space) {
            space = false;
            if (tag_start_char === '{') {
              content[content.length - 1] += ' ';
              this.line_char_count++;
            } else {
              var wrapped = this.print_space_or_wrap(content, raw_token.text);
              if (raw_token.type === TOKEN.ATTRIBUTE) {
                var indentAttrs = wrapped && !is_wrap_attributes_force;

                if (is_wrap_attributes_force) {
                  var force_first_attr_wrap = false;
                  if (is_wrap_attributes_force_expand_multiline && attr_count === 1) {
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

                  if (attr_count > 1 || force_first_attr_wrap) {
                    this.print_newline(false, content);
                    this.print_indentation(content);
                    indentAttrs = true;
                  }
                }
                if (indentAttrs) {
                  has_wrapped_attrs = true;
                  content.push(alignment_string);
                  this.line_char_count += alignment_size;
                }
              }
            }
          }

          this.add_text_item(content, raw_token.text);
          if (raw_token.type === TOKEN.TAG_CLOSE || this._tokens.peek().type === TOKEN.EOF) {
            break;
          }

          raw_token = this._tokens.next();
        }
      }
      var tag_complete;

      if (tag_check === 'script' || tag_check === 'style') {
        tag_complete = content.join('');
      }

      if (!parser_token.type) {
        if (content.length > 1 && content[content.length - 1] === '/>') {
          parser_token.type = 'TK_TAG_SINGLE';
          parser_token.is_closing_tag = true;
        } else if (parser_token.is_unformatted || parser_token.is_content_unformatted) {
          // do not reformat the "unformatted" or "content_unformatted" tags
          if (this._tokens.peek().type === TOKEN.TEXT) {
            this.add_raw_token(content, this._tokens.next());
          }

          if (this._tokens.peek().type === TOKEN.TAG_OPEN) {
            this.add_raw_token(content, this._tokens.next());
            if (this._tokens.peek().type === TOKEN.TAG_CLOSE) {
              this.add_raw_token(content, this._tokens.next());
            }
          }
          parser_token.type = 'TK_TAG_SINGLE';
          parser_token.is_closing_tag = true;
        } else if (custom_beautifier) {
          this.record_tag(tag_check);
          if (tag_check === 'script') {
            parser_token.type = 'TK_TAG_SCRIPT';
          } else {
            parser_token.type = 'TK_TAG_STYLE';
          }
        } else if (!parser_token.is_closing_tag) { // it's a start-tag
          this.record_tag(tag_check, parser_token); //push it on the tag stack
          if (tag_check !== 'html') {
            this.indent_content = true;
          }
          parser_token.type = 'TK_TAG_START';
          parser_token.is_opening_tag = true;
        }
      }

      parser_token.text = content.join('');

      return parser_token; //returns fully formatted tag
    };

    this.get_full_indent = function(level) {
      level = this.indent_level + (level || 0);
      if (level < 1) {
        return '';
      }

      return Array(level + 1).join(this.indent_string);
    };

    this.printer = function(source_text, tokens, indent_character, indent_size, wrap_line_length, brace_style) { //handles input/output and some other printing functions

      source_text = source_text || '';

      // HACK: newline parsing inconsistent. This brute force normalizes the input.
      source_text = source_text.replace(/\r\n|[\r\u2028\u2029]/g, '\n');

      this.input = new InputScanner(source_text); //gets the input for the Parser
      this._tokens = tokens;
      this.output = [];
      this.indent_character = indent_character;
      this.indent_string = '';
      this.indent_size = indent_size;
      this.brace_style = brace_style;
      this.indent_level = 0;
      this.wrap_line_length = wrap_line_length;
      this.line_char_count = 0; //count to see if wrap_line_length was exceeded

      for (var i = 0; i < this.indent_size; i++) {
        this.indent_string += this.indent_character;
      }

      this.add_text_item = function(arr, text) {
        if (text) {
          arr.push(text);
          this.line_char_count += text.length;
        }
      };

      this.add_raw_token = function(arr, token) {
        for (var x = 0; x < token.newlines; x++) {
          this.print_newline(true, arr);
        }
        this.add_text_item(arr, token.whitespace_before);
        this.add_multiline_item(arr, token.text);
      };

      this.add_multiline_item = function(arr, text) {
        if (text) {
          this.add_text_item(arr, text);
          var last_newline_index = text.lastIndexOf('\n');
          if (last_newline_index !== -1) {
            this.line_char_count = text.length - last_newline_index;
          }
        }
      };

      this.traverse_whitespace = function(raw_token) {
        if (raw_token.whitespace_before || raw_token.newlines) {
          if (this.output.length) {

            var newlines = 0;

            if (raw_token.type !== TOKEN.TEXT && raw_token.previous.type !== TOKEN.TEXT) {
              newlines = raw_token.newlines ? 1 : 0;
            }

            if (preserve_newlines) {
              newlines = raw_token.newlines < max_preserve_newlines + 1 ? raw_token.newlines : max_preserve_newlines + 1;
            }

            for (var n = 0; n < newlines; n++) {
              this.print_newline(n > 0, this.output);
            }
            this.print_space_or_wrap(this.output, raw_token.text);
          }
          return true;
        }
        return false;
      };

      // Append a space to the given content (string array) or, if we are
      // at the wrap_line_length, append a newline/indentation.
      // return true if a newline was added, false if a space was added
      this.print_space_or_wrap = function(content, text) {
        if (content && content.length) {
          if (this.line_char_count + text.length + 1 >= this.wrap_line_length) { //insert a line when the wrap_line_length is reached
            this.print_newline(false, content);
            this.print_indentation(content);
            return true;
          } else {
            var previous = content[content.length - 1];
            if (!this.Utils.in_array(previous[previous.length - 1], this.Utils.whitespace)) {
              this.line_char_count++;
              content[content.length - 1] += ' ';
            }
          }
        }
        return false;
      };

      this.print_newline = function(force, arr) {
        if (!arr || !arr.length) {
          return;
        }
        var previous = arr[arr.length - 1];
        var previous_rtrim = rtrim(previous);

        if (force || (previous_rtrim !== '')) { //we might want the extra line
          this.line_char_count = 0;
          if (previous !== '\n') {
            arr[arr.length - 1] = previous_rtrim;
          }
          arr.push('\n');
        }
      };

      this.print_indentation = function(arr) {
        if (arr && arr.length) {
          var previous = arr[arr.length - 1];
          if (previous === '\n') {
            this.add_text_item(arr, this.get_full_indent());
          }
        }
      };

      this.print_token = function(text, count_chars) {
        // Avoid printing initial whitespace.
        if (text || text !== '') {
          if (this.output.length) {
            this.print_indentation(this.output);
            var previous = this.output[this.output.length - 1];
            if (this.Utils.in_array(previous[previous.length - 1], this.Utils.whitespace)) {
              text = ltrim(text);
            }
          } else {
            text = ltrim(text);
          }
        }
        if (count_chars) {
          this.line_char_count += text.length;
        }
        this.print_token_raw(text);
      };

      this.print_token_raw = function(text) {
        if (text && text !== '') {
          if (text.length > 1 && text.charAt(text.length - 1) === '\n') {
            // unformatted tags can grab newlines as their last character
            this.output.push(text.slice(0, -1));
            this.print_newline(false, this.output);
          } else {
            this.output.push(text);
          }
        }

      };

      this.indent = function() {
        this.indent_level++;
      };

      this.unindent = function() {
        if (this.indent_level > 0) {
          this.indent_level--;
        }
      };
    };
    return this;
  }

  /*_____________________--------------------_____________________*/

  this.beautify = function() {
    multi_parser = new Parser(); //wrapping functions Parser
    this._tokens = new Tokenizer(html_source, this._options).tokenize();
    multi_parser.printer(html_source, this._tokens, indent_character, indent_size, wrap_line_length, brace_style); //initialize starting values d  d

    var parser_token = null;
    var last_tag_token = {
      text: '',
      type: '',
      tag_name: '',
      is_opening_tag: false,
      is_closing_tag: false,
      is_inline_tag: false
    };
    raw_token = this._tokens.next();
    while (raw_token.type !== TOKEN.EOF) {

      if (multi_parser.last_token.type === 'TK_TAG_SCRIPT' || multi_parser.last_token.type === 'TK_TAG_STYLE') { //check if we need to format javascript
        var type = multi_parser.last_token.type.substr(7);
        parser_token = { text: raw_token.text, type: 'TK_' + type };
      } else if (raw_token.type === TOKEN.TAG_OPEN || raw_token.type === TOKEN.COMMENT) {
        parser_token = multi_parser.get_tag(raw_token);
      } else if (raw_token.type === TOKEN.TEXT) {
        parser_token = { text: raw_token.text, type: 'TK_CONTENT' };
      }

      switch (parser_token.type) {
        case 'TK_TAG_START':
          if (!parser_token.is_inline_tag && multi_parser.last_token.type !== 'TK_CONTENT') {
            if (parser_token.parent) {
              parser_token.parent.multiline_content = true;
            }
            multi_parser.print_newline(false, multi_parser.output);

          }
          multi_parser.print_token(parser_token.text);
          if (multi_parser.indent_content) {
            if ((multi_parser.indent_body_inner_html || parser_token.tag_name !== 'body') &&
              (multi_parser.indent_head_inner_html || parser_token.tag_name !== 'head')) {

              multi_parser.indent();
            }

            multi_parser.indent_content = false;
          }
          last_tag_token = parser_token;
          break;
        case 'TK_TAG_STYLE':
        case 'TK_TAG_SCRIPT':
          multi_parser.print_newline(false, multi_parser.output);
          multi_parser.print_token(parser_token.text);
          last_tag_token = parser_token;
          break;
        case 'TK_TAG_END':
          if ((parser_token.start_tag_token && parser_token.start_tag_token.multiline_content) ||
            !(parser_token.is_inline_tag ||
              (last_tag_token.is_inline_tag) ||
              (multi_parser.last_token === last_tag_token && last_tag_token.is_opening_tag && parser_token.is_closing_tag && last_tag_token.tag_name === parser_token.tag_name) ||
              (multi_parser.last_token.type === 'TK_CONTENT')
            )) {
            multi_parser.print_newline(false, multi_parser.output);
          }
          multi_parser.print_token(parser_token.text);
          last_tag_token = parser_token;
          break;
        case 'TK_TAG_SINGLE':
          // Don't add a newline before elements that should remain unformatted.
          if (parser_token.tag_name === '!--' && multi_parser.last_token.is_closing_tag && parser_token.text.indexOf('\n') === -1) {
            //Do nothing. Leave comments on same line.
          } else if (!parser_token.is_inline_tag && !parser_token.is_unformatted) {
            multi_parser.print_newline(false, multi_parser.output);
          }
          multi_parser.print_token(parser_token.text);
          last_tag_token = parser_token;
          break;
        case 'TK_TAG_HANDLEBARS_ELSE':
          // Don't add a newline if opening {{#if}} tag is on the current line
          var foundIfOnCurrentLine = false;
          for (var lastCheckedOutput = multi_parser.output.length - 1; lastCheckedOutput >= 0; lastCheckedOutput--) {
            if (multi_parser.output[lastCheckedOutput] === '\n') {
              break;
            } else {
              if (multi_parser.output[lastCheckedOutput].match(/{{#if/)) {
                foundIfOnCurrentLine = true;
                break;
              }
            }
          }
          if (!foundIfOnCurrentLine) {
            multi_parser.print_newline(false, multi_parser.output);
          }
          multi_parser.print_token(parser_token.text);
          if (multi_parser.indent_content) {
            multi_parser.indent();
            multi_parser.indent_content = false;
          }
          last_tag_token = parser_token;
          break;
        case 'TK_TAG_HANDLEBARS_COMMENT':
          multi_parser.print_token(parser_token.text);
          break;
        case 'TK_CONTENT':
          multi_parser.traverse_whitespace(raw_token);
          multi_parser.print_token(parser_token.text, true);
          break;
        case 'TK_STYLE':
        case 'TK_SCRIPT':
          if (parser_token.text !== '') {
            multi_parser.print_newline(false, multi_parser.output);
            var text = parser_token.text,
              _beautifier,
              script_indent_level = 1;
            if (parser_token.type === 'TK_SCRIPT') {
              _beautifier = typeof js_beautify === 'function' && js_beautify;
            } else if (parser_token.type === 'TK_STYLE') {
              _beautifier = typeof css_beautify === 'function' && css_beautify;
            }

            if (options.indent_scripts === "keep") {
              script_indent_level = 0;
            } else if (options.indent_scripts === "separate") {
              script_indent_level = -multi_parser.indent_level;
            }

            var indentation = multi_parser.get_full_indent(script_indent_level);
            if (_beautifier) {

              // call the Beautifier if avaliable
              var Child_options = function() {
                this.eol = '\n';
              };
              Child_options.prototype = options;
              var child_options = new Child_options();
              text = _beautifier(text.replace(/^\s*/, indentation), child_options);
            } else {
              // simply indent the string otherwise
              var white = text.match(/^\s*/)[0];
              var _level = white.match(/[^\n\r]*$/)[0].split(multi_parser.indent_string).length - 1;
              var reindent = multi_parser.get_full_indent(script_indent_level - _level);
              text = text.replace(/^\s*/, indentation)
                .replace(/\r\n|\r|\n/g, '\n' + reindent)
                .replace(/\s+$/, '');
            }
            if (text) {
              multi_parser.print_token_raw(text);
              multi_parser.print_newline(true, multi_parser.output);
            }
          }
          break;
        default:
          // We should not be getting here but we don't want to drop input on the floor
          // Just output the text and move on
          if (parser_token.text !== '') {
            multi_parser.print_token(parser_token.text);
          }
          break;
      }
      multi_parser.last_token = parser_token;

      raw_token = this._tokens.next();
    }
    var sweet_code = multi_parser.output.join('').replace(/[\r\n\t ]+$/, '');

    // establish end_with_newline
    if (end_with_newline) {
      sweet_code += '\n';
    }

    if (eol !== '\n') {
      sweet_code = sweet_code.replace(/[\n]/g, eol);
    }

    return sweet_code;
  };
}

module.exports.Beautifier = Beautifier;