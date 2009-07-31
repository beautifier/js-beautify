/*global js_beautify */
var tests_passed = 0;
var tests_failed = 0;
var test_result  = '';


var indent_size       = 4;
var indent_char       = ' ';
var preserve_newlines = true;

function lazy_escape(str)
{
    return str.replace(/</g, '&lt;').replace(/\>/g, '&gt;').replace(/\n/g, '<br />');
}

function bt(input, expected)
{
    expected = expected || input;

    var result = js_beautify(input, {indent_size: indent_size, indent_char: indent_char, preserve_newlines: preserve_newlines});

    if (result !== expected) {
        test_result +=
            '\n---- input --------\n' + lazy_escape(input) +
            '\n---- expected -----\n' + lazy_escape(expected) +
            '\n---- received -----\n' + lazy_escape(result) +
            '\n-------------------';
        tests_failed += 1;
    } else {
        tests_passed += 1;
    }

}

function results()
{
    if (tests_failed === 0) {
        test_result += 'All ' + tests_passed + ' tests passed.';
    } else {
        test_result += '\n' + tests_failed + ' tests failed.';
    }
    return test_result;
}

function test_js_beautify()
{
    indent_size       = 4;
    tests_passed      = 0;
    tests_failed      = 0;
    indent_char       = ' ';
    test_result       = '';
    preserve_newlines = true;

    bt('');
    bt('a        =          1', 'a = 1');
    bt('a=1', 'a = 1');
    bt("a();\n\nb();", "a();\n\nb();");
    bt('var a = 1 var b = 2', "var a = 1\nvar b = 2");
    bt('a = " 12345 "');
    bt("a = ' 12345 '");
    bt('if (a == 1) b = 2', "if (a == 1) b = 2");
    bt('if(1){2}else{3}', "if (1) {\n    2\n} else {\n    3\n}");
    bt('if(1||2)', 'if (1 || 2)');
    bt('(a==1)||(b==2)', '(a == 1) || (b == 2)');
    bt('var a = 1 if (2) 3', "var a = 1\nif (2) 3");
    bt('a = a + 1');
    bt('a = a == 1');
    bt('/12345[^678]*9+/.match(a)');
    bt('a /= 5');
    bt('a = 0.5 * 3');
    bt('a *= 10.55');
    bt('a < .5');
    bt('a <= .5');
    bt('a<.5', 'a < .5');
    bt('a<=.5', 'a <= .5');
    bt('a = 0xff;');
    bt('a=0xff+4', 'a = 0xff + 4');
    bt('a = [1, 2, 3, 4]');
    bt('F*(g/=f)*g+b', 'F * (g /= f) * g + b');
    bt('a.b({c:d})', "a.b({\n    c: d\n})");
    bt('a.b\n(\n{\nc:\nd\n}\n)', "a.b({\n    c: d\n})");
    bt('a=!b', 'a = !b');
    bt('a?b:c', 'a ? b : c');
    bt('a?1:2', 'a ? 1 : 2');
    bt('a?(b):c', 'a ? (b) : c');
    bt('x={a:1,b:w=="foo"?x:y,c:z}', 'x = {\n    a: 1,\n    b: w == "foo" ? x : y,\n    c: z\n}');  
    bt('x=a?b?c?d:e:f:g;', 'x = a ? b ? c ? d : e : f : g;');   
    bt('x=a?b?c?d:{e1:1,e2:2}:f:g;', 'x = a ? b ? c ? d : {\n    e1: 1,\n    e2: 2\n} : f : g;');
    bt('function void(void) {}');
    bt('if(!a)', 'if (!a)');
    bt('a=~a', 'a = ~a');
    bt('a;/*comment*/b;', "a;\n/*comment*/\nb;");
    bt('if(a)break', "if (a) break");
    bt('if(a){break}', "if (a) {\n    break\n}");
    bt('if((a))', 'if ((a))');
    bt('for(var i=0;;)', 'for (var i = 0;;)');
    bt('a++;', 'a++;');
    bt('for(;;i++)', 'for (;; i++)');
    bt('for(;;++i)', 'for (;; ++i)');
    bt('return(1)', 'return (1)');
    bt('try{a();}catch(b){c();}finally{d();}', "try {\n    a();\n} catch(b) {\n    c();\n} finally {\n    d();\n}");
    bt('(xx)()'); // magic function call
    bt('a[1]()'); // another magic function call
    bt('if(a){b();}else if(', "if (a) {\n    b();\n} else if (");
    bt('switch(x) {case 0: case 1: a(); break; default: break}', "switch (x) {\ncase 0:\ncase 1:\n    a();\n    break;\ndefault:\n    break\n}");
    bt('switch(x){case -1:break;case !y:break;}', 'switch (x) {\ncase -1:\n    break;\ncase !y:\n    break;\n}');
    bt('a !== b');
    bt('if (a) b(); else c();', "if (a) b();\nelse c();");
    bt("// comment\n(function()", "// comment\n(function ()"); // typical greasemonkey start
    bt("// comment\n(function something()"); // typical greasemonkey start
    bt("{\n\n    x();\n\n}"); // was: duplicating newlines
    bt('if (a in b)');
    //bt('var a, b');
    bt('{a:1, b:2}', "{\n    a: 1,\n    b: 2\n}");
    bt('a={1:[-1],2:[+1]}', 'a = {\n    1: [-1],\n    2: [+1]\n}');
    bt('var l = {\'a\':\'1\', \'b\':\'2\'}', "var l = {\n    'a': '1',\n    'b': '2'\n}");
    bt('if (template.user[n] in bk)');
    bt('{{}/z/}', "{\n    {}\n    /z/\n}");
    bt('return 45', "return 45");
    bt('If[1]', "If[1]");
    bt('Then[1]', "Then[1]");
    bt('a = 1e10', "a = 1e10");
    bt('a = 1.3e10', "a = 1.3e10");
    bt('a = 1.3e-10', "a = 1.3e-10");
    bt('a = -1.3e-10', "a = -1.3e-10");
    bt('a = 1e-10', "a = 1e-10");
    bt('a = e - 10', "a = e - 10");
    bt('a = 11-10', "a = 11 - 10");
    bt("a = 1;// comment\n", "a = 1; // comment");
    bt("a = 1; // comment\n", "a = 1; // comment");
    bt("a = 1;\n // comment\n", "a = 1;\n// comment");

    bt("if (a) {\n    do();\n}"); // was: extra space appended
    bt("if\n(a)\nb()", "if (a) b()"); // test for proper newline removal

    bt("if (a) {\n// comment\n}else{\n// comment\n}", "if (a) {\n    // comment\n} else {\n    // comment\n}"); // if/else statement with empty body
    bt("if (a) {\n// comment\n// comment\n}", "if (a) {\n    // comment\n    // comment\n}"); // multiple comments indentation
    bt("if (a) b() else c()", "if (a) b()\nelse c()");
    bt("if (a) b() else if c() d()", "if (a) b()\nelse if c() d()");

    bt("{}");
    bt("{\n\n}");
    bt("do { a(); } while ( 1 );", "do {\n    a();\n} while (1);");
    bt("do {} while (1);");
    bt("do {\n} while (1);", "do {} while (1);");
    bt("do {\n\n} while (1);");
    bt("var a, b, c, d = 0, c = function() {}, d = '';", "var a, b, c, d = 0,\nc = function () {},\nd = '';");
    bt("var a = x(a, b, c)");
    bt("delete x if (a) b();", "delete x\nif (a) b();");
    bt("delete x[x] if (a) b();", "delete x[x]\nif (a) b();");
    bt("for(var a=1,b=2)", "for (var a = 1, b = 2)");
    bt("for(var a=1,b=2,c=3)", "for (var a = 1, b = 2, c = 3)");
    bt("for(var a=1,b=2,c=3;d<3;d++)", "for (var a = 1, b = 2, c = 3; d < 3; d++)");
    bt("function x(){(a||b).c()}", "function x() {\n    (a || b).c()\n}");
    bt("function x(){return - 1}", "function x() {\n    return -1\n}");
    bt("function x(){return ! a}", "function x() {\n    return !a\n}");

    bt("a = 'a'\nb = 'b'");
    bt("a = /reg/exp");
    bt("a = /reg/");
    bt('/abc/.test()');
    bt('/abc/i.test()');
    bt("{/abc/i.test()}", "{\n    /abc/i.test()\n}");

    bt('{x=#1=[]}', '{\n    x = #1=[]\n}');
    bt('{a:#1={}}', '{\n    a: #1={}\n}');
    bt('{a:#1#}', '{\n    a: #1#\n}');
    bt('{a:#1', '{\n    a: #1'); // incomplete
    bt('{a:#', '{\n    a: #'); // incomplete

    bt('<!--\nvoid();\n// -->', '<!--\nvoid();\n// -->');

    bt('a=/regexp', 'a = /regexp'); // incomplete regexp

    bt('{a:#1=[],b:#1#,c:#999999#}', '{\n    a: #1=[],\n    b: #1#,\n    c: #999999#\n}');
 
    bt("a = 1e+2");
    bt("a = 1e-2");
    bt("do{x()}while(a>1)", "do {\n    x()\n} while (a > 1)");

    bt("x(); /reg/exp.match(something)", "x();\n/reg/exp.match(something)");

    bt("something();(", "something();\n(");

    bt("function namespace::something()");

    bt("<!--\nsomething();\n-->", "<!--\nsomething();\n-->");
    bt("<!--\nif(i<0){bla();}\n-->", "<!--\nif (i < 0) {\n    bla();\n}\n-->");

    bt("<!--\nsomething();\n-->\n<!--\nsomething();\n-->", "<!--\nsomething();\n-->\n<!--\nsomething();\n-->");
    bt("<!--\nif(i<0){bla();}\n-->\n<!--\nif(i<0){bla();}\n-->", "<!--\nif (i < 0) {\n    bla();\n}\n-->\n<!--\nif (i < 0) {\n    bla();\n}\n-->");

    bt('var o=$.extend(a,function(){alert(x);}', 'var o = $.extend(a, function () {\n    alert(x);\n}');
    bt('var o=$.extend(a);function(){alert(x);}', 'var o = $.extend(a);\nfunction () {\n    alert(x);\n}');

    // regexps
    bt('a(/abc\\/\\/def/);b()', "a(/abc\\/\\/def/);\nb()");
    bt('a(/a[b\\[\\]c]d/);b()', "a(/a[b\\[\\]c]d/);\nb()");
    bt('a(/a[b\\[', "a(/a[b\\["); // incomplete char class
    // allow unescaped / in char classes
    bt('a(/[a/b]/);b()', "a(/[a/b]/);\nb()");

    indent_size = 1;
    indent_char = ' ';
    bt('{ one_char() }', "{\n one_char()\n}");

    indent_size = 4;
    indent_char = ' ';
    bt('{ one_char() }', "{\n    one_char()\n}");

    indent_size = 1;
    indent_char = "\t";
    bt('{ one_char() }', "{\n\tone_char()\n}");

    preserve_newlines = false;
    bt('var\na=dont_preserve_newlines', 'var a = dont_preserve_newlines');

    preserve_newlines = true;
    bt('var\na=do_preserve_newlines', 'var\na = do_preserve_newlines');

    return results();
}
