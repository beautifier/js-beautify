/*jshint node:true */

'use strict';

var requirejs = require('requirejs'),
  SanityTest = require('./sanitytest'),
  Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
  run_javascript_tests = require('./generated/beautify-javascript-tests').run_javascript_tests,
  run_css_tests = require('./generated/beautify-css-tests').run_css_tests,
  run_html_tests = require('./generated/beautify-html-tests').run_html_tests;

requirejs.config({
  paths: {
    'beautify': "..",
    'beautify-lib': "../lib"
  }
});

function amd_beautifier_index_tests(name, test_runner) {
  console.log('Testing ' + name + ' with node.js Require.js (index)...');
  var results = new SanityTest();
  var beautify = requirejs('beautify/index');

  test_runner(
    results,
    Urlencoded,
    beautify.js,
    beautify.html,
    beautify.css);

  console.log(results.results_raw());
  return results.get_exitcode();
}

function amd_beautifier_bundle_tests(name, test_runner) {
  console.log('Testing ' + name + ' with node.js Require.js (bundle)...');
  var results = new SanityTest();
  var js_beautify = requirejs('beautify-lib/beautify'),
    css_beautify = requirejs('beautify-lib/beautify-css'),
    html_beautify = requirejs('beautify-lib/beautify-html');

  test_runner(
    results,
    Urlencoded,
    js_beautify.js_beautify,
    html_beautify.html_beautify,
    css_beautify.css_beautify);

  console.log(results.results_raw());
  return results.get_exitcode();
}



if (require.main === module) {
  var exit = 0;
  exit = exit || amd_beautifier_bundle_tests('js-beautifier', run_javascript_tests);
  exit = exit || amd_beautifier_bundle_tests('cs-beautifier', run_css_tests);
  exit = exit || amd_beautifier_bundle_tests('html-beautifier', run_html_tests);
  exit = exit || amd_beautifier_index_tests('js-beautifier', run_javascript_tests);
  exit = exit || amd_beautifier_index_tests('css-beautifier', run_css_tests);
  exit = exit || amd_beautifier_index_tests('html-beautifier', run_html_tests);

  process.exit(exit);
}
