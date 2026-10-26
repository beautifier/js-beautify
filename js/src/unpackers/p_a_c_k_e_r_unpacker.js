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

//
// Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
//
// Coincidentally, it can defeat a couple of other eval-based compressors.
//
// usage:
//
// if (P_A_C_K_E_R.detect(some_string)) {
//     var unpacked = P_A_C_K_E_R.unpack(some_string);
// }
//
//

/*jshint strict:false */

var P_A_C_K_E_R = {
  detect: function(str) {
    return (P_A_C_K_E_R.get_chunks(str).length > 0);
  },

  get_chunks: function(str) {
    var chunks = str.match(/eval\s*\(\s*\(?\s*function\s*\(p\s*,\s*a\s*,\s*c\s*,\s*k\s*,\s*e[\s\S]*?\.split\(['"]\|['"]\)[\s\S]*?\)\s*\)?\s*\)/g);
    return chunks ? chunks : [];
  },

  unpack: function(str) {
    var chunks = P_A_C_K_E_R.get_chunks(str);
    for (var i = 0; i < chunks.length; i++) {
      var chunk = chunks[i];
      str = str.split(chunk).join(P_A_C_K_E_R.unpack_chunk(chunk));
    }
    return str;
  },

  _filterargs: function(source) {
    var juicers = [
      /}\s*\('([\s\S]*)',\s*(\d+|\[\]),\s*(\d+),\s*'([\s\S]*)'\.split\(['"]\|['"]\)(?:,\s*(\d+),\s*([\s\S]*)\)\))?/,
      /}\s*\("([\s\S]*)",\s*(\d+|\[\]),\s*(\d+),\s*"([\s\S]*)"\.split\(['"]\|['"]\)(?:,\s*(\d+),\s*([\s\S]*)\)\))?/
    ];
    for (var i = 0; i < juicers.length; i++) {
      var match = source.match(juicers[i]);
      if (match) {
        var radixStr = match[2];
        var radix = radixStr === '[]' ? 62 : parseInt(radixStr, 10);
        var count = parseInt(match[3], 10);
        return {
          payload: match[1],
          radix: radix,
          count: count,
          symtab: match[4].split('|')
        };
      }
    }
    return null;
  },

  _unbaser: function(base) {
    var ALPHABET_62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var ALPHABET_95 = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~';
    var dict = {};
    var alphabet;
    if (base >= 2 && base <= 62) {
      alphabet = ALPHABET_62.slice(0, base);
    } else if (base === 95) {
      alphabet = ALPHABET_95;
    } else {
      throw new Error('Unsupported base ' + base);
    }
    for (var i = 0; i < alphabet.length; i++) {
      dict[alphabet.charAt(i)] = i;
    }
    return function(str) {
      var ret = 0;
      var pow = 1;
      for (var k = str.length - 1; k >= 0; k--) {
        var cipher = str.charAt(k);
        if (!(cipher in dict)) {
          return NaN;
        }
        ret += dict[cipher] * pow;
        pow *= base;
      }
      return ret;
    };
  },

  _replacestrings: function(source) {
    var match = source.match(/var\s+(_\w+)\s*=\s*\["([\s\S]*?)"\];/);
    if (match) {
      var varname = match[1];
      var strings = match[2];
      var startpoint = match[0].length;
      var lookup = strings.split('","');
      var variable;
      for (var index = 0; index < lookup.length; index++) {
        variable = varname + '[' + index + ']';
        source = source.split(variable).join('"' + lookup[index] + '"');
      }
      return source.substr(startpoint);
    }
    return source;
  },

  unpack_chunk: function(str) {
    try {
      var args = P_A_C_K_E_R._filterargs(str);
      if (!args) {
        return str;
      }
      if (args.count !== args.symtab.length) {
        return str;
      }
      var unbase = P_A_C_K_E_R._unbaser(args.radix);
      var payload = args.payload.replace(/\\\\/g, '\\').replace(/\\'/g, "'").replace(/\\"/g, '"');
      var symtab = args.symtab;
      var source = payload.replace(/\b\w+\b/g, function(word) {
        var val = unbase(word);
        if (!isNaN(val) && val < symtab.length && symtab[val]) {
          return symtab[val];
        }
        return word;
      });
      return P_A_C_K_E_R._replacestrings(source);
    } catch (e) {
      return str;
    }
  },

  run_tests: function(sanity_test) {
    var t = sanity_test || new SanityTest();

    var pk1 = "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,3,'var||a'.split('|'),0,{}))";
    var unpk1 = 'var a=1';
    var pk2 = "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,3,'foo||b'.split('|'),0,{}))";
    var unpk2 = 'foo b=1';
    // For static unpacking, a count/symtab length mismatch represents corrupted/malformed packer data
    var pk_broken = "eval(function(p,a,c,k,e,r){BORKBORK;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',3,4,'var||a'.split('|'),0,{}))";
    var pk3 = "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1{}))',3,3,'var||a'.split('|'),0,{}))";
    var unpk3 = 'var a=1{}))';

    t.test_function(P_A_C_K_E_R.detect, "P_A_C_K_E_R.detect");
    t.expect('', false);
    t.expect('var a = b', false);
    t.test_function(P_A_C_K_E_R.unpack, "P_A_C_K_E_R.unpack");
    t.expect(pk_broken, pk_broken);
    t.expect(pk1, unpk1);
    t.expect(pk2, unpk2);
    t.expect(pk3, unpk3);
    t.expect("function test (){alert ('This is a test!')}; " +
      "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String))" +
      "{while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function" +
      "(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp(" +
      "'\\b'+e(c)+'\\b','g'),k[c]);return p}('0 2=\\\'{Íâ–+›ï;ã†Ù¥#\\\'',3,3," +
      "'var||a'.split('|'),0,{}))",
      "function test (){alert ('This is a test!')}; var a='{Íâ–+›ï;ã†Ù¥#'");


    var filler = '\nfiller\n';
    t.expect(filler + pk1 + "\n" + pk_broken + filler + pk2 + filler, filler + unpk1 + "\n" + pk_broken + filler + unpk2 + filler);

    return t;
  }
};
