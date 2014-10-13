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
        name: "New Test Suite"
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
