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

var TOKEN = {
  RAW: 'TK_RAW',
  EOF: 'TK_EOF'
};

function Tokenizer(input_string, opts) { // jshint unused:false

  this._input = null;
  this._tokens = null;

  this.tokenize = function() {
    this._input = new InputScanner(input_string);
    this._tokens = []; //new TokenStream();

    this.reset();

    var current, last;
    var open_token = null;
    var open_stack = [];
    var comments = [];

    while (!(last && last.type === TOKEN.EOF)) {
      current = this.get_next_token();
      while (this.is_comment(current)) {
        comments.push(current);
        current = this.get_next_token();
      }

      if (comments.length) {
        current.comments_before = comments;
        comments = [];
      }

      if (this.is_opening(current)) {
        current.parent = last;
        open_stack.push(open_token);
        open_token = current;
      } else if (open_token && this.is_closing(current, open_token)) {
        current.parent = open_token.parent;
        current.opened = open_token;

        open_token = open_stack.pop();
      }

      this._tokens.push(current);
      last = current;
    }

    return this._tokens;
  };

  this.reset = function() {
  };

  this.get_next_token = function() {
    var resulting_string = this._input.readWhile(/.+/g);
    if (resulting_string) {
      return new Token(TOKEN.RAW, resulting_string, 0, '');
    } else {
      return new Token(TOKEN.EOF, '', 0, '');
    }
  };


  this.is_comment = function(current_token) { // jshint unused:false
    return false;
  };

  this.is_opening = function(current_token) { // jshint unused:false
    return false;
  };

  this.is_closing = function(current_token, open_token) { // jshint unused:false
    return false;
  };
}


module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;