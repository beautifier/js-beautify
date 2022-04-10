/*jshint node:true */
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

'use strict';

//var InputScanner = require('../core/inputscanner').InputScanner;
var BaseTokenizer = require('../core/tokenizer').Tokenizer;
var BASETOKEN = require('../core/tokenizer').TOKEN;
var Directives = require('../core/directives').Directives;
var Pattern = require('../core/pattern').Pattern;
var TemplatablePattern = require('../core/templatablepattern').TemplatablePattern;


var TOKEN = {
  STRING: 'TK_STRING',
  BLOCK_COMMENT: 'TK_BLOCK_COMMENT',
  COMMENT: 'TK_COMMENT',
  LEGACY: 'TK_LEGACY',
  UNKNOWN: 'TK_UNKNOWN',
  START: BASETOKEN.START,
  RAW: BASETOKEN.RAW,
  EOF: BASETOKEN.EOF
};

var directives_core = new Directives(/\/\*/, /\*\//);


// Whether a single character denotes a newline.

var newline = /[\n\r]/;

// Matches a whole line break (where CRLF is considered a single
// line break). Used to count lines.

// in javascript, these two differ
// in python they are the same, different methods are called on them
var lineBreak = new RegExp('\r\n|' + newline.source);
var allLineBreaks = new RegExp(lineBreak.source, 'g');



var Tokenizer = function(input_string, options) {
  BaseTokenizer.call(this, input_string, options);

  this._patterns.whitespace = this._patterns.whitespace.matching(
    /\u00A0\u1680\u180e\u2000-\u200a\u202f\u205f\u3000\ufeff/.source,
    /\u2028\u2029/.source);

  var pattern_reader = new Pattern(this._input);
  var templatable = new TemplatablePattern(this._input)
    .read_options(this._options);

  this.__patterns = {
    template: templatable,
    // comment ends just before nearest linefeed or end of file
    comment: pattern_reader.starting_with(/\/\//).until(/[\n\r\u2028\u2029]/),
    //  /* ... */ comment ends with nearest */ or end of file
    block_comment: pattern_reader.starting_with(/\/\*/).until_after(/\*\//),
    single_quote: templatable.until(/['\\\n\r\u2028\u2029]/),
    double_quote: templatable.until(/["\\\n\r\u2028\u2029]/)
  };

};

Tokenizer.prototype = new BaseTokenizer();

Tokenizer.prototype._is_comment = function(current_token) {
  return current_token.type === TOKEN.COMMENT || current_token.type === TOKEN.BLOCK_COMMENT || current_token.type === TOKEN.UNKNOWN;
};

Tokenizer.prototype._is_opening = function(current_token) {
  return current_token === null;
};

Tokenizer.prototype._is_closing = function(current_token, open_token) {
  return current_token === null && open_token === null;
};

Tokenizer.prototype._reset = function() {
};

Tokenizer.prototype._get_next_token = function(previous_token, open_token) { // jshint unused:false
  var token = null;
  this._readWhitespace();
  var c = this._input.peek();

  if (c === null) {
    return this._create_token(TOKEN.EOF, '');
  }

  // token = token || this._read_string(c);
  // token = token || this._read_comment(c);
  token = token || this._read_legacy(previous_token);
  token = token || this._create_token(TOKEN.UNKNOWN, this._input.next());

  return token;
};

Tokenizer.prototype._read_legacy = function(previous_token) {
  var token = this._create_token(TOKEN.LEGACY, this._input.next());

  // legacy doesn't understand the whitespace before text
  token.text = token.whitespace_before + token.text;
  for (var x = 0; x < token.newlines; x++) {
    token.text = '\n' + token.text;
  }

  // it also is the fall through of other tokens
  // so we attempt to match other tokens and
  // start or add to legacy if no other token is matched
  if (previous_token.type === TOKEN.LEGACY) {
    previous_token.text += token.text;
    token = previous_token;
  }

  return token;
};

Tokenizer.prototype._read_comment = function(c) {
  var token = null;
  if (c === '/') {
    var comment = '';
    if (this._input.peek(1) === '*') {
      // peek for comment /* ... */
      comment = this.__patterns.block_comment.read();
      var directives = directives_core.get_directives(comment);
      if (directives && directives.ignore === 'start') {
        comment += directives_core.readIgnored(this._input);
      }
      comment = comment.replace(allLineBreaks, '\n');
      token = this._create_token(TOKEN.BLOCK_COMMENT, comment);
      token.directives = directives;
    } else if (this._input.peek(1) === '/') {
      // peek for comment // ...
      comment = this.__patterns.comment.read();
      token = this._create_token(TOKEN.COMMENT, comment);
    }
  }
  return token;
};

Tokenizer.prototype._read_string = function(c) {
  if (c === '`' || c === "'" || c === '"') {
    var resulting_string = this._input.next();
    this.has_char_escapes = false;

    if (c === '`') {
      resulting_string += this._read_string_recursive('`', true, '${');
    } else {
      resulting_string += this._read_string_recursive(c);
    }

    if (this._input.peek() === c) {
      resulting_string += this._input.next();
    }

    resulting_string = resulting_string.replace(allLineBreaks, '\n');

    return this._create_token(TOKEN.STRING, resulting_string);
  }

  return null;
};

module.exports.allLineBreaks = allLineBreaks;

module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;
