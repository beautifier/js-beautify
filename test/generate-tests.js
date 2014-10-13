#!/usr/bin/env node
var fs = require('fs');
var mustache = require('mustache');

function generate_tests() {
    var test_data, template;

    // javascript
    test_data = require(__dirname + '/data/javascript.js').test_data;
    template = fs.readFileSync(__dirname + '/template/node-javascript.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-javascript-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    template = fs.readFileSync(__dirname + '/template/python-javascript.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../python/jsbeautifier/tests/testjsbeautifier.py', mustache.render(template, test_data), {encoding: 'utf-8'});

    // css
    test_data = require(__dirname + '/data/css.js').test_data;
    template = fs.readFileSync(__dirname + '/template/node-css.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-css-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    template = fs.readFileSync(__dirname + '/template/python-css.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../python/cssbeautifier/tests/test.py', mustache.render(template, test_data), {encoding: 'utf-8'});

    // html
    test_data = require(__dirname + '/data/html.js').test_data;
    template = fs.readFileSync(__dirname + '/template/node-html.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-html-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    // no python html beautifier, so no tests
}

generate_tests();
