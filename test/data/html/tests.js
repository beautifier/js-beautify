exports.test_data = {
    default_options: [
        { name: "indent_size", value: "4" },
        { name: "indent_char", value: "' '" },
        { name: "indent_with_tabs", value: "false" },
        { name: "preserve_newlines", value: "true" },
        { name: "jslint_happy", value: "false" },
        { name: "keep_array_indentation", value: "false" },
        { name: "brace_style", value: "'collapse'" },
        { name: "extra_liners", value: "['html', 'head', '/html']" }
    ],
    groups: [{
        name: "Handle inline and block elements differently",
        description: "",
        matrix: [{}],
        tests: [{
            fragment: true,
            input: '<body><h1>Block</h1></body>',
            output: [
                '<body>',
                '    <h1>Block</h1>',
                '</body>'
            ]
        }, {
            fragment: true,
            unchanged: '<body><i>Inline</i></body>'
        }]
    }, {
        name: "End With Newline",
        description: "",
        matrix: [{
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
            { fragment: true, input: '', output: '{{eof}}' },
            { fragment: true, input: '<div></div>', output: '<div></div>{{eof}}' },
            // { fragment: true, input: '   \n\n<div></div>\n\n\n\n', output: '   <div></div>{{eof}}' },
            { fragment: true, input: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "Custom Extra Liners (empty)",
        description: "",
        matrix: [{
                options: [
                    { name: "extra_liners", value: "[]" }
                ]
            },

        ],
        tests: [{
            fragment: true,
            input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
            output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n        <p>x</p>\n    </div>\n</body>\n</html>'
        }],
    }, {
        name: "Custom Extra Liners (default)",
        description: "",
        matrix: [{
                options: [
                    { name: "extra_liners", value: "null" }
                ]
            },

        ],
        tests: [{
            fragment: true,
            input: '<html><head></head><body></body></html>',
            output: '<html>\n\n<head></head>\n\n<body></body>\n\n</html>'
        }],
    }, {
        name: "Custom Extra Liners (p, string)",
        description: "",
        matrix: [{
                options: [
                    { name: "extra_liners", value: "'p,/p'" }
                ]
            },

        ],
        tests: [{
            fragment: true,
            input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
            output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
        }],
    }, {
        name: "Custom Extra Liners (p)",
        description: "",
        matrix: [{
                options: [
                    { name: "extra_liners", value: "['p', '/p']" }
                ]
            },

        ],
        tests: [{
            fragment: true,
            input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
            output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
        }],
    }, {
        name: "Tests for script and style types (issue 453, 821",
        description: "Only format recognized script types",
        tests: [{
                input: '<script type="text/unknown"><div></div></script>',
                output: [
                    '<script type="text/unknown">',
                    '    <div></div>',
                    '</script>'
                ]
            }, {
                input: '<script type="text/javascript"><div></div></script>',
                output: [
                    '<script type="text/javascript">',
                    '    < div > < /div>',
                    '</script>'
                ]
            }, {
                input: '<script><div></div></script>',
                output: [
                    '<script>',
                    '    < div > < /div>',
                    '</script>'
                ]
            }, {
                input: '<script>var foo = "bar";</script>',
                output: [
                    '<script>',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="text/javascript">var foo = "bar";</script>',
                output: [
                    '<script type="text/javascript">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="application/javascript">var foo = "bar";</script>',
                output: [
                    '<script type="application/javascript">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="application/javascript;version=1.8">var foo = "bar";</script>',
                output: [
                    '<script type="application/javascript;version=1.8">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="application/x-javascript">var foo = "bar";</script>',
                output: [
                    '<script type="application/x-javascript">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="application/ecmascript">var foo = "bar";</script>',
                output: [
                    '<script type="application/ecmascript">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="dojo/aspect">this.domNode.style.display="none";</script>',
                output: [
                    '<script type="dojo/aspect">',
                    '    this.domNode.style.display = "none";',
                    '</script>'
                ]
            }, {
                input: '<script type="dojo/method">this.domNode.style.display="none";</script>',
                output: [
                    '<script type="dojo/method">',
                    '    this.domNode.style.display = "none";',
                    '</script>'
                ]
            }, {
                input: '<script type="text/javascript1.5">var foo = "bar";</script>',
                output: [
                    '<script type="text/javascript1.5">',
                    '    var foo = "bar";',
                    '</script>'
                ]
            }, {
                input: '<script type="application/json">{"foo":"bar"}</script>',
                output: [
                    '<script type="application/json">',
                    '    {',
                    '        "foo": "bar"',
                    '    }',
                    '</script>'
                ]
            }, {
                input: '<script type="application/ld+json">{"foo":"bar"}</script>',
                output: [
                    '<script type="application/ld+json">',
                    '    {',
                    '        "foo": "bar"',
                    '    }',
                    '</script>'
                ]
            }, {
                input: '<style type="text/unknown"><tag></tag></style>',
                output: [
                    '<style type="text/unknown">',
                    '    <tag></tag>',
                    '</style>'
                ]
            }, {
                input: '<style type="text/css"><tag></tag></style>',
                output: [
                    '<style type="text/css">',
                    '    <tag></tag>',
                    '</style>'
                ]
            }, {
                input: '<style><tag></tag></style>',
                output: [
                    '<style>',
                    '    <tag></tag>',
                    '</style>'
                ]
            }, {
                input: '<style>.selector {font-size:12px;}</style>',
                output: [
                    '<style>',
                    '    .selector {',
                    '        font-size: 12px;',
                    '    }',
                    '</style>'
                ]
            }, {
                input: '<style type="text/css">.selector {font-size:12px;}</style>',
                output: [
                    '<style type="text/css">',
                    '    .selector {',
                    '        font-size: 12px;',
                    '    }',
                    '</style>'
                ]
            },

        ],
    }, {
        name: "Attribute Wrap",
        description: "Wraps attributes inside of html tags",
        matrix: [{
            options: [
                { name: "wrap_attributes", value: "'force'" }
            ],
            indent_attr: '\\n    ',
            indent_over80: '\\n    '
        }, {
            options: [
                { name: "wrap_attributes", value: "'force'" },
                { name: "wrap_line_length", value: "80" }
            ],
            indent_attr: '\\n    ',
            indent_over80: '\\n    '
        }, {
            options: [
                { name: "wrap_attributes", value: "'force'" },
                { name: "wrap_attributes_indent_size", value: "8" },
            ],
            indent_attr: '\\n        ',
            indent_over80: '\\n        '
        }, {
            options: [
                { name: "wrap_attributes", value: "'auto'" },
                { name: "wrap_line_length", value: "80" },
                { name: "wrap_attributes_indent_size", value: "0" }
            ],
            indent_attr: ' ',
            indent_over80: '\\n'
        }, {
            options: [
                { name: "wrap_attributes", value: "'auto'" },
                { name: "wrap_line_length", value: "80" },
                { name: "wrap_attributes_indent_size", value: "4" }
            ],
            indent_attr: ' ',
            indent_over80: '\\n    '
        }, {
            options: [
                { name: "wrap_attributes", value: "'auto'" },
                { name: "wrap_line_length", value: "0" }
            ],
            indent_attr: ' ',
            indent_over80: ' '
        }],
        tests: [{
            fragment: true,
            input: '<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>',
            output: '<div attr0{{indent_attr}}attr1="123"{{indent_attr}}data-attr2="hello    t here">This is some text</div>'
        }, {
            fragment: true,
            input: '<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>',
            output: '<div lookatthissuperduperlongattributenamewhoahcrazy0="true"{{indent_attr}}attr0{{indent_attr}}attr1="123"{{indent_attr}}data-attr2="hello    t here"{{indent_over80}}heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>'
        }, {
            fragment: true,
            input: '<img attr0 attr1="123" data-attr2="hello    t here"/>',
            output: '<img attr0{{indent_attr}}attr1="123"{{indent_attr}}data-attr2="hello    t here" />'
        }, {
            fragment: true,
            input: '<?xml version="1.0" encoding="UTF-8" ?><root attr1="foo" attr2="bar"/>',
            output: '<?xml version="1.0" encoding="UTF-8" ?>\n<root attr1="foo"{{indent_attr}}attr2="bar" />'
        }, {
            fragment: true,
            input: '<link href="//fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,700,300&amp;subset=latin" rel="stylesheet" type="text/css">',
            output: '<link href="//fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,700,300&amp;subset=latin"{{indent_over80}}rel="stylesheet"{{indent_attr}}type="text/css">'
        }]
    }, {
        name: "Handlebars Indenting Off",
        description: "Test handlebar behavior when indenting is off",
        template: "^^^ $$$",
        options: [
            { name: "indent_handlebars", value: "false" }
        ],
        tests: [{
                fragment: true,
                input_: '{{#if 0}}\n' +
                    '    <div>\n' +
                    '    </div>\n' +
                    '{{/if}}',
                output: '{{#if 0}}\n' +
                    '<div>\n' +
                    '</div>\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                input_: '<div>\n' +
                    '{{#each thing}}\n' +
                    '    {{name}}\n' +
                    '{{/each}}\n' +
                    '</div>',
                output: '<div>\n' +
                    '    {{#each thing}} {{name}} {{/each}}\n' +
                    '</div>'
            }

        ]
    }, {
        name: "Handlebars Indenting On",
        description: "Test handlebar formatting",
        template: "^^^ $$$",
        matrix: [{
            options: [
                { name: "indent_handlebars", value: "true" }
            ],
            content: '{{field}}'
        }, {
            options: [
                { name: "indent_handlebars", value: "true" }
            ],
            content: '{{! comment}}'
        }, {
            options: [
                { name: "indent_handlebars", value: "true" }
            ],
            content: '{pre{{field1}} {{field2}} {{field3}}post'
        }, {
            options: [
                { name: "indent_handlebars", value: "true" }
            ],
            content: '{{! \\n mult-line\\ncomment  \\n     with spacing\\n}}'
        }],
        tests: [
            { fragment: true, unchanged: '{{page-title}}' },
            { fragment: true, unchanged: '{{#if 0}}{{/if}}' },
            { fragment: true, unchanged: '{{#if 0}}^^^content$$${{/if}}' },
            { fragment: true, unchanged: '{{#if 0}}\n{{/if}}' }, {
                fragment: true,
                input_: '{{#if     words}}{{/if}}',
                output: '{{#if words}}{{/if}}'
            }, {
                fragment: true,
                input_: '{{#if     words}}^^^content$$${{/if}}',
                output: '{{#if words}}^^^content$$${{/if}}'
            }, {
                fragment: true,
                input_: '{{#if     words}}^^^content$$${{/if}}',
                output: '{{#if words}}^^^content$$${{/if}}'
            }, {
                fragment: true,
                unchanged: '{{#if 1}}\n' +
                    '    <div>\n' +
                    '    </div>\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                input_: '{{#if 1}}\n' +
                    '<div>\n' +
                    '</div>\n' +
                    '{{/if}}',
                output: '{{#if 1}}\n' +
                    '    <div>\n' +
                    '    </div>\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                unchanged: '<div>\n' +
                    '    {{#if 1}}\n' +
                    '    {{/if}}\n' +
                    '</div>'
            }, {
                fragment: true,
                input_: '<div>\n' +
                    '{{#if 1}}\n' +
                    '{{/if}}\n' +
                    '</div>',
                output: '<div>\n' +
                    '    {{#if 1}}\n' +
                    '    {{/if}}\n' +
                    '</div>'
            }, {
                fragment: true,
                input_: '{{#if}}\n' +
                    '{{#each}}\n' +
                    '{{#if}}\n' +
                    '^^^content$$$\n' +
                    '{{/if}}\n' +
                    '{{#if}}\n' +
                    '^^^content$$$\n' +
                    '{{/if}}\n' +
                    '{{/each}}\n' +
                    '{{/if}}',
                output: '{{#if}}\n' +
                    '    {{#each}}\n' +
                    '        {{#if}}\n' +
                    '            ^^^content$$$\n' +
                    '        {{/if}}\n' +
                    '        {{#if}}\n' +
                    '            ^^^content$$$\n' +
                    '        {{/if}}\n' +
                    '    {{/each}}\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                unchanged: '{{#if 1}}\n' +
                    '    <div>\n' +
                    '    </div>\n' +
                    '{{/if}}'
            },

            // Test {{else}} aligned with {{#if}} and {{/if}}
            {
                fragment: true,
                input_: '{{#if 1}}\n' +
                    '    ^^^content$$$\n' +
                    '    {{else}}\n' +
                    '    ^^^content$$$\n' +
                    '{{/if}}',
                output: '{{#if 1}}\n' +
                    '    ^^^content$$$\n' +
                    '{{else}}\n' +
                    '    ^^^content$$$\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                input_: '{{#if 1}}\n' +
                    '    {{else}}\n' +
                    '    {{/if}}',
                output: '{{#if 1}}\n' +
                    '{{else}}\n' +
                    '{{/if}}'
            }, {
                fragment: true,
                input_: '{{#if thing}}\n' +
                    '{{#if otherthing}}\n' +
                    '    ^^^content$$$\n' +
                    '    {{else}}\n' +
                    '^^^content$$$\n' +
                    '    {{/if}}\n' +
                    '       {{else}}\n' +
                    '^^^content$$$\n' +
                    '{{/if}}',
                output: '{{#if thing}}\n' +
                    '    {{#if otherthing}}\n' +
                    '        ^^^content$$$\n' +
                    '    {{else}}\n' +
                    '        ^^^content$$$\n' +
                    '    {{/if}}\n' +
                    '{{else}}\n' +
                    '    ^^^content$$$\n' +
                    '{{/if}}'
            },
            // Test {{}} inside of <> tags, which should be separated by spaces
            // for readability, unless they are inside a string.
            {
                fragment: true,
                input_: '<div{{somestyle}}></div>',
                output: '<div {{somestyle}}></div>'
            }, {
                fragment: true,
                input_: '<div{{#if test}}class="foo"{{/if}}>^^^content$$$</div>',
                output: '<div {{#if test}} class="foo" {{/if}}>^^^content$$$</div>'
            }, {
                fragment: true,
                input_: '<div{{#if thing}}{{somestyle}}class="{{class}}"{{else}}class="{{class2}}"{{/if}}>^^^content$$$</div>',
                output: '<div {{#if thing}} {{somestyle}} class="{{class}}" {{else}} class="{{class2}}" {{/if}}>^^^content$$$</div>'
            }, {
                fragment: true,
                input_: '<span{{#if condition}}class="foo"{{/if}}>^^^content$$$</span>',
                output: '<span {{#if condition}} class="foo" {{/if}}>^^^content$$$</span>'
            }, {
                fragment: true,
                unchanged: '<div unformatted="{{#if}}^^^content$$${{/if}}">^^^content$$$</div>'
            }, {
                fragment: true,
                unchanged: '<div unformatted="{{#if  }}    ^^^content$$${{/if}}">^^^content$$$</div>'
            },

            // Quotes found inside of Handlebars expressions inside of quoted
            // strings themselves should not be considered string delimiters.
            {
                fragment: true,
                unchanged: '<div class="{{#if thingIs "value"}}^^^content$$${{/if}}"></div>'
            }, {
                fragment: true,
                unchanged: '<div class="{{#if thingIs \\\'value\\\'}}^^^content$$${{/if}}"></div>'
            }, {
                fragment: true,
                unchanged: '<div class=\\\'{{#if thingIs "value"}}^^^content$$${{/if}}\\\'></div>'
            }, {
                fragment: true,
                unchanged: '<div class=\\\'{{#if thingIs \\\'value\\\'}}^^^content$$${{/if}}\\\'></div>'
            }
        ],
    }, {
        name: "Handlebars Else tag indenting",
        description: "Handlebar Else tags should be newlined after formatted tags",
        template: "^^^ $$$",
        options: [
            { name: "indent_handlebars", value: "true" }
        ],
        tests: [{
            fragment: true,
            input_: '{{#if test}}<div></div>{{else}}<div></div>{{/if}}',
            output: '{{#if test}}\n' +
                '    <div></div>\n' +
                '{{else}}\n' +
                '    <div></div>\n' +
                '{{/if}}'
        }, {
            fragment: true,
            unchanged: '{{#if test}}<span></span>{{else}}<span></span>{{/if}}'
        }]
    }, {
        name: "Unclosed html elements",
        description: "Unclosed elements should not indent",
        options: [],
        tests: [
            { fragment: true, unchanged: '<source>\n<source>' },
            { fragment: true, unchanged: '<br>\n<br>' },
            { fragment: true, unchanged: '<input>\n<input>' },
            { fragment: true, unchanged: '<meta>\n<meta>' },
            { fragment: true, unchanged: '<link>\n<link>' },
            { fragment: true, unchanged: '<colgroup>\n    <col>\n    <col>\n</colgroup>' }
        ]
    }, {
        name: "Unformatted tags",
        description: "Unformatted tag behavior",
        options: [],
        tests: [
            { fragment: true, unchanged: '<ol>\n    <li>b<pre>c</pre></li>\n</ol>' },
            { fragment: true, unchanged: '<ol>\n    <li>b<code>c</code></li>\n</ol>' },
            { fragment: true, unchanged: '<ul>\n    <li>\n        <span class="octicon octicon-person"></span>\n        <a href="/contact/">Kontakt</a>\n    </li>\n</ul>' },
            { fragment: true, unchanged: '<div class="searchform"><input type="text" value="" name="s" id="s" /><input type="submit" id="searchsubmit" value="Search" /></div>' },
            { fragment: true, unchanged: '<div class="searchform"><input type="text" value="" name="s" id="s"><input type="submit" id="searchsubmit" value="Search"></div>' },
        ]
    }, {
        name: "Php formatting",
        description: "Php (<?php ... ?>) treated as comments.",
        options: [],
        tests: [{
            fragment: true,
            input: '<h1 class="content-page-header"><?=$view["name"]; ?></h1>',
            output: '<h1 class="content-page-header">\n    <?=$view["name"]; ?>\n</h1>',
        }, {
            fragment: true,
            unchanged: [
                '<?php',
                'for($i = 1; $i <= 100; $i++;) {',
                '    #count to 100!',
                '    echo($i . "</br>");',
                '}',
                '?>'
            ]
        }, {
            fragment: true,
            unchanged: [
                '<?php ?>',
                '<!DOCTYPE html>',
                '',
                '<html>',
                '',
                '<head></head>',
                '',
                '<body></body>',
                '',
                '</html>'
            ]
        }]
    }, {
        name: "underscore.js  formatting",
        description: "underscore.js templates (<% ... %>) treated as comments.",
        options: [],
        tests: [{
            fragment: true,
            unchanged: [
                '<div class="col-sm-9">',
                '    <textarea id="notes" class="form-control" rows="3">',
                '        <%= notes %>',
                '    </textarea>',
                '</div>'
            ]
        }, ]
    }, {
        name: "Indent with tabs",
        description: "Use one tab instead of several spaces for indentation",
        template: "^^^ $$$",
        options: [
            { name: "indent_with_tabs", value: "true" }
        ],
        tests: [{
            fragment: true,
            input_: '<div>\n' +
                '<div>\n' +
                '</div>\n' +
                '</div>',
            output: '<div>\n' +
                '\t<div>\n' +
                '\t</div>\n' +
                '</div>'
        }]
    }, {
        name: "Indent without tabs",
        description: "Use several spaces for indentation",
        template: "^^^ $$$",
        options: [
            { name: "indent_with_tabs", value: "false" }
        ],
        tests: [{
            fragment: true,
            input_: '<div>\n' +
                '<div>\n' +
                '</div>\n' +
                '</div>',
            output: '<div>\n' +
                '    <div>\n' +
                '    </div>\n' +
                '</div>'
        }]
    }, {
        name: "Indent body inner html by default",
        description: "",
        tests: [{
            fragment: true,
            input: '<html>\n<body>\n<div></div>\n</body>\n\n</html>',
            output: '<html>\n<body>\n    <div></div>\n</body>\n\n</html>'
        }]
    }, {
        name: "indent_body_inner_html set to false prevents indent of body inner html",
        description: "",
        options: [
            { name: 'indent_body_inner_html', value: "false" }
        ],
        tests: [{
            fragment: true,
            unchanged: '<html>\n<body>\n<div></div>\n</body>\n\n</html>'
        }]
    }, {
        name: "Indent head inner html by default",
        description: "",
        tests: [{
            fragment: true,
            input: '<html>\n\n<head>\n<meta>\n</head>\n\n</html>',
            output: '<html>\n\n<head>\n    <meta>\n</head>\n\n</html>'
        }]
    }, {
        name: "indent_head_inner_html set to false prevents indent of head inner html",
        description: "",
        options: [
            { name: 'indent_head_inner_html', value: "false" }
        ],
        tests: [{
            fragment: true,
            unchanged: '<html>\n\n<head>\n<meta>\n</head>\n\n</html>'
        }]
    }, {
        name: "New Test Suite"
    }],
};