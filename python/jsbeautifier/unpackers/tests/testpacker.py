# -*- coding: utf-8 -*-
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#

"""Tests for P.A.C.K.E.R. unpacker."""

import unittest
from jsbeautifier.unpackers.packer import detect, unpack

# pylint: disable=R0904


class TestPacker(unittest.TestCase):
    """P.A.C.K.E.R. testcase."""

    def test_detect(self):
        """Test detect() function."""

        def positive(source):
            return self.assertTrue(detect(source))

        def negative(source):
            return self.assertFalse(detect(source))

        negative("")
        negative("var a = b")
        positive("eval(function(p,a,c,k,e,r")
        positive("eval ( function(p, a, c, k, e, r")

    def test_unpack(self):
        """Test unpack() function."""

        def check(inp, out):
            return detect(inp) and self.assertEqual(unpack(inp), out)

        check(
            "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)"
            "){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e="
            "function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace("
            "new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',"
            "62,3,'var||a'.split('|'),0,{}))",
            "var a=1",
        )

        check(
            "function test (){alert ('This is a test!')}; "
            "eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String))"
            "{while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function"
            "(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp("
            "'\\b'+e(c)+'\\b','g'),k[c]);return p}('0 2=\\'{Íâ–+›ï;ã†Ù¥#\\'',3,3,"
            "'var||a'.split('|'),0,{}))",
            "function test (){alert ('This is a test!')}; var a='{Íâ–+›ï;ã†Ù¥#'",
        )

        check(
            "eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('2 0=\"4 3!\";2 1=0.5(/b/6);a.9(\"8\").7=1;',12,12,'str|n|var|W3Schools|Visit|search|i|innerHTML|demo|getElementById|document|w3Schools'.split('|'),0,{}))",
            'var str="Visit W3Schools!";var n=str.search(/w3Schools/i);document.getElementById("demo").innerHTML=n;',
        )

        check(
            "a=b;\r\nwhile(1){\ng=h;{return'\\w+'};break;eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('$(5).4(3(){$('.1').0(2);$('.6').0(d);$('.7').0(b);$('.a').0(8);$('.9').0(c)});',14,14,'html|r5e57|8080|function|ready|document|r1655|rc15b|8888|r39b0|r6ae9|3128|65309|80'.split('|'),0,{}))c=abx;",
            "a=b;\r\nwhile(1){\ng=h;{return'\\w+'};break;$(document).ready(function(){$('.r5e57').html(8080);$('.r1655').html(80);$('.rc15b').html(3128);$('.r6ae9').html(8888);$('.r39b0').html(65309)});c=abx;",
        )

        check(
            "eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};if('0'.replace(0,e)==0){while(c--)r[e(c)]=k[c];k=[function(e){return r[e]||e}];e=function(){return'[0-9ab]'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('$(5).a(6(){ $('.8').0(1); $('.b').0(4); $('.9').0(2); $('.7').0(3)})',[],12,'html|52136|555|65103|8088|document|function|r542c|r8ce6|rb0de|ready|rfab0'.split('|'),0,{}))",
            "$(document).ready(function(){ $('.r8ce6').html(52136); $('.rfab0').html(8088); $('.rb0de').html(555); $('.r542c').html(65103)})",
        )


if __name__ == "__main__":
    unittest.main()
