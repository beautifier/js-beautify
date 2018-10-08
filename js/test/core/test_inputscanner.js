/*jshint mocha:true */
'use strict';

var assert = require('assert');
var InputScanner = require('../../src/core/inputscanner').InputScanner;

describe('IndexScanner', function() {
  describe('new', function() {
    it('should return empty scanner when input is not present', function() {
      assert.equal(new InputScanner().hasNext(), false);
    });
  });

  describe('next', function() {
    it('should return the value at current index and increments the index', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.equal(inputText.next(), value[0]);
      assert.equal(inputText.next(), value[1]);
    });
  });

  describe('peek', function() {
    it('should return value at index passed as parameter', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.equal(inputText.peek(3), value[3]);
      inputText.next();
      assert.equal(inputText.peek(3), value[4]);
    });
  });

  describe('peek without parameters', function() {
    it('should return value at index 0 if parameter is not present', function() {
      var value = 'howdy';
      var inputText = new InputScanner(value);
      assert.equal(inputText.peek(), value[0]);
      inputText.next();
      assert.equal(inputText.peek(3), value[4]);
    });
  });

  describe('test', function() {
    it('should return whether the pattern is matched or not', function() {
      var value = 'howdy';
      var pattern = /how/;
      var index = 0;
      var inputText = new InputScanner(value);
      assert.equal(inputText.test(pattern, index), true);
      inputText.next();
      assert.equal(inputText.test(pattern, index), false);
    });
  });

  describe('testChar', function() {
    it('should return whether pattern matched or not for particular index', function() {
      var value = 'howdy';
      var pattern = /o/;
      var index = 1;
      var inputText = new InputScanner(value);
      assert.equal(inputText.testChar(pattern, index), true);
    });
  });


});
