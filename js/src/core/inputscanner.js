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

function InputScanner(input_string) {
  this._input = input_string || '';
  this._input_length = this._input.length;
  this._position = 0;
}

InputScanner.prototype.restart = function() {
  this._position = 0;
};

InputScanner.prototype.back = function() {
  if (this._position > 0) {
    this._position -= 1;
  }
};

InputScanner.prototype.hasNext = function() {
  return this._position < this._input_length;
};

InputScanner.prototype.next = function() {
  var val = null;
  if (this.hasNext()) {
    val = this._input.charAt(this._position);
    this._position += 1;
  }
  return val;
};

InputScanner.prototype.peek = function(index) {
  var val = null;
  index = index || 0;
  index += this._position;
  if (index >= 0 && index < this._input_length) {
    val = this._input.charAt(index);
  }
  return val;
};

InputScanner.prototype.test = function(pattern, index) {
  index = index || 0;
  index += this._position;
  pattern.lastIndex = index;

  if (index >= 0 && index < this._input_length) {
    var pattern_match = pattern.exec(this._input);
    return pattern_match && pattern_match.index === index;
  } else {
    return false;
  }
};

InputScanner.prototype.testChar = function(pattern, index) {
  // test one character regex match
  var val = this.peek(index);
  return val !== null && pattern.test(val);
};

InputScanner.prototype.match = function(pattern) {
  pattern.lastIndex = this._position;
  var pattern_match = pattern.exec(this._input);
  if (pattern_match && pattern_match.index === this._position) {
    this._position += pattern_match[0].length;
  } else {
    pattern_match = null;
  }
  return pattern_match;
};

InputScanner.prototype.read = function(pattern) {
  var val = '';
  var match = this.match(pattern);
  if (match) {
    val = match[0];
  }
  return val;
};

InputScanner.prototype.readUntil = function(pattern, include_match) {
  var val = '';
  var match_index = this._position;
  pattern.lastIndex = this._position;
  var pattern_match = pattern.exec(this._input);
  if (pattern_match) {
    if (include_match) {
      match_index = pattern_match.index + pattern_match[0].length;
    } else {
      match_index = pattern_match.index;
    }
  } else {
    match_index = this._input_length;
  }

  val = this._input.substring(this._position, match_index);
  this._position = match_index;
  return val;
};

InputScanner.prototype.readUntilAfter = function(pattern) {
  return this.readUntil(pattern, true);
};

/* css beautifier legacy helpers */
InputScanner.prototype.peekUntilAfter = function(pattern) {
  var start = this._position;
  var val = this.readUntilAfter(pattern);
  this._position = start;
  return val;
};

InputScanner.prototype.lookBack = function(testVal) {
  var start = this._position - 1;
  return start >= testVal.length && this._input.substring(start - testVal.length, start)
    .toLowerCase() === testVal;
};


module.exports.InputScanner = InputScanner;