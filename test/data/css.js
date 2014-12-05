exports.test_data = {
    default_options: [
        { name: "indent_size", value: "1" },
        { name: "indent_char", value: "'\\t'" },
        { name: "selector_separator_newline", value: "true" },
        { name: "end_with_newline", value: "false" },
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
            { fragment: '   .tabs{}', output: '   .tabs {}{{eof}}' },
            { fragment: '   \n\n.tabs{}\n\n\n\n', output: '   .tabs {}{{eof}}' },
            { fragment: '\n', output: '{{eof}}' }
        ],
    }, {
        name: "Empty braces",
        description: "",
        tests: [
            { input: '.tabs{}', output: '.tabs {}' },
            { input: '.tabs { }', output: '.tabs {}' },
            { input: '.tabs    {    }', output: '.tabs {}' },
            // When we support preserving newlines this will need to change
            { input: '.tabs    \n{\n    \n  }', output: '.tabs {}' }
        ],
    }, {
        name: "Functions braces",
        description: "",
        tests: [
            { input: '.tabs(){}', output: '.tabs() {}' },
            { input: '.tabs (pa, pa(1,2)), .cols { }', output: '.tabs (pa, pa(1, 2)),\n.cols {}' },
//          Still not supported to check if there are opening roundBracs after name
//          { input: '.tabs (   )   {    }', output: '.tabs() {}' },
            { input: '.tabs  (t, t2)  \n{\n  key: val(p1  ,p2);  \n  }', output: '.tabs (t, t2) {\n\tkey: val(p1, p2);\n}' }
        ],
    }, {

    }]
}
