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

var BaseTokenizer = require('../core/tokenizer').Tokenizer;
var BASETOKEN = require('../core/tokenizer').TOKEN;
var Directives = require('../core/directives').Directives;
var acorn = require('../core/acorn');

var TOKEN = {
  TAG_OPEN: 'TK_TAG_OPEN',
  TAG_CLOSE: 'TK_TAG_CLOSE',
  ATTRIBUTE: 'TK_ATTRIBUTE',
  EQUALS: 'TK_EQUALS',
  VALUE: 'TK_VALUE',
  COMMENT: 'TK_COMMENT',
  TEXT: 'TK_TEXT',
  UNKNOWN: 'TK_UNKNOWN',
  START: BASETOKEN.START,
  RAW: BASETOKEN.RAW,
  EOF: BASETOKEN.EOF
};

var directives_core = new Directives(/<\!--/, /-->/);

var Tokenizer = function(input_string, opts) {
  BaseTokenizer.call(this, input_string);
  this._opts = opts || {};
  this._current_tag_name = '';

  // Words end at whitespace or when a tag starts
  // if we are indenting handlebars, they are considered tags
  this._word_pattern = this._opts.indent_handlebars ? /[\s<]|{{/g : /[\s<]/g;
};
Tokenizer.prototype = new BaseTokenizer();

Tokenizer.prototype.is_comment = function(current_token) { // jshint unused:false
  return false; //current_token.type === TOKEN.COMMENT || current_token.type === TOKEN.UNKNOWN;
};

Tokenizer.prototype.is_opening = function(current_token) {
  return current_token.type === TOKEN.TAG_OPEN;
};

Tokenizer.prototype.is_closing = function(current_token, open_token) {
  return current_token.type === TOKEN.TAG_CLOSE &&
    (open_token && (
      ((current_token.text === '>' || current_token.text === '/>') && open_token.text[0] === '<') ||
      (current_token.text === '}}' && open_token.text[0] === '{' && open_token.text[1] === '{')));
};

Tokenizer.prototype.reset = function() {
  this._current_tag_name = '';
};

Tokenizer.prototype.get_next_token = function(previous_token, open_token) { // jshint unused:false
  this.readWhitespace();
  var token = null;
  var c = this._input.peek();

  if (c === null) {
    return this.create_token(TOKEN.EOF, '');
  }

  token = token || this._read_attribute(c, previous_token, open_token);
  token = token || this._read_raw_content(previous_token, open_token);
  token = token || this._read_comment(c);
  token = token || this._read_open_close(c, open_token);
  token = token || this._read_content_word();
  token = token || this.create_token(TOKEN.UNKNOWN, this._input.next());

  return token;
};


Tokenizer.prototype._read_comment = function(c) { // jshint unused:false
  var token = null;
  if (c === '<' || c === '{') {
    var peek1 = this._input.peek(1);
    var peek2 = this._input.peek(2);
    if ((c === '<' && (peek1 === '!' || peek1 === '?' || peek1 === '%')) ||
      this._opts.indent_handlebars && c === '{' && peek1 === '{' && peek2 === '!') {
      //if we're in a comment, do something special
      // We treat all comments as literals, even more than preformatted tags
      // we just look for the appropriate close tag

      // this is will have very poor perf, but will work for now.
      var comment = '',
        delimiter = '>',
        matched = false;

      var input_char = this._input.next();

      while (input_char) {
        comment += input_char;

        // only need to check for the delimiter if the last chars match
        if (comment.charAt(comment.length - 1) === delimiter.charAt(delimiter.length - 1) &&
          comment.indexOf(delimiter) !== -1) {
          break;
        }

        // only need to search for custom delimiter for the first few characters
        if (!matched) {
          matched = comment.length > 10;
          if (comment.indexOf('<![if') === 0) { //peek for <![if conditional comment
            delimiter = '<![endif]>';
            matched = true;
          } else if (comment.indexOf('<![cdata[') === 0) { //if it's a <[cdata[ comment...
            delimiter = ']]>';
            matched = true;
          } else if (comment.indexOf('<![') === 0) { // some other ![ comment? ...
            delimiter = ']>';
            matched = true;
          } else if (comment.indexOf('<!--') === 0) { // <!-- comment ...
            delimiter = '-->';
            matched = true;
          } else if (comment.indexOf('{{!--') === 0) { // {{!-- handlebars comment
            delimiter = '--}}';
            matched = true;
          } else if (comment.indexOf('{{!') === 0) { // {{! handlebars comment
            if (comment.length === 5 && comment.indexOf('{{!--') === -1) {
              delimiter = '}}';
              matched = true;
            }
          } else if (comment.indexOf('<?') === 0) { // {{! handlebars comment
            delimiter = '?>';
            matched = true;
          } else if (comment.indexOf('<%') === 0) { // {{! handlebars comment
            delimiter = '%>';
            matched = true;
          }
        }

        input_char = this._input.next();
      }

      var directives = directives_core.get_directives(comment);
      if (directives && directives.ignore === 'start') {
        comment += directives_core.readIgnored(this._input);
      }
      comment = comment.replace(acorn.allLineBreaks, '\n');
      token = this.create_token(TOKEN.COMMENT, comment);
      token.directives = directives;
    }
  }

  return token;
};

Tokenizer.prototype._read_open_close = function(c, open_token) { // jshint unused:false
  var resulting_string = null;
  if (open_token && open_token.text[0] === '<' && (c === '>' || (c === '/' && this._input.peek(1) === '>'))) {
    resulting_string = this._input.next();
    if (this._input.peek() === '>') {
      resulting_string += this._input.next();
    }
    return this.create_token(TOKEN.TAG_CLOSE, resulting_string);
  } else if (open_token && open_token.text[0] === '{' && c === '}' && this._input.peek(1) === '}') {
    this._input.next();
    this._input.next();
    return this.create_token(TOKEN.TAG_CLOSE, '}}');
  } else if (!open_token) {
    if (c === '<') {
      resulting_string = this._input.next();
      resulting_string += this._input.read(/[^\s>{][^\s>{/]*/g);
      return this.create_token(TOKEN.TAG_OPEN, resulting_string);
    } else if (this._opts.indent_handlebars && c === '{' && this._input.peek(1) === '{') {
      this._input.next();
      this._input.next();
      resulting_string = '{{';
      resulting_string += this._input.readUntil(/[\s}]/g);
      return this.create_token(TOKEN.TAG_OPEN, resulting_string);
    }
  }
  return null;
};

Tokenizer.prototype._read_attribute = function(c, previous_token, open_token) { // jshint unused:false
  if (open_token && open_token.text[0] === '<') {
    if (c === '=') {
      return this.create_token(TOKEN.EQUALS, this._input.next());
    } else if (c === '"' || c === "'") {
      var content = this._input.next();
      var input_string = '';
      var string_pattern = new RegExp(c + '|{{', 'g');
      while (this._input.hasNext()) {
        input_string = this._input.readUntilAfter(string_pattern);
        content += input_string;
        if (input_string[input_string.length - 1] === '"' || input_string[input_string.length - 1] === "'") {
          break;
        } else if (this._input.hasNext()) {
          content += this._input.readUntilAfter(/}}/g);
        }
      }

      return this.create_token(TOKEN.VALUE, content);
    }

    var resulting_string = '';

    if (c === '{' && this._input.peek(1) === '{') {
      resulting_string = this._input.readUntilAfter(/}}/g);
    } else {
      resulting_string = this._input.readUntil(/[\s=\/>]/g);
    }

    if (resulting_string) {
      if (previous_token.type === TOKEN.EQUALS) {
        return this.create_token(TOKEN.VALUE, resulting_string);
      } else {
        return this.create_token(TOKEN.ATTRIBUTE, resulting_string);
      }
    }
  }
  return null;
};

Tokenizer.prototype._read_raw_content = function(previous_token, open_token) { // jshint unused:false
  var resulting_string = '';
  if (open_token && open_token.text[0] === '{') {
    resulting_string = this._input.readUntil(/}}/g);
    if (resulting_string) {
      return this.create_token(TOKEN.TEXT, resulting_string);
    }
  } else if (previous_token.type === TOKEN.TAG_CLOSE && (previous_token.opened.text[0] === '<')) {
    var tag_name = previous_token.opened.text.substr(1).toLowerCase();
    if (tag_name === 'script' || tag_name === 'style' ||
      this._opts.content_unformatted.indexOf(tag_name) !== -1 ||
      this._opts.unformatted.indexOf(tag_name) !== -1) {
      return this.create_token(TOKEN.TEXT, this._input.readUntil(new RegExp('</' + tag_name + '\\s*?>', 'ig')));
    }
  }
  return null;
};

Tokenizer.prototype._read_content_word = function() {
  // if we get here and we see handlebars treat them as a
  var resulting_string = this._input.readUntil(this._word_pattern);
  if (resulting_string) {
    return this.create_token(TOKEN.TEXT, resulting_string);
  }
};

module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;