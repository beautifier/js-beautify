#!/usr/bin/env node

/*jshint node:true */

'use strict';

var SanityTest = require('./sanitytest'),
  Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
  run_javascript_tests = require('./generated/beautify-javascript-tests').run_javascript_tests,
  run_css_tests = require('./generated/beautify-css-tests').run_css_tests,
  run_html_tests = require('./generated/beautify-html-tests').run_html_tests;

function test_names() {
  var beautify = require('../index');
  var results = new SanityTest();

  console.log('Ensure all expected functions are defined');
  results.expect(typeof beautify.js, 'function');
  results.expect(typeof beautify.css, 'function');
  results.expect(typeof beautify.html, 'function');

  results.expect(typeof beautify.js.minify, 'function');
  results.expect(typeof beautify.css.minify, 'function');
  results.expect(typeof beautify.html.minify, 'function');

  console.log(results.results_raw());
  return results.get_exitcode();
}

function test_minify_output() {
  var beautify = require('../index');
  var results = new SanityTest();

  var html_source = '<head>\n<style>\n* {\nmargin: 0 auto;\n}\n</style>\n</head>\n<body>\n<p>example blah blah blah</p>\n</body>';
  var html_expected = '<head><style>* { margin: 0 auto; } </style></head><body><p>example blah blah blah</p></body>';

  results.expect(beautify.html.minify(html_source), html_expected);

  var css_source = '* {\nmargin: 0 auto;\npadding: 10px;\n}';
  var css_expected = '* { margin: 0 auto; padding: 10px; }';
  results.expect(beautify.css.minify(css_source), css_expected);

  var js_source = 'function f() {\n    return 1;\n}';
  var js_expected = 'function f() { return 1; }';
  results.expect(beautify.js.minify(js_source), js_expected);

  console.log(results.results_raw());
  return results.get_exitcode();
}

function node_beautifier_index_tests(name, test_runner) {
  console.log('Testing ' + name + ' with node.js CommonJS (src/index)...');
  var beautify = require('../src/index');

  var results = new SanityTest();
  test_runner(
    results,
    Urlencoded,
    beautify.js,
    beautify.html,
    beautify.css);

  console.log(results.results_raw());
  return results.get_exitcode();
}

if (require.main === module) {
  var exit = 0;
  exit = exit || test_names();
  exit = exit || test_minify_output();
  exit = exit || node_beautifier_index_tests('js-beautifier', run_javascript_tests);
  exit = exit || node_beautifier_index_tests('css-beautifier', run_css_tests);
  exit = exit || node_beautifier_index_tests('html-beautifier', run_html_tests);

  process.exit(exit);
}
