/*jshint mocha:true */
'use strict';

var assert = require('assert');
var options = require('../../src/core/options');

describe('Options', function() {
  describe('mergeOpts', function() {
    it('should merge child option a with the parent options', function() {
      assert.deepEqual(options.mergeOpts({
        a: 1,
        b: { a: 2 }
      }, 'b'), {
        a: 2
      });
    });
    it('should include child option c and d with the parent options', function() {
      assert.deepEqual(options.mergeOpts({
        a: 1,
        b: { c: 2, d: 3 }
      }, 'b'), {
        a: 1,
        c: 2,
        d: 3
      });
    });
    it('should merge child option a and include c with the parent options', function() {
      assert.deepEqual(options.mergeOpts({
        a: 1,
        b: { a: 2, c: 3 }
      }, 'b'), {
        a: 2,
        c: 3
      });
    });
  });

  describe('normalizeOpts', function() {
    it('should replace key with - to _', function() {
      assert.deepEqual(options.normalizeOpts({
        'a-b': 1
      }), {
        a_b: 1
      });
    });
    it('should do nothing', function() {
      assert.deepEqual(options.mergeOpts({
        a: 1,
        b_c: 2
      }, 'b'), {
        a: 1,
        b_c: 2
      });
    });
  });

  describe('_get_boolean', function() {
    it('should return false with no option and no default', function() {
      assert.equal(new options.Options()._get_boolean(), false);
    });
    it('should return true as default since no option', function() {
      assert.equal(new options.Options()._get_boolean('a', true), true);
    });
    it('should return false as in option', function() {
      assert.equal(new options.Options({ a: false })._get_boolean('a', true), false);
    });
  });

  describe('_get_characters', function() {
    it('should return \'\' with no option', function() {
      assert.equal(new options.Options()._get_characters(), '');
    });
    it('should return \'character\' as default since no option', function() {
      assert.equal(new options.Options()._get_characters('a', 'character'), 'character');
    });
    it('should return \'char\' as in option', function() {
      assert.equal(new options.Options({ a: 'char' })._get_characters('a', 'character'), 'char');
    });
  });

  describe('_get_number', function() {
    it('should return 0 with no option', function() {
      assert.equal(new options.Options()._get_number(), 0);
    });
    it('should return 1 as default since no option', function() {
      assert.equal(new options.Options()._get_number('a', 1), 1);
    });
    it('should return 10 as in option', function() {
      assert.equal(new options.Options({ a: 10 })._get_number('a', 1), 10);
    });
    it('should return 0 for NaN as in option', function() {
      assert.equal(new options.Options({ a: 'abc' })._get_number('a'), 0);
    });
    it('should return 0 for NaN as in default', function() {
      assert.equal(new options.Options()._get_number('a', 'abc'), 0);
    });
  });

  describe('_get_array', function() {
    it('should return [] with no option', function() {
      assert.deepEqual(new options.Options()._get_array(), []);
    });
    it('should return [\'a\',\'b\'] as default since no option', function() {
      assert.deepEqual(new options.Options()._get_array('a', ['a', 'b']), ['a', 'b']);
    });
    it('should return [\'c\',\'d\'] as in option', function() {
      assert.deepEqual(new options.Options({ a: ['c', 'd'] })._get_array('a', ['a', 'b']), ['c', 'd']);
    });
    it('should return [\'c\',\'d\'] as in option comma separated', function() {
      assert.deepEqual(new options.Options({ a: 'c,d' })._get_array('a', ['a', 'b']), ['c', 'd']);
    });
  });

  describe('_is_valid_selection', function() {
    it('should return false with empty selection', function() {
      assert.equal(new options.Options()._is_valid_selection(['a', 'b'], []), false);
    });
    it('should return false with selection inexistent', function() {
      assert.equal(new options.Options()._is_valid_selection(['a', 'b'], ['c']), false);
    });
    it('should return true with selection existent', function() {
      assert.equal(new options.Options()._is_valid_selection(['a', 'b'], ['a', 'b']), true);
    });
  });

  describe('_get_selection_list', function() {
    it('should throw error with empty selection', function() {
      assert.throws(new options.Options()._get_selection_list, /^Error: Selection list cannot be empty.$/);
    });
    it('should throw error with invalid default', function() {
      assert.throws(function() { new options.Options()._get_selection_list('a', ['a', 'b'], ['c']); }, /^Error: Invalid Default Value!$/);
    });
    it('should throw error with invalid option', function() {
      assert.throws(function() { new options.Options({ a: ['c', 'd'] })._get_selection_list('a', ['a', 'b'], ['a']); }, /^Error: Invalid Option Value: The option/);
    });
    it('should return [\'a\'] as in option', function() {
      assert.deepEqual(new options.Options({ a: ['a'] })._get_selection_list('a', ['a', 'b'], ['a']), ['a']);
    });
  });

  describe('_get_selection', function() {
    it('should throw error with multiple selection', function() {
      assert.throws(function() { new options.Options({ a: ['a', 'b'] })._get_selection('a', ['a', 'b'], ['a']); }, /^Error: Invalid Option Value: The option/);
    });
    it('should return \'a\' as in option ', function() {
      assert.equal(new options.Options({ a: ['a'] })._get_selection('a', ['a', 'b'], ['a']), 'a');
    });
  });

});
