/*jshint mocha:true */
'use strict';

var assert = require('assert');
var InputScanner = require('../../src/core/inputscanner').InputScanner;

describe('IndexScanner', function() {
  describe('new', function() {
    it('should return empty scanner when input is not present', function() {
      assert.strictEqual(new InputScanner().hasNext(), false);
    });
  });

  describe('next', function() {
    it('should return the value at current index and increments the index', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.next(), value[0]);
      assert.strictEqual(inputText.next(), value[1]);
    });

    it('should return null if index is at then end of the value', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      inputText.readUntilAfter(/howdy/);
      assert.strictEqual(inputText.next(), null);
    });
  });

  describe('peek', function() {
    it('should return value at index passed as parameter', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.peek(3), value[3]);
      inputText.next();
      assert.strictEqual(inputText.peek(3), value[4]);
    });

    it('should return null if index is less than 0 or greater than text length', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.peek(-2), null);
      assert.strictEqual(inputText.peek(5), null);
    });
  });

  describe('peek without parameters', function() {
    it('should return value at index 0 if parameter is not present', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.peek(), value[0]);
      inputText.next();
      assert.strictEqual(inputText.peek(3), value[4]);
    });
  });

  describe('test', function() {
    it('should return whether the pattern is matched or not', function() {
      var value = 'howdy';
      var pattern = /how/;
      var index = 0;
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.test(pattern, index), true);
      inputText.next();
      assert.strictEqual(inputText.test(pattern, index), false);
    });
  });

  describe('testChar', function() {
    it('should return whether pattern matched or not for particular index', function() {
      var value = 'howdy';
      var pattern = /o/;
      var index = 1;
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.testChar(pattern, index), true);
    });
  });

  describe('restart', function() {
    it('should reset index to 0', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      inputText.next();
      assert.strictEqual(inputText.peek(), value[1]);
      inputText.restart();
      assert.strictEqual(inputText.peek(), value[0]);
    });
  });

  describe('back', function() {
    it('should move the index one place back if current position is not 0', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      inputText.next();
      assert.strictEqual(inputText.peek(), value[1]);
      inputText.back();
      assert.strictEqual(inputText.peek(), value[0]);
    });

    it('should not move the index back if current position is 0', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      assert.strictEqual(inputText.peek(), value[0]);
      inputText.back();
      assert.strictEqual(inputText.peek(), value[0]);
    });
  });

  describe('hasNext', function() {
    it('should return true if index is not at the last position', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      inputText.readUntilAfter(/howd/);
      assert.strictEqual(inputText.hasNext(), true);
    });

    it('should return false if index is at the last position', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      inputText.readUntilAfter(/howdy/);
      assert.strictEqual(inputText.hasNext(), false);
    });
  });

  describe('match', function() {
    it('should return details of pattern match and move index to next position', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      var patternmatch = inputText.match(/how/);
      assert.strictEqual(inputText.peek(), value[3]);
      assert.notStrictEqual(patternmatch, null);
      assert.strictEqual(patternmatch[0], 'how');
    });

    it('should return null and not move index if there is no match', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      var patternmatch = inputText.match(/test/);
      assert.strictEqual(inputText.peek(), value[0]);
      assert.strictEqual(patternmatch, null);
    });
  });

  describe('read', function() {
    it('should return the matched substring', function() {
      var inputText = new InputScanner("howdy");
      var patternmatch = inputText.read(/how/);
      assert.strictEqual(patternmatch, "how");
    });

    it('should return the empty string if there is no match', function() {
      var inputText = new InputScanner("howdy");
      var patternmatch = inputText.read(/ow/);
      assert.strictEqual(patternmatch, "");
    });

    it('should return substring from start to until pattern when unitilAfter is true', function() {
      var inputText = new InputScanner("howdy");
      var startPattern = /how/;
      var untilPattern = /dy/;
      var untilAfter = true;
      var patternmatch = inputText.read(startPattern, untilPattern, untilAfter);
      assert.strictEqual(patternmatch, "howdy");
    });

    it('should return the substring matched for startPattern when untilPattern is given but unitilAfter is false', function() {
      var inputText = new InputScanner("howdy");
      var startPattern = /how/;
      var untilPattern = /dy/;
      var untilAfter = false;
      var patternmatch = inputText.read(startPattern, untilPattern, untilAfter);
      assert.strictEqual(patternmatch, "how");
    });

    it('should return substring matched for untilPattern when startPattern is null', function() {
      var inputText = new InputScanner("howdy");
      var startPattern = null;
      var untilPattern = /how/;
      var untilAfter = true;
      var patternmatch = inputText.read(startPattern, untilPattern, untilAfter);
      assert.strictEqual(patternmatch, "how");
    });

    it('should return substring matched for untilPattern when startPattern is null and untilAfter is false', function() {
      var inputText = new InputScanner("howdy");
      var startPattern = null;
      var untilPattern = /how/;
      var untilAfter = false;
      var patternmatch = inputText.read(startPattern, untilPattern, untilAfter);
      assert.strictEqual(patternmatch, "");
    });
  });

  describe('readUntil', function() {
    it('should return substring matched for pattern when untilAfter is true', function() {
      var inputText = new InputScanner("howdy");
      var pattern = /how/;
      var untilAfter = true;
      var patternmatch = inputText.readUntil(pattern, untilAfter);
      assert.strictEqual(patternmatch, "how");
    });

    it('should return substring from index 0 to start index of matched substring when untilAfter is false', function() {
      var inputText = new InputScanner("howdy");
      var pattern = /wd/;
      var untilAfter = false;
      var patternmatch = inputText.readUntil(pattern, untilAfter);
      assert.strictEqual(patternmatch, "ho");
    });

    it('should return empty string when start index of matched substring is 0 and untilAfter is false', function() {
      var inputText = new InputScanner("howdy");
      var pattern = /how/;
      var untilAfter = false;
      var patternmatch = inputText.readUntil(pattern, untilAfter);
      assert.strictEqual(patternmatch, "");
    });
  });

  describe('readUntilAfter', function() {
    it('should return matched substring', function() {
      var inputText = new InputScanner("howdy");
      var pattern = /how/;
      var patternmatch = inputText.readUntilAfter(pattern);
      assert.strictEqual(patternmatch, "how");
    });
  });

  describe('get_regexp', function() {
    it('should return regex for string passed', function() {
      var inputText = new InputScanner("howdy");
      var pattern = "ow";
      assert.deepStrictEqual(inputText.get_regexp(pattern), /ow/g);
    });

    it('should return regex pattern with sticky flag when match_from is true', function() {
      var inputText = new InputScanner("howdy");
      var matchFrom = true;
      var pattern = "ow";
      assert.deepStrictEqual(inputText.get_regexp(pattern, matchFrom).toString(), '/ow/y');
    });

    it('should return pattern with flags appeded when the input is not a string', function() {
      var inputText = new InputScanner("howdy");
      var matchFrom = true;
      var pattern = /ow/;
      assert.deepStrictEqual(inputText.get_regexp(pattern, matchFrom).toString(), '/ow/y');
      assert.deepStrictEqual(inputText.get_regexp(pattern), /ow/g);
    });
  });

  describe('get_literal_regexp', function() {
    it('should return pattern for literal string', function() {
      var inputText = new InputScanner("howdy");
      var pattern = "ow$/h";
      assert.deepStrictEqual(inputText.get_literal_regexp(pattern), /ow\$\/h/);
    });
  });

  describe('peekUntilAfter', function() {
    it('should return matched substring and retain index position', function() {
      var value = "howdy";
      var inputText = new InputScanner(value);
      var pattern = /how/;
      assert.strictEqual(inputText.peek(), value[0]);
      assert.strictEqual(inputText.peekUntilAfter(pattern), "how");
      assert.strictEqual(inputText.peek(), value[0]);
    });
  });

  describe('lookBack', function() {
    it('should return whether testVal is obtained by shifting index to the left', function() {
      var inputText = new InputScanner("howdy");
      var testVal = "how";
      inputText.readUntilAfter(/howd/);
      assert.strictEqual(inputText.lookBack(testVal), true);
      testVal = "ho";
      assert.strictEqual(inputText.lookBack(testVal), false);
    });
  });
});
