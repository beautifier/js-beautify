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
            }
        ]
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
    }]
};
