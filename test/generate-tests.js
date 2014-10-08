#!/usr/bin/env node
var fs = require('fs');
var mustache = require('mustache');

function generate_tests() {
    var test_data, template;
    test_data = require('./data.js').test_data;
    template = fs.readFileSync(__dirname + '/js-beautifier-node.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../js/test/beautify-tests.js', mustache.render(template, test_data), {encoding: 'utf-8'});

    template = fs.readFileSync(__dirname + '/js-beautifier-python.mustache', {encoding: 'utf-8'});
    fs.writeFileSync(__dirname + '/../python/jsbeautifier/tests/testjsbeautifier.py', mustache.render(template, test_data), {encoding: 'utf-8'});
}

generate_tests();
