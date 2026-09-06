/*jshint mocha:true */
'use strict';

var assert = require('assert');
var fs = require('fs');
var path = require('path');
var vm = require('vm');

// Only urlencode_unpacker.js exports via module.exports; P_A_C_K_E_R and
// JavascriptObfuscator are browser-only globals (plain `var X = {...}`
// declarations meant to be loaded via <script> tags), so they're run as
// source into the sandbox below instead of required.
var Urlencoded = require('../../src/unpackers/urlencode_unpacker');

function runFileInContext(sandbox, filePath) {
  var source = fs.readFileSync(filePath, 'utf8');
  vm.runInContext(source, sandbox, { filename: path.basename(filePath) });
}

// web/common-function.js is a browser script (no module.exports) that relies
// on globals like window/requirejs/jQuery/the unpacker libs loaded via <script>
// tags. Load it into a sandboxed vm context with just the globals its
// pure/logic functions need, then pull those functions off the sandbox.
function loadCommonFunctions() {
  var sandbox = {
    window: { location: { href: '' } },
    requirejs: function() {},
    Urlencoded: Urlencoded
  };
  sandbox.requirejs.config = function() {};

  vm.createContext(sandbox);
  runFileInContext(sandbox, path.join(__dirname, '../../src/unpackers/p_a_c_k_e_r_unpacker.js'));
  runFileInContext(sandbox, path.join(__dirname, '../../src/unpackers/javascriptobfuscator_unpacker.js'));
  runFileInContext(sandbox, path.join(__dirname, '../../../web/common-function.js'));
  return sandbox;
}

describe('web/common-function.js', function() {
  var common = loadCommonFunctions();

  describe('any', function() {
    it('returns the first argument when truthy', function() {
      assert.equal(common.any(1, 2), 1);
    });
    it('falls back to the second argument when the first is falsy', function() {
      assert.equal(common.any(0, 2), 2);
      assert.equal(common.any(null, 'x'), 'x');
    });
  });

  describe('mergeObjects', function() {
    it('overrides base options with additional options', function() {
      assert.deepEqual(
        common.mergeObjects({ a: 1, b: 2 }, { b: 3, c: 4 }), { a: 1, b: 3, c: 4 });
    });
    it('returns a copy of the base options when no additional options are given', function() {
      assert.deepEqual(common.mergeObjects({ a: 1 }, {}), { a: 1 });
    });
  });

  describe('unpacker_filter', function() {
    it('passes through source with no leading comments', function() {
      assert.equal(common.unpacker_filter('var a = 1;'), '\nvar a = 1;');
    });

    it('preserves a single leading block comment', function() {
      assert.equal(
        common.unpacker_filter('/* comment */var a = 1;'),
        '/* comment */\nvar a = 1;');
    });

    it('preserves a single leading line comment', function() {
      assert.equal(
        common.unpacker_filter('// comment\nvar a = 1;'),
        '// comment\nvar a = 1;');
    });

    // Regression test for #1546: a second leading comment used to lose its
    // formatting because whitespace was stripped after every comment instead
    // of once after all leading comments were collected.
    it('preserves multiple leading block comments in order', function() {
      var input = '/* first */\n/* second */\nvar a = 1;';
      assert.equal(common.unpacker_filter(input), input);
    });

    it('preserves a mix of leading line and block comments', function() {
      var input = '// line one\n/* block two */\nvar a = 1;';
      assert.equal(common.unpacker_filter(input), input);
    });

    it('unpacks urlencoded source after stripping leading comments', function() {
      assert.equal(
        common.unpacker_filter('/* encoded */javascript:var%20a=1'),
        '/* encoded */\n\njavascript:var a=1');
    });
  });

  describe('JavascriptObfuscator.unpack', function() {
    // Regression test for #1610: replacement strings containing `$` were
    // interpreted as special `$`-patterns by String.replace(), corrupting the
    // output (e.g. `$'` was replaced with the rest of the input).
    it('replaces string array references literally when values contain $', function() {
      var input = [
        'var _0xbe98 = ["\\x63\\x75\\x72\\x72\\x65\\x6e\\x63\\x79\\x53\\x79\\x6d\\x62\\x6f\\x6c", "\\x24"];',
        'var a = {};',
        "a['\\x61'] = '\\x31';",
        "a['\\x62'] = 0x2;",
        'a[_0xbe98[0]] = _0xbe98[1];',
        "a['\\x63'] = 0x3;"
      ].join('\n');
      var expected = [
        'var a = {};',
        "a['\\x61'] = '\\x31';",
        "a['\\x62'] = 0x2;",
        "a['currencySymbol'] = '$';",
        "a['\\x63'] = 0x3;"
      ].join('\n');
      assert.equal(common.JavascriptObfuscator.unpack(input), '\n' + expected);
    });

    it('does not interpret $ patterns ($&, $1, etc.) in replacement values', function() {
      var input = 'var _0xabc=["\\x24\\x26"];\nx[_0xabc[0]]=1;';
      assert.equal(common.JavascriptObfuscator.unpack(input), "\nx['$&']=1;");
    });

    it('passes through non-packed code unchanged', function() {
      assert.equal(common.JavascriptObfuscator.unpack('var a=1;'), 'var a=1;');
    });
  });
});
