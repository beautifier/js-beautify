var tests_passed = 0;
var tests_failed = 0;
var test_result = '';


var indent_size = 4;
var indent_char = ' ';

function lazy_escape(str)
{
    return str.replace(/</g, '&lt;').replace(/\>/g, '&gt;').replace(/\n/g, '<br />');
}

function bt(input, expected)
{
    expected = expected || input;

    result = js_beautify(input, indent_size, indent_char);

    if (result != expected) {
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
    if (tests_failed == 0) {
        test_result += 'All ' + tests_passed + ' tests passed.';
    } else {
        test_result += '\n' + tests_failed + ' tests failed.';
    }
    return test_result;
}

function test_js_beautify()
{

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
    bt('a=!b', 'a = !b');
    bt('a?b:c', 'a ? b: c'); // 'a ? b : c' would need too make parser more complex to differentiate between ternary op and object assignment
    bt('a?1:2', 'a ? 1 : 2'); // 'a ? b : c' would need too make parser more complex to differentiate between ternary op and object assignment
    bt('a?(b):c', 'a ? (b) : c'); // this works, though
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
    bt('a !== b');
    bt('if (a) b(); else c();', "if (a) b();\nelse c();");
    bt("// comment\n(function()"); // typical greasemonkey start
    bt("// comment\n(function something()"); // typical greasemonkey start
    bt("{\n\n    x();\n\n}"); // was: duplicating newlines
    bt('if (a in b)');
    //bt('var a, b');
    bt('{a:1, b:2}', "{\n    a: 1,\n    b: 2\n}");
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
    bt("a = 1;// comment\n", "a = 1; // comment\n");
    bt("a = 1; // comment\n", "a = 1; // comment\n");
    bt("a = 1;\n // comment\n", "a = 1;\n// comment\n");

    bt("if (a) {\n    do();\n}"); // was: extra space appended
    bt("if\n(a)\nb()", "if (a) b()"); // test for proper newline removal
    
    bt("if (a) {\n// comment\n}else{\n// comment\n}", "if (a) {\n    // comment\n} else {\n    // comment\n}"); // if/else statement with empty body
    bt("if (a) {\n// comment\n// comment\n}", "if (a) {\n    // comment\n    // comment\n}"); // multiple comments indentation
    bt("if (a) b() else c()", "if (a) b()\nelse c()");
    bt("if (a) b() else if c() d()", "if (a) b()\nelse if c() d()");

    bt("{}");
    bt("{\n\n}");
    bt("do { a(); } while ( 1 );", "do {\n    a();\n} while ( 1 );");
    bt("do {} while ( 1 );");
    bt("do {\n} while ( 1 );", "do {} while ( 1 );");
    bt("do {\n\n} while ( 1 );");
    bt("var a, b, c, d = 0, c = function() {}, d = '';", "var a, b, c, d = 0,\nc = function() {},\nd = '';");
    bt("var a = x(a, b, c)");
    bt("delete x if (a) b();", "delete x\nif (a) b();");
    bt("delete x[x] if (a) b();", "delete x[x]\nif (a) b();");


    indent_size = 1;
    indent_char = ' ';
    bt('{ one_char() }', "{\n one_char()\n}")

    indent_size = 4;
    indent_char = ' ';
    bt('{ one_char() }', "{\n    one_char()\n}")

    indent_size = 1;
    indent_char = "\t";
    bt('{ one_char() }', "{\n\tone_char()\n}")
    return results();
}
