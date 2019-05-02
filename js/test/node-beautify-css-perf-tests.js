/*global js_beautify: true */
/*jshint node:true */
/*jshint unused:false */

'use strict';

var fs = require('fs'),
  SanityTest = require('./sanitytest'),
  Benchmark = require('benchmark'),
  Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
  beautifier = require('../src/index');

function node_beautifier_html_tests() {
  console.log('Testing performance...');
  var github_css = fs.readFileSync(__dirname + '/../../test/resources/github.css', 'utf8');
  var options = {
    wrap_line_length: 80
  };

  //warm-up
  beautifier.css(github_css, options);

  var suite = new Benchmark.Suite();

  suite.add("css-beautify (github.css)", function() {
      beautifier.css(github_css, options);
    })
    // add listeners
    .on('cycle', function(event) {
      console.log(String(event.target));
    })
    .on('error', function(event) {
      return 1;
    })
    .on('complete', function(event) {})
    .run();
  return 0;
}




if (require.main === module) {
  process.exit(node_beautifier_html_tests());
}
