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
var TokenFactory = require('../core/token').TokenFactory;
var BaseTokenizer = require('../core/tokenizer').Tokenizer;
var BASETOKEN = require('../core/tokenizer').TOKEN;
var acorn = require('../core/acorn');
var Directives = require('../core/directives').Directives;

function in_array(what, arr) {
  return arr.indexOf(what) !== -1;
}


var TOKEN = {
  START_EXPR: 'TK_START_EXPR',
  END_EXPR: 'TK_END_EXPR',
  START_BLOCK: 'TK_START_BLOCK',
  END_BLOCK: 'TK_END_BLOCK',
  WORD: 'TK_WORD',
  RESERVED: 'TK_RESERVED',
  SEMICOLON: 'TK_SEMICOLON',
  STRING: 'TK_STRING',
  EQUALS: 'TK_EQUALS',
  OPERATOR: 'TK_OPERATOR',
  COMMA: 'TK_COMMA',
  BLOCK_COMMENT: 'TK_BLOCK_COMMENT',
  COMMENT: 'TK_COMMENT',
  DOT: 'TK_DOT',
  UNKNOWN: 'TK_UNKNOWN',
  EOF: BASETOKEN.EOF
};

function Tokenizer(input_string, opts) {
  BaseTokenizer.call(this, input_string, opts);

  var directives_core = new Directives(/\/\*/, /\*\//);

  var number_pattern = /0[xX][0123456789abcdefABCDEF]*|0[oO][01234567]*|0[bB][01]*|\d+n|(?:\.\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?/g;

  var digit = /[0-9]/;

  this.positionable_operators = '!= !== % & && * ** + - / : < << <= == === > >= >> >>> ? ^ | ||'.split(' ');
  var punct = this.positionable_operators.concat(
    // non-positionable operators - these do not follow operator position settings
    '! %= &= *= **= ++ += , -- -= /= :: <<= = => >>= >>>= ^= |= ~ ...'.split(' '));

  // words which should always start on new line.
  this.line_starters = 'continue,try,throw,return,var,let,const,if,switch,case,default,for,while,break,function,import,export'.split(',');
  var reserved_words = this.line_starters.concat(['do', 'in', 'of', 'else', 'get', 'set', 'new', 'catch', 'finally', 'typeof', 'yield', 'async', 'await', 'from', 'as']);

  //  /* ... */ comment ends with nearest */ or end of file
  var block_comment_pattern = /\/\*(?:[\s\S]*?)((?:\*\/)|$)/g;

  // comment ends just before nearest linefeed or end of file
  var comment_pattern = /\/\/(?:[^\n\r\u2028\u2029]*)/g;

  var template_pattern = /(?:(?:<\?php|<\?=)[\s\S]*?\?>)|(?:<%[\s\S]*?%>)/g;

  var in_html_comment, tokens, input;

  this.is_comment = function(current_token) {
    return current_token.type === TOKEN.COMMENT || current_token.type === TOKEN.BLOCK_COMMENT || current_token.type === TOKEN.UNKNOWN;
  };

  this.is_opening = function(current_token) {
    return current_token.type === TOKEN.START_BLOCK || current_token.type === TOKEN.START_EXPR;
  };

  this.is_closing = function(current_token, open_token) {
    return (current_token.type === TOKEN.END_BLOCK || current_token.type === TOKEN.END_EXPR) &&
      (open_token && (
        (current_token.text === ']' && open_token.text === '[') ||
        (current_token.text === ')' && open_token.text === '(') ||
        (current_token.text === '}' && open_token.text === '{')));
  };

  this.reset = function() {
    in_html_comment = false;
    input = this._input;
    tokens = this._tokens;
  };

  this.token_factory = new TokenFactory();

  this.get_next_token = function() {
    var resulting_string;

    var last_token;
    if (tokens.length) {
      last_token = tokens[tokens.length - 1];
    } else {
      // For the sake of tokenizing we can pretend that there was on open brace to start
      last_token = new Token(TOKEN.START_BLOCK, '{');
    }

    this.token_factory.readWhitespace(input);

    resulting_string = input.readWhile(acorn.identifier);
    if (resulting_string !== '') {
      if (!(last_token.type === TOKEN.DOT ||
          (last_token.type === TOKEN.RESERVED && in_array(last_token.text, ['set', 'get']))) &&
        in_array(resulting_string, reserved_words)) {
        if (resulting_string === 'in' || resulting_string === 'of') { // hack for 'in' and 'of' operators
          return this.token_factory.create(TOKEN.OPERATOR, resulting_string);
        }
        return this.token_factory.create(TOKEN.RESERVED, resulting_string);
      }

      return this.token_factory.create(TOKEN.WORD, resulting_string);
    }

    resulting_string = input.readWhile(number_pattern);
    if (resulting_string !== '') {
      return this.token_factory.create(TOKEN.WORD, resulting_string);
    }

    var c = input.next();

    if (c === null) {
      return this.token_factory.create(TOKEN.EOF, '');
    }


    if (c === '(' || c === '[') {
      return this.token_factory.create(TOKEN.START_EXPR, c);
    }

    if (c === ')' || c === ']') {
      return this.token_factory.create(TOKEN.END_EXPR, c);
    }

    if (c === '{') {
      return this.token_factory.create(TOKEN.START_BLOCK, c);
    }

    if (c === '}') {
      return this.token_factory.create(TOKEN.END_BLOCK, c);
    }

    if (c === ';') {
      return this.token_factory.create(TOKEN.SEMICOLON, c);
    }

    if (c === '/') {
      var token;
      var comment = '';
      // peek for comment /* ... */
      if (input.peek() === '*') {
        input.back();
        comment = input.readWhile(block_comment_pattern);
        var directives = directives_core.get_directives(comment);
        if (directives && directives.ignore === 'start') {
          comment += directives_core.readIgnored(input);
        }
        comment = comment.replace(acorn.allLineBreaks, '\n');
        token = this.token_factory.create(TOKEN.BLOCK_COMMENT, comment);
        token.directives = directives;
        return token;
      }
      // peek for comment // ...
      if (input.peek() === '/') {
        input.back();
        comment = input.readWhile(comment_pattern);
        return this.token_factory.create(TOKEN.COMMENT, comment);
      }

    }

    var startXmlRegExp = /<()([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*('[^']*'|"[^"]*"|{[\s\S]+?}))*\s*(\/?)\s*>/g;

    var xmlRegExp = /[\s\S]*?<(\/?)([-a-zA-Z:0-9_.]+|{[\s\S]+?}|!\[CDATA\[[\s\S]*?\]\])(\s+{[\s\S]+?}|\s+[-a-zA-Z:0-9_.]+|\s+[-a-zA-Z:0-9_.]+\s*=\s*('[^']*'|"[^"]*"|{[\s\S]+?}))*\s*(\/?)\s*>/g;

    function allowRegExOrXML() {
      // regex and xml can only appear in specific locations during parsing
      return (last_token.type === TOKEN.RESERVED && in_array(last_token.text, ['return', 'case', 'throw', 'else', 'do', 'typeof', 'yield'])) ||
        (last_token.type === TOKEN.END_EXPR && last_token.text === ')' &&
          last_token.parent && last_token.parent.type === TOKEN.RESERVED && in_array(last_token.parent.text, ['if', 'while', 'for'])) ||
        (in_array(last_token.type, [TOKEN.COMMENT, TOKEN.START_EXPR, TOKEN.START_BLOCK,
          TOKEN.END_BLOCK, TOKEN.OPERATOR, TOKEN.EQUALS, TOKEN.EOF, TOKEN.SEMICOLON, TOKEN.COMMA
        ]));
    }

    var isString = (c === '`' || c === "'" || c === '"');
    var isRegExp = (c === '/') && allowRegExOrXML();
    var isXML = (opts.e4x && c === "<" && input.test(startXmlRegExp, -1)) && allowRegExOrXML();
    var sep = c,
      esc = false,
      has_char_escapes = false;

    resulting_string = c;


    if (isString) {
      // handle string
      //
      var parse_string = function(delimiter, allow_unescaped_newlines, start_sub) {
        // Template strings can travers lines without escape characters.
        // Other strings cannot
        var current_char;
        while (input.hasNext()) {
          current_char = input.peek();
          if (!(esc || (current_char !== delimiter &&
              (allow_unescaped_newlines || !acorn.newline.test(current_char))))) {
            break;
          }

          // Handle \r\n linebreaks after escapes or in template strings
          if ((esc || allow_unescaped_newlines) && acorn.newline.test(current_char)) {
            if (current_char === '\r' && input.peek(1) === '\n') {
              input.next();
              current_char = input.peek();
            }
            resulting_string += '\n';
          } else {
            resulting_string += current_char;
          }

          if (esc) {
            if (current_char === 'x' || current_char === 'u') {
              has_char_escapes = true;
            }
            esc = false;
          } else {
            esc = current_char === '\\';
          }

          input.next();

          if (start_sub && resulting_string.indexOf(start_sub, resulting_string.length - start_sub.length) !== -1) {
            if (delimiter === '`') {
              parse_string('}', allow_unescaped_newlines, '`');
            } else {
              parse_string('`', allow_unescaped_newlines, '${');
            }

            if (input.hasNext()) {
              resulting_string += input.next();
            }
          }
        }
      };

      if (sep === '`') {
        parse_string('`', true, '${');
      } else {
        parse_string(sep);
      }

    } else if (isRegExp) {
      // handle regexp
      //
      var in_char_class = false;
      while (input.hasNext() &&
        ((esc || in_char_class || input.peek() !== sep) &&
          !input.testChar(acorn.newline))) {
        resulting_string += input.peek();
        if (!esc) {
          esc = input.peek() === '\\';
          if (input.peek() === '[') {
            in_char_class = true;
          } else if (input.peek() === ']') {
            in_char_class = false;
          }
        } else {
          esc = false;
        }
        input.next();
      }

    } else if (isXML) {
      // handle e4x xml literals
      //
      input.back();
      var xmlStr = '';
      var match = input.match(startXmlRegExp);
      if (match) {
        // Trim root tag to attempt to
        var rootTag = match[2].replace(/^{\s+/, '{').replace(/\s+}$/, '}');
        var isCurlyRoot = rootTag.indexOf('{') === 0;
        var depth = 0;
        while (match) {
          var isEndTag = !!match[1];
          var tagName = match[2];
          var isSingletonTag = (!!match[match.length - 1]) || (tagName.slice(0, 8) === "![CDATA[");
          if (!isSingletonTag &&
            (tagName === rootTag || (isCurlyRoot && tagName.replace(/^{\s+/, '{').replace(/\s+}$/, '}')))) {
            if (isEndTag) {
              --depth;
            } else {
              ++depth;
            }
          }
          xmlStr += match[0];
          if (depth <= 0) {
            break;
          }
          match = input.match(xmlRegExp);
        }
        // if we didn't close correctly, keep unformatted.
        if (!match) {
          xmlStr += input.match(/[\s\S]*/g)[0];
        }
        xmlStr = xmlStr.replace(acorn.allLineBreaks, '\n');
        return this.token_factory.create(TOKEN.STRING, xmlStr);
      }
    }

    if (isRegExp || isString) {
      if (has_char_escapes && opts.unescape_strings) {
        resulting_string = unescape_string(resulting_string);
      }
      if (input.peek() === sep) {
        resulting_string += sep;
        input.next();

        if (sep === '/') {
          // regexps may have modifiers /regexp/MOD , so fetch those, too
          // Only [gim] are valid, but if the user puts in garbage, do what we can to take it.
          resulting_string += input.readWhile(acorn.identifier);
        }
      }
      return this.token_factory.create(TOKEN.STRING, resulting_string);
    }

    if (c === '#') {

      if (tokens.length === 0 && input.peek() === '!') {
        // shebang
        resulting_string = c;
        while (input.hasNext() && c !== '\n') {
          c = input.next();
          resulting_string += c;
        }
        return this.token_factory.create(TOKEN.UNKNOWN, resulting_string.trim() + '\n');
      }

      // Spidermonkey-specific sharp variables for circular references. Considered obsolete.
      var sharp = '#';
      if (input.hasNext() && input.testChar(digit)) {
        do {
          c = input.next();
          sharp += c;
        } while (input.hasNext() && c !== '#' && c !== '=');
        if (c === '#') {
          //
        } else if (input.peek() === '[' && input.peek(1) === ']') {
          sharp += '[]';
          input.next();
          input.next();
        } else if (input.peek() === '{' && input.peek(1) === '}') {
          sharp += '{}';
          input.next();
          input.next();
        }
        return this.token_factory.create(TOKEN.WORD, sharp);
      }
    }

    if (c === '<' && (input.peek() === '?' || input.peek() === '%')) {
      input.back();
      var template_match = input.match(template_pattern);
      if (template_match) {
        c = template_match[0];
        c = c.replace(acorn.allLineBreaks, '\n');
        return this.token_factory.create(TOKEN.STRING, c);
      }
    }

    if (c === '<' && input.match(/\!--/g)) {
      c = '<!--';
      while (input.hasNext() && !input.testChar(acorn.newline)) {
        c += input.next();
      }
      in_html_comment = true;
      return this.token_factory.create(TOKEN.COMMENT, c);
    }

    if (c === '-' && in_html_comment && input.match(/->/g)) {
      in_html_comment = false;
      return this.token_factory.create(TOKEN.COMMENT, '-->');
    }

    if (c === '.') {
      if (input.peek() === '.' && input.peek(1) === '.') {
        c += input.next() + input.next();
        return this.token_factory.create(TOKEN.OPERATOR, c);
      }
      return this.token_factory.create(TOKEN.DOT, c);
    }

    if (in_array(c, punct)) {
      while (input.hasNext() && in_array(c + input.peek(), punct)) {
        c += input.next();
        if (!input.hasNext()) {
          break;
        }
      }

      if (c === ',') {
        return this.token_factory.create(TOKEN.COMMA, c);
      } else if (c === '=') {
        return this.token_factory.create(TOKEN.EQUALS, c);
      } else {
        return this.token_factory.create(TOKEN.OPERATOR, c);
      }
    }

    return this.token_factory.create(TOKEN.UNKNOWN, c);
  };


  function unescape_string(s) {
    // You think that a regex would work for this
    // return s.replace(/\\x([0-9a-f]{2})/gi, function(match, val) {
    //         return String.fromCharCode(parseInt(val, 16));
    //     })
    // However, dealing with '\xff', '\\xff', '\\\xff' makes this more fun.
    var out = '',
      escaped = 0;

    var input_scan = new InputScanner(s);
    var matched = null;

    while (input_scan.hasNext()) {
      // Keep any whitespace, non-slash characters
      // also keep slash pairs.
      matched = input_scan.match(/([\s]|[^\\]|\\\\)+/g);

      if (matched) {
        out += matched[0];
      }

      if (input_scan.peek() === '\\') {
        input_scan.next();
        if (input_scan.peek() === 'x') {
          matched = input_scan.match(/x([0-9A-Fa-f]{2})/g);
        } else if (input_scan.peek() === 'u') {
          matched = input_scan.match(/u([0-9A-Fa-f]{4})/g);
        } else {
          out += '\\';
          if (input_scan.hasNext()) {
            out += input_scan.next();
          }
          continue;
        }

        // If there's some error decoding, return the original string
        if (!matched) {
          return s;
        }

        escaped = parseInt(matched[1], 16);

        if (escaped > 0x7e && escaped <= 0xff && matched[0].indexOf('x') === 0) {
          // we bail out on \x7f..\xff,
          // leaving whole string escaped,
          // as it's probably completely binary
          return s;
        } else if (escaped >= 0x00 && escaped < 0x20) {
          // leave 0x00...0x1f escaped
          out += '\\' + matched[0];
          continue;
        } else if (escaped === 0x22 || escaped === 0x27 || escaped === 0x5c) {
          // single-quote, apostrophe, backslash - escape these
          out += '\\' + String.fromCharCode(escaped);
        } else {
          out += String.fromCharCode(escaped);
        }
      }
    }

    return out;
  }
}

module.exports.Tokenizer = Tokenizer;
module.exports.TOKEN = TOKEN;