exports.test_data = {
    default_options: [
        { name: "indent_size", value: "4" },
        { name: "indent_char", value: "' '" },
        { name: "preserve_newlines", value: "true" },
        { name: "jslint_happy", value: "false" },
        { name: "keep_array_indentation", value: "false" },
        { name: "brace_style", value: "'collapse'" },
        { name: "extra_liners", value: "['html', 'head', '/html']" }
    ],
    groups: [{
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
            { fragment: true, input: '', output: '{{eof}}' },
            { fragment: true, input: '<div></div>', output: '<div></div>{{eof}}' },
            // { fragment: true, input: '   \n\n<div></div>\n\n\n\n', output: '   <div></div>{{eof}}' },
            { fragment: true, input: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "Custom Extra Liners (empty)",
        description: "",
        matrix: [
            {
                options: [
                    { name: "extra_liners", value: "[]" }
                ]
            },

        ],
        tests: [
            {
                fragment: true,
                input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
                output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n        <p>x</p>\n    </div>\n</body>\n</html>'
            }
        ],
    }, {
        name: "Custom Extra Liners (default)",
        description: "",
        matrix: [
            {
                options: [
                    { name: "extra_liners", value: "null" }
                ]
            },

        ],
        tests: [
            {
                fragment: true,
                input: '<html><head></head><body></body></html>',
                output: '<html>\n\n<head></head>\n\n<body></body>\n\n</html>'
            }
        ],
    }, {
        name: "Custom Extra Liners (p, string)",
        description: "",
        matrix: [
            {
                options: [
                    { name: "extra_liners", value: "'p,/p'" }
                ]
            },

        ],
        tests: [
            {
                fragment: true,
                input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
                output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
            }
        ],
    }, {
        name: "Custom Extra Liners (p)",
        description: "",
        matrix: [
            {
                options: [
                    { name: "extra_liners", value: "['p', '/p']" }
                ]
            },

        ],
        tests: [
            {
                fragment: true,
                input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
                output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
            }
        ],
    }, {
        name: "Attribute Wrap",
        description: "Wraps attributes inside of html tags",
        matrix: [
          {
              options: [
                  { name: "wrap_attributes", value: "'force'" }
              ],
              eof: '\\n',
              indent_attr: '    ',
              over80: '\\n'
          }, {
              options: [
                  { name: "wrap_attributes", value: "'force'" },
                  { name: "wrap_line_length", value: "80" }
              ],
              eof: '\\n',
              indent_attr: '    ',
              over80: '\\n'
          }, {
              options: [
                  { name: "wrap_attributes", value: "'force'" },
                  { name: "wrap_attributes_indent_size", value: "8" },
              ],
              eof: '\\n',
              indent_attr: '        ',
              over80: '\\n'
          }, {
              options: [
                  { name: "wrap_attributes", value: "'auto'" },
                  { name: "wrap_line_length", value: "80" }
              ],
              eof: ' ',
              indent_attr: '',
              over80: '\\n'
          }, {
              options: [
                  { name: "wrap_attributes", value: "'auto'" },
                  { name: "wrap_line_length", value: "0" }
              ],
              eof: ' ',
              indent_attr: '',
              over80: ' '
          }
        ],
        tests: [
            {
                fragment: true,
                input: '<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>',
                output: '<div attr0{{eof}}{{indent_attr}}attr1="123"{{eof}}{{indent_attr}}data-attr2="hello    t here">This is some text</div>'
            },
            {
                fragment: true,
                input: '<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>',
                output: '<div lookatthissuperduperlongattributenamewhoahcrazy0="true"{{eof}}{{indent_attr}}attr0{{eof}}{{indent_attr}}attr1="123"{{eof}}{{indent_attr}}data-attr2="hello    t here"{{over80}}{{indent_attr}}heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>'
            },
            {
                fragment: true,
                input: '<img attr0 attr1="123" data-attr2="hello    t here"/>',
                output: '<img attr0{{eof}}{{indent_attr}}attr1="123"{{eof}}{{indent_attr}}data-attr2="hello    t here" />'
            },
            {
                input: '<?xml version="1.0" encoding="UTF-8" ?><root attr1="foo" attr2="bar"/>',
                output: '<?xml version="1.0" encoding="UTF-8" ?>{{eof}}<root attr1="foo"{{eof}}{{indent_attr}}attr2="bar"/>'
            }
        ]
    }, {
        name: "Handlebars Indenting Off",
        description: "Test handlebar behavior when indenting is off",
        template: "^^^ $$$",
        options: [
            { name: "indent_handlebars", value: "false" }
        ],
        tests: [
            { fragment: true,
                input_:
                '{{#if 0}}\n' +
                '    <div>\n' +
                '    </div>\n' +
                '{{/if}}',
                output:
                '{{#if 0}}\n' +
                '<div>\n' +
                '</div>\n' +
                '{{/if}}' },
            { fragment: true,
                input_:
                '<div>\n' +
                '{{#each thing}}\n' +
                '    {{name}}\n' +
                '{{/each}}\n' +
                '</div>',
                output:
                '<div>\n' +
                '    {{#each thing}} {{name}} {{/each}}\n' +
                '</div>'}

        ]
    }, {
        name: "Handlebars Indenting On",
        description: "Test handlebar formatting",
        template: "^^^ $$$",
        matrix: [
            {
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
            }
            , {
                options: [
                    { name: "indent_handlebars", value: "true" }
                ],
                content: '{{! \\n mult-line\\ncomment  \\n     with spacing\\n}}'
            }
        ],
        tests: [
            { fragment: true, unchanged: '{{#if 0}}{{/if}}' },
            { fragment: true, unchanged: '{{#if 0}}^^^content$$${{/if}}' },
            { fragment: true, unchanged: '{{#if 0}}\n{{/if}}' },
            { fragment: true,
                input_: '{{#if     words}}{{/if}}',
                output: '{{#if words}}{{/if}}' },
            { fragment: true,
                input_: '{{#if     words}}^^^content$$${{/if}}',
                output: '{{#if words}}^^^content$$${{/if}}' },
            { fragment: true,
                input_: '{{#if     words}}^^^content$$${{/if}}',
                output: '{{#if words}}^^^content$$${{/if}}' },
            { fragment: true,
                unchanged:
                '{{#if 1}}\n' +
                '    <div>\n' +
                '    </div>\n' +
                '{{/if}}' },
            { fragment: true,
                input_:
                '{{#if 1}}\n' +
                '<div>\n' +
                '</div>\n' +
                '{{/if}}',
                output:
                '{{#if 1}}\n' +
                '    <div>\n' +
                '    </div>\n' +
                '{{/if}}' },
            { fragment: true,
                unchanged:
                '<div>\n' +
                '    {{#if 1}}\n' +
                '    {{/if}}\n' +
                '</div>' },
            { fragment: true,
                input_:
                '<div>\n' +
                '{{#if 1}}\n' +
                '{{/if}}\n' +
                '</div>',
                output:
                '<div>\n' +
                '    {{#if 1}}\n' +
                '    {{/if}}\n' +
                '</div>' },
            { fragment: true,
                input_:
                '{{#if}}\n' +
                '{{#each}}\n' +
                '{{#if}}\n' +
                '^^^content$$$\n' +
                '{{/if}}\n' +
                '{{#if}}\n' +
                '^^^content$$$\n' +
                '{{/if}}\n' +
                '{{/each}}\n' +
                '{{/if}}',
                output:
                '{{#if}}\n' +
                '    {{#each}}\n' +
                '        {{#if}}\n' +
                '            ^^^content$$$\n' +
                '        {{/if}}\n' +
                '        {{#if}}\n' +
                '            ^^^content$$$\n' +
                '        {{/if}}\n' +
                '    {{/each}}\n' +
                '{{/if}}' },
            { fragment: true, unchanged: '{{#if 1}}\n' +
                '    <div>\n' +
                '    </div>\n' +
                '{{/if}}' },

            // Test {{else}} aligned with {{#if}} and {{/if}}
            { fragment: true,
                input_:
                '{{#if 1}}\n' +
                '    ^^^content$$$\n' +
                '    {{else}}\n' +
                '    ^^^content$$$\n' +
                '{{/if}}',
                output:
                '{{#if 1}}\n' +
                '    ^^^content$$$\n' +
                '{{else}}\n' +
                '    ^^^content$$$\n' +
                '{{/if}}' },
            { fragment: true,
                input_:
                '{{#if 1}}\n' +
                '    {{else}}\n' +
                '    {{/if}}',
                output:
                '{{#if 1}}\n' +
                '{{else}}\n' +
                '{{/if}}' },
            { fragment: true,
                input_:
                '{{#if thing}}\n' +
                '{{#if otherthing}}\n' +
                '    ^^^content$$$\n' +
                '    {{else}}\n' +
                '^^^content$$$\n' +
                '    {{/if}}\n' +
                '       {{else}}\n'+
                '^^^content$$$\n' +
                '{{/if}}',
                output:
                '{{#if thing}}\n' +
                '    {{#if otherthing}}\n' +
                '        ^^^content$$$\n' +
                '    {{else}}\n' +
                '        ^^^content$$$\n' +
                '    {{/if}}\n' +
                '{{else}}\n'+
                '    ^^^content$$$\n' +
                '{{/if}}' },
                // Test {{}} inside of <> tags, which should be separated by spaces
                // for readability, unless they are inside a string.
            { fragment: true,
                input_: '<div{{somestyle}}></div>',
                output: '<div {{somestyle}}></div>' },
            { fragment: true,
                input_: '<div{{#if test}}class="foo"{{/if}}>^^^content$$$</div>',
                output: '<div {{#if test}} class="foo" {{/if}}>^^^content$$$</div>' },
            { fragment: true,
                input_: '<div{{#if thing}}{{somestyle}}class="{{class}}"{{else}}class="{{class2}}"{{/if}}>^^^content$$$</div>',
                output: '<div {{#if thing}} {{somestyle}} class="{{class}}" {{else}} class="{{class2}}" {{/if}}>^^^content$$$</div>' },
            { fragment: true,
                input_: '<span{{#if condition}}class="foo"{{/if}}>^^^content$$$</span>',
                output: '<span {{#if condition}} class="foo" {{/if}}>^^^content$$$</span>' },
            { fragment: true,
                unchanged: '<div unformatted="{{#if}}^^^content$$${{/if}}">^^^content$$$</div>' },
            { fragment: true,
                unchanged: '<div unformatted="{{#if  }}    ^^^content$$${{/if}}">^^^content$$$</div>' },

            // Quotes found inside of Handlebars expressions inside of quoted
            // strings themselves should not be considered string delimiters.
            { fragment: true,
                unchanged: '<div class="{{#if thingIs "value"}}^^^content$$${{/if}}"></div>' },
            { fragment: true,
                unchanged: '<div class="{{#if thingIs \\\'value\\\'}}^^^content$$${{/if}}"></div>' },
            { fragment: true,
                unchanged: '<div class=\\\'{{#if thingIs "value"}}^^^content$$${{/if}}\\\'></div>' },
            { fragment: true,
                unchanged: '<div class=\\\'{{#if thingIs \\\'value\\\'}}^^^content$$${{/if}}\\\'></div>' }
        ],
    }, {
        name: "Unformatted tags",
        description: "Unformatted tag behavior",
        options: [],
        tests: [
            { fragment: true, input: '<ol>\n    <li>b<pre>c</pre></li>\n</ol>' },
            { fragment: true, input: '<ol>\n    <li>b<code>c</code></li>\n</ol>' },
        ]
    }, {
        name: "New Test Suite"
    }],
};
