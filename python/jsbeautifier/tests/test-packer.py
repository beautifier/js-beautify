from __future__ import print_function
import sys
import jsbeautifier

opts = jsbeautifier.default_options()
opts.eol = "\n"
global fails
fails = 0


def test_str(str, expected):
    global fails
    res = jsbeautifier.beautify(str, opts)
    if(res == expected):
        print(".")
        return True
    else:
        print("___got:" + res + "\n___expected:" + expected + "\n")
        fails = fails + 1
        return False


str = "eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('2 0=\"4 3!\";2 1=0.5(/b/6);a.9(\"8\").7=1;',12,12,'str|n|var|W3Schools|Visit|search|i|innerHTML|demo|getElementById|document|w3Schools'.split('|'),0,{}))"
expected = "var str = \"Visit W3Schools!\";\nvar n = str.search(/w3Schools/i);\ndocument.getElementById(\"demo\").innerHTML = n;"

res = test_str(str, expected)

str = "a=b;\r\nwhile(1){\ng=h;{return'\\w+'};break;eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('$(5).4(3(){$(\'.1\').0(2);$(\'.6\').0(d);$(\'.7\').0(b);$(\'.a\').0(8);$(\'.9\').0(c)});',14,14,'html|r5e57|8080|function|ready|document|r1655|rc15b|8888|r39b0|r6ae9|3128|65309|80'.split('|'),0,{}))c=abx;"
expected = "a = b;\nwhile (1) {\n    g = h; {\n        return '\\w+'\n    };\n    break;\n    $(document).ready(function() {\n        $('.r5e57').html(8080);\n        $('.r1655').html(80);\n        $('.rc15b').html(3128);\n        $('.r6ae9').html(8888);\n        $('.r39b0').html(65309)\n    });\n    c = abx;"

res = test_str(str, expected)

str = "eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};if('0'.replace(0,e)==0){while(c--)r[e(c)]=k[c];k=[function(e){return r[e]||e}];e=function(){return'[0-9ab]'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('$(5).a(6(){ $(\'.8\').0(1); $(\'.b\').0(4); $(\'.9\').0(2); $(\'.7\').0(3)})',[],12,'html|52136|555|65103|8088|document|function|r542c|r8ce6|rb0de|ready|rfab0'.split('|'),0,{}))"
expected = "$(document).ready(function() {\n    $(\'.r8ce6\').html(52136);\n    $(\'.rfab0\').html(8088);\n    $(\'.rb0de\').html(555);\n    $(\'.r542c\').html(65103)\n})"

res = test_str(str, expected)

if (fails == 0):
    print("OK")
