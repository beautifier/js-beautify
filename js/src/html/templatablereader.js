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

function PatternReader(input_scanner) {
  this._input = input_scanner;
  this._until_pattern = null;
  this._from_pattern = null;
  this._include_match = false;
}

PatternReader.prototype.read = function() {
  var result = '';
  if (this._from_pattern) {
    result = this._input.read(this._from_pattern, this._until_pattern, this._include_match);
  } else {
    result = this._input.readUntil(this._until_pattern, this._include_match);
  }
  return result;
};

PatternReader.prototype.until_after = function(pattern) {
  this.include_match = true;
  this._until_pattern = pattern;
  return this;
};

PatternReader.prototype.until = function(pattern) {
  this.include_match = false;
  this._until_pattern = pattern;
  return this;
};

PatternReader.prototype.from = function(pattern) {
  this._from_pattern = pattern;
  return this;
};

function TemplatableReader(input_scanner) {
  PatternReader.call(this, input_scanner);
  this.__template_pattern = null;
  this.handlebars = true;
  this.php = true;
  this.asp = true;
  this.__language = {
    handlebars_comment: new PatternReader(input_scanner).from(/{{!--/g).until_after(/--}}/g),
    handlebars: new PatternReader(input_scanner).from(/{{/g).until_after(/}}/g),
    php: new PatternReader(input_scanner).from(/<\?(?:[=]|php)/g).until_after(/\?>/g),
    asp: new PatternReader(input_scanner).from(/<%/g).until_after(/%>/g)
  };
}
TemplatableReader.prototype = new PatternReader();

// This lets templates appear anywhere we would do a readUntil
// The cost is higher but it is pay to play.
TemplatableReader.prototype.with_templates = function() {
  this.__set_templated_pattern();
  return this;
};

TemplatableReader.prototype.read = function() {
  var result;
  if (this._from_pattern) {
    result = this._input.read(this._from_pattern, this.__template_pattern);
  } else {
    result = this._input.readUntil(this.__template_pattern);
  }
  var next = '';
  do {
    result += next;
    next = this.read_template();
    if (next !== '') {
      next += this._input.readUntil(this.__template_pattern);
    }
  } while (this._input.hasNext() && next !== '');
  result += next;

  if (this.include_match) {
    result += this._input.readUntilAfter(this._until_pattern);
  }
  return result;
};

TemplatableReader.prototype.__set_templated_pattern = function() {
  var items = [];

  if (this._until_pattern) {
    items.push(this._until_pattern.source);
  }

  if (this.php) {
    items.push(this.__language.php._from_pattern.source);
  }

  if (this.handlebars) {
    items.push(this.__language.handlebars._from_pattern.source);
  }

  if (this.asp) {
    items.push(this.__language.asp._from_pattern.source);
  }

  this.__template_pattern = new RegExp('(?:' + items.join('|') + ')', 'g');
};

TemplatableReader.prototype.read_template = function() {
  var resulting_string = '';
  var c = this._input.peek();
  if (c === '<') {
    var peek1 = this._input.peek(1);
    //if we're in a comment, do something special
    // We treat all comments as literals, even more than preformatted tags
    // we just look for the appropriate close tag
    if (this.php && peek1 === '?') {
      resulting_string = resulting_string ||
        this.__language.php.read();
    }
    if (this.asp && peek1 === '%') {
      resulting_string = resulting_string ||
        this.__language.asp.read();
    }
  } else if (c === '{') {
    if (this.handlebars) {
      resulting_string = resulting_string ||
        this.__language.handlebars_comment.read();
      resulting_string = resulting_string ||
        this.__language.handlebars.read();
    }
  }
  return resulting_string;
};


module.exports.TemplatableReader = TemplatableReader;
