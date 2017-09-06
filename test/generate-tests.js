#!/usr/bin/env node

/*
  The MIT License (MIT)

  Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation files
  (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*/

var fs = require('fs');
var mustache = require('mustache');
var path = require('path');

function generate_tests() {
    // javascript
    generate_test_files('javascript', 'bt', 'js/test/generated/beautify-javascript-tests.js', 'python/jsbeautifier/tests/generated/tests.py');

    // css
    generate_test_files('css', 't', 'js/test/generated/beautify-css-tests.js', 'python/cssbeautifier/tests/generated/tests.py');

    // html
    // no python html beautifier, so no tests
    generate_test_files('html', 'bth', 'js/test/generated/beautify-html-tests.js');
}

function generate_test_files(data_folder, test_method, node_output, python_output) {
    var data_file_path, input_path, template_file_path;
    var test_data, template;

    input_path = path.resolve(__dirname, 'data', data_folder);
    data_file_path = path.resolve(input_path, 'tests.js');
    test_data = require(data_file_path).test_data;

    template_file_path = path.resolve(input_path, 'node.mustache');
    template = fs.readFileSync(template_file_path, { encoding: 'utf-8' });
    set_formatters(test_data, test_method, '// ');
    set_generated_header(test_data, data_file_path, template_file_path);
    fs.writeFileSync(path.resolve(__dirname, '..', node_output),
        mustache.render(template, test_data), { encoding: 'utf-8' });

    if (python_output) {
        template_file_path = path.resolve(input_path, 'python.mustache');
        template = fs.readFileSync(template_file_path, { encoding: 'utf-8' });
        set_formatters(test_data, test_method, '# ');
        set_generated_header(test_data, data_file_path, template_file_path);
        fs.writeFileSync(path.resolve(__dirname, '..', python_output),
            mustache.render(template, test_data), { encoding: 'utf-8' });
    }
}

function set_generated_header(data, data_file_path, template_file_path) {
    var relative_script_path = path.relative(process.cwd(), __filename).split(path.sep).join('/');
    var relative_data_file_path = path.relative(process.cwd(), data_file_path).split(path.sep).join('/');
    var relative_template_file_path = path.relative(process.cwd(), template_file_path).split(path.sep).join('/');

    data.header_text =
        '    AUTO-GENERATED. DO NOT MODIFY.\n' +
        '    Script: ' + relative_script_path + '\n' +
        '    Template: ' + relative_template_file_path + '\n' +
        '    Data: ' + relative_data_file_path;

}

function isStringOrArray(val) {
    return typeof val === 'string' || val instanceof Array;
}

function getTestString(val) {
    val = val.split('\n');

    var result = "'" + val.join("\\n' +\n            '").replace(/\t/g, '\\t') + "'";
    result = result.replace(/' \+\n            ''$/, "'");
    return result;
}

function set_formatters(data, test_method, comment_mark) {

    // utility mustache functions
    data.matrix_context_string = function() {
        var context = this;
        return function(text, render) {
            var outputs = [];
            // text is ignored for this
            for (var name in context) {
                if (name === 'options') {
                    continue;
                }

                if (context.hasOwnProperty(name)) {
                    outputs.push(name + ' = "' + context[name].replace(/\n/g, '\\n').replace(/\t/g, '\\t') + '"');
                }
            }
            return render(outputs.join(', '));
        };
    };

    data.test_line = function() {
        return function(text, render) {
            var method_text = this.fragment ? 'test_fragment' : test_method;
            var comment = '';
            var before_input = method_text + '(';
            var input = null;
            var before_output = ', ';
            var output = null;

            // text is ignored for this.
            if (typeof this.comment === 'string') {
                this.comment = this.comment.split('\n');
            }

            if (this.comment instanceof Array) {
                comment = '\n        ' + comment_mark + this.comment.join('\n        ' + comment_mark) + '\n        ';
            }

            // input: the default field
            // input_: allow underscore for formatting alignment with "output"
            // unchanged: use "unchanged" instead of "input" if there is no output
            input = this.input || this.input_ || this.unchanged;
            if (input instanceof Array) {
                input = input.join('\n');
            }

            if (isStringOrArray(this.output)) {
                output = this.output;
                if (output instanceof Array) {
                    output = output.join('\n');
                }
            }

            // Do all most error checking
            if (!(this.input !== null || this.input_ !== null || this.unchanged !== null)) {
                throw "Missing test input field (input, input_, or unchanged).";
            } else if ((this.input !== null && (this.input_ !== null || this.unchanged !== null)) &&
                (this.input_ === null || this.unchanged === null)) {
                throw "Only one test input field allowed (input, input_, or unchanged): " + input;
            } else if (output && isStringOrArray(this.unchanged)) {
                throw "Cannot specify 'output' with 'unchanged' test input: " + input;
            } else if (!output && !isStringOrArray(this.unchanged)) {
                throw "Neither 'output' nor 'unchanged' specified for test input: " + input;
            } else if (input === output) {
                // Raw input and output can be the same, just omit output.
                throw "Test strings are identical.  Omit 'output' and use 'unchanged': " + input;
            }

            if (output && output.indexOf('<%') !== -1) {
                mustache.tags = ['<%', '%>'];
            }

            input = getTestString(render(input));

            if (output) {
                output = getTestString(render(output));
            } else {
                output = '';
            }

            if (output && output.indexOf('<%') !== -1) {
                mustache.tags = ['{{', '}}'];
            }

            if (this.input_ || input.indexOf('\n') !== -1 || output.indexOf('\n') !== -1) {
                before_input = method_text + '(\n            ';
                before_output = ',\n            ' + comment_mark + ' -- output --\n            ';
            }
            if (output === '') {
                before_output = '';
            }

            // Rendered input and output can be the same, just omit output.
            if (output === input) {
                before_output = '';
                output = '';
            }
            return comment + before_input + input + before_output + output + ')';
        };
    };

    data.set_mustache_tags = function() {
        return function( /* text, render */ ) {
            if (this.template) {
                mustache.tags = this.template.split(' ');
            }
            return '';
        };
    };

    data.unset_mustache_tags = function() {
        return function( /* text , render */ ) {
            if (this.template) {
                mustache.tags = ['{{', '}}'];
            }
            return '';
        };
    };
}

generate_tests();