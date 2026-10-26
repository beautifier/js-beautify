/*jshint mocha:true */
'use strict';

var assert = require('assert');
var fs = require('fs');
var path = require('path');
var vm = require('vm');
var SanityTest = require('../sanitytest');

function loadUnpacker(relPath) {
  var filePath = path.join(__dirname, relPath);
  var code = fs.readFileSync(filePath, 'utf8');
  var sandbox = {
    console: console,
    Buffer: Buffer,
    SanityTest: SanityTest
  };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
  return sandbox;
}

var P_A_C_K_E_R = loadUnpacker('../../src/unpackers/p_a_c_k_e_r_unpacker.js').P_A_C_K_E_R;
var MyObfuscate = loadUnpacker('../../src/unpackers/myobfuscate_unpacker.js').MyObfuscate;

describe('unpackers (safe static deobfuscation)', function() {
  describe('P_A_C_K_E_R', function() {
    var pk1 = "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,3,'var||a'.split('|'),0,{}))";
    var unpk1 = 'var a=1';

    var pk2 = "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,3,'foo||b'.split('|'),0,{}))";
    var unpk2 = 'foo b=1';

    var unicodePacked = "function test (){alert ('This is a test!')}; " +
      "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String))" +
      "{while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function" +
      "(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp(" +
      "'\\b'+e(c)+'\\b','g'),k[c]);return p}('0 2=\\\'{Íâ–+›ï;ã†Ù¥#\\\'',3,3," +
      "'var||a'.split('|'),0,{}))";
    var unicodeExpected = "function test (){alert ('This is a test!')}; var a='{Íâ–+›ï;ã†Ù¥#'";

    it('detects packed scripts', function() {
      assert.strictEqual(P_A_C_K_E_R.detect(''), false);
      assert.strictEqual(P_A_C_K_E_R.detect('var a = b'), false);
      assert.strictEqual(P_A_C_K_E_R.detect(pk1), true);
      assert.strictEqual(P_A_C_K_E_R.detect('eval ( function(p, a, c, k, e, r'), false);
    });

    it('unpacks basic packer scripts without eval', function() {
      assert.strictEqual(P_A_C_K_E_R.unpack(pk1), unpk1);
      assert.strictEqual(P_A_C_K_E_R.unpack(pk2), unpk2);
    });

    it('unpacks scripts with unicode content', function() {
      assert.strictEqual(P_A_C_K_E_R.unpack(unicodePacked), unicodeExpected);
    });

    it('preserves code before and after packed chunks', function() {
      var filler = '\nfiller\n';
      var combined = filler + pk1 + '\n' + filler + pk2 + filler;
      var expected = filler + unpk1 + '\n' + filler + unpk2 + filler;
      assert.strictEqual(P_A_C_K_E_R.unpack(combined), expected);
    });

    it('unpacks complex base-62 files matching Python implementation', function() {
      var inputPath = path.join(__dirname, '../../../python/jsbeautifier/unpackers/tests/test-packer-62-input.js');
      var expectedPath = path.join(__dirname, '../../../python/jsbeautifier/unpackers/tests/test-packer-non62-input.js');
      var code62 = fs.readFileSync(inputPath, 'utf8');
      var exp62 = fs.readFileSync(expectedPath, 'utf8');

      assert.strictEqual(P_A_C_K_E_R.detect(code62), true);
      assert.strictEqual(P_A_C_K_E_R.unpack(code62), exp62);
    });

    it('unpacks double-quoted packer scripts with escaped quotes in payload', function() {
      var doubleQuoted = 'eval(function(p,a,c,k,e,r){return p}("0 2=\\\"1\\\"",3,3,"var||a".split("|"),0,{}))';
      assert.strictEqual(P_A_C_K_E_R.unpack(doubleQuoted), 'var a="1"');
    });

    it('unpacks scripts using base-12 and base-14 radices', function() {
      var base12 = "eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('2 0=\"4 3!\";2 1=0.5(/b/6);a.9(\"8\").7=1;',12,12,'str|n|var|W3Schools|Visit|search|i|innerHTML|demo|getElementById|document|w3Schools'.split('|'),0,{}))";
      var expected12 = 'var str="Visit W3Schools!";var n=str.search(/w3Schools/i);document.getElementById("demo").innerHTML=n;';
      assert.strictEqual(P_A_C_K_E_R.unpack(base12), expected12);

      var baseDefault62 = "eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};if('0'.replace(0,e)==0){while(c--)r[e(c)]=k[c];k=[function(e){return r[e]||e}];e=function(){return'[0-9ab]'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('$(5).a(6(){ $('.8').0(1); $('.b').0(4); $('.9').0(2); $('.7').0(3)})',[],12,'html|52136|555|65103|8088|document|function|r542c|r8ce6|rb0de|ready|rfab0'.split('|'),0,{}))";
      var expectedDefault62 = "$(document).ready(function(){ $('.r8ce6').html(52136); $('.rfab0').html(8088); $('.rb0de').html(555); $('.r542c').html(65103)})";
      assert.strictEqual(P_A_C_K_E_R.unpack(baseDefault62), expectedDefault62);
    });

    it('unpacks packer scripts with double-digit string lookup tables without index collisions', function() {
      var packed = 'var _0=["s0","s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11"];' +
        'alert(_0[1], _0[10], _0[11]);';
      assert.strictEqual(
        P_A_C_K_E_R._replacestrings(packed),
        'alert("s1", "s10", "s11");'
      );
    });

    it('safely handles malformed symtabs without throwing', function() {
      var malformed = "eval(function(p,a,c,k,e,r){if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,4,'var||a'.split('|'),0,{}))";
      assert.strictEqual(P_A_C_K_E_R.unpack(malformed), malformed);
    });

    it('runs internal SanityTest suite with 0 failures', function() {
      var t = P_A_C_K_E_R.run_tests(new SanityTest());
      assert.strictEqual(t.get_exitcode(), 0);
    });

    it('works in CSP environments where eval throws EvalError', function() {
      var source = fs.readFileSync(path.join(__dirname, '../../src/unpackers/p_a_c_k_e_r_unpacker.js'), 'utf8');
      var cspSandbox = {
        console: console,
        eval: function() {
          throw new EvalError("Refused to evaluate string due to CSP script-src 'self'");
        }
      };
      vm.createContext(cspSandbox);
      vm.runInContext(source, cspSandbox);
      var result = cspSandbox.P_A_C_K_E_R.unpack(pk1);
      assert.strictEqual(result, unpk1);
    });

    it('does not execute arbitrary side-effects in packed payload', function() {
      var executed = false;
      var source = fs.readFileSync(path.join(__dirname, '../../src/unpackers/p_a_c_k_e_r_unpacker.js'), 'utf8');
      var sandbox = {
        console: console,
        hook: function() {
          executed = true;
        }
      };
      vm.createContext(sandbox);
      vm.runInContext(source, sandbox);

      var malicious = "eval(function(p,a,c,k,e,r){hook();while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+c+'\\\\b','g'),k[c]);return p}('0',1,1,'safe'.split('|'),0,{}))";
      sandbox.P_A_C_K_E_R.unpack(malicious);
      assert.strictEqual(executed, false, 'Malicious payload hook should NEVER be executed');
    });
  });

  describe('MyObfuscate', function() {
    var inputPath = path.join(__dirname, '../../../python/jsbeautifier/unpackers/tests/test-myobfuscate-input.js');
    var outputPath = path.join(__dirname, '../../../python/jsbeautifier/unpackers/tests/test-myobfuscate-output.js');
    var input = fs.readFileSync(inputPath, 'utf8');
    var expectedOutput = fs.readFileSync(outputPath, 'utf8');

    it('detects myobfuscate scripts', function() {
      assert.strictEqual(MyObfuscate.detect(''), false);
      assert.strictEqual(MyObfuscate.detect('var a = 1;'), false);
      assert.strictEqual(MyObfuscate.detect(input), true);
    });

    it('unpacks myobfuscate scripts matching Python implementation', function() {
      var unpacked = MyObfuscate.unpack(input);
      assert.strictEqual(unpacked, expectedOutput);
    });

    it('unpacks myobfuscate payload when script tags are not present', function() {
      // payload containing base64 reverse of encoded "var _escape='alert(1)';"
      var payload = "alert(1)";
      var base64Reverse = Buffer.from("var _escape='" + payload + "';").toString('base64').split('').reverse().join('');
      var mockScript = "var _O0l = '" + base64Reverse + "'; eval(a(b(_O0l)));";
      var unpacked = MyObfuscate.unpack(mockScript);
      assert.strictEqual(unpacked.indexOf(payload) !== -1, true);
    });

    it('runs internal SanityTest suite with 0 failures', function() {
      var t = MyObfuscate.run_tests(new SanityTest());
      assert.strictEqual(t.get_exitcode(), 0);
    });

    it('works in CSP environments where eval throws EvalError', function() {
      var source = fs.readFileSync(path.join(__dirname, '../../src/unpackers/myobfuscate_unpacker.js'), 'utf8');
      var cspSandbox = {
        console: console,
        atob: function(str) {
          return Buffer.from(str, 'base64').toString('binary');
        },
        eval: function() {
          throw new EvalError("Refused to evaluate string due to CSP");
        }
      };
      vm.createContext(cspSandbox);
      vm.runInContext(source, cspSandbox);
      var result = cspSandbox.MyObfuscate.unpack(input);
      assert.strictEqual(result, expectedOutput);
    });
  });
});
