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
            { fragment: '', output: '{{eof}}' },
            { fragment: '<div></div>', output: '<div></div>{{eof}}' },
            // { fragment: '   \n\n<div></div>\n\n\n\n', output: '   <div></div>{{eof}}' },
            { fragment: '\n', output: '{{eof}}' }
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
            { fragment: '<html><head><meta></head></html>', output: '<html>\n<head>\n    <meta>\n</head>\n</html>' }
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
            { fragment: '<html><head></head><body></body></html>', output: '<html>\n\n<head></head>\n\n<body></body>\n\n</html>' }
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
            { fragment: '<div><p>x</p></div>', output: '<div>\n\n    <p>x\n\n    </p>\n</div>' }
        ],
    }, {
        name: "New Test Suite"
    }]
}
