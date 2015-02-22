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
            { fragment: '', output: '{{eof}}' },
            { fragment: '<div></div>', output: '<div></div>{{eof}}' },
            // { fragment: '   \n\n<div></div>\n\n\n\n', output: '   <div></div>{{eof}}' },
            { fragment: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "Attribute Wrap",
        description: "Wraps attributes inside of html tags",
        matrix: [
          {
              options: [
                  { name: "wrap_attributes", value: "true" }
              ],
              eof: '\\n',
              indent_attr: '    '
          }, {
              options: [
                  { name: "wrap_attributes", value: "true" },
                  { name: "wrap_indent", value: "8" },
              ],
              eof: '\\n',
              indent_attr: '        '
          }, {
              options: [
                  { name: "wrap_attributes", value: "false" }
              ],
              eof: ' ',
              indent_attr: ''
          }
        ],
        tests: [
            {
                fragment: '<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>',
                output: '<div attr0{{eof}}{{indent_attr}}attr1="123"{{eof}}{{indent_attr}}data-attr2="hello    t here">This is some text</div>'
            },
            {
                fragment: '<img attr0 attr1="123" data-attr2="hello    t here"/>',
                output: '<img attr0{{eof}}{{indent_attr}}attr1="123"{{eof}}{{indent_attr}}data-attr2="hello    t here" />'
            }
        ]
    }, {
        name: "New Test Suite"
    }]
};
