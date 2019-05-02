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
  exit = exit || node_beautifier_index_tests('js-beautifier', run_javascript_tests);
  exit = exit || node_beautifier_index_tests('css-beautifier', run_css_tests);
  exit = exit || node_beautifier_index_tests('html-beautifier', run_html_tests);

  process.exit(exit);
}
