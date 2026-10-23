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
// simple unpacker/deobfuscator for scripts messed up with myobfuscate.com
// You really don't want to obfuscate your scripts there: they're tracking
// your unpackings, your script gets turned into something like this,
// as of 2011-04-25:
/*

    var _escape = 'your_script_escaped';
    var _111 = document.createElement('script');
    _111.src = 'http://api.www.myobfuscate.com/?getsrc=ok' +
        '&ref=' + encodeURIComponent(document.referrer) +
        '&url=' + encodeURIComponent(document.URL);
    var 000 = document.getElementsByTagName('head')[0];
    000.appendChild(_111);
    document.write(unescape(_escape));

*/
//
// written by Einar Lielmanis <einar@beautifier.io>
//
// usage:
//
// if (MyObfuscate.detect(some_string)) {
//     var unpacked = MyObfuscate.unpack(some_string);
// }
//
//

/*jshint strict:false */

var SIGNATURE = '["\\x41\\x42\\x43\\x44\\x45\\x46\\x47\\x48\\x49\\x4A\\x4B\\x4C\\x4D\\x4E\\x4F' +
  '\\x50\\x51\\x52\\x53\\x54\\x55\\x56\\x57\\x58\\x59\\x5A\\x61\\x62\\x63\\x64\\x65' +
  '\\x66\\x67\\x68\\x69\\x6A\\x6B\\x6C\\x6D\\x6E\\x6F\\x70\\x71\\x72\\x73\\x74\\x75' +
  '\\x76\\x77\\x78\\x79\\x7A\\x30\\x31\\x32\\x33\\x34\\x35\\x36\\x37\\x38\\x39\\x2B' +
  '\\x2F\\x3D","","\\x63\\x68\\x61\\x72\\x41\\x74","\\x69\\x6E\\x64\\x65\\x78' +
  '\\x4F\\x66","\\x66\\x72\\x6F\\x6D\\x43\\x68\\x61\\x72\\x43\\x6F\\x64\\x65","' +
  '\\x6C\\x65\\x6E\\x67\\x74\\x68"]';

var CAVEAT = '//\n// Unpacker warning: be careful when using myobfuscate.com for your projects:\n' +
  '// scripts obfuscated by the free online version call back home.\n//\n\n';

var MyObfuscate = {
  detect: function(str) {
    if (str.indexOf(SIGNATURE) !== -1) {
      return true;
    }
    if (/^var\s+_?[0O1lI]{3}\s*=\s*('|\[).*\)\)\);/.test(str)) {
      return true;
    }
    if (/^function\s+_?[0O1lI]{3}\(_/.test(str) && /eval\s*\(/.test(str)) {
      return true;
    }
    return false;
  },

  _base64Decode: function(str) {
    if (typeof Buffer !== 'undefined') {
      return Buffer.from(str, 'base64').toString('utf8');
    }
    if (typeof atob !== 'undefined') {
      try {
        return decodeURIComponent(escape(atob(str)));
      } catch (e) {
        return atob(str);
      }
    }
    return '';
  },

  unpack: function(str) {
    if (!MyObfuscate.detect(str)) {
      return str;
    }
    try {
      var varnameMatch = str.match(/eval\s*\(\s*\w+\s*\(\s*\w+\s*\(\s*(\w+)\s*\)\s*\)\s*\);/);
      if (!varnameMatch) {
        return str;
      }
      var varname = varnameMatch[1];
      var escapedVarname = varname.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      var regex = new RegExp('var\\s+' + escapedVarname + '\\s*=\\s*\'([^\']*)\';');
      var match = str.match(regex);
      if (!match) {
        return str;
      }
      var reverse = match[1].split('').reverse().join('');
      var decoded = MyObfuscate._base64Decode(reverse);
      var unquoted = unescape(decoded);
      var scriptMatch = unquoted.match(/^var _escape='<script>([\s\S]*?)<\/script>'/);
      var escapeMatch = unquoted.match(/^var _escape='([\s\S]*?)';?$/);
      var polished = scriptMatch ? scriptMatch[1] : (escapeMatch ? escapeMatch[1] : unquoted);
      return CAVEAT + polished;
    } catch (e) {
      return str;
    }
  },

  starts_with: function(str, what) {
    return str.substr(0, what.length) === what;
  },

  ends_with: function(str, what) {
    return str.substr(str.length - what.length, what.length) === what;
  },

  run_tests: function(sanity_test) {
    var t = sanity_test || new SanityTest();
    t.test_function(MyObfuscate.detect, "MyObfuscate.detect");
    t.expect('', false);
    t.expect('var a = 1;', false);
    t.test_function(MyObfuscate.unpack, "MyObfuscate.unpack");
    t.expect('', '');
    t.expect('var a = 1;', 'var a = 1;');
    return t;
  }
};
