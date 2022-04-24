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

var BaseTokenizer = require('../core/tokenizer').Tokenizer;
var BASETOKEN = require('../core/tokenizer').TOKEN;

var TOKEN = {
    STRING: 'TK_STRING',
    COMMA: 'TK_COMMA',
    UNKNOWN: 'TK_UNKNOWN',
    START: BASETOKEN.START,
    RAW: BASETOKEN.RAW,
    EOF: BASETOKEN.EOF
};

var Tokenizer = function(input_string, options) {
    BaseTokenizer.call(this, input_string, options);

    this._position_map = {};
};
Tokenizer.prototype = new BaseTokenizer();

Tokenizer.prototype._get_next_token = function(previous_token, open_token) { // jshint unused:false
    var token = null;
    var pos;
    this._readWhitespace();
    var c = this._input.peek();

    if(c === null) {
        pos = this._input.__position;
        return this._create_token_with_pos(TOKEN.EOF, '', [pos, pos]);
    }

    token = token || this._read_strings(c);
    token = token || this._read_commas(c);
    if(!token) {
        pos = this._input.__position;
        token = this._create_token_with_pos(TOKEN.UNKNOWN, this._input.next(), [pos, pos]);
    }

    return token;
};

Tokenizer.prototype._create_token_with_pos = function (type, text, position) {
    var token = BaseTokenizer.prototype._create_token.call(this, type, text);
    token.position = position;
    this._position_map[position[0]] = token;
    return token;
};

Tokenizer.prototype.get_positional_map = function () {
    return this._position_map;
};

Tokenizer.prototype._read_commas = function (c) {
    var token = null;

    if (c === ',') {
        var pos = this._input.__position;
        this._input.next();
        token = this._create_token_with_pos(TOKEN.COMMA, c, [pos, pos]);
    }

    return token;
};

Tokenizer.prototype._read_strings = function(c) {
    if (c === '\'' || c === '"') {
        var startPos = this._input.__position;

        var result = c;
        this._input.next(); // skip current char
        var ch = this._input.next();
        while (ch) {
            result += ch;
            if (ch === "\\") {
                result += this._input.next();
            } else if (c.indexOf(ch) !== -1 || ch === "\n") {
                break;
            }
            ch = this._input.next();
        }

        var endPos = this._input.__position - 1;
        return this._create_token_with_pos(TOKEN.STRING, result, [startPos, endPos]);
    }

    return null;
};

module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;