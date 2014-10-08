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
        name: "Common smoke tests",
        description: "",
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
            { input: '["a", "b"].join("")' }
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
    }],
    // utility mustache functions
    matrix_context_string: function() {
        var context = this;
        return function(text, render) {
            var outputs = [];
            // text is ignored for this
            for (var name in context) {
                if (name === 'options') {
                    continue;
                }

                if (context.hasOwnProperty(name)) {
                    outputs.push(name + ' = "' + context[name] + '"');
                }
            }
            return render(outputs.join(', '));
        }
    },
    test_line: function() {
        return function(text, render) {
            // text is ignored for this.
            var method = "bt";
            var input = "''";
            if (typeof this.input === "string") {
                input = "'" + this.input.replace(/\n/g,'\\n') + "'";
            } else if (this.input instanceof Array) {
                input = "'" + this.input.join("\\n' +\n            '") + "'";

            } else if (typeof this.fragment === "string") {
                method = "test_fragment";
                input = "'" + this.fragment.replace(/\n/g,'\\n') + "'";
            } else if (this.fragment instanceof Array) {
                method = "test_fragment";
                input = "'" + this.fragment.join("\\n' +\n            '") + "'";
            }
            input = render(input);

            var output = "";
            var before_output = "";
            if (typeof this.output === "string") {
                before_output = ', ';
                output =  "'" + this.output.replace(/\n/g,'\\n') + "'";
            } else if (this.output instanceof Array) {
                before_output = ',\n           ';
                output = "'" + this.output.join("\\n' +\n           '") + "'";
            }
            output = render(output);

            if (output === input) {
                output = "";
                before_output = "";
            }
            return  method + "(" + input + before_output + output + ")";
        }
    }
}
