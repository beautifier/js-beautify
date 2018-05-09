/*
  The MIT License (MIT)

  Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

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

var inputlib = require('./inputlib');

exports.test_data = {
    default_options: [
        { name: "indent_size", value: "4" },
        { name: "indent_char", value: "' '" },
        { name: "preserve_newlines", value: "true" },
        { name: "jslint_happy", value: "false" },
        { name: "keep_array_indentation", value: "false" },
        { name: "brace_style", value: "'collapse'" },
        { name: "operator_position", value: "'before-newline'" }
    ],
    groups: [{
        name: "Unicode Support",
        description: "",
        tests: [{
            unchanged: "var ' + unicode_char(3232) + '_' + unicode_char(3232) + ' = \"hi\";"
        }, {
            unchanged: [
                "var ' + unicode_char(228) + 'x = {",
                "    ' + unicode_char(228) + 'rgerlich: true",
                "};"
            ]
        }]
    }, {
        name: "Test template and continuation strings",
        description: "",
        tests: [
            { unchanged: '`This is a ${template} string.`' },
            { unchanged: '`This\n  is\n  a\n  ${template}\n  string.`' },
            { unchanged: 'a = `This is a continuation\\\\\nstring.`' },
            { unchanged: 'a = "This is a continuation\\\\\nstring."' },
            { unchanged: '`SELECT\n  nextval(\\\'${this.options.schema ? `${this.options.schema}.` : \\\'\\\'}"${this.tableName}_${this.autoIncrementField}_seq"\\\'::regclass\n  ) nextval;`' },
            {
                comment: 'Tests for #1030',
                unchanged: [
                    'const composeUrl = (host) => {',
                    '    return `${host `test`}`;',
                    '};'
                ]
            }, {
                unchanged: [
                    'const composeUrl = (host, api, key, data) => {',
                    '    switch (api) {',
                    '        case "Init":',
                    '            return `${host}/vwapi/Init?VWID=${key}&DATA=${encodeURIComponent(',
                    '                Object.keys(data).map((k) => `${k}=${ data[k]}` ).join(";")',
                    '            )}`;',
                    '        case "Pay":',
                    '            return `${host}/vwapi/Pay?SessionId=${par}`;',
                    '    };',
                    '};'
                ]
            }
        ]
    }, {
        name: "ES7 Decorators",
        description: "Permit ES7 decorators, which are invoked with a leading \"@\".",
        tests: [
            { unchanged: '@foo' },
            { unchanged: '@foo(bar)' },
            {
                unchanged: [
                    '@foo(function(k, v) {',
                    '    implementation();',
                    '})'
                ]
            }
        ]
    }, {
        name: "ES7 exponential",
        description: "ES7 exponential",
        tests: [
            { unchanged: 'x ** 2' },
            { unchanged: 'x ** -2' }
        ]
    }, {
        name: "Spread operator",
        description: "Spread operator",
        options: [
            { name: 'brace_style', value: '"collapse,preserve-inline"' }
        ],
        tests: [
            { unchanged: 'const m = { ...item, c: 3 };' },
            { unchanged: 'const m = {\n    ...item,\n    c: 3\n};' },
            { unchanged: 'const m = { c: 3, ...item };' },
            { unchanged: 'const m = [...item, 3];' },
            { unchanged: 'const m = [3, ...item];' }
        ]
    }, {
        name: "Object literal shorthand functions",
        description: "Object literal shorthand functions",
        tests: [
            { unchanged: 'return {\n    foo() {\n        return 42;\n    }\n}' },
            {
                unchanged: [
                    'var foo = {',
                    '    * bar() {',
                    '        yield 42;',
                    '    }',
                    '};'
                ]
            },
            {
                input: 'var foo = {bar(){return 42;},*barGen(){yield 42;}};',
                output: ['var foo = {',
                    '    bar() {',
                    '        return 42;',
                    '    },',
                    '    * barGen() {',
                    '        yield 42;',
                    '    }',
                    '};'
                ]
            }, {
                comment: 'also handle generator shorthand in class - #1013',
                unchanged: [
                    'class A {',
                    '    fn() {',
                    '        return true;',
                    '    }',
                    '',
                    '    * gen() {',
                    '        return true;',
                    '    }',
                    '}'
                ]
            }, {
                unchanged: [
                    'class A {',
                    '    * gen() {',
                    '        return true;',
                    '    }',
                    '',
                    '    fn() {',
                    '        return true;',
                    '    }',
                    '}'
                ]
            }
        ]
    }, {
        name: "End With Newline",
        description: "",
        matrix: [{
                options: [
                    { name: "end_with_newline", value: "true" }
                ],
                eof: '\n'
            }, {
                options: [
                    { name: "end_with_newline", value: "false" }
                ],
                eof: ''
            }

        ],
        tests: [
            { fragment: true, input: '', output: '{{eof}}' },
            { fragment: true, input: '   return .5', output: '   return .5{{eof}}' },
            { fragment: true, input: '   \n\nreturn .5\n\n\n\n', output: '   return .5{{eof}}' },
            { fragment: true, input: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "Support simple language specific option inheritance/overriding",
        description: "Support simple language specific option inheritance/overriding",
        matrix: [{
                options: [
                    { name: "js", value: "{ 'indent_size': 3 }" },
                    { name: "css", value: "{ 'indent_size': 5 }" }
                ],
                j: '   '
            },
            {
                options: [
                    { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 } }" }
                ],
                j: '    '
            },
            {
                options: [
                    { name: "indent_size", value: "9" },
                    { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 }, 'indent_size': 2}" },
                    { name: "js", value: "{ 'indent_size': 4 }" },
                    { name: "css", value: "{ 'indent_size': 3 }" }
                ],
                j: '    '
            }
        ],
        tests: [{
            unchanged: [
                'if (a == b) {',
                '{{j}}test();',
                '}'
            ]
        }, ]
    }, {
        name: "Brace style permutations",
        description: "",
        template: "< >",
        matrix: [
            // brace_style collapse,preserve-inline - Should preserve if no newlines
            {
                options: [
                    { name: "brace_style", value: "'collapse,preserve-inline'" }
                ],
                ibo: '',
                iao: '',
                ibc: '',
                iac: '',
                obo: ' ',
                oao: ' ',
                obc: ' ',
                oac: ' '
            },
            {
                options: [
                    { name: "brace_style", value: "'collapse,preserve-inline'" }
                ],
                ibo: '\n',
                iao: '\n',
                ibc: '\n',
                iac: '\n',
                obo: ' ',
                oao: '\n    ',
                obc: '\n',
                oac: ' '
            },

            // brace_style collapse - Shouldn't preserve if no newlines (uses collapse styling)
            {
                options: [
                    { name: "brace_style", value: "'collapse'" }
                ],
                ibo: '',
                iao: '',
                ibc: '',
                iac: '',
                obo: ' ',
                oao: '\n    ',
                obc: '\n',
                oac: ' '
            },
            {
                options: [
                    { name: "brace_style", value: "'collapse'" }
                ],
                ibo: '\n',
                iao: '\n',
                ibc: '\n',
                iac: '\n',
                obo: ' ',
                oao: '\n    ',
                obc: '\n',
                oac: ' '
            },
        ],
        tests: [{
                input: 'var a =<ibo>{<iao>a: 2<ibc>}<iac>;\nvar a =<ibo>{<iao>a: 2<ibc>}<iac>;',
                output: 'var a =<obo>{<oao>a: 2<obc>};\nvar a =<obo>{<oao>a: 2<obc>};'
            },
            // {
            //     input: 'var a =<ibo>{<iao>a:<ibo>{<iao>a:<ibo>{<iao>a:2<ibc>}<iac><ibc>}<iac>}<iac>;\nvar a =<ibo>{<iao>a:<ibo>{<iao>a:<ibo>{<iao>a:2<ibc>}<iac><ibc>}<iac>}<iac>;',
            //     output: 'var a =<obo>{<oao>a:<obo>{<oao>a:<obo>{<oao>a: 2<obc>}<oac><obc>}<oac><obc>};\nvar a =<obo>{<oao>a:<obo>{<oao>a:<obo>{<oao>a: 2<obc>}<oac><obc>}<oac><obc>};'
            // },
            {
                input: '//case 1\nif (a == 1)<ibo>{}\n//case 2\nelse if (a == 2)<ibo>{}',
                output: '//case 1\nif (a == 1)<obo>{}\n//case 2\nelse if (a == 2)<obo>{}'
            },
            {
                input: 'if(1)<ibo>{<iao>2<ibc>}<iac>else<ibo>{<iao>3<ibc>}',
                output: 'if (1)<obo>{<oao>2<obc>}<oac>else<obo>{<oao>3<obc>}'
            },
            {
                input: 'try<ibo>{<iao>a();<ibc>}<iac>' +
                    'catch(b)<ibo>{<iao>c();<ibc>}<iac>' +
                    'catch(d)<ibo>{}<iac>' +
                    'finally<ibo>{<iao>e();<ibc>}',
                output:
                    // expected
                    'try<obo>{<oao>a();<obc>}<oac>' +
                    'catch (b)<obo>{<oao>c();<obc>}<oac>' +
                    'catch (d)<obo>{}<oac>' +
                    'finally<obo>{<oao>e();<obc>}'
            }
        ],
    }, {
        name: "Comma-first option",
        description: "Put commas at the start of lines instead of the end",
        matrix: [{
            options: [
                { name: "comma_first", value: "false" }
            ],
            c0: ',\n',
            c1: ',\n    ',
            c2: ',\n        ',
            c3: ',\n            ',
            // edge cases where engine bails
            f1: '    ,\n    '
        }, {
            options: [
                { name: "comma_first", value: "true" }
            ],
            c0: '\n, ',
            c1: '\n    , ',
            c2: '\n        , ',
            c3: '\n            , ',
            // edge cases where engine bails
            f1: ', '
        }],
        tests: [
            { input: '{a:1, b:2}', output: "{\n    a: 1{{c1}}b: 2\n}" },
            { input: 'var a=1, b=c[d], e=6;', output: 'var a = 1{{c1}}b = c[d]{{c1}}e = 6;' },
            { input: "for(var a=1,b=2,c=3;d<3;d++)\ne", output: "for (var a = 1, b = 2, c = 3; d < 3; d++)\n    e" },
            { input: "for(var a=1,b=2,\nc=3;d<3;d++)\ne", output: "for (var a = 1, b = 2{{c2}}c = 3; d < 3; d++)\n    e" },
            { unchanged: 'function foo() {\n    return [\n        "one"{{c2}}"two"\n    ];\n}' },
            { input: 'a=[[1,2],[4,5],[7,8]]', output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}[7, 8]\n]" },
            { input: 'a=[[1,2],[4,5],[7,8],]', output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}[7, 8]{{c0}}]" },
            {
                input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}[7, 8]\n]"
            },
            {
                input: 'a=[[1,2],[4,5],function(){},function(){},[7,8]]',
                output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}function() {}{{c1}}[7, 8]\n]"
            },
            {
                input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2]{{c1}}[4, 5]{{c1}}function() {}{{c1}}[7, 8]\n]"
            },
            {
                input: 'a=[b,c,function(){},function(){},d]',
                output: "a = [b, c, function() {}, function() {}, d]"
            },
            {
                input: 'a=[b,c,\nfunction(){},function(){},d]',
                output: "a = [b, c{{c1}}function() {}{{c1}}function() {}{{c1}}d\n]"
            },
            { input: 'a=[a[1],b[4],c[d[7]]]', output: "a = [a[1], b[4], c[d[7]]]" },
            { input: '[1,2,[3,4,[5,6],7],8]', output: "[1, 2, [3, 4, [5, 6], 7], 8]" },

            {
                input: '[[["1","2"],["3","4"]],[["5","6","7"],["8","9","0"]],[["1","2","3"],["4","5","6","7"],["8","9","0"]]]',
                output: '[\n    [\n        ["1", "2"]{{c2}}["3", "4"]\n    ]{{c1}}[\n        ["5", "6", "7"]{{c2}}["8", "9", "0"]\n    ]{{c1}}[\n        ["1", "2", "3"]{{c2}}["4", "5", "6", "7"]{{c2}}["8", "9", "0"]\n    ]\n]'
            },
            {
                input: [
                    'changeCollection.add({',
                    '    name: "Jonathan" // New line inserted after this line on every save',
                    '    , age: 25',
                    '});'
                ],
                output: [
                    'changeCollection.add({',
                    '    name: "Jonathan" // New line inserted after this line on every save',
                    '    {{f1}}age: 25',
                    '});'
                ]
            },
            {
                input: [
                    'changeCollection.add(',
                    '    function() {',
                    '        return true;',
                    '    },',
                    '    function() {',
                    '        return true;',
                    '    }',
                    ');'
                ],
                output: [
                    'changeCollection.add(',
                    '    function() {',
                    '        return true;',
                    '    }{{c1}}function() {',
                    '        return true;',
                    '    }',
                    ');'
                ]
            },
        ],
    }, {
        name: "Unindent chained functions",
        description: "Don't indent chained functions if unindent_chained_functions is true",
        matrix: [{
            options: [
                { name: "unindent_chained_methods", value: "true" }
            ]
        }],
        tests: [{
                input: [
                    'f().f().f()',
                    '    .f().f();',
                ],
                output: [
                    'f().f().f()',
                    '.f().f();'
                ]
            },
            {
                input: [
                    'f()',
                    '    .f()',
                    '    .f();'
                ],
                output: [
                    'f()',
                    '.f()',
                    '.f();'
                ]
            },
            {
                input: [
                    'f(function() {',
                    '    f()',
                    '        .f()',
                    '        .f();',
                    '});'
                ],
                output: [
                    'f(function() {',
                    '    f()',
                    '    .f()',
                    '    .f();',
                    '});'
                ]
            }
        ],
    }, {
        name: "Space in parens tests",
        description: "put space inside parens",
        matrix: [{
            options: [
                { name: "space_in_paren", value: "false" },
                { name: "space_in_empty_paren", value: "false" },
            ],
            s: '',
            e: '',
        }, {
            options: [
                { name: "space_in_paren", value: "false" },
                { name: "space_in_empty_paren", value: "true" },
            ],
            s: '',
            e: '',
        }, {
            options: [
                { name: "space_in_paren", value: "true" },
                { name: "space_in_empty_paren", value: "false" },
            ],
            s: ' ',
            e: '',
        }, {
            options: [
                { name: "space_in_paren", value: "true" },
                { name: "space_in_empty_paren", value: "true" },
            ],
            s: ' ',
            e: ' ',
        }],
        tests: [{
                input: 'if(p) foo(a,b);',
                output: 'if ({{s}}p{{s}}) foo({{s}}a, b{{s}});'
            },
            {
                input: 'try{while(true){willThrow()}}catch(result)switch(result){case 1:++result }',
                output: 'try {\n    while ({{s}}true{{s}}) {\n        willThrow({{e}})\n    }\n} catch ({{s}}result{{s}}) switch ({{s}}result{{s}}) {\n    case 1:\n        ++result\n}'
            },
            {
                input: '((e/((a+(b)*c)-d))^2)*5;',
                output: '({{s}}({{s}}e / ({{s}}({{s}}a + ({{s}}b{{s}}) * c{{s}}) - d{{s}}){{s}}) ^ 2{{s}}) * 5;'
            },
            {
                input: 'function f(a,b) {if(a) b()}function g(a,b) {if(!a) b()}',
                output: 'function f({{s}}a, b{{s}}) {\n    if ({{s}}a{{s}}) b({{e}})\n}\n\nfunction g({{s}}a, b{{s}}) {\n    if ({{s}}!a{{s}}) b({{e}})\n}'
            },
            {
                input: 'a=[];',
                output: 'a = [{{e}}];'
            },
            {
                input: 'a=[b,c,d];',
                output: 'a = [{{s}}b, c, d{{s}}];'
            },
            {
                input: 'a= f[b];',
                output: 'a = f[{{s}}b{{s}}];'
            },
            {
                input: [
                    '{',
                    '    files: [ {',
                    '        expand: true,',
                    '        cwd: "www/gui/",',
                    '        src: [ "im/design_standards/*.*" ],',
                    '        dest: "www/gui/build"',
                    '    } ]',
                    '}'
                ],
                output: [
                    '{',
                    '    files: [{{s}}{',
                    '        expand: true,',
                    '        cwd: "www/gui/",',
                    '        src: [{{s}}"im/design_standards/*.*"{{s}}],',
                    '        dest: "www/gui/build"',
                    '    }{{s}}]',
                    '}'
                ],
            },
        ],
    }, {
        name: "operator_position option - ensure no neswlines if preserve_newlines is false",
        matrix: [{
            options: [
                { name: "operator_position", value: "'before-newline'" },
                { name: "preserve_newlines", value: "false" }
            ]
        }, {
            options: [
                { name: "operator_position", value: "'after-newline'" },
                { name: "preserve_newlines", value: "false" }
            ]
        }, {
            options: [
                { name: "operator_position", value: "'preserve-newline'" },
                { name: "preserve_newlines", value: "false" }
            ]
        }],
        tests: [{
            unchanged: inputlib.operator_position.sanity
        }, {
            input: inputlib.operator_position.comprehensive,
            output: inputlib.operator_position.sanity,
        }]
    }, {
        name: "operator_position option - set to 'before-newline' (default value)",
        tests: [{
            comment: 'comprehensive, various newlines',
            input: inputlib.operator_position.comprehensive,
            output: [
                'var res = a + b -',
                '    c /',
                '    d * e %',
                '    f;',
                'var res = g & h |',
                '    i ^',
                '    j;',
                'var res = (k &&',
                '        l ||',
                '        m) ?',
                '    n :',
                '    o;',
                'var res = p >>',
                '    q <<',
                '    r >>>',
                '    s;',
                'var res = t',
                '',
                '    ===',
                '    u !== v !=',
                '    w ==',
                '    x >=',
                '    y <= z > aa <',
                '    ab;',
                'ac +',
                '    -ad'
            ]
        }, {
            comment: 'colon special case',
            input: inputlib.operator_position.colon_special_case,
            output: [
                'var a = {',
                '    b: bval,',
                '    c: cval,',
                '    d: dval',
                '};',
                'var e = f ? g :',
                '    h;',
                'var i = j ? k :',
                '    l;'
            ]
        }, {
            comment: 'catch-all, includes brackets and other various code',
            input: inputlib.operator_position.catch_all,
            output: [
                'var d = 1;',
                'if (a === b &&',
                '    c) {',
                '    d = (c * everything /',
                '            something_else) %',
                '        b;',
                '    e',
                '        += d;',
                '',
                '} else if (!(complex && simple) ||',
                '    (emotion && emotion.name === "happy")) {',
                '    cryTearsOfJoy(many ||',
                '        anOcean ||',
                '        aRiver);',
                '}'
            ]
        }]
    }, {
        name: "operator_position option - set to 'after_newline'",
        options: [{
            name: "operator_position",
            value: "'after-newline'"
        }],
        tests: [{
            comment: 'comprehensive, various newlines',
            input: inputlib.operator_position.comprehensive,
            output: [
                'var res = a + b',
                '    - c',
                '    / d * e',
                '    % f;',
                'var res = g & h',
                '    | i',
                '    ^ j;',
                'var res = (k',
                '        && l',
                '        || m)',
                '    ? n',
                '    : o;',
                'var res = p',
                '    >> q',
                '    << r',
                '    >>> s;',
                'var res = t',
                '',
                '    === u !== v',
                '    != w',
                '    == x',
                '    >= y <= z > aa',
                '    < ab;',
                'ac',
                '    + -ad'
            ]
        }, {
            comment: 'colon special case',
            input: inputlib.operator_position.colon_special_case,
            output: [
                'var a = {',
                '    b: bval,',
                '    c: cval,',
                '    d: dval',
                '};',
                'var e = f ? g',
                '    : h;',
                'var i = j ? k',
                '    : l;'
            ]
        }, {
            comment: 'catch-all, includes brackets and other various code',
            input: inputlib.operator_position.catch_all,
            output: [
                'var d = 1;',
                'if (a === b',
                '    && c) {',
                '    d = (c * everything',
                '            / something_else)',
                '        % b;',
                '    e',
                '        += d;',
                '',
                '} else if (!(complex && simple)',
                '    || (emotion && emotion.name === "happy")) {',
                '    cryTearsOfJoy(many',
                '        || anOcean',
                '        || aRiver);',
                '}'
            ]
        }]
    }, {
        name: "operator_position option - set to 'preserve-newline'",
        options: [{
            name: "operator_position",
            value: "'preserve-newline'"
        }],
        tests: [{
            comment: 'comprehensive, various newlines',
            input: inputlib.operator_position.comprehensive,
            output: [
                'var res = a + b',
                '    - c /',
                '    d * e',
                '    %',
                '    f;',
                'var res = g & h',
                '    | i ^',
                '    j;',
                'var res = (k &&',
                '        l',
                '        || m) ?',
                '    n',
                '    : o;',
                'var res = p',
                '    >> q <<',
                '    r',
                '    >>> s;',
                'var res = t',
                '',
                '    === u !== v',
                '    !=',
                '    w',
                '    == x >=',
                '    y <= z > aa <',
                '    ab;',
                'ac +',
                '    -ad'
            ]
        }, {
            comment: 'colon special case',
            input: inputlib.operator_position.colon_special_case,
            output: [
                'var a = {',
                '    b: bval,',
                '    c: cval,',
                '    d: dval',
                '};',
                'var e = f ? g',
                '    : h;',
                'var i = j ? k :',
                '    l;'
            ]
        }, {
            comment: 'catch-all, includes brackets and other various code',
            unchanged: inputlib.operator_position.catch_all
        }]
    }, {
        name: "Yield tests",
        description: "ES6 yield tests",
        tests: [
            { unchanged: 'yield /foo\\\\//;' },
            { unchanged: 'result = yield pgClient.query_(queryString);' },
            { unchanged: 'yield [1, 2]' },
            { unchanged: 'yield function() {};' },
            { unchanged: "yield* bar();" },
            {
                comment: "yield should have no space between yield and star",
                input: "yield * bar();",
                output: "yield* bar();"
            },
            {
                comment: "yield should have space between star and generator",
                input: "yield *bar();",
                output: "yield* bar();"
            }
        ]
    }, {
        name: "Async / await tests",
        description: "ES7 async / await tests",
        tests: [
            { unchanged: "async function foo() {}" },
            { unchanged: "let w = async function foo() {}" },
            { unchanged: "async function foo() {}\nvar x = await foo();" },
            {
                comment: "async function as an input to another function",
                unchanged: "wrapper(async function foo() {})"
            },
            {
                comment: "await on inline anonymous function. should have a space after await",
                input_: "async function() {\n    var w = await(async function() {\n        return await foo();\n    })();\n}",
                output: "async function() {\n    var w = await (async function() {\n        return await foo();\n    })();\n}"
            },
            {
                comment: "ensure that this doesn't break anyone with the async library",
                unchanged: "async.map(function(t) {})"
            },
            {
                comment: "async on arrow function. should have a space after async",
                input_: "async() => {}",
                output: "async () => {}"
            },
            {
                comment: "async on arrow function. should have a space after async",
                input_: "async() => {\n    return 5;\n}",
                output: "async () => {\n    return 5;\n}"
            },
            {
                comment: "async on arrow function returning expression. should have a space after async",
                input_: "async() => 5;",
                output: "async () => 5;"
            },
            {
                comment: "async on arrow function returning object literal. should have a space after async",
                input_: "async(x) => ({\n    foo: \"5\"\n})",
                output: "async (x) => ({\n    foo: \"5\"\n})"
            },
            {
                unchanged: "async (x) => {\n    return x * 2;\n}"
            },
            {
                unchanged: "async () => 5;"
            },
            {
                unchanged: "async x => x * 2;"
            }
        ]
    }, {
        name: "e4x - Test that e4x literals passed through when e4x-option is enabled",
        description: "",
        options: [
            { name: 'e4x', value: true }
        ],
        tests: [
            { input: 'xml=<a b="c"><d/><e>\n foo</e>x</a>;', output: 'xml = <a b="c"><d/><e>\n foo</e>x</a>;' },
            { unchanged: '<a b=\\\'This is a quoted "c".\\\'/>' },
            { unchanged: '<a b="This is a quoted \\\'c\\\'."/>' },
            { unchanged: '<a b="A quote \\\' inside string."/>' },
            { unchanged: '<a b=\\\'A quote " inside string.\\\'/>' },
            { unchanged: '<a b=\\\'Some """ quotes ""  inside string.\\\'/>' },

            {
                comment: 'Handles inline expressions',
                input: 'xml=<{a} b="c"><d/><e v={z}>\n foo</e>x</{a}>;',
                output: 'xml = <{a} b="c"><d/><e v={z}>\n foo</e>x</{a}>;'
            },
            {
                input: 'xml=<{a} b="c">\n    <e v={z}>\n foo</e>x</{a}>;',
                output: 'xml = <{a} b="c">\n    <e v={z}>\n foo</e>x</{a}>;'
            },
            {
                comment: 'xml literals with special characters in elem names - see http://www.w3.org/TR/REC-xml/#NT-NameChar',
                unchanged: 'xml = <_:.valid.xml- _:.valid.xml-="123"/>;'
            },
            {
                comment: 'xml literals with attributes without equal sign',
                unchanged: 'xml = <elem someAttr/>;'
            },

            {
                comment: 'Handles CDATA',
                input: 'xml=<![CDATA[ b="c"><d/><e v={z}>\n foo</e>x/]]>;',
                output: 'xml = <![CDATA[ b="c"><d/><e v={z}>\n foo</e>x/]]>;'
            },
            { input: 'xml=<![CDATA[]]>;', output: 'xml = <![CDATA[]]>;' },
            { input: 'xml=<a b="c"><![CDATA[d/></a></{}]]></a>;', output: 'xml = <a b="c"><![CDATA[d/></a></{}]]></a>;' },

            {
                comment: 'JSX - working jsx from http://prettydiff.com/unit_tests/beautification_javascript_jsx.txt',
                unchanged: [
                    'var ListItem = React.createClass({',
                    '    render: function() {',
                    '        return (',
                    '            <li className="ListItem">',
                    '                <a href={ "/items/" + this.props.item.id }>',
                    '                    this.props.item.name',
                    '                </a>',
                    '            </li>',
                    '        );',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'var List = React.createClass({',
                    '    renderList: function() {',
                    '        return this.props.items.map(function(item) {',
                    '            return <ListItem item={item} key={item.id} />;',
                    '        });',
                    '    },',
                    '',
                    '    render: function() {',
                    '        return <ul className="List">',
                    '                this.renderList()',
                    '            </ul>',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'var Mist = React.createClass({',
                    '    renderList: function() {',
                    '        return this.props.items.map(function(item) {',
                    '            return <ListItem item={return <tag>{item}</tag>} key={item.id} />;',
                    '        });',
                    '    }',
                    '});',
                ]
            },
            {
                unchanged: [
                    '// JSX',
                    'var box = <Box>',
                    '    {shouldShowAnswer(user) ?',
                    '        <Answer value={false}>no</Answer> : <Box.Comment>',
                    '        Text Content',
                    '        </Box.Comment>}',
                    '    </Box>;',
                    'var a = function() {',
                    '    return <tsdf>asdf</tsdf>;',
                    '};',
                    '',
                    'var HelloMessage = React.createClass({',
                    '    render: function() {',
                    '        return <div {someAttr}>Hello {this.props.name}</div>;',
                    '    }',
                    '});',
                    'React.render(<HelloMessage name="John" />, mountNode);',
                ]
            },
            {
                unchanged: [
                    'var Timer = React.createClass({',
                    '    getInitialState: function() {',
                    '        return {',
                    '            secondsElapsed: 0',
                    '        };',
                    '    },',
                    '    tick: function() {',
                    '        this.setState({',
                    '            secondsElapsed: this.state.secondsElapsed + 1',
                    '        });',
                    '    },',
                    '    componentDidMount: function() {',
                    '        this.interval = setInterval(this.tick, 1000);',
                    '    },',
                    '    componentWillUnmount: function() {',
                    '        clearInterval(this.interval);',
                    '    },',
                    '    render: function() {',
                    '        return (',
                    '            <div>Seconds Elapsed: {this.state.secondsElapsed}</div>',
                    '        );',
                    '    }',
                    '});',
                    'React.render(<Timer />, mountNode);'
                ]
            },
            {
                unchanged: [
                    'var TodoList = React.createClass({',
                    '    render: function() {',
                    '        var createItem = function(itemText) {',
                    '            return <li>{itemText}</li>;',
                    '        };',
                    '        return <ul>{this.props.items.map(createItem)}</ul>;',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'var TodoApp = React.createClass({',
                    '    getInitialState: function() {',
                    '        return {',
                    '            items: [],',
                    '            text: \\\'\\\'',
                    '        };',
                    '    },',
                    '    onChange: function(e) {',
                    '        this.setState({',
                    '            text: e.target.value',
                    '        });',
                    '    },',
                    '    handleSubmit: function(e) {',
                    '        e.preventDefault();',
                    '        var nextItems = this.state.items.concat([this.state.text]);',
                    '        var nextText = \\\'\\\';',
                    '        this.setState({',
                    '            items: nextItems,',
                    '            text: nextText',
                    '        });',
                    '    },',
                    '    render: function() {',
                    '        return (',
                    '            <div>',
                    '                <h3 {someAttr}>TODO</h3>',
                    '                <TodoList items={this.state.items} />',
                    '                <form onSubmit={this.handleSubmit}>',
                    '                    <input onChange={this.onChange} value={this.state.text} />',
                    '                    <button>{\\\'Add #\\\' + (this.state.items.length + 1)}</button>',
                    '                </form>',
                    '            </div>',
                    '        );',
                    '    }',
                    '});',
                    'React.render(<TodoApp />, mountNode);'
                ]
            },
            {
                input: [
                    'var converter = new Showdown.converter();',
                    'var MarkdownEditor = React.createClass({',
                    '    getInitialState: function() {',
                    '        return {value: \\\'Type some *markdown* here!\\\'};',
                    '    },',
                    '    handleChange: function() {',
                    '        this.setState({value: this.refs.textarea.getDOMNode().value});',
                    '    },',
                    '    render: function() {',
                    '        return (',
                    '            <div className="MarkdownEditor">',
                    '                <h3>Input</h3>',
                    '                <textarea',
                    '                    onChange={this.handleChange}',
                    '                    ref="textarea"',
                    '                    defaultValue={this.state.value} />',
                    '                <h3>Output</h3>',
                    '            <div',
                    '                className="content"',
                    '                dangerouslySetInnerHTML={{',
                    '                        __html: converter.makeHtml(this.state.value)',
                    '                    }}',
                    '                />',
                    '            </div>',
                    '        );',
                    '    }',
                    '});',
                    'React.render(<MarkdownEditor />, mountNode);'

                ],
                output: [
                    'var converter = new Showdown.converter();',
                    'var MarkdownEditor = React.createClass({',
                    '    getInitialState: function() {',
                    '        return {',
                    '            value: \\\'Type some *markdown* here!\\\'',
                    '        };',
                    '    },',
                    '    handleChange: function() {',
                    '        this.setState({',
                    '            value: this.refs.textarea.getDOMNode().value',
                    '        });',
                    '    },',
                    '    render: function() {',
                    '        return (',
                    '            <div className="MarkdownEditor">',
                    '                <h3>Input</h3>',
                    '                <textarea',
                    '                    onChange={this.handleChange}',
                    '                    ref="textarea"',
                    '                    defaultValue={this.state.value} />',
                    '                <h3>Output</h3>',
                    '            <div',
                    '                className="content"',
                    '                dangerouslySetInnerHTML={{',
                    '                        __html: converter.makeHtml(this.state.value)',
                    '                    }}',
                    '                />',
                    '            </div>',
                    '        );',
                    '    }',
                    '});',
                    'React.render(<MarkdownEditor />, mountNode);'
                ]
            },
            {
                comment: 'JSX - Not quite correct jsx formatting that still works',
                input: [
                    'var content = (',
                    '        <Nav>',
                    '            {/* child comment, put {} around */}',
                    '            <Person',
                    '                /* multi',
                    '         line',
                    '         comment */',
                    '         //attr="test"',
                    '                name={window.isLoggedIn ? window.name : \\\'\\\'} // end of line comment',
                    '            />',
                    '        </Nav>',
                    '    );',
                    'var qwer = <DropDown> A dropdown list <Menu> <MenuItem>Do Something</MenuItem> <MenuItem>Do Something Fun!</MenuItem> <MenuItem>Do Something Else</MenuItem> </Menu> </DropDown>;',
                    'render(dropdown);',
                ],
                output: [
                    'var content = (',
                    '    <Nav>',
                    '            {/* child comment, put {} around */}',
                    '            <Person',
                    '                /* multi',
                    '         line',
                    '         comment */',
                    '         //attr="test"',
                    '                name={window.isLoggedIn ? window.name : \\\'\\\'} // end of line comment',
                    '            />',
                    '        </Nav>',
                    ');',
                    'var qwer = <DropDown> A dropdown list <Menu> <MenuItem>Do Something</MenuItem> <MenuItem>Do Something Fun!</MenuItem> <MenuItem>Do Something Else</MenuItem> </Menu> </DropDown>;',
                    'render(dropdown);',
                ]
            },
            {
                comment: [
                    "Handles messed up tags, as long as it isn't the same name",
                    "as the root tag. Also handles tags of same name as root tag",
                    "as long as nesting matches."
                ],
                input_: 'xml=<a x="jn"><c></b></f><a><d jnj="jnn"><f></a ></nj></a>;',
                output: 'xml = <a x="jn"><c></b></f><a><d jnj="jnn"><f></a ></nj></a>;'
            },

            {
                comment: [
                    "If xml is not terminated, the remainder of the file is treated",
                    "as part of the xml-literal (passed through unaltered)"
                ],
                fragment: true,
                input_: 'xml=<a></b>\nc<b;',
                output: 'xml = <a></b>\nc<b;'
            },
            {
                comment: 'Issue #646 = whitespace is allowed in attribute declarations',
                unchanged: [
                    'let a = React.createClass({',
                    '    render() {',
                    '        return (',
                    '            <p className=\\\'a\\\'>',
                    '                <span>c</span>',
                    '            </p>',
                    '        );',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'let a = React.createClass({',
                    '    render() {',
                    '        return (',
                    '            <p className = \\\'b\\\'>',
                    '                <span>c</span>',
                    '            </p>',
                    '        );',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'let a = React.createClass({',
                    '    render() {',
                    '        return (',
                    '            <p className = "c">',
                    '                <span>c</span>',
                    '            </p>',
                    '        );',
                    '    }',
                    '});'
                ]
            },
            {
                unchanged: [
                    'let a = React.createClass({',
                    '    render() {',
                    '        return (',
                    '            <{e}  className = {d}>',
                    '                <span>c</span>',
                    '            </{e}>',
                    '        );',
                    '    }',
                    '});'
                ]
            },
            {
                comment: 'Issue #914 - Multiline attribute in root tag',
                unchanged: [
                    'return (',
                    '    <a href="#"',
                    '        onClick={e => {',
                    '            e.preventDefault()',
                    '            onClick()',
                    '       }}>',
                    '       {children}',
                    '    </a>',
                    ');'
                ]
            },
            {
                unchanged: [
                    'return (',
                    '    <{',
                    '        a + b',
                    '    } href="#"',
                    '        onClick={e => {',
                    '            e.preventDefault()',
                    '            onClick()',
                    '       }}>',
                    '       {children}',
                    '    </{',
                    '        a + b',
                    '    }>',
                    ');'
                ]
            },
            {
                input: [
                    'return (',
                    '    <{',
                    '        a + b',
                    '    } href="#"',
                    '        onClick={e => {',
                    '            e.preventDefault()',
                    '            onClick()',
                    '       }}>',
                    '       {children}',
                    '    </{a + b}>',
                    '    );'
                ],
                output: [
                    'return (',
                    '    <{',
                    '        a + b',
                    '    } href="#"',
                    '        onClick={e => {',
                    '            e.preventDefault()',
                    '            onClick()',
                    '       }}>',
                    '       {children}',
                    '    </{a + b}>',
                    ');'
                ]
            }
        ]
    }, {
        name: "e4x disabled",
        description: "",
        options: [
            { name: 'e4x', value: false }
        ],
        tests: [{
            input_: 'xml=<a b="c"><d/><e>\n foo</e>x</a>;',
            output: 'xml = < a b = "c" > < d / > < e >\n    foo < /e>x</a > ;'
        }]
    }, {
        name: "Multiple braces",
        description: "",
        template: "^^^ $$$",
        options: [],
        tests: [
            { input: '{{}/z/}', output: '{\n    {}\n    /z/\n}' }
        ]
    }, {
        name: "Beautify preserve formatting",
        description: "Allow beautifier to preserve sections",
        tests: [
            { unchanged: "/* beautify preserve:start */\n/* beautify preserve:end */" },
            { unchanged: "/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */" },
            { unchanged: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */" },
            { unchanged: "/* beautify preserve:start */     {asdklgh;y;;{}dd2d}/* beautify preserve:end */" },
            {
                input_: "var a =  1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */",
                output: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */"
            },
            {
                input_: "var a = 1;\n /* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */",
                output: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */"
            },
            {
                unchanged: [
                    'var a = {',
                    '    /* beautify preserve:start */',
                    '    one   :  1',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '    /* beautify preserve:end */',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/* beautify preserve:start */',
                    '    one   :  1,',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '/* beautify preserve:end */',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify preserve:start */',
                    '    one   :  1,',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '/* beautify preserve:end */',
                    '};'
                ]
            },
            {
                comment: 'one space before and after required, only single spaces inside.',
                input: [
                    'var a = {',
                    '/*  beautify preserve:start  */',
                    '    one   :  1,',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /*  beautify preserve:start  */',
                    '    one: 1,',
                    '    two: 2,',
                    '    three: 3,',
                    '    ten: 10',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/*beautify preserve:start*/',
                    '    one   :  1,',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /*beautify preserve:start*/',
                    '    one: 1,',
                    '    two: 2,',
                    '    three: 3,',
                    '    ten: 10',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/*beautify  preserve:start*/',
                    '    one   :  1,',
                    '    two   :  2,',
                    '    three :  3,',
                    '    ten   : 10',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /*beautify  preserve:start*/',
                    '    one: 1,',
                    '    two: 2,',
                    '    three: 3,',
                    '    ten: 10',
                    '};'
                ]
            },

            {
                comment: 'Directive: ignore',
                unchanged: "/* beautify ignore:start */\n/* beautify ignore:end */"
            },
            { unchanged: "/* beautify ignore:start */\n   var a,,,{ 1;\n/* beautify ignore:end */" },
            { unchanged: "var a = 1;\n/* beautify ignore:start */\n   var a = 1;\n/* beautify ignore:end */" },
            { unchanged: "/* beautify ignore:start */     {asdklgh;y;+++;dd2d}/* beautify ignore:end */" },
            {
                input_: "var a =  1;\n/* beautify ignore:start */\n   var a,,,{ 1;\n/* beautify ignore:end */",
                output: "var a = 1;\n/* beautify ignore:start */\n   var a,,,{ 1;\n/* beautify ignore:end */"
            },
            {
                input_: "var a = 1;\n /* beautify ignore:start */\n   var a,,,{ 1;\n/* beautify ignore:end */",
                output: "var a = 1;\n/* beautify ignore:start */\n   var a,,,{ 1;\n/* beautify ignore:end */"
            },
            {
                unchanged: [
                    'var a = {',
                    '    /* beautify ignore:start */',
                    '    one   :  1',
                    '    two   :  2,',
                    '    three :  {',
                    '    ten   : 10',
                    '    /* beautify ignore:end */',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/* beautify ignore:start */',
                    '    one   :  1',
                    '    two   :  2,',
                    '    three :  {',
                    '    ten   : 10',
                    '/* beautify ignore:end */',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify ignore:start */',
                    '    one   :  1',
                    '    two   :  2,',
                    '    three :  {',
                    '    ten   : 10',
                    '/* beautify ignore:end */',
                    '};'
                ]
            },
            {
                comment: 'Directives - multiple and interacting',
                input: [
                    'var a = {',
                    '/* beautify preserve:start */',
                    '/* beautify preserve:start */',
                    '    one   :  1,',
                    '  /* beautify preserve:end */',
                    '    two   :  2,',
                    '    three :  3,',
                    '/* beautify preserve:start */',
                    '    ten   : 10',
                    '/* beautify preserve:end */',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify preserve:start */',
                    '/* beautify preserve:start */',
                    '    one   :  1,',
                    '  /* beautify preserve:end */',
                    '    two: 2,',
                    '    three: 3,',
                    '    /* beautify preserve:start */',
                    '    ten   : 10',
                    '/* beautify preserve:end */',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/* beautify ignore:start */',
                    '    one   :  1',
                    ' /* beautify ignore:end */',
                    '    two   :  2,',
                    '/* beautify ignore:start */',
                    '    three :  {',
                    '    ten   : 10',
                    '/* beautify ignore:end */',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify ignore:start */',
                    '    one   :  1',
                    ' /* beautify ignore:end */',
                    '    two: 2,',
                    '    /* beautify ignore:start */',
                    '    three :  {',
                    '    ten   : 10',
                    '/* beautify ignore:end */',
                    '};'
                ]
            },
            {
                comment: 'Starts can occur together, ignore:end must occur alone.',
                input: [
                    'var a = {',
                    '/* beautify ignore:start */',
                    '    one   :  1',
                    '    NOTE: ignore end block does not support starting other directives',
                    '    This does not match the ending the ignore...',
                    ' /* beautify ignore:end preserve:start */',
                    '    two   :  2,',
                    '/* beautify ignore:start */',
                    '    three :  {',
                    '    ten   : 10',
                    '    ==The next comment ends the starting ignore==',
                    '/* beautify ignore:end */',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify ignore:start */',
                    '    one   :  1',
                    '    NOTE: ignore end block does not support starting other directives',
                    '    This does not match the ending the ignore...',
                    ' /* beautify ignore:end preserve:start */',
                    '    two   :  2,',
                    '/* beautify ignore:start */',
                    '    three :  {',
                    '    ten   : 10',
                    '    ==The next comment ends the starting ignore==',
                    '/* beautify ignore:end */',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/* beautify ignore:start preserve:start */',
                    '    one   :  {',
                    ' /* beautify ignore:end */',
                    '    two   :  2,',
                    '  /* beautify ignore:start */',
                    '    three :  {',
                    '/* beautify ignore:end */',
                    '    ten   : 10',
                    '   // This is all preserved',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify ignore:start preserve:start */',
                    '    one   :  {',
                    ' /* beautify ignore:end */',
                    '    two   :  2,',
                    '  /* beautify ignore:start */',
                    '    three :  {',
                    '/* beautify ignore:end */',
                    '    ten   : 10',
                    '   // This is all preserved',
                    '};'
                ]
            },
            {
                input: [
                    'var a = {',
                    '/* beautify ignore:start preserve:start */',
                    '    one   :  {',
                    ' /* beautify ignore:end */',
                    '    two   :  2,',
                    '  /* beautify ignore:start */',
                    '    three :  {',
                    '/* beautify ignore:end */',
                    '    ten   : 10,',
                    '/* beautify preserve:end */',
                    '     eleven: 11',
                    '};'
                ],
                output: [
                    'var a = {',
                    '    /* beautify ignore:start preserve:start */',
                    '    one   :  {',
                    ' /* beautify ignore:end */',
                    '    two   :  2,',
                    '  /* beautify ignore:start */',
                    '    three :  {',
                    '/* beautify ignore:end */',
                    '    ten   : 10,',
                    '/* beautify preserve:end */',
                    '    eleven: 11',
                    '};'
                ]
            },
        ]
    }, {
        name: "Comments and  tests",
        description: "Comments should be in the right indent and not side-ffect.",
        options: [],
        tests: [{
                comment: '#913',

                unchanged: [
                    'class test {',
                    '    method1() {',
                    '        let resp = null;',
                    '    }',
                    '    /**',
                    '     * @param {String} id',
                    '     */',
                    '    method2(id) {',
                    '        let resp2 = null;',
                    '    }',
                    '}'
                ]
            },
            {
                comment: '#1090',
                unchanged: [
                    'for (var i = 0; i < 20; ++i) // loop',
                    '    if (i % 3) {',
                    '        console.log(i);',
                    '    }',
                    'console.log("done");',
                ]
            },
            {
                comment: '#1043',
                unchanged: [
                    'var o = {',
                    '    k: 0',
                    '}',
                    '// ...',
                    'foo(o)',
                ]
            },
            {
                comment: '#713 and #964',
                unchanged: [
                    'Meteor.call("foo", bar, function(err, result) {',
                    '    Session.set("baz", result.lorem)',
                    '})',
                    '//blah blah',
                ]
            },
            {
                comment: '#815',
                unchanged: [
                    'foo()',
                    '// this is a comment',
                    'bar()',
                    '',
                    'const foo = 5',
                    '// comment',
                    'bar()',
                ]
            },
            {
                comment: 'This shows current behavior.  Note #1069 is not addressed yet.',
                unchanged: [
                    'if (modulus === 2) {',
                    '    // i might be odd here',
                    '    i += (i & 1);',
                    '    // now i is guaranteed to be even',
                    '    // this block is obviously about the statement above',
                    '',
                    '    // #1069 This should attach to the block below',
                    '    // this comment is about the block after it.',
                    '} else {',
                    '    // rounding up using integer arithmetic only',
                    '    if (i % modulus)',
                    '        i += modulus - (i % modulus);',
                    '    // now i is divisible by modulus',
                    '    // behavior of comments should be different for single statements vs block statements/expressions',
                    '}',
                    '',
                    'if (modulus === 2)',
                    '    // i might be odd here',
                    '    i += (i & 1);',
                    '// now i is guaranteed to be even',
                    '// non-braced comments unindent immediately',
                    '',
                    '// this comment is about the block after it.',
                    'else',
                    '    // rounding up using integer arithmetic only',
                    '    if (i % modulus)',
                    '        i += modulus - (i % modulus);',
                    '// behavior of comments should be different for single statements vs block statements/expressions',
                ]
            },

        ]
    }, {
        name: "Template Formatting",
        description: "Php (<?php ... ?>) and underscore.js templating treated as strings.",
        options: [],
        tests: [
            { unchanged: '<?=$view["name"]; ?>' },
            { unchanged: 'a = <?= external() ?>;' },
            {
                unchanged: [
                    '<?php',
                    'for($i = 1; $i <= 100; $i++;) {',
                    '    #count to 100!',
                    '    echo($i . "</br>");',
                    '}',
                    '?>'
                ]
            },
            { unchanged: 'a = <%= external() %>;' }
        ]
    }, {
        name: "jslint and space after anon function",
        description: "jslint_happy and space_after_anon_function tests",
        matrix: [{
                options: [
                    { name: "jslint_happy", value: "true" },
                    { name: "space_after_anon_function", value: "true" }
                ],
                f: ' ',
                c: ''
            }, {
                options: [
                    { name: "jslint_happy", value: "true" },
                    { name: "space_after_anon_function", value: "false" }
                ],
                f: ' ',
                c: ''
            }, {
                options: [
                    { name: "jslint_happy", value: "false" },
                    { name: "space_after_anon_function", value: "true" }
                ],
                f: ' ',
                c: '    '
            }, {
                options: [
                    { name: "jslint_happy", value: "false" },
                    { name: "space_after_anon_function", value: "false" }
                ],
                f: '',
                c: '    '
            }


        ],
        tests: [{
                input_: 'a=typeof(x)',
                output: 'a = typeof{{f}}(x)'
            },
            {
                input_: 'x();\n\nfunction(){}',
                output: 'x();\n\nfunction{{f}}() {}'
            },
            {
                input_: 'x();\n\nvar x = {\nx: function(){}\n}',
                output: 'x();\n\nvar x = {\n    x: function{{f}}() {}\n}'
            },
            {
                input_: 'function () {\n    var a, b, c, d, e = [],\n        f;\n}',
                output: 'function{{f}}() {\n    var a, b, c, d, e = [],\n        f;\n}'
            },

            {
                input_: 'switch(x) {case 0: case 1: a(); break; default: break}',
                output: 'switch (x) {\n{{c}}case 0:\n{{c}}case 1:\n{{c}}    a();\n{{c}}    break;\n{{c}}default:\n{{c}}    break\n}'
            },
            {
                input: 'switch(x){case -1:break;case !y:break;}',
                output: 'switch (x) {\n{{c}}case -1:\n{{c}}    break;\n{{c}}case !y:\n{{c}}    break;\n}'
            },
            {
                comment: 'typical greasemonkey start',
                fragment: true,
                unchanged: '// comment 2\n(function{{f}}()'
            },

            {
                input_: 'var a2, b2, c2, d2 = 0, c = function() {}, d = \\\'\\\';',
                output: 'var a2, b2, c2, d2 = 0,\n    c = function{{f}}() {},\n    d = \\\'\\\';'
            },
            {
                input_: 'var a2, b2, c2, d2 = 0, c = function() {},\nd = \\\'\\\';',
                output: 'var a2, b2, c2, d2 = 0,\n    c = function{{f}}() {},\n    d = \\\'\\\';'
            },
            {
                input_: 'var o2=$.extend(a);function(){alert(x);}',
                output: 'var o2 = $.extend(a);\n\nfunction{{f}}() {\n    alert(x);\n}'
            },
            { input: 'function*() {\n    yield 1;\n}', output: 'function*{{f}}() {\n    yield 1;\n}' },
            { unchanged: 'function* x() {\n    yield 1;\n}' },
        ]
    }, {
        name: "Regression tests",
        description: "Ensure specific bugs do not recur",
        options: [],
        tests: [{
                comment: "Issue 241",
                unchanged: [
                    'obj',
                    '    .last({',
                    '        foo: 1,',
                    '        bar: 2',
                    '    });',
                    'var test = 1;'
                ]
            },
            {
                unchanged: [
                    'obj',
                    '    .last(a, function() {',
                    '        var test;',
                    '    });',
                    'var test = 1;'
                ]
            },
            {
                unchanged: [
                    'obj.first()',
                    '    .second()',
                    '    .last(function(err, response) {',
                    '        console.log(err);',
                    '    });'
                ]
            },
            {
                comment: "Issue 268 and 275",
                unchanged: [
                    'obj.last(a, function() {',
                    '    var test;',
                    '});',
                    'var test = 1;'
                ]
            },
            {
                unchanged: [
                    'obj.last(a,',
                    '    function() {',
                    '        var test;',
                    '    });',
                    'var test = 1;'
                ]
            },
            {
                input: '(function() {if (!window.FOO) window.FOO || (window.FOO = function() {var b = {bar: "zort"};});})();',
                output: [
                    '(function() {',
                    '    if (!window.FOO) window.FOO || (window.FOO = function() {',
                    '        var b = {',
                    '            bar: "zort"',
                    '        };',
                    '    });',
                    '})();'
                ]
            },
            {
                comment: "Issue 281",
                unchanged: [
                    'define(["dojo/_base/declare", "my/Employee", "dijit/form/Button",',
                    '    "dojo/_base/lang", "dojo/Deferred"',
                    '], function(declare, Employee, Button, lang, Deferred) {',
                    '    return declare(Employee, {',
                    '        constructor: function() {',
                    '            new Button({',
                    '                onClick: lang.hitch(this, function() {',
                    '                    new Deferred().then(lang.hitch(this, function() {',
                    '                        this.salary * 0.25;',
                    '                    }));',
                    '                })',
                    '            });',
                    '        }',
                    '    });',
                    '});'
                ]
            },
            {
                unchanged: [
                    'define(["dojo/_base/declare", "my/Employee", "dijit/form/Button",',
                    '        "dojo/_base/lang", "dojo/Deferred"',
                    '    ],',
                    '    function(declare, Employee, Button, lang, Deferred) {',
                    '        return declare(Employee, {',
                    '            constructor: function() {',
                    '                new Button({',
                    '                    onClick: lang.hitch(this, function() {',
                    '                        new Deferred().then(lang.hitch(this, function() {',
                    '                            this.salary * 0.25;',
                    '                        }));',
                    '                    })',
                    '                });',
                    '            }',
                    '        });',
                    '    });'
                ]
            },
            {
                comment: "Issue 459",
                unchanged: [
                    '(function() {',
                    '    return {',
                    '        foo: function() {',
                    '            return "bar";',
                    '        },',
                    '        bar: ["bar"]',
                    '    };',
                    '}());'
                ]
            },
            {
                comment: "Issue 505 - strings should end at newline unless continued by backslash",
                unchanged: [
                    'var name = "a;',
                    'name = "b";'
                ]
            },
            {
                unchanged: [
                    'var name = "a;\\\\',
                    '    name = b";'
                ]
            },
            {
                comment: "Issue 514 - some operators require spaces to distinguish them",
                unchanged: 'var c = "_ACTION_TO_NATIVEAPI_" + ++g++ + +new Date;'
            },
            {
                unchanged: 'var c = "_ACTION_TO_NATIVEAPI_" - --g-- - -new Date;'
            },
            {
                comment: "Issue 440 - reserved words can be used as object property names",
                unchanged: [
                    'a = {',
                    '    function: {},',
                    '    "function": {},',
                    '    throw: {},',
                    '    "throw": {},',
                    '    var: {},',
                    '    "var": {},',
                    '    set: {},',
                    '    "set": {},',
                    '    get: {},',
                    '    "get": {},',
                    '    if: {},',
                    '    "if": {},',
                    '    then: {},',
                    '    "then": {},',
                    '    else: {},',
                    '    "else": {},',
                    '    yay: {}',
                    '};'
                ]
            },
            {
                comment: "Issue 331 - if-else with braces edge case",
                input: 'if(x){a();}else{b();}if(y){c();}',
                output: [
                    'if (x) {',
                    '    a();',
                    '} else {',
                    '    b();',
                    '}',
                    'if (y) {',
                    '    c();',
                    '}'
                ]
            },
            {
                comment: "Issue 485 - ensure function declarations behave the same in arrays as elsewhere",
                unchanged: [
                    'var v = ["a",',
                    '    function() {',
                    '        return;',
                    '    }, {',
                    '        id: 1',
                    '    }',
                    '];'
                ]
            },
            {
                unchanged: [
                    'var v = ["a", function() {',
                    '    return;',
                    '}, {',
                    '    id: 1',
                    '}];'
                ]
            },
            {
                comment: "Issue 382 - initial totally cursory support for es6 module export",
                unchanged: [
                    'module "Even" {',
                    '    import odd from "Odd";',
                    '    export function sum(x, y) {',
                    '        return x + y;',
                    '    }',
                    '    export var pi = 3.141593;',
                    '    export default moduleName;',
                    '}'
                ]
            },
            {
                unchanged: [
                    'module "Even" {',
                    '    export default function div(x, y) {}',
                    '}'
                ]
            },
            {
                comment: 'Issue 889 - export default { ... }',
                unchanged: [
                    'export default {',
                    '    func1() {},',
                    '    func2() {}',
                    '    func3() {}',
                    '}'
                ]
            },
            {
                unchanged: [
                    'export default {',
                    '    a() {',
                    '        return 1;',
                    '    },',
                    '    b() {',
                    '        return 2;',
                    '    },',
                    '    c() {',
                    '        return 3;',
                    '    }',
                    '}'
                ]
            },
            {
                comment: "Issue 508",
                unchanged: 'set["name"]'
            },
            {
                unchanged: 'get["name"]'
            },
            {
                fragmeent: true,
                unchanged: [
                    'a = {',
                    '    set b(x) {},',
                    '    c: 1,',
                    '    d: function() {}',
                    '};'
                ]
            },
            {
                fragmeent: true,
                unchanged: [
                    'a = {',
                    '    get b() {',
                    '        retun 0;',
                    '    },',
                    '    c: 1,',
                    '    d: function() {}',
                    '};'
                ]
            },
            {
                comment: "Issue 298 - do not under indent if/while/for condtionals experesions",
                unchanged: [
                    '\\\'use strict\\\';',
                    'if ([].some(function() {',
                    '        return false;',
                    '    })) {',
                    '    console.log("hello");',
                    '}'
                ]
            },
            {
                comment: "Issue 298 - do not under indent if/while/for condtionals experesions",
                unchanged: [
                    '\\\'use strict\\\';',
                    'if ([].some(function() {',
                    '        return false;',
                    '    })) {',
                    '    console.log("hello");',
                    '}'
                ]
            },
            {
                comment: "Issue 552 - Typescript?  Okay... we didn't break it before, so try not to break it now.",
                unchanged: [
                    'class Test {',
                    '    blah: string[];',
                    '    foo(): number {',
                    '        return 0;',
                    '    }',
                    '    bar(): number {',
                    '        return 0;',
                    '    }',
                    '}'
                ]
            },
            {
                unchanged: [
                    'interface Test {',
                    '    blah: string[];',
                    '    foo(): number {',
                    '        return 0;',
                    '    }',
                    '    bar(): number {',
                    '        return 0;',
                    '    }',
                    '}'
                ]
            },
            {
                comment: "Issue 583 - Functions with comments after them should still indent correctly.",
                unchanged: [
                    'function exit(code) {',
                    '    setTimeout(function() {',
                    '        phantom.exit(code);',
                    '    }, 0);',
                    '    phantom.onError = function() {};',
                    '}',
                    '// Comment'
                ]
            },
            {
                comment: "Issue 806 - newline arrow functions",
                unchanged: [
                    'a.b("c",',
                    '    () => d.e',
                    ')'
                ]
            },
            {
                comment: "Issue 810 - es6 object literal detection",
                unchanged: [
                    'function badFormatting() {',
                    '    return {',
                    '        a,',
                    '        b: c,',
                    '        d: e,',
                    '        f: g,',
                    '        h,',
                    '        i,',
                    '        j: k',
                    '    }',
                    '}',
                    '',
                    'function goodFormatting() {',
                    '    return {',
                    '        a: b,',
                    '        c,',
                    '        d: e,',
                    '        f: g,',
                    '        h,',
                    '        i,',
                    '        j: k',
                    '    }',
                    '}'
                ]
            },
            {
                comment: "Issue 602 - ES6 object literal shorthand functions",
                unchanged: [
                    'return {',
                    '    fn1() {},',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'throw {',
                    '    fn1() {},',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'foo({',
                    '    fn1(a) {}',
                    '    fn2(a) {}',
                    '})'
                ]
            }, {
                unchanged: [
                    'foo("text", {',
                    '    fn1(a) {}',
                    '    fn2(a) {}',
                    '})'
                ]
            }, {
                unchanged: [
                    'oneArg = {',
                    '    fn1(a) {',
                    '        do();',
                    '    },',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'multiArg = {',
                    '    fn1(a, b, c) {',
                    '        do();',
                    '    },',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'noArgs = {',
                    '    fn1() {',
                    '        do();',
                    '    },',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'emptyFn = {',
                    '    fn1() {},',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'nested = {',
                    '    fns: {',
                    '        fn1() {},',
                    '        fn2() {}',
                    '    }',
                    '}'
                ]
            }, {
                unchanged: [
                    'array = [{',
                    '    fn1() {},',
                    '    prop: val,',
                    '    fn2() {}',
                    '}]'
                ]
            }, {
                unchanged: [
                    'expr = expr ? expr : {',
                    '    fn1() {},',
                    '    fn2() {}',
                    '}'
                ]
            }, {
                unchanged: [
                    'strange = valid + {',
                    '    fn1() {},',
                    '    fn2() {',
                    '        return 1;',
                    '    }',
                    '}.fn2()'
                ]
            },
            {
                comment: "Issue 854 - Arrow function with statement block",
                unchanged: [
                    'test(() => {',
                    '    var a = {}',
                    '',
                    '    a.what = () => true ? 1 : 2',
                    '',
                    '    a.thing = () => {',
                    '        b();',
                    '    }',
                    '})'
                ]
            },
            {
                comment: "Issue 406 - Multiline array",
                unchanged: [
                    'var tempName = [',
                    '    "temp",',
                    '    process.pid,',
                    '    (Math.random() * 0x1000000000).toString(36),',
                    '    new Date().getTime()',
                    '].join("-");'
                ]
            },
            {
                comment: "Issue #996 - Input ends with backslash throws exception",
                fragment: true,
                unchanged: [
                    'sd = 1;',
                    '/'
                ]
            },
            {
                comment: "Issue #1079 - unbraced if with comments should still look right",
                unchanged: [
                    'if (console.log)',
                    '    for (var i = 0; i < 20; ++i)',
                    '        if (i % 3)',
                    '            console.log(i);',
                    '// all done',
                    'console.log("done");'
                ]
            },
            {
                comment: "Issue #1085 - function should not have blank line in a number of cases",
                unchanged: [
                    'var transformer =',
                    '    options.transformer ||',
                    '    globalSettings.transformer ||',
                    '    function(x) {',
                    '        return x;',
                    '    };'
                ]
            },
            {
                comment: "Issue #569 - function should not have blank line in a number of cases",
                unchanged: [
                    '(function(global) {',
                    '    "use strict";',
                    '',
                    '    /* jshint ignore:start */',
                    '    include "somefile.js"',
                    '    /* jshint ignore:end */',
                    '}(this));'
                ]
            },
            {
                unchanged: [
                    'function bindAuthEvent(eventName) {',
                    '    self.auth.on(eventName, function(event, meta) {',
                    '        self.emit(eventName, event, meta);',
                    '    });',
                    '}',
                    '["logged_in", "logged_out", "signed_up", "updated_user"].forEach(bindAuthEvent);',
                    '',
                    'function bindBrowserEvent(eventName) {',
                    '    browser.on(eventName, function(event, meta) {',
                    '        self.emit(eventName, event, meta);',
                    '    });',
                    '}',
                    '["navigating"].forEach(bindBrowserEvent);'
                ]
            },
            {
                comment: "Issue #892 - new line between chained methods ",
                unchanged: [
                    'foo',
                    '    .who()',
                    '',
                    '    .knows()',
                    '    // comment',
                    '    .nothing() // comment',
                    '',
                    '    .more()'
                ]
            }
        ]
    }, {
        name: "Test non-positionable-ops",
        description: "Ensure specific bugs do not recur",
        tests: [
            { unchanged: 'a += 2;' },
            { unchanged: 'a -= 2;' },
            { unchanged: 'a *= 2;' },
            { unchanged: 'a /= 2;' },
            { unchanged: 'a %= 2;' },
            { unchanged: 'a &= 2;' },
            { unchanged: 'a ^= 2;' },
            { unchanged: 'a |= 2;' },
            { unchanged: 'a **= 2;' },
            { unchanged: 'a <<= 2;' },
            { unchanged: 'a >>= 2;' },
        ]
    }, {
        //Relies on the tab being four spaces as default for the tests
        name: "brace_style ,preserve-inline tests",
        description: "brace_style *,preserve-inline varying different brace_styles",
        template: "< >",
        matrix: [
            //test for all options of brace_style
            {
                options: [
                    { name: "brace_style", value: "'collapse,preserve-inline'" }
                ],
                obo: ' ',
                obot: '', //Output Before Open curlybrace & Tab character
                oao: '\n',
                oaot: '    ', //Output After Open curlybrace & corresponding Tab
                obc: '\n', //Output Before Close curlybrace
                oac: ' ',
                oact: '' //Output After Close curlybrace & corresponding Tab character
            },
            {
                options: [
                    { name: "brace_style", value: "'expand,preserve-inline'" }
                ],
                obo: '\n',
                obot: '    ',
                oao: '\n',
                oaot: '    ',
                obc: '\n',
                oac: '\n',
                oact: '    '
            },
            {
                options: [
                    { name: "brace_style", value: "'end-expand,preserve-inline'" }
                ],
                obo: ' ',
                obot: '',
                oao: '\n',
                oaot: '    ',
                obc: '\n',
                oac: '\n',
                oact: '    '
            },
            {
                //None tries not to touch brace style so all the tests in this
                //matrix were formatted as if they were collapse
                options: [
                    { name: "brace_style", value: "'none,preserve-inline'" }
                ],
                obo: ' ',
                obot: '',
                oao: '\n',
                oaot: '    ',
                obc: '\n',
                oac: ' ',
                oact: ''
            },
            //Test for backward compatibility
            {
                options: [
                    { name: "brace_style", value: "'collapse-preserve-inline'" }
                ],
                //Equivalent to the output of the first test
                obo: ' ',
                obot: '',
                oao: '\n',
                oaot: '    ',
                obc: '\n',
                oac: ' ',
                oact: ''
            }
        ],
        tests: [
            //Test single inline blocks
            {
                unchanged: 'import { asdf } from "asdf";'
            },
            {
                unchanged: 'import { get } from "asdf";'
            },
            {
                unchanged: 'function inLine() { console.log("oh em gee"); }'
            },
            {
                unchanged: 'if (cancer) { console.log("Im sorry but you only have so long to live..."); }'
            },
            //Test more complex inliners
            {
                input: 'if (ding) { console.log("dong"); } else { console.log("dang"); }',
                output: 'if (ding) { console.log("dong"); }<oac>else { console.log("dang"); }'
            },
            //Test complex mixes of the two
            {
                //The outer function and the third object (obj3) should not
                //be preserved. All other objects should be
                input: [
                    'function kindaComplex() {',
                    '    var a = 2;',
                    '    var obj = {};',
                    '    var obj2 = { a: "a", b: "b" };',
                    '    var obj3 = {',
                    '        c: "c",',
                    '        d: "d",',
                    '        e: "e"',
                    '    };',
                    '}'
                ],
                output: [
                    'function kindaComplex()<obo>{<oao>' + //NL in templates
                    '<oaot>var a = 2;',
                    '    var obj = {};',
                    '    var obj2 = { a: "a", b: "b" };',
                    '    var obj3 = {<oao>' + //NL in templates, Expand doesnt affect js objects
                    '<oaot><oaot>c: "c",',
                    '        d: "d",',
                    '        e: "e"' + //NL in templates
                    '<obc>    };' + //NL in templates
                    '<obc>}'
                ]
            },
            {
                //All inlines should be preserved, all non-inlines (specifically
                //complex(), obj, and obj.b should not be preserved (and hence
                //have the template spacing defined in output)
                input: [
                    'function complex() {',
                    '    console.log("wowe");',
                    '    (function() { var a = 2; var b = 3; })();',
                    '    $.each(arr, function(el, idx) { return el; });',
                    '    var obj = {',
                    '        a: function() { console.log("test"); },',
                    '        b() {',
                    '             console.log("test2");',
                    '        }',
                    '    };',
                    '}'

                ],
                output: [
                    'function complex()<obo>{<oao>' + //NL in templates
                    '<oaot>console.log("wowe");',
                    '    (function() { var a = 2; var b = 3; })();',
                    '    $.each(arr, function(el, idx) { return el; });',
                    '    var obj = {<oao>' + //NL in templates
                    '<oaot><oaot>a: function() { console.log("test"); },',
                    '        b()<obo><obot><obot>{<oao>' + //NL in templates
                    '<oaot><oaot><oaot>console.log("test2");' +
                    '<obc>        }' + //NL in templates
                    '<obc>    };' + //NL in templates
                    '<obc>}'
                ]
            }
        ]
    }, {
        name: "Destructured and related",
        description: "Ensure specific bugs do not recur",
        options: [
            { name: "brace_style", value: "'collapse,preserve-inline'" }
        ], //Issue 1052, now collapse,preserve-inline instead of collapse-preserve-inline
        tests: [{
                comment: "Issue 382 - import destructured ",
                unchanged: [
                    'module "Even" {',
                    '    import { odd, oddly } from "Odd";',
                    '}'
                ]
            },
            {
                unchanged: [
                    'import defaultMember from "module-name";',
                    'import * as name from "module-name";',
                    'import { member } from "module-name";',
                    'import { member as alias } from "module-name";',
                    'import { member1, member2 } from "module-name";',
                    'import { member1, member2 as alias2 } from "module-name";',
                    'import defaultMember, { member, member2 } from "module-name";',
                    'import defaultMember, * as name from "module-name";',
                    'import "module-name";'
                ]
            },
            {
                comment: "Issue 858 - from is a keyword only after import",
                unchanged: [
                    'if (from < to) {',
                    '    from++;',
                    '} else {',
                    '    from--;',
                    '}'
                ]
            },
            {
                comment: "Issue 511 - destrutured",
                unchanged: [
                    'var { b, c } = require("../stores");',
                    'var { ProjectStore } = require("../stores");',
                    '',
                    'function takeThing({ prop }) {',
                    '    console.log("inner prop", prop)',
                    '}'
                ]
            },
            {
                comment: "Issue 315 - Short objects",
                unchanged: [
                    'var a = { b: { c: { d: e } } };'
                ]
            },
            {
                unchanged: [
                    'var a = {',
                    '    b: {',
                    '        c: { d: e }',
                    '        c3: { d: e }',
                    '    },',
                    '    b2: { c: { d: e } }',
                    '};'
                ]
            },
            {
                comment: "Issue 370 - Short objects in array",
                unchanged: [
                    'var methods = [',
                    '    { name: "to" },',
                    '    { name: "step" },',
                    '    { name: "move" },',
                    '    { name: "min" },',
                    '    { name: "max" }',
                    '];'
                ]
            },
            {
                comment: "Issue 838 - Short objects in array",
                unchanged: [
                    'function(url, callback) {',
                    '    var script = document.createElement("script")',
                    '    if (true) script.onreadystatechange = function() {',
                    '        foo();',
                    '    }',
                    '    else script.onload = callback;',
                    '}'
                ]
            },
            {
                comment: "Issue 578 - Odd indenting after function",
                unchanged: [
                    'function bindAuthEvent(eventName) {',
                    '    self.auth.on(eventName, function(event, meta) {',
                    '        self.emit(eventName, event, meta);',
                    '    });',
                    '}',
                    '["logged_in", "logged_out", "signed_up", "updated_user"].forEach(bindAuthEvent);',
                ]
            },
            {
                comment: "Issue #487 - some short expressions examples",
                unchanged: [
                    'if (a == 1) { a++; }',
                    'a = { a: a };',
                    'UserDB.findOne({ username: "xyz" }, function(err, user) {});',
                    'import { fs } from "fs";'
                ]
            },
            {
                comment: "Issue #982 - Fixed return expression collapse-preserve-inline",
                unchanged: [
                    'function foo(arg) {',
                    '    if (!arg) { a(); }',
                    '    if (!arg) { return false; }',
                    '    if (!arg) { throw "inline"; }',
                    '    return true;',
                    '}'
                ]
            },
            {
                comment: "Issue #338 - Short expressions ",
                unchanged: [
                    'if (someCondition) { return something; }',
                    'if (someCondition) {',
                    '    return something;',
                    '}',
                    'if (someCondition) { break; }',
                    'if (someCondition) {',
                    '    return something;',
                    '}'
                ]
            }
        ]
    }, {
        // =======================================================
        // New tests groups should be added above this line.
        // Everything below is a work in progress - converting
        // old test to generated form.
        // =======================================================
        name: "Old tests",
        description: "Largely unorganized pile of tests",
        options: [],
        tests: [
            { unchanged: '' },
            { fragment: true, unchanged: '   return .5' },
            { fragment: true, unchanged: '   return .5;\n   a();' },
            { fragment: true, unchanged: '    return .5;\n    a();' },
            { fragment: true, unchanged: '     return .5;\n     a();' },
            { fragment: true, unchanged: '   < div' },
            { input: 'a        =          1', output: 'a = 1' },
            { input: 'a=1', output: 'a = 1' },
            { unchanged: '(3) / 2' },
            { unchanged: '["a", "b"].join("")' },
            { unchanged: 'a();\n\nb();' },
            { input: 'var a = 1 var b = 2', output: 'var a = 1\nvar b = 2' },
            { input: 'var a=1, b=c[d], e=6;', output: 'var a = 1,\n    b = c[d],\n    e = 6;' },
            { unchanged: 'var a,\n    b,\n    c;' },
            { input: 'let a = 1 let b = 2', output: 'let a = 1\nlet b = 2' },
            { input: 'let a=1, b=c[d], e=6;', output: 'let a = 1,\n    b = c[d],\n    e = 6;' },
            { unchanged: 'let a,\n    b,\n    c;' },
            { input: 'const a = 1 const b = 2', output: 'const a = 1\nconst b = 2' },
            { input: 'const a=1, b=c[d], e=6;', output: 'const a = 1,\n    b = c[d],\n    e = 6;' },
            { unchanged: 'const a,\n    b,\n    c;' },
            { unchanged: 'a = " 12345 "' },
            { unchanged: "a = \\' 12345 \\'" },
            { unchanged: 'if (a == 1) b = 2;' },
            { input: 'if(1){2}else{3}', output: 'if (1) {\n    2\n} else {\n    3\n}' },
            { input: 'if(1||2);', output: 'if (1 || 2);' },
            { input: '(a==1)||(b==2)', output: '(a == 1) || (b == 2)' },
            { input: 'var a = 1 if (2) 3;', output: 'var a = 1\nif (2) 3;' },
            { unchanged: 'a = a + 1' },
            { unchanged: 'a = a == 1' },
            { unchanged: '/12345[^678]*9+/.match(a)' },
            { unchanged: 'a /= 5' },
            { unchanged: 'a = 0.5 * 3' },
            { unchanged: 'a *= 10.55' },
            { unchanged: 'a < .5' },
            { unchanged: 'a <= .5' },
            { input: 'a<.5', output: 'a < .5' },
            { input: 'a<=.5', output: 'a <= .5' },

            {
                comment: 'exponent literals',
                unchanged: 'a = 1e10'
            },
            { unchanged: 'a = 1.3e10' },
            { unchanged: 'a = 1.3e-10' },
            { unchanged: 'a = -12345.3e-10' },
            { unchanged: 'a = .12345e-10' },
            { unchanged: 'a = 06789e-10' },
            { unchanged: 'a = e - 10' },
            { unchanged: 'a = 1.3e+10' },
            { unchanged: 'a = 1.e-7' },
            { unchanged: 'a = -12345.3e+10' },
            { unchanged: 'a = .12345e+10' },
            { unchanged: 'a = 06789e+10' },
            { unchanged: 'a = e + 10' },
            { input: 'a=0e-12345.3e-10', output: 'a = 0e-12345 .3e-10' },
            { input: 'a=0.e-12345.3e-10', output: 'a = 0.e-12345 .3e-10' },
            { input: 'a=0x.e-12345.3e-10', output: 'a = 0x.e - 12345.3e-10' },
            { input: 'a=0x0.e-12345.3e-10', output: 'a = 0x0.e - 12345.3e-10' },
            { input: 'a=0x0.0e-12345.3e-10', output: 'a = 0x0 .0e-12345 .3e-10' },
            { input: 'a=0g-12345.3e-10', output: 'a = 0 g - 12345.3e-10' },
            { input: 'a=0.g-12345.3e-10', output: 'a = 0. g - 12345.3e-10' },
            { input: 'a=0x.g-12345.3e-10', output: 'a = 0x.g - 12345.3e-10' },
            { input: 'a=0x0.g-12345.3e-10', output: 'a = 0x0.g - 12345.3e-10' },
            { input: 'a=0x0.0g-12345.3e-10', output: 'a = 0x0 .0 g - 12345.3e-10' },

            {
                comment: 'Decimal literals',
                unchanged: 'a = 0123456789;'
            },
            { unchanged: 'a = 9876543210;' },
            { unchanged: 'a = 5647308291;' },
            { input: 'a=030e-5', output: 'a = 030e-5' },
            { input: 'a=00+4', output: 'a = 00 + 4' },
            { input: 'a=32+4', output: 'a = 32 + 4' },
            { input: 'a=0.6g+4', output: 'a = 0.6 g + 4' },
            { input: 'a=01.10', output: 'a = 01.10' },
            { input: 'a=a.10', output: 'a = a .10' },
            { input: 'a=00B0x0', output: 'a = 00 B0x0' },
            { input: 'a=00B0xb0', output: 'a = 00 B0xb0' },
            { input: 'a=00B0x0b0', output: 'a = 00 B0x0b0' },
            { input: 'a=0090x0', output: 'a = 0090 x0' },
            { input: 'a=0g0b0o0', output: 'a = 0 g0b0o0' },

            {
                comment: 'Hexadecimal literals',
                unchanged: 'a = 0x0123456789abcdef;'
            },
            { unchanged: 'a = 0X0123456789ABCDEF;' },
            { unchanged: 'a = 0xFeDcBa9876543210;' },
            { input: 'a=0x30e-5', output: 'a = 0x30e - 5' },
            { input: 'a=0xF0+4', output: 'a = 0xF0 + 4' },
            { input: 'a=0Xff+4', output: 'a = 0Xff + 4' },
            { input: 'a=0Xffg+4', output: 'a = 0Xff g + 4' },
            { input: 'a=0x01.10', output: 'a = 0x01 .10' },
            { unchanged: 'a = 0xb0ce;' },
            { unchanged: 'a = 0x0b0;' },
            { input: 'a=0x0B0x0', output: 'a = 0x0B0 x0' },
            { input: 'a=0x0B0xb0', output: 'a = 0x0B0 xb0' },
            { input: 'a=0x0B0x0b0', output: 'a = 0x0B0 x0b0' },
            { input: 'a=0X090x0', output: 'a = 0X090 x0' },
            { input: 'a=0Xg0b0o0', output: 'a = 0X g0b0o0' },

            {
                comment: 'Octal literals',
                unchanged: 'a = 0o01234567;'
            },
            { unchanged: 'a = 0O01234567;' },
            { unchanged: 'a = 0o34120675;' },
            { input: 'a=0o30e-5', output: 'a = 0o30 e - 5' },
            { input: 'a=0o70+4', output: 'a = 0o70 + 4' },
            { input: 'a=0O77+4', output: 'a = 0O77 + 4' },
            { input: 'a=0O778+4', output: 'a = 0O77 8 + 4' },
            { input: 'a=0O77a+4', output: 'a = 0O77 a + 4' },
            { input: 'a=0o01.10', output: 'a = 0o01 .10' },
            { input: 'a=0o0B0x0', output: 'a = 0o0 B0x0' },
            { input: 'a=0o0B0xb0', output: 'a = 0o0 B0xb0' },
            { input: 'a=0o0B0x0b0', output: 'a = 0o0 B0x0b0' },
            { input: 'a=0O090x0', output: 'a = 0O0 90 x0' },
            { input: 'a=0Og0b0o0', output: 'a = 0O g0b0o0' },

            {
                comment: 'Binary literals',
                unchanged: 'a = 0b010011;'
            },
            { unchanged: 'a = 0B010011;' },
            { unchanged: 'a = 0b01001100001111;' },
            { input: 'a=0b10e-5', output: 'a = 0b10 e - 5' },
            { input: 'a=0b10+4', output: 'a = 0b10 + 4' },
            { input: 'a=0B11+4', output: 'a = 0B11 + 4' },
            { input: 'a=0B112+4', output: 'a = 0B11 2 + 4' },
            { input: 'a=0B11a+4', output: 'a = 0B11 a + 4' },
            { input: 'a=0b01.10', output: 'a = 0b01 .10' },
            { input: 'a=0b0B0x0', output: 'a = 0b0 B0x0' },
            { input: 'a=0b0B0xb0', output: 'a = 0b0 B0xb0' },
            { input: 'a=0b0B0x0b0', output: 'a = 0b0 B0x0b0' },
            { input: 'a=0B090x0', output: 'a = 0B0 90 x0' },
            { input: 'a=0Bg0b0o0', output: 'a = 0B g0b0o0' },
            { unchanged: 'a = [1, 2, 3, 4]' },
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
            { unchanged: 'function void(void) {}' },
            { input: 'if(!a)foo();', output: 'if (!a) foo();' },
            { input: 'a=~a', output: 'a = ~a' },
            { input: 'a;/*comment*/b;', output: "a; /*comment*/\nb;" },
            { input: 'a;/* comment */b;', output: "a; /* comment */\nb;" },
            { fragment: true, input: 'a;/*\ncomment\n*/b;', output: "a;\n/*\ncomment\n*/\nb;", comment: "simple comments don't get touched at all" },
            { input: 'a;/**\n* javadoc\n*/b;', output: "a;\n/**\n * javadoc\n */\nb;" },
            { fragment: true, input: 'a;/**\n\nno javadoc\n*/b;', output: "a;\n/**\n\nno javadoc\n*/\nb;" },
            { input: 'a;/*\n* javadoc\n*/b;', output: "a;\n/*\n * javadoc\n */\nb;", comment: 'comment blocks detected and reindented even w/o javadoc starter' },
            { input: 'if(a)break;', output: "if (a) break;" },
            { input: 'if(a){break}', output: "if (a) {\n    break\n}" },
            { input: 'if((a))foo();', output: 'if ((a)) foo();' },
            { input: 'for(var i=0;;) a', output: 'for (var i = 0;;) a' },
            { input: 'for(var i=0;;)\na', output: 'for (var i = 0;;)\n    a' },
            { unchanged: 'a++;' },
            { input: 'for(;;i++)a()', output: 'for (;; i++) a()' },
            { input: 'for(;;i++)\na()', output: 'for (;; i++)\n    a()' },
            { input: 'for(;;++i)a', output: 'for (;; ++i) a' },
            { input: 'return(1)', output: 'return (1)' },
            { input: 'try{a();}catch(b){c();}finally{d();}', output: "try {\n    a();\n} catch (b) {\n    c();\n} finally {\n    d();\n}" },
            { unchanged: '(xx)()', comment: ' magic function call' },
            { unchanged: 'a[1]()', comment: 'another magic function call' },
            { input: 'if(a){b();}else if(c) foo();', output: "if (a) {\n    b();\n} else if (c) foo();" },
            { input: 'switch(x) {case 0: case 1: a(); break; default: break}', output: "switch (x) {\n    case 0:\n    case 1:\n        a();\n        break;\n    default:\n        break\n}" },
            { input: 'switch(x){case -1:break;case !y:break;}', output: 'switch (x) {\n    case -1:\n        break;\n    case !y:\n        break;\n}' },
            { unchanged: 'a !== b' },
            { input: 'if (a) b(); else c();', output: "if (a) b();\nelse c();" },
            { unchanged: "// comment\n(function something() {})", comment: 'typical greasemonkey start' },
            { unchanged: "{\n\n    x();\n\n}", comment: 'duplicating newlines' },
            { unchanged: 'if (a in b) foo();' },
            { unchanged: 'if (a of b) foo();' },
            { unchanged: 'if (a of [1, 2, 3]) foo();' },
            {
                input: 'if(X)if(Y)a();else b();else c();',
                output: "if (X)\n    if (Y) a();\n    else b();\nelse c();"
            },
            { unchanged: 'if (foo) bar();\nelse break' },
            { unchanged: 'var a, b;' },
            { unchanged: 'var a = new function();' },
            { fragment: true, unchanged: 'new function' },
            { unchanged: 'var a, b' },
            { input: '{a:1, b:2}', output: "{\n    a: 1,\n    b: 2\n}" },
            { input: 'a={1:[-1],2:[+1]}', output: 'a = {\n    1: [-1],\n    2: [+1]\n}' },
            { input: "var l = {\\'a\\':\\'1\\', \\'b\\':\\'2\\'}", output: "var l = {\n    \\'a\\': \\'1\\',\n    \\'b\\': \\'2\\'\n}" },
            { unchanged: 'if (template.user[n] in bk) foo();' },
            { unchanged: 'return 45' },
            { unchanged: 'return this.prevObject ||\n\n    this.constructor(null);' },
            { unchanged: 'If[1]' },
            { unchanged: 'Then[1]' },
            { input: "a = 1;// comment", output: "a = 1; // comment" },
            { unchanged: "a = 1; // comment" },
            { input: "a = 1;\n // comment", output: "a = 1;\n// comment" },
            { unchanged: 'a = [-1, -1, -1]' },

            // These must work as non-fragments.
            { unchanged: ['// a', '// b', '', '', '', '// c', '// d'] },
            { unchanged: ['// func-comment', '', 'function foo() {}', '', '// end-func-comment'] },

            {
                comment: 'The exact formatting these should have is open for discussion, but they are at least reasonable',
                unchanged: 'a = [ // comment\n    -1, -1, -1\n]'
            },
            { unchanged: 'var a = [ // comment\n    -1, -1, -1\n]' },
            { unchanged: 'a = [ // comment\n    -1, // comment\n    -1, -1\n]' },
            { unchanged: 'var a = [ // comment\n    -1, // comment\n    -1, -1\n]' },

            { input: 'o = [{a:b},{c:d}]', output: 'o = [{\n    a: b\n}, {\n    c: d\n}]' },

            {
                comment: 'was: extra space appended',
                unchanged: "if (a) {\n    do();\n}"
            },

            {
                comment: 'if/else statement with empty body',
                input: "if (a) {\n// comment\n}else{\n// comment\n}",
                output: "if (a) {\n    // comment\n} else {\n    // comment\n}"
            },
            { comment: 'multiple comments indentation', input: "if (a) {\n// comment\n// comment\n}", output: "if (a) {\n    // comment\n    // comment\n}" },
            { input: "if (a) b() else c();", output: "if (a) b()\nelse c();" },
            { input: "if (a) b() else if c() d();", output: "if (a) b()\nelse if c() d();" },

            { unchanged: "{}" },
            { unchanged: "{\n\n}" },
            { input: "do { a(); } while ( 1 );", output: "do {\n    a();\n} while (1);" },
            { unchanged: "do {} while (1);" },
            { input: "do {\n} while (1);", output: "do {} while (1);" },
            { unchanged: "do {\n\n} while (1);" },
            { unchanged: "var a = x(a, b, c)" },
            { input: "delete x if (a) b();", output: "delete x\nif (a) b();" },
            { input: "delete x[x] if (a) b();", output: "delete x[x]\nif (a) b();" },
            { input: "for(var a=1,b=2)d", output: "for (var a = 1, b = 2) d" },
            { input: "for(var a=1,b=2,c=3) d", output: "for (var a = 1, b = 2, c = 3) d" },
            { input: "for(var a=1,b=2,c=3;d<3;d++)\ne", output: "for (var a = 1, b = 2, c = 3; d < 3; d++)\n    e" },
            { input: "function x(){(a||b).c()}", output: "function x() {\n    (a || b).c()\n}" },
            { input: "function x(){return - 1}", output: "function x() {\n    return -1\n}" },
            { input: "function x(){return ! a}", output: "function x() {\n    return !a\n}" },
            { unchanged: "x => x" },
            { unchanged: "(x) => x" },
            { input: "x => { x }", output: "x => {\n    x\n}" },
            { input: "(x) => { x }", output: "(x) => {\n    x\n}" },

            {
                comment: 'a common snippet in jQuery plugins',
                input_: "settings = $.extend({},defaults,settings);",
                output: "settings = $.extend({}, defaults, settings);"
            },

            // reserved words used as property names
            { unchanged: "$http().then().finally().default()" },
            { input: "$http()\n.then()\n.finally()\n.default()", output: "$http()\n    .then()\n    .finally()\n    .default()" },
            { unchanged: "$http().when.in.new.catch().throw()" },
            { input: "$http()\n.when\n.in\n.new\n.catch()\n.throw()", output: "$http()\n    .when\n    .in\n    .new\n    .catch()\n    .throw()" },

            { input: '{xxx;}()', output: '{\n    xxx;\n}()' },

            { unchanged: "a = \\'a\\'\nb = \\'b\\'" },
            { unchanged: "a = /reg/exp" },
            { unchanged: "a = /reg/" },
            { unchanged: '/abc/.test()' },
            { unchanged: '/abc/i.test()' },
            { input: "{/abc/i.test()}", output: "{\n    /abc/i.test()\n}" },
            { input: 'var x=(a)/a;', output: 'var x = (a) / a;' },

            { unchanged: 'x != -1' },

            { input: 'for (; s-->0;)t', output: 'for (; s-- > 0;) t' },
            { input: 'for (; s++>0;)u', output: 'for (; s++ > 0;) u' },
            { input: 'a = s++>s--;', output: 'a = s++ > s--;' },
            { input: 'a = s++>--s;', output: 'a = s++ > --s;' },

            { input: '{x=#1=[]}', output: '{\n    x = #1=[]\n}' },
            { input: '{a:#1={}}', output: '{\n    a: #1={}\n}' },
            { input: '{a:#1#}', output: '{\n    a: #1#\n}' },

            { fragment: true, unchanged: '"incomplete-string' },
            { fragment: true, unchanged: "\\'incomplete-string" },
            { fragment: true, unchanged: '/incomplete-regex' },
            { fragment: true, unchanged: '`incomplete-template-string' },

            { fragment: true, input: '{a:1},{a:2}', output: '{\n    a: 1\n}, {\n    a: 2\n}' },
            { fragment: true, input: 'var ary=[{a:1}, {a:2}];', output: 'var ary = [{\n    a: 1\n}, {\n    a: 2\n}];' },

            { comment: 'incomplete', fragment: true, input: '{a:#1', output: '{\n    a: #1' },
            { comment: 'incomplete', fragment: true, input: '{a:#', output: '{\n    a: #' },

            { comment: 'incomplete', fragment: true, input: '}}}', output: '}\n}\n}' },

            { fragment: true, unchanged: '<!--\nvoid();\n// -->' },

            { comment: 'incomplete regexp', fragment: true, input: 'a=/regexp', output: 'a = /regexp' },

            { input: '{a:#1=[],b:#1#,c:#999999#}', output: '{\n    a: #1=[],\n    b: #1#,\n    c: #999999#\n}' },

            { input: "do{x()}while(a>1)", output: "do {\n    x()\n} while (a > 1)" },

            { input: "x(); /reg/exp.match(something)", output: "x();\n/reg/exp.match(something)" },

            { fragment: true, input: "something();(", output: "something();\n(" },
            { fragment: true, input: "#!she/bangs, she bangs\nf=1", output: "#!she/bangs, she bangs\n\nf = 1" },
            { fragment: true, input: "#!she/bangs, she bangs\n\nf=1", output: "#!she/bangs, she bangs\n\nf = 1" },
            { fragment: true, unchanged: "#!she/bangs, she bangs\n\n/* comment */" },
            { fragment: true, unchanged: "#!she/bangs, she bangs\n\n\n/* comment */" },
            { fragment: true, unchanged: "#" },
            { fragment: true, unchanged: "#!" },

            { unchanged: "function namespace::something()" },

            { fragment: true, unchanged: "<!--\nsomething();\n-->" },
            { fragment: true, input: "<!--\nif(i<0){bla();}\n-->", output: "<!--\nif (i < 0) {\n    bla();\n}\n-->" },

            { input: '{foo();--bar;}', output: '{\n    foo();\n    --bar;\n}' },
            { input: '{foo();++bar;}', output: '{\n    foo();\n    ++bar;\n}' },
            { input: '{--bar;}', output: '{\n    --bar;\n}' },
            { input: '{++bar;}', output: '{\n    ++bar;\n}' },
            { input: 'if(true)++a;', output: 'if (true) ++a;' },
            { input: 'if(true)\n++a;', output: 'if (true)\n    ++a;' },
            { input: 'if(true)--a;', output: 'if (true) --a;' },
            { input: 'if(true)\n--a;', output: 'if (true)\n    --a;' },
            { unchanged: 'elem[array]++;' },
            { unchanged: 'elem++ * elem[array]++;' },
            { unchanged: 'elem-- * -elem[array]++;' },
            { unchanged: 'elem-- + elem[array]++;' },
            { unchanged: 'elem-- - elem[array]++;' },
            { unchanged: 'elem-- - -elem[array]++;' },
            { unchanged: 'elem-- - +elem[array]++;' },


            {
                comment: 'Handling of newlines around unary ++ and -- operators',
                input: '{foo\n++bar;}',
                output: '{\n    foo\n    ++bar;\n}'
            },
            { input: '{foo++\nbar;}', output: '{\n    foo++\n    bar;\n}' },

            {
                comment: 'This is invalid, but harder to guard against. Issue #203.',
                input: '{foo\n++\nbar;}',
                output: '{\n    foo\n    ++\n    bar;\n}'
            },

            {
                comment: 'regexps',
                input: 'a(/abc\\\\/\\\\/def/);b()',
                output: "a(/abc\\\\/\\\\/def/);\nb()"
            },
            { input: 'a(/a[b\\\\[\\\\]c]d/);b()', output: "a(/a[b\\\\[\\\\]c]d/);\nb()" },
            { comment: 'incomplete char class', fragment: true, unchanged: 'a(/a[b\\\\[' },

            {
                comment: 'allow unescaped / in char classes',
                input: 'a(/[a/b]/);b()',
                output: "a(/[a/b]/);\nb()"
            },
            { unchanged: 'typeof /foo\\\\//;' },
            { unchanged: 'throw /foo\\\\//;' },
            { unchanged: 'do /foo\\\\//;' },
            { unchanged: 'return /foo\\\\//;' },
            { unchanged: 'switch (a) {\n    case /foo\\\\//:\n        b\n}' },
            { unchanged: 'if (a) /foo\\\\//\nelse /foo\\\\//;' },

            { unchanged: 'if (foo) /regex/.test();' },
            { unchanged: "for (index in [1, 2, 3]) /^test$/i.test(s)" },

            { unchanged: 'function foo() {\n    return [\n        "one",\n        "two"\n    ];\n}' },
            { input: 'a=[[1,2],[4,5],[7,8]]', output: "a = [\n    [1, 2],\n    [4, 5],\n    [7, 8]\n]" },
            {
                input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    [7, 8]\n]"
            },
            {
                input: 'a=[[1,2],[4,5],function(){},function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    function() {},\n    [7, 8]\n]"
            },
            {
                input: 'a=[[1,2],[4,5],function(){},[7,8]]',
                output: "a = [\n    [1, 2],\n    [4, 5],\n    function() {},\n    [7, 8]\n]"
            },
            {
                input: 'a=[b,c,function(){},function(){},d]',
                output: "a = [b, c, function() {}, function() {}, d]"
            },
            {
                input: 'a=[b,c,\nfunction(){},function(){},d]',
                output: "a = [b, c,\n    function() {},\n    function() {},\n    d\n]"
            },
            { input: 'a=[a[1],b[4],c[d[7]]]', output: "a = [a[1], b[4], c[d[7]]]" },
            { input: '[1,2,[3,4,[5,6],7],8]', output: "[1, 2, [3, 4, [5, 6], 7], 8]" },

            {
                input: '[[["1","2"],["3","4"]],[["5","6","7"],["8","9","0"]],[["1","2","3"],["4","5","6","7"],["8","9","0"]]]',
                output: '[\n    [\n        ["1", "2"],\n        ["3", "4"]\n    ],\n    [\n        ["5", "6", "7"],\n        ["8", "9", "0"]\n    ],\n    [\n        ["1", "2", "3"],\n        ["4", "5", "6", "7"],\n        ["8", "9", "0"]\n    ]\n]'
            },

            { input: '{[x()[0]];indent;}', output: '{\n    [x()[0]];\n    indent;\n}' },
            { unchanged: '/*\n foo trailing space    \n * bar trailing space   \n**/' },
            { unchanged: '{\n    /*\n    foo    \n    * bar    \n    */\n}' },

            { unchanged: 'return ++i' },
            { unchanged: 'return !!x' },
            { unchanged: 'return !x' },
            { input: 'return [1,2]', output: 'return [1, 2]' },
            { unchanged: 'return;' },
            { unchanged: 'return\nfunc' },
            { input: 'catch(e)', output: 'catch (e)' },

            {
                input: 'var a=1,b={foo:2,bar:3},{baz:4,wham:5},c=4;',
                output: 'var a = 1,\n    b = {\n        foo: 2,\n        bar: 3\n    },\n    {\n        baz: 4,\n        wham: 5\n    }, c = 4;'
            },
            {
                input: 'var a=1,b={foo:2,bar:3},{baz:4,wham:5},\nc=4;',
                output: 'var a = 1,\n    b = {\n        foo: 2,\n        bar: 3\n    },\n    {\n        baz: 4,\n        wham: 5\n    },\n    c = 4;'
            },

            {
                comment: 'inline comment',
                input_: 'function x(/*int*/ start, /*string*/ foo)',
                output: 'function x( /*int*/ start, /*string*/ foo)'
            },

            {
                comment: 'javadoc comment',
                input: '/**\n* foo\n*/',
                output: '/**\n * foo\n */'
            },
            { input: '{\n/**\n* foo\n*/\n}', output: '{\n    /**\n     * foo\n     */\n}' },

            {
                comment: 'starless block comment',
                unchanged: '/**\nfoo\n*/'
            },
            { unchanged: '/**\nfoo\n**/' },
            { unchanged: '/**\nfoo\nbar\n**/' },
            { unchanged: '/**\nfoo\n\nbar\n**/' },
            { unchanged: '/**\nfoo\n    bar\n**/' },
            { input: '{\n/**\nfoo\n*/\n}', output: '{\n    /**\n    foo\n    */\n}' },
            { input: '{\n/**\nfoo\n**/\n}', output: '{\n    /**\n    foo\n    **/\n}' },
            { input: '{\n/**\nfoo\nbar\n**/\n}', output: '{\n    /**\n    foo\n    bar\n    **/\n}' },
            { input: '{\n/**\nfoo\n\nbar\n**/\n}', output: '{\n    /**\n    foo\n\n    bar\n    **/\n}' },
            { input: '{\n/**\nfoo\n    bar\n**/\n}', output: '{\n    /**\n    foo\n        bar\n    **/\n}' },
            { unchanged: '{\n    /**\n    foo\nbar\n    **/\n}' },

            { input: 'var a,b,c=1,d,e,f=2;', output: 'var a, b, c = 1,\n    d, e, f = 2;' },
            { input: 'var a,b,c=[],d,e,f=2;', output: 'var a, b, c = [],\n    d, e, f = 2;' },
            { unchanged: 'function() {\n    var a, b, c, d, e = [],\n        f;\n}' },

            { input: 'do/regexp/;\nwhile(1);', output: 'do /regexp/;\nwhile (1);' },
            { input: 'var a = a,\na;\nb = {\nb\n}', output: 'var a = a,\n    a;\nb = {\n    b\n}' },

            { unchanged: 'var a = a,\n    /* c */\n    b;' },
            { unchanged: 'var a = a,\n    // c\n    b;' },

            {
                comment: 'weird element referencing',
                unchanged: 'foo.("bar");'
            },


            { unchanged: 'if (a) a()\nelse b()\nnewline()' },
            { unchanged: 'if (a) a()\nnewline()' },
            { input: 'a=typeof(x)', output: 'a = typeof(x)' },

            { unchanged: 'var a = function() {\n        return null;\n    },\n    b = false;' },

            { unchanged: 'var a = function() {\n    func1()\n}' },
            { unchanged: 'var a = function() {\n    func1()\n}\nvar b = function() {\n    func2()\n}' },

            {
                comment: 'code with and without semicolons',
                input_: 'var whatever = require("whatever");\nfunction() {\n    a = 6;\n}',
                output: 'var whatever = require("whatever");\n\nfunction() {\n    a = 6;\n}'
            },
            {
                input: 'var whatever = require("whatever")\nfunction() {\n    a = 6\n}',
                output: 'var whatever = require("whatever")\n\nfunction() {\n    a = 6\n}'
            },

            { input: '{"x":[{"a":1,"b":3},\n7,8,8,8,8,{"b":99},{"a":11}]}', output: '{\n    "x": [{\n            "a": 1,\n            "b": 3\n        },\n        7, 8, 8, 8, 8, {\n            "b": 99\n        }, {\n            "a": 11\n        }\n    ]\n}' },
            { input: '{"x":[{"a":1,"b":3},7,8,8,8,8,{"b":99},{"a":11}]}', output: '{\n    "x": [{\n        "a": 1,\n        "b": 3\n    }, 7, 8, 8, 8, 8, {\n        "b": 99\n    }, {\n        "a": 11\n    }]\n}' },

            { input: '{"1":{"1a":"1b"},"2"}', output: '{\n    "1": {\n        "1a": "1b"\n    },\n    "2"\n}' },
            { input: '{a:{a:b},c}', output: '{\n    a: {\n        a: b\n    },\n    c\n}' },

            { input: '{[y[a]];keep_indent;}', output: '{\n    [y[a]];\n    keep_indent;\n}' },

            { input: 'if (x) {y} else { if (x) {y}}', output: 'if (x) {\n    y\n} else {\n    if (x) {\n        y\n    }\n}' },

            { unchanged: 'if (foo) one()\ntwo()\nthree()' },
            { unchanged: 'if (1 + foo() && bar(baz()) / 2) one()\ntwo()\nthree()' },
            { unchanged: 'if (1 + foo() && bar(baz()) / 2) one();\ntwo();\nthree();' },

            { input: 'var a=1,b={bang:2},c=3;', output: 'var a = 1,\n    b = {\n        bang: 2\n    },\n    c = 3;' },
            { input: 'var a={bing:1},b=2,c=3;', output: 'var a = {\n        bing: 1\n    },\n    b = 2,\n    c = 3;' },

        ],
    }],
    examples: [{
        // Example
        group_name: "one",
        description: "",
        options: [],
        values: [{
            source: "", //string or array of lines
            output: "" //string or array of lines
        }]
    }]
};