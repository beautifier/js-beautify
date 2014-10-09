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
            var method = "t";
            var input = "''";
            if (typeof this.input === "string") {
                input = "'" + this.input.replace(/\n/g,'\\n') + "'";
            } else if (this.input instanceof Array) {
                input = "'" + this.input.join("\\n' +\n            '") + "'";

            } else if (typeof this.fragment === "string") {
                method = "t";
                input = "'" + this.fragment.replace(/\n/g,'\\n') + "'";
            } else if (this.fragment instanceof Array) {
                method = "t";
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
