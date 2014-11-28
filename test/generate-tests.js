#!/usr/bin/env node
var fs = require('fs');
var mustache = require('mustache');

function generate_tests() {
    var test_data, template;

    // javascript
    test_data = require(__dirname + '/data/javascript.js').test_data;
    set_formatters(test_data, 'bt', '// ')
    template = fs.readFileSync(__dirname + '/template/node-javascript.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-javascript-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    set_formatters(test_data, 'bt', '# ')
    template = fs.readFileSync(__dirname + '/template/python-javascript.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../python/jsbeautifier/tests/testjsbeautifier.py', mustache.render(template, test_data), {encoding: 'utf-8'});

    // css
    test_data = require(__dirname + '/data/css.js').test_data;
    set_formatters(test_data, 't', '// ')
    template = fs.readFileSync(__dirname + '/template/node-css.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-css-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    set_formatters(test_data, 't', '# ')
    template = fs.readFileSync(__dirname + '/template/python-css.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../python/cssbeautifier/tests/test.py', mustache.render(template, test_data), {encoding: 'utf-8'});

    // html
    test_data = require(__dirname + '/data/html.js').test_data;
    set_formatters(test_data, 'bth', '// ')
    template = fs.readFileSync(__dirname + '/template/node-html.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-html-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    // no python html beautifier, so no tests
}

function set_formatters (data, test_method, comment_mark) {
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
                    outputs.push(name + ' = "' + context[name] + '"');
                }
            }
            return render(outputs.join(', '));
        }
    };

    data.test_line = function() {
        return function(text, render) {

            // text is ignored for this.
            var comment = "";
            if (typeof this.comment === "string") {
                comment = "\n        " + comment_mark + this.comment + '\n        ';
            } else if (this.comment instanceof Array) {
                comment = "\n        " + comment_mark + this.comment.join('\n        ' + comment_mark);
            }

            var input = "";
            var before_input = "";
            if (typeof this.input === "string") {
                before_input = test_method + "(";
                input = "'" + this.input.replace(/\n/g,'\\n').replace(/\t/g,'\\t') + "'";
            } else if (this.input instanceof Array) {
                before_input = test_method + "(\n            ";
                input = "'" + this.input.join("\\n' +\n            '").replace(/\t/g,'\\t') + "'";

            } else if (typeof this.fragment === "string") {
                before_input = "test_fragment(";
                input = "'" + this.fragment.replace(/\n/g,'\\n').replace(/\t/g,'\\t') + "'";
            } else if (this.fragment instanceof Array) {
                before_input = "test_fragment(\n            ";
                input = "'" + this.fragment.join("\\n' +\n            '").replace(/\t/g,'\\t') + "'";
            }
            input = render(input);

            var output = "";
            var before_output = "";
            if (typeof this.output === "string") {
                before_output = ', ';
                output =  "'" + this.output.replace(/\n/g,'\\n').replace(/\t/g,'\\t') + "'";
            } else if (this.output instanceof Array) {
                before_output = ',\n           ';
                output = "'" + this.output.join("\\n' +\n           '").replace(/\t/g,'\\t') + "'";
            }
            output = render(output);

            if (output === input) {
                output = "";
                before_output = "";
            }
            return  comment  + before_input + input + before_output + output + ")";
        }
    };
}

generate_tests();
