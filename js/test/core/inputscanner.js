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
});