exports.test_data = {
    default_options: [
        {name: "indent_size", value: "4"},
        {name: "indent_char", value: "' '"},
        {name: "preserve_newlines", value: "true"},
        {name: "jslint_happy", value: "false"},
        {name: "keep_array_indentation", value: "false"},
        {name: "brace_style", value: "'collapse'"}
    ],
    tests: [{
        name: "Unicode Support",
        description: "",
        values: [
            {
                source: "var ' + unicode_char(3232) + '_' + unicode_char(3232) + ' = \"hi\";"
            }, {
                source: "var ' + unicode_char(228) + 'x = {\\n    ' + unicode_char(228) + 'rgerlich: true\\n};"
            }
        ],
    }, {
        name: "End With Newline ",
        description: "",
        options: [
            {name: "end_with_newline", value: "true"}
        ],
        fragments: [
            { source: '', output: '\\n' },
            { source: '   return .5', output: '   return .5\\n' },
            { source: '   \\n\\nreturn .5\\n\\n\\n\\n', output: '   return .5\\n' },
            { source: '\\n', output: '\\n' }
        ],
    }],
    // Example
    examples: [{
        name: "one",
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
    get_source: function() {
        if (typeof this.source === "string") {
            return "'" + this.source + "'";
        } else if (this.source instanceof Array) {
            return "'" + this.source.join("\\n' +\n            '") + "'";
        } else {
            return "''";
        }
    },
    get_output: function() {
        if (this.output  === this.source) {
            return "";
        }
        else if (typeof this.output === "string") {
            return ", '" + this.output + "'";
        } else if (this.output instanceof Array) {
            return ",\n           '" + this.output.join("\\n' +\n           '") + "'";
        } else {
            return "";
        }
    }
}
