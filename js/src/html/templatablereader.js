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

function PatternReader(input_scanner, parent) {
  this._input = input_scanner;
  this._until_pattern = parent && parent._until_pattern ? new RegExp(parent._until_pattern) : null;
  this._from_pattern = parent && parent._from_pattern ? new RegExp(parent._from_pattern) : null;
  this._include_match = parent ? parent._include_match : false;
}

PatternReader.prototype._read = function() {
  var result = '';
  if (this._from_pattern) {
    result = this._input.read(this._from_pattern, this._until_pattern, this._include_match);
  } else {
    result = this._input.readUntil(this._until_pattern, this._include_match);
  }
  return result;
};

PatternReader.prototype.read = function() {
  return this._read();
};

PatternReader.prototype.until_after = function(pattern) {
  var result = this._create();
  result.include_match = true;
  result._until_pattern = pattern;
  result._update();
  return result;
};

PatternReader.prototype.until = function(pattern) {
  var result = this._create();
  result.include_match = false;
  result._until_pattern = pattern;
  result._update();
  return result;
};

PatternReader.prototype.from = function(pattern) {
  var result = this._create();
  result._from_pattern = pattern;
  result._update();
  return result;
};

PatternReader.prototype._create = function() {
  return new PatternReader(this._input, this);
};

PatternReader.prototype._update = function() {};

// This lets templates appear anywhere we would do a readUntil
// The cost is higher but it is pay to play.
function TemplatableReader(input_scanner, parent) {
  PatternReader.call(this, input_scanner, parent);
  this.__template_pattern = parent && parent.__template_pattern ? new RegExp(parent.__template_pattern) : null;
  this._excluded = {
    django: false,
    erb: false,
    handlebars: false,
    php: false
  };
  if (parent) {
    this._excluded = Object.assign(this._excluded, parent._excluded);
  }
  var pattern_reader = new PatternReader(input_scanner);
  this.__patterns = {
    handlebars_comment: pattern_reader.from(/{{!--/g).until_after(/--}}/g),
    handlebars: pattern_reader.from(/{{/g).until_after(/}}/g),
    php: pattern_reader.from(/<\?(?:[=]|php)/g).until_after(/\?>/g),
    erb: pattern_reader.from(/<%[^%]/g).until_after(/[^%]%>/g),
    // django coflicts with handlebars a bit.
    django: pattern_reader.from(/{%/g).until_after(/%}/g),
    django_value: pattern_reader.from(/{{/g).until_after(/}}/g),
    django_comment: pattern_reader.from(/{#/g).until_after(/#}/g)
  };
}
TemplatableReader.prototype = new PatternReader();

TemplatableReader.prototype._create = function() {
  return new TemplatableReader(this._input, this);
};

TemplatableReader.prototype._update = function() {
  this.__set_templated_pattern();
};

TemplatableReader.prototype.exclude = function(language) {
  var result = this._create();
  result._excluded[language] = true;
  result._update();
  return result;
};

TemplatableReader.prototype.read = function() {
  var result = '';
  if (this._from_pattern) {
    result = this._input.read(this._from_pattern, this.__template_pattern);
    if (!result) {
      return result;
    }
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

  items.push(this.__patterns.php._from_pattern.source);
  items.push(this.__patterns.handlebars._from_pattern.source);
  items.push(this.__patterns.erb._from_pattern.source);
  items.push(this.__patterns.django._from_pattern.source);
  items.push(this.__patterns.django_value._from_pattern.source);
  items.push(this.__patterns.django_comment._from_pattern.source);

  if (this._until_pattern) {
    items.push(this._until_pattern.source);
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
    if (!this._excluded.php && peek1 === '?') {
      resulting_string = resulting_string ||
        this.__patterns.php.read();
    }
    if (!this._excluded.erb && peek1 === '%') {
      resulting_string = resulting_string ||
        this.__patterns.erb.read();
    }
  } else if (c === '{') {
    if (!this._excluded.handlebars) {
      resulting_string = resulting_string ||
        this.__patterns.handlebars_comment.read();
      resulting_string = resulting_string ||
        this.__patterns.handlebars.read();
    }
    // django coflicts with handlebars a bit.
    if (!this._excluded.django && !this._excluded.handlebars) {
      resulting_string = resulting_string ||
        this.__patterns.django_value.read();
    }
    if (!this._excluded.django) {
      resulting_string = resulting_string ||
        this.__patterns.django_comment.read();
      resulting_string = resulting_string ||
        this.__patterns.django.read();
    }
  }
  return resulting_string;
};


module.exports.TemplatableReader = TemplatableReader;
