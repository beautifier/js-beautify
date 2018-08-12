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

var InputScanner = require('../core/inputscanner').InputScanner;
var Token = require('../core/token').Token;
var TokenStream = require('../core/tokenstream').TokenStream;

var TOKEN = {
  START: 'TK_START',
  RAW: 'TK_RAW',
  EOF: 'TK_EOF'
};

var Tokenizer = function(input_string) { // jshint unused:false
  this._input = new InputScanner(input_string);
  this._tokens = null;
  this._newline_count = 0;
  this._whitespace_before_token = '';

  this._whitespace_pattern = /[\n\r\u2028\u2029\t ]+/g;
  this._newline_pattern = /([\t ]*)(\r\n|[\n\r\u2028\u2029])?/g;
};

Tokenizer.prototype.tokenize = function() {
  this._input.restart();
  this._tokens = new TokenStream();

  this.reset();

  var current;
  var previous = new Token(TOKEN.START, '');
  var open_token = null;
  var open_stack = [];
  var comments = new TokenStream();

  while (previous.type !== TOKEN.EOF) {
    current = this.get_next_token(previous, open_token);
    while (this.is_comment(current)) {
      comments.add(current);
      current = this.get_next_token(previous, open_token);
    }

    if (!comments.isEmpty()) {
      current.comments_before = comments;
      comments = new TokenStream();
    }

    current.parent = open_token;

    if (this.is_opening(current)) {
      current.opened = open_token;
      open_stack.push(open_token);
      open_token = current;
    } else if (open_token && this.is_closing(current, open_token)) {
      current.opened = open_token;
      open_token = open_stack.pop();
      current.parent = open_token;
    }

    current.previous = previous;

    this._tokens.add(current);
    previous = current;
  }

  return this._tokens;
};


Tokenizer.prototype.reset = function() {};

Tokenizer.prototype.get_next_token = function(previous_token, open_token) { // jshint unused:false
  this.readWhitespace();
  var resulting_string = this._input.read(/.+/g);
  if (resulting_string) {
    return this.create_token(TOKEN.RAW, resulting_string);
  } else {
    return this.create_token(TOKEN.EOF, '');
  }
};


Tokenizer.prototype.is_comment = function(current_token) { // jshint unused:false
  return false;
};

Tokenizer.prototype.is_opening = function(current_token) { // jshint unused:false
  return false;
};

Tokenizer.prototype.is_closing = function(current_token, open_token) { // jshint unused:false
  return false;
};

Tokenizer.prototype.create_token = function(type, text) {
  var token = new Token(type, text, this._newline_count, this._whitespace_before_token);
  this._newline_count = 0;
  this._whitespace_before_token = '';
  return token;
};

Tokenizer.prototype.readWhitespace = function() {
  var resulting_string = this._input.read(this._whitespace_pattern);
  if (resulting_string !== '') {
    if (resulting_string === ' ') {
      this._whitespace_before_token = resulting_string;
    } else {
      this._newline_pattern.lastIndex = 0;
      var nextMatch = this._newline_pattern.exec(resulting_string);
      while (nextMatch[2]) {
        this._newline_count += 1;
        nextMatch = this._newline_pattern.exec(resulting_string);
      }
      this._whitespace_before_token = nextMatch[1];
    }
  }
};



module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;