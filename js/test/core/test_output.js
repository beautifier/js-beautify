/*jshint mocha:true */
'use strict';

var assert = require('assert');
var Output = require('../../src/core/output').Output;

function makeOutput(overrides) {
  var options = {
    indent_size: 4,
    indent_char: ' ',
    indent_with_tabs: false,
    indent_level: 0,
    end_with_newline: false,
    wrap_line_length: 0,
    indent_empty_lines: false
  };

  Object.keys(overrides || {}).forEach(function(key) {
    options[key] = overrides[key];
  });

  return new Output(options);
}

describe('Output', function() {
  describe('ensure_empty_line_above', function() {
    it('should insert a blank line before the current line when the previous line does not match', function() {
      var output = makeOutput();

      output.add_token('alpha');
      output.add_new_line();
      output.add_token('beta');
      output.add_new_line();
      output.add_token('gamma');

      output.ensure_empty_line_above('skip', 'end');

      assert.strictEqual(output.get_code('\n'), 'alpha\nbeta\n\ngamma');
    });

    it('should not insert a blank line when the previous line starts with the requested prefix', function() {
      var output = makeOutput();

      output.add_token('skip-this');
      output.add_new_line();
      output.add_token('gamma');

      output.ensure_empty_line_above('skip', 'end');

      assert.strictEqual(output.get_code('\n'), 'skip-this\ngamma');
    });

    it('should not insert a blank line when the previous line ends with the requested suffix', function() {
      var output = makeOutput();

      output.add_token('end');
      output.add_new_line();
      output.add_token('gamma');

      output.ensure_empty_line_above('skip', 'end');

      assert.strictEqual(output.get_code('\n'), 'end\ngamma');
    });
  });
});
