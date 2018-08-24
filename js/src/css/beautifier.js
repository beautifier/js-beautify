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

var Options = require('./options').Options;
var acorn = require('../core/acorn');
var Output = require('../core/output').Output;
var InputScanner = require('../core/inputscanner').InputScanner;

var lineBreak = acorn.lineBreak;
var allLineBreaks = acorn.allLineBreaks;

function Beautifier(source_text, options) {
  this._source_text = source_text || '';
  // Allow the setting of language/file-type specific options
  // with inheritance of overall settings
  this._options = new Options(options);

  // tokenizer
  var whitespaceChar = /\s/;
  var whitespacePattern = /(?:\s|\n)+/g;
  var block_comment_pattern = /\/\*(?:[\s\S]*?)((?:\*\/)|$)/g;
  var comment_pattern = /\/\/(?:[^\n\r\u2028\u2029]*)/g;

  var ch;
  var parenLevel = 0;
  var input;

  function eatString(endChars) {
    var result = '';
    ch = input.next();
    while (ch) {
      result += ch;
      if (ch === "\\") {
        result += input.next();
      } else if (endChars.indexOf(ch) !== -1 || ch === "\n") {
        break;
      }
      ch = input.next();
    }
    return result;
  }

  // Skips any white space in the source text from the current position.
  // When allowAtLeastOneNewLine is true, will output new lines for each
  // newline character found; if the user has preserve_newlines off, only
  // the first newline will be output
  this.eatWhitespace = function(allowAtLeastOneNewLine) {
    var result = whitespaceChar.test(input.peek());
    var isFirstNewLine = true;

    while (whitespaceChar.test(input.peek())) {
      ch = input.next();
      if (allowAtLeastOneNewLine && ch === '\n') {
        if (this._options.preserve_newlines || isFirstNewLine) {
          isFirstNewLine = false;
          output.add_new_line(true);
        }
      }
    }
    return result;
  };

  // Nested pseudo-class if we are insideRule
  // and the next special character found opens
  // a new block
  function foundNestedPseudoClass() {
    var openParen = 0;
    var i = 1;
    var ch = input.peek(i);
    while (ch) {
      if (ch === "{") {
        return true;
      } else if (ch === '(') {
        // pseudoclasses can contain ()
        openParen += 1;
      } else if (ch === ')') {
        if (openParen === 0) {
          return false;
        }
        openParen -= 1;
      } else if (ch === ";" || ch === "}") {
        return false;
      }
      i++;
      ch = input.peek(i);
    }
    return false;
  }

  var indentLevel;
  var nestedLevel;
  var output;

  function print_string(output_string) {
    if (output.just_added_newline()) {
      output.set_indent(indentLevel);
    }
    output.add_token(output_string);
  }

  function preserveSingleSpace(isAfterSpace) {
    if (isAfterSpace) {
      output.space_before_token = true;
    }
  }

  function indent() {
    indentLevel++;
  }

  function outdent() {
    if (indentLevel > 0) {
      indentLevel--;
    }
  }

  /*_____________________--------------------_____________________*/

  this.beautify = function() {
    if (this._options.disabled) {
      return this._source_text;
    }

    var source_text = this._source_text;
    var eol = this._options.eol;
    if (eol === 'auto') {
      eol = '\n';
      if (source_text && lineBreak.test(source_text || '')) {
        eol = source_text.match(lineBreak)[0];
      }
    }


    // HACK: newline parsing inconsistent. This brute force normalizes the input.
    source_text = source_text.replace(allLineBreaks, '\n');

    // reset
    var baseIndentString = '';
    var preindent_index = 0;
    if (source_text && source_text.length) {
      while ((source_text.charAt(preindent_index) === ' ' || source_text.charAt(preindent_index) === '\t')) {
        preindent_index += 1;
      }
      baseIndentString = source_text.substring(0, preindent_index);
      source_text = source_text.substring(preindent_index);
    }

    output = new Output(this._options.indent_string, baseIndentString);
    input = new InputScanner(source_text);
    indentLevel = 0;
    nestedLevel = 0;

    ch = null;
    parenLevel = 0;

    var insideRule = false;
    // This is the value side of a property value pair (blue in the following ex)
    // label { content: blue }
    var insidePropertyValue = false;
    var enteringConditionalGroup = false;
    var insideAtExtend = false;
    var insideAtImport = false;
    var topCharacter = ch;

    while (true) {
      var whitespace = input.read(whitespacePattern);
      var isAfterSpace = whitespace !== '';
      var previous_ch = topCharacter;
      ch = input.next();
      topCharacter = ch;

      if (!ch) {
        break;
      } else if (ch === '/' && input.peek() === '*') {
        // /* css comment */
        // Always start block comments on a new line.
        // This handles scenarios where a block comment immediately
        // follows a property definition on the same line or where
        // minified code is being beautified.
        output.add_new_line();
        input.back();
        print_string(input.read(block_comment_pattern));

        // Ensures any new lines following the comment are preserved
        this.eatWhitespace(true);

        // Block comments are followed by a new line so they don't
        // share a line with other properties
        output.add_new_line();
      } else if (ch === '/' && input.peek() === '/') {
        // // single line comment
        // Preserves the space before a comment
        // on the same line as a rule
        output.space_before_token = true;
        input.back();
        print_string(input.read(comment_pattern));

        // Ensures any new lines following the comment are preserved
        this.eatWhitespace(true);
      } else if (ch === '@') {
        preserveSingleSpace(isAfterSpace);

        // deal with less propery mixins @{...}
        if (input.peek() === '{') {
          print_string(ch + eatString('}'));
        } else {
          print_string(ch);

          // strip trailing space, if present, for hash property checks
          var variableOrRule = input.peekUntilAfter(/[: ,;{}()[\]\/='"]/g);

          if (variableOrRule.match(/[ :]$/)) {
            // we have a variable or pseudo-class, add it and insert one space before continuing
            variableOrRule = eatString(": ").replace(/\s$/, '');
            print_string(variableOrRule);
            output.space_before_token = true;
          }

          variableOrRule = variableOrRule.replace(/\s$/, '');

          if (variableOrRule === 'extend') {
            insideAtExtend = true;
          } else if (variableOrRule === 'import') {
            insideAtImport = true;
          }

          // might be a nesting at-rule
          if (variableOrRule in this.NESTED_AT_RULE) {
            nestedLevel += 1;
            if (variableOrRule in this.CONDITIONAL_GROUP_RULE) {
              enteringConditionalGroup = true;
            }
            // might be less variable
          } else if (!insideRule && parenLevel === 0 && variableOrRule.indexOf(':') !== -1) {
            insidePropertyValue = true;
            indent();
          }
        }
      } else if (ch === '#' && input.peek() === '{') {
        preserveSingleSpace(isAfterSpace);
        print_string(ch + eatString('}'));
      } else if (ch === '{') {
        if (insidePropertyValue) {
          insidePropertyValue = false;
          outdent();
        }
        indent();
        output.space_before_token = true;
        print_string(ch);

        // when entering conditional groups, only rulesets are allowed
        if (enteringConditionalGroup) {
          enteringConditionalGroup = false;
          insideRule = (indentLevel > nestedLevel);
        } else {
          // otherwise, declarations are also allowed
          insideRule = (indentLevel >= nestedLevel);
        }
        if (this._options.newline_between_rules && insideRule) {
          if (output.previous_line && output.previous_line.item(-1) !== '{') {
            output.ensure_empty_line_above('/', ',');
          }
        }
        this.eatWhitespace(true);
        output.add_new_line();
      } else if (ch === '}') {
        outdent();
        output.add_new_line();
        if (previous_ch === '{') {
          output.trim(true);
        }
        insideAtImport = false;
        insideAtExtend = false;
        if (insidePropertyValue) {
          outdent();
          insidePropertyValue = false;
        }
        print_string(ch);
        insideRule = false;
        if (nestedLevel) {
          nestedLevel--;
        }

        this.eatWhitespace(true);
        output.add_new_line();

        if (this._options.newline_between_rules && !output.just_added_blankline()) {
          if (input.peek() !== '}') {
            output.add_new_line(true);
          }
        }
      } else if (ch === ":") {
        if ((insideRule || enteringConditionalGroup) && !(input.lookBack("&") || foundNestedPseudoClass()) && !input.lookBack("(") && !insideAtExtend) {
          // 'property: value' delimiter
          // which could be in a conditional group query
          print_string(':');
          if (!insidePropertyValue) {
            insidePropertyValue = true;
            output.space_before_token = true;
            this.eatWhitespace(true);
            indent();
          }
        } else {
          // sass/less parent reference don't use a space
          // sass nested pseudo-class don't use a space

          // preserve space before pseudoclasses/pseudoelements, as it means "in any child"
          if (input.lookBack(" ")) {
            output.space_before_token = true;
          }
          if (input.peek() === ":") {
            // pseudo-element
            ch = input.next();
            print_string("::");
          } else {
            // pseudo-class
            print_string(':');
          }
        }
      } else if (ch === '"' || ch === '\'') {
        preserveSingleSpace(isAfterSpace);
        print_string(ch + eatString(ch));
        this.eatWhitespace(true);
      } else if (ch === ';') {
        if (insidePropertyValue) {
          outdent();
          insidePropertyValue = false;
        }
        insideAtExtend = false;
        insideAtImport = false;
        print_string(ch);
        this.eatWhitespace(true);

        // This maintains single line comments on the same
        // line. Block comments are also affected, but
        // a new line is always output before one inside
        // that section
        if (input.peek() !== '/') {
          output.add_new_line();
        }
      } else if (ch === '(') { // may be a url
        if (input.lookBack("url")) {
          print_string(ch);
          this.eatWhitespace();
          ch = input.next();
          if (ch === ')' || ch === '"' || ch !== '\'') {
            input.back();
            parenLevel++;
          } else if (ch) {
            print_string(ch + eatString(')'));
          }
        } else {
          parenLevel++;
          preserveSingleSpace(isAfterSpace);
          print_string(ch);
          this.eatWhitespace();
        }
      } else if (ch === ')') {
        print_string(ch);
        parenLevel--;
      } else if (ch === ',') {
        print_string(ch);
        this.eatWhitespace(true);
        if (this._options.selector_separator_newline && !insidePropertyValue && parenLevel < 1 && !insideAtImport) {
          output.add_new_line();
        } else {
          output.space_before_token = true;
        }
      } else if ((ch === '>' || ch === '+' || ch === '~') && !insidePropertyValue && parenLevel < 1) {
        //handle combinator spacing
        if (this._options.space_around_combinator) {
          output.space_before_token = true;
          print_string(ch);
          output.space_before_token = true;
        } else {
          print_string(ch);
          this.eatWhitespace();
          // squash extra whitespace
          if (ch && whitespaceChar.test(ch)) {
            ch = '';
          }
        }
      } else if (ch === ']') {
        print_string(ch);
      } else if (ch === '[') {
        preserveSingleSpace(isAfterSpace);
        print_string(ch);
      } else if (ch === '=') { // no whitespace before or after
        this.eatWhitespace();
        print_string('=');
        if (whitespaceChar.test(ch)) {
          ch = '';
        }
      } else if (ch === '!') { // !important
        print_string(' ');
        print_string(ch);
      } else {
        preserveSingleSpace(isAfterSpace);
        print_string(ch);
      }
    }

    var sweetCode = output.get_code(this._options.end_with_newline, eol);

    return sweetCode;
  };

  // https://developer.mozilla.org/en-US/docs/Web/CSS/At-rule
  this.NESTED_AT_RULE = {
    "@page": true,
    "@font-face": true,
    "@keyframes": true,
    // also in CONDITIONAL_GROUP_RULE below
    "@media": true,
    "@supports": true,
    "@document": true
  };
  this.CONDITIONAL_GROUP_RULE = {
    "@media": true,
    "@supports": true,
    "@document": true
  };
}

module.exports.Beautifier = Beautifier;