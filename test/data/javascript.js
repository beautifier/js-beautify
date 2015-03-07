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
            {
              input: "var ' + unicode_char(3232) + '_' + unicode_char(3232) + ' = \"hi\";"
            },
            {
                input: [
                    "var ' + unicode_char(228) + 'x = {",
                    "    ' + unicode_char(228) + 'rgerlich: true",
                    "};"]
            }
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
        name: "Comma-first option",
        description: "Put commas at the start of lines instead of the end",
        matrix: [
        {
            options: [
                { name: "comma_first", value: "true" }
            ],
            c0: '\\n, ',
            c1: '\\n    , ',
            c2: '\\n        , ',
            c3: '\\n            , '
        }, {
            options: [
                { name: "comma_first", value: "false" }
            ],
            c0: ',\\n',
            c1: ',\\n    ',
            c2: ',\\n        ',
            c3: ',\\n            '
        }
        ],
        tests: [
            { input: '{a:1, b:2}', output: "{\n    a: 1{{c1}}b: 2\n}" },
            { input: 'var a=1, b=c[d], e=6;', output: 'var a = 1{{c1}}b = c[d]{{c1}}e = 6;' },
            { input: "for(var a=1,b=2,c=3;d<3;d++)\ne", output: "for (var a = 1, b = 2, c = 3; d < 3; d++)\n    e" },
            { input: "for(var a=1,b=2,\nc=3;d<3;d++)\ne", output: "for (var a = 1, b = 2{{c2}}c = 3; d < 3; d++)\n    e" },
            { input: 'function foo() {\n    return [\n        "one"{{c2}}"two"\n    ];\n}' },
            { input: 'a=[[1,2],[4,5],[7,8]]', output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}[7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],[7,8],]', output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}[7, 8]{{c0}}]" },
            { input: 'a=[[1,2],[4,5],function(){},[7,8]]',
            output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}[7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],function(){},function(){},[7,8]]',
            output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}function() {}{{c1}}[7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],function(){},[7,8]]',
            output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}[7, 8]\n]" },
            { input: 'a=[b,c,function(){},function(){},d]',
            output: "a = [b, c, function() {}, function() {}, d]" },
            { input: 'a=[b,c,\nfunction(){},function(){},d]',
            output: "a = [b, c{{c1}}function() {}{{c1}}function() {}{{c1}}d\n]" },
            { input: 'a=[a[1],b[4],c[d[7]]]', output: "a = [a[1], b[4], c[d[7]]]" },
            { input: '[1,2,[3,4,[5,6],7],8]', output: "[1, 2, [3, 4, [5, 6], 7], 8]" },

            { input: '[[["1","2"],["3","4"]],[["5","6","7"],["8","9","0"]],[["1","2","3"],["4","5","6","7"],["8","9","0"]]]',
            output: '[\n    [\n        ["1", "2"]{{c2}}["3", "4"]\n    ]{{c1}}[\n        ["5", "6", "7"]{{c2}}["8", "9", "0"]\n    ]{{c1}}[\n        ["1", "2", "3"]{{c2}}["4", "5", "6", "7"]{{c2}}["8", "9", "0"]\n    ]\n]' },

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
            { input: 'if (template.user[n] in bk) foo();' },
            { input: 'return 45', output: "return 45" },
            { input: 'return this.prevObject ||\n\n    this.constructor(null);' },
            { input: 'If[1]', output: "If[1]" },
            { input: 'Then[1]', output: "Then[1]" },
            { input: 'a = 1e10', output: "a = 1e10" },
            { input: 'a = 1.3e10', output: "a = 1.3e10" },
            { input: 'a = 1.3e-10', output: "a = 1.3e-10" },
            { input: 'a = -1.3e-10', output: "a = -1.3e-10" },
            { input: 'a = 1e-10', output: "a = 1e-10" },
            { input: 'a = e - 10', output: "a = e - 10" },
            { input: 'a = 11-10', output: "a = 11 - 10" },
            { input: "a = 1;// comment", output: "a = 1; // comment" },
            { input: "a = 1; // comment", output: "a = 1; // comment" },
            { input: "a = 1;\n // comment", output: "a = 1;\n// comment" },
            { input: 'a = [-1, -1, -1]' },


            { comment: 'The exact formatting these should have is open for discussion, but they are at least reasonable',
                input: 'a = [ // comment\n    -1, -1, -1\n]' },
            { input: 'var a = [ // comment\n    -1, -1, -1\n]' },
            { input: 'a = [ // comment\n    -1, // comment\n    -1, -1\n]' },
            { input: 'var a = [ // comment\n    -1, // comment\n    -1, -1\n]' },

            { input: 'o = [{a:b},{c:d}]', output: 'o = [{\n    a: b\n}, {\n    c: d\n}]' },

            { comment: 'was: extra space appended',
                input: "if (a) {\n    do();\n}" },

            { comment: 'if/else statement with empty body',
                input: "if (a) {\n// comment\n}else{\n// comment\n}", output: "if (a) {\n    // comment\n} else {\n    // comment\n}" },
            { comment: 'multiple comments indentation', input: "if (a) {\n// comment\n// comment\n}", output: "if (a) {\n    // comment\n    // comment\n}" },
            { input: "if (a) b() else c();", output: "if (a) b()\nelse c();" },
            { input: "if (a) b() else if c() d();", output: "if (a) b()\nelse if c() d();" },

            { input: "{}" },
            { input: "{\n\n}" },
            { input: "do { a(); } while ( 1 );", output: "do {\n    a();\n} while (1);" },
            { input: "do {} while (1);" },
            { input: "do {\n} while (1);", output: "do {} while (1);" },
            { input: "do {\n\n} while (1);" },
            { input: "var a = x(a, b, c)" },
            { input: "delete x if (a) b();", output: "delete x\nif (a) b();" },
            { input: "delete x[x] if (a) b();", output: "delete x[x]\nif (a) b();" },
            { input: "for(var a=1,b=2)d", output: "for (var a = 1, b = 2) d" },
            { input: "for(var a=1,b=2,c=3) d", output: "for (var a = 1, b = 2, c = 3) d" },
            { input: "for(var a=1,b=2,c=3;d<3;d++)\ne", output: "for (var a = 1, b = 2, c = 3; d < 3; d++)\n    e" },
            { input: "function x(){(a||b).c()}", output: "function x() {\n    (a || b).c()\n}" },
            { input: "function x(){return - 1}", output: "function x() {\n    return -1\n}" },
            { input: "function x(){return ! a}", output: "function x() {\n    return !a\n}" },
            { input: "x => x", output: "x => x" },
            { input: "(x) => x", output: "(x) => x" },
            { input: "x => { x }", output: "x => {\n    x\n}" },
            { input: "(x) => { x }", output: "(x) => {\n    x\n}" },

            { comment: 'a common snippet in jQuery plugins',
                input: "settings = $.extend({},defaults,settings);",
                output: "settings = $.extend({}, defaults, settings);" },

            // reserved words used as property names
            { input: "$http().then().finally().default()", output: "$http().then().finally().default()" },
            { input: "$http()\n.then()\n.finally()\n.default()", output: "$http()\n    .then()\n    .finally()\n    .default()" },
            { input: "$http().when.in.new.catch().throw()", output: "$http().when.in.new.catch().throw()" },
            { input: "$http()\n.when\n.in\n.new\n.catch()\n.throw()", output: "$http()\n    .when\n    .in\n    .new\n    .catch()\n    .throw()" },

            { input: '{xxx;}()', output: '{\n    xxx;\n}()' },

            { input: "a = \\'a\\'\nb = \\'b\\'" },
            { input: "a = /reg/exp" },
            { input: "a = /reg/" },
            { input: '/abc/.test()' },
            { input: '/abc/i.test()' },
            { input: "{/abc/i.test()}", output: "{\n    /abc/i.test()\n}" },
            { input: 'var x=(a)/a;', output: 'var x = (a) / a;' },

            { input: 'x != -1', output: 'x != -1' },

            { input: 'for (; s-->0;)t', output: 'for (; s-- > 0;) t' },
            { input: 'for (; s++>0;)u', output: 'for (; s++ > 0;) u' },
            { input: 'a = s++>s--;', output: 'a = s++ > s--;' },
            { input: 'a = s++>--s;', output: 'a = s++ > --s;' },

            { input: '{x=#1=[]}', output: '{\n    x = #1=[]\n}' },
            { input: '{a:#1={}}', output: '{\n    a: #1={}\n}' },
            { input: '{a:#1#}', output: '{\n    a: #1#\n}' },

            { fragment: '"incomplete-string' },
            { fragment: "\\'incomplete-string" },
            { fragment: '/incomplete-regex' },
            { fragment: '`incomplete-template-string' },

            { fragment: '{a:1},{a:2}', output: '{\n    a: 1\n}, {\n    a: 2\n}' },
            { fragment: 'var ary=[{a:1}, {a:2}];', output: 'var ary = [{\n    a: 1\n}, {\n    a: 2\n}];' },

            { comment: 'incomplete', fragment: '{a:#1', output: '{\n    a: #1' },
            { comment: 'incomplete', fragment: '{a:#', output: '{\n    a: #' },

            { comment: 'incomplete', fragment: '}}}', output: '}\n}\n}' },

            { fragment: '<!--\nvoid();\n// -->', output: '<!--\nvoid();\n// -->' },

            { comment: 'incomplete regexp', fragment: 'a=/regexp', output: 'a = /regexp' },

            { input: '{a:#1=[],b:#1#,c:#999999#}', output: '{\n    a: #1=[],\n    b: #1#,\n    c: #999999#\n}' },

            { input: "a = 1e+2" },
            { input: "a = 1e-2" },
            { input: "do{x()}while(a>1)", output: "do {\n    x()\n} while (a > 1)" },

            { input: "x(); /reg/exp.match(something)", output: "x();\n/reg/exp.match(something)" },

            { fragment: "something();(", output: "something();\n(" },
            { fragment: "#!she/bangs, she bangs\nf=1", output: "#!she/bangs, she bangs\n\nf = 1" },
            { fragment: "#!she/bangs, she bangs\n\nf=1", output: "#!she/bangs, she bangs\n\nf = 1" },
            { fragment: "#!she/bangs, she bangs\n\n/* comment */", output: "#!she/bangs, she bangs\n\n/* comment */" },
            { fragment: "#!she/bangs, she bangs\n\n\n/* comment */", output: "#!she/bangs, she bangs\n\n\n/* comment */" },
            { fragment: "#", output: "#" },
            { fragment: "#!", output: "#!" },

            { input: "function namespace::something()" },

            { fragment: "<!--\nsomething();\n-->", output: "<!--\nsomething();\n-->" },
            { fragment: "<!--\nif(i<0){bla();}\n-->", output: "<!--\nif (i < 0) {\n    bla();\n}\n-->" },

            { input: '{foo();--bar;}', output: '{\n    foo();\n    --bar;\n}' },
            { input: '{foo();++bar;}', output: '{\n    foo();\n    ++bar;\n}' },
            { input: '{--bar;}', output: '{\n    --bar;\n}' },
            { input: '{++bar;}', output: '{\n    ++bar;\n}' },
            { input: 'if(true)++a;', output: 'if (true) ++a;' },
            { input: 'if(true)\n++a;', output: 'if (true)\n    ++a;' },
            { input: 'if(true)--a;', output: 'if (true) --a;' },
            { input: 'if(true)\n--a;', output: 'if (true)\n    --a;' },
            { input: 'elem[array]++;' },
            { input: 'elem++ * elem[array]++;' },
            { input: 'elem-- * -elem[array]++;' },
            { input: 'elem-- + elem[array]++;' },
            { input: 'elem-- - elem[array]++;' },
            { input: 'elem-- - -elem[array]++;' },
            { input: 'elem-- - +elem[array]++;' },


            { comment: 'Handling of newlines around unary ++ and -- operators',
                input: '{foo\n++bar;}', output: '{\n    foo\n    ++bar;\n}' },
            { input: '{foo++\nbar;}', output: '{\n    foo++\n    bar;\n}' },

            { comment: 'This is invalid, but harder to guard against. Issue #203.',
                input: '{foo\n++\nbar;}', output: '{\n    foo\n    ++\n    bar;\n}' },

            { comment: 'regexps',
                input: 'a(/abc\\\\/\\\\/def/);b()', output: "a(/abc\\\\/\\\\/def/);\nb()" },
            { input: 'a(/a[b\\\\[\\\\]c]d/);b()', output: "a(/a[b\\\\[\\\\]c]d/);\nb()" },
            { comment: 'incomplete char class', fragment: 'a(/a[b\\\\[', output: "a(/a[b\\\\[" },

            { comment: 'allow unescaped / in char classes',
                input: 'a(/[a/b]/);b()', output: "a(/[a/b]/);\nb()" },
            { input: 'typeof /foo\\\\//;' },
            { input: 'yield /foo\\\\//;' },
            { input: 'throw /foo\\\\//;' },
            { input: 'do /foo\\\\//;' },
            { input: 'return /foo\\\\//;' },
            { input: 'switch (a) {\n    case /foo\\\\//:\n        b\n}' },
            { input: 'if (a) /foo\\\\//\nelse /foo\\\\//;' },

            { input: 'if (foo) /regex/.test();' },
            { input: 'result = yield pgClient.query_(queryString);' },

            { input: 'function foo() {\n    return [\n        "one",\n        "two"\n    ];\n}' },
            { input: 'a=[[1,2],[4,5],[7,8]]', output: "a = [\n    [1, 2],\n    [4, 5],\n    [7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    [7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],function(){},function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    function() {},\n    [7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    [7, 8]\n]" },
            { input: 'a=[b,c,function(){},function(){},d]',
                output: "a = [b, c, function() {}, function() {}, d]" },
            { input: 'a=[b,c,\nfunction(){},function(){},d]',
                output: "a = [b, c,\n    function() {},\n    function() {},\n    d\n]" },
            { input: 'a=[a[1],b[4],c[d[7]]]', output: "a = [a[1], b[4], c[d[7]]]" },
            { input: '[1,2,[3,4,[5,6],7],8]', output: "[1, 2, [3, 4, [5, 6], 7], 8]" },

            { input: '[[["1","2"],["3","4"]],[["5","6","7"],["8","9","0"]],[["1","2","3"],["4","5","6","7"],["8","9","0"]]]',
              output: '[\n    [\n        ["1", "2"],\n        ["3", "4"]\n    ],\n    [\n        ["5", "6", "7"],\n        ["8", "9", "0"]\n    ],\n    [\n        ["1", "2", "3"],\n        ["4", "5", "6", "7"],\n        ["8", "9", "0"]\n    ]\n]' },

            { input: '{[x()[0]];indent;}', output: '{\n    [x()[0]];\n    indent;\n}' },
            { input: '/*\n foo trailing space    \n * bar trailing space   \n**/',
             output: '/*\n foo trailing space    \n * bar trailing space   \n**/'},
            { input: '{\n    /*\n    foo    \n    * bar    \n    */\n}',
             output: '{\n    /*\n    foo    \n    * bar    \n    */\n}'}
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
