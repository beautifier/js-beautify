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

function TokenStream(parent_token) {
  // private
  this._tokens = [];
  this._tokens_length = this._tokens.length;
  this._position = 0;
  this._parent_token = parent_token;

  this.restart = function() {
    this._position = 0;
  };

  this.hasNext = function() {
    return this._position < this._tokens_length;
  };

  this.next = function() {
    var val = null;
    if (this.hasNext()) {
      val = this._tokens[this._position];
      this._position += 1;
    }
    return val;
  };

  this.peek = function(index) {
    var val = null;
    index = index || 0;
    index += this._position;
    if (index >= 0 && index < this._tokens_length) {
      val = this._tokens[index];
    }
    return val;
  };

  this.add = function(token) {
    if (this._parent_token) {
      token.parent = this._parent_token;
    }
    this._tokens.push(token);
    this._tokens_length += 1;
  };
}

module.exports.TokenStream = TokenStream;