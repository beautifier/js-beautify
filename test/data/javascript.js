exports.test_data = {
    default_options: [
        { name: "indent_size", value: "4" },
        { name: "indent_char", value: "' '" },
        { name: "preserve_newlines", value: "true" },
        { name: "jslint_happy", value: "false" },
        { name: "keep_array_indentation", value: "false" },
        { name: "brace_style", value: "'collapse'" }
    ],
    groups: [{
        name: "Unicode Support",
        description: "",
        tests: [
            { input: "var ' + unicode_char(3232) + '_' + unicode_char(3232) + ' = \"hi\";" },
            { input: "var ' + unicode_char(228) + 'x = {\n    ' + unicode_char(228) + 'rgerlich: true\n};" }
        ],
    }, {
        name: "End With Newline",
        description: "",
        matrix: [
            {
                options: [
                    { name: "end_with_newline", value: "true" }
                ],
                eof: '\\n'
            }, {
                options: [
                    { name: "end_with_newline", value: "false" }
                ],
                eof: ''
            }

        ],
        tests: [
            { fragment: '', output: '{{eof}}' },
            { fragment: '   return .5', output: '   return .5{{eof}}' },
            { fragment: '   \n\nreturn .5\n\n\n\n', output: '   return .5{{eof}}' },
            { fragment: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "New Test Suite"
    },
        // =======================================================
        // New tests groups should be added above this line.
        // Everything below is a work in progress - converting
        // old test to generated form.
        // =======================================================
    {
        name: "Old tests",
        description: "Largely unorganized pile of tests",
        options: [],
        tests: [
            { input: '' },
            { fragment: '   return .5'},
            { fragment: '   return .5;\n   a();' },
            { fragment: '    return .5;\n    a();' },
            { fragment: '     return .5;\n     a();' },
            { fragment: '   < div'},
            { input: 'a        =          1', output: 'a = 1' },
            { input: 'a=1', output: 'a = 1' },
            { input: '(3) / 2' },
            { input: '["a", "b"].join("")' },
            { input: 'a();\n\nb();', output: 'a();\n\nb();' },
            { input: 'var a = 1 var b = 2', output: 'var a = 1\nvar b = 2' },
            { input: 'var a=1, b=c[d], e=6;', output: 'var a = 1,\n    b = c[d],\n    e = 6;' },
            { input: 'var a,\n    b,\n    c;' },
            { input: 'let a = 1 let b = 2', output: 'let a = 1\nlet b = 2' },
            { input: 'let a=1, b=c[d], e=6;', output: 'let a = 1,\n    b = c[d],\n    e = 6;' },
            { input: 'let a,\n    b,\n    c;' },
            { input: 'const a = 1 const b = 2', output: 'const a = 1\nconst b = 2' },
            { input: 'const a=1, b=c[d], e=6;', output: 'const a = 1,\n    b = c[d],\n    e = 6;' },
            { input: 'const a,\n    b,\n    c;' },
            { input: 'a = " 12345 "' },
            { input: "a = \\' 12345 \\'" },
            { input: 'if (a == 1) b = 2;', output: 'if (a == 1) b = 2;' },
            { input: 'if(1){2}else{3}', output: 'if (1) {\n    2\n} else {\n    3\n}' },
            { input: 'if(1||2);', output: 'if (1 || 2);' },
            { input: '(a==1)||(b==2)', output: '(a == 1) || (b == 2)' },
            { input: 'var a = 1 if (2) 3;', output: 'var a = 1\nif (2) 3;' },
            { input: 'a = a + 1' },
            { input: 'a = a == 1' },
            { input: '/12345[^678]*9+/.match(a)' },
            { input: 'a /= 5' },
            { input: 'a = 0.5 * 3' },
            { input: 'a *= 10.55' },
            { input: 'a < .5' },
            { input: 'a <= .5' },
            { input: 'a<.5', output: 'a < .5' },
            { input: 'a<=.5', output: 'a <= .5' },
            { input: 'a = 0xff;' },
            { input: 'a=0xff+4', output: 'a = 0xff + 4' },
            { input: 'a = [1, 2, 3, 4]' },
            { input: 'F*(g/=f)*g+b', output: 'F * (g /= f) * g + b' },
            { input: 'a.b({c:d})', output: 'a.b({\n    c: d\n})' },
            { input: 'a.b\n(\n{\nc:\nd\n}\n)', output: 'a.b({\n    c: d\n})' },
            { input: 'a.b({c:"d"})', output: 'a.b({\n    c: "d"\n})' },
            { input: 'a.b\n(\n{\nc:\n"d"\n}\n)', output: 'a.b({\n    c: "d"\n})' },
            { input: 'a=!b', output: 'a = !b' },
            { input: 'a=!!b', output: 'a = !!b' },
            { input: 'a?b:c', output: 'a ? b : c' },
            { input: 'a?1:2', output: 'a ? 1 : 2' },
            { input: 'a?(b):c', output: 'a ? (b) : c' },
            { input: 'x={a:1,b:w=="foo"?x:y,c:z}', output: 'x = {\n    a: 1,\n    b: w == "foo" ? x : y,\n    c: z\n}' },
            { input: 'x=a?b?c?d:e:f:g;', output: 'x = a ? b ? c ? d : e : f : g;' },
            { input: 'x=a?b?c?d:{e1:1,e2:2}:f:g;', output: 'x = a ? b ? c ? d : {\n    e1: 1,\n    e2: 2\n} : f : g;' },
            { input: 'function void(void) {}' },
            { input: 'if(!a)foo();', output: 'if (!a) foo();' },
            { input: 'a=~a', output: 'a = ~a' },
            { input: 'a;/*comment*/b;', output: "a; /*comment*/\nb;" },
            { input: 'a;/* comment */b;', output: "a; /* comment */\nb;" },
            { fragment: 'a;/*\ncomment\n*/b;', output: "a;\n/*\ncomment\n*/\nb;", comment: "simple comments don't get touched at all"  },
            { input: 'a;/**\n* javadoc\n*/b;', output: "a;\n/**\n * javadoc\n */\nb;" },
            { fragment: 'a;/**\n\nno javadoc\n*/b;', output: "a;\n/**\n\nno javadoc\n*/\nb;" },
            { input: 'a;/*\n* javadoc\n*/b;', output: "a;\n/*\n * javadoc\n */\nb;", comment: 'comment blocks detected and reindented even w/o javadoc starter' },
            { input: 'if(a)break;', output: "if (a) break;" },
            { input: 'if(a){break}', output: "if (a) {\n    break\n}" },
            { input: 'if((a))foo();', output: 'if ((a)) foo();' },
            { input: 'for(var i=0;;) a', output: 'for (var i = 0;;) a' },
            { input: 'for(var i=0;;)\na', output: 'for (var i = 0;;)\n    a' },
            { input: 'a++;', output: 'a++;' },
            { input: 'for(;;i++)a()', output: 'for (;; i++) a()' },
            { input: 'for(;;i++)\na()', output: 'for (;; i++)\n    a()' },
            { input: 'for(;;++i)a', output: 'for (;; ++i) a' },
            { input: 'return(1)', output: 'return (1)' },
            { input: 'try{a();}catch(b){c();}finally{d();}', output: "try {\n    a();\n} catch (b) {\n    c();\n} finally {\n    d();\n}" },
            { input: '(xx)()', comment: ' magic function call'},
            { input: 'a[1]()', comment: 'another magic function call'},
            { input: 'if(a){b();}else if(c) foo();', output: "if (a) {\n    b();\n} else if (c) foo();" },
            { input: 'switch(x) {case 0: case 1: a(); break; default: break}', output: "switch (x) {\n    case 0:\n    case 1:\n        a();\n        break;\n    default:\n        break\n}" },
            { input: 'switch(x){case -1:break;case !y:break;}', output: 'switch (x) {\n    case -1:\n        break;\n    case !y:\n        break;\n}' },
            { input: 'a !== b' },
            { input: 'if (a) b(); else c();', output: "if (a) b();\nelse c();" },
            { input: "// comment\n(function something() {})", comment: 'typical greasemonkey start' },
            { input: "{\n\n    x();\n\n}", comment: 'duplicating newlines' },
            { input: 'if (a in b) foo();' },
            { input: 'if(X)if(Y)a();else b();else c();',
                output: "if (X)\n    if (Y) a();\n    else b();\nelse c();" },
            { input: 'if (foo) bar();\nelse break' },
            { input: 'var a, b;' },
            { input: 'var a = new function();' },
            { fragment: 'new function' },
            { input: 'var a, b' },
            { input: '{a:1, b:2}', output: "{\n    a: 1,\n    b: 2\n}" },
            { input: 'a={1:[-1],2:[+1]}', output: 'a = {\n    1: [-1],\n    2: [+1]\n}' },
            { input: "var l = {\\'a\\':\\'1\\', \\'b\\':\\'2\\'}", output: "var l = {\n    \\'a\\': \\'1\\',\n    \\'b\\': \\'2\\'\n}" },
            { input: 'if (template.user[n] in bk) foo();' }
        ],
    }],
    // Example
    examples: [{
        group_name: "one",
        description: "",
        options: [],
        values: [
            {
                source: "", //string or array of lines
                output: ""  //string or array of lines
            }
        ]
    }]
}
