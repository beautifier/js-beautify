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
  var github_html = fs.readFileSync(__dirname + '/../../test/resources/github.html', 'utf8');
  var index_html = fs.readFileSync(__dirname + '/../../index.html', 'utf8');
  var data_attr = fs.readFileSync(__dirname + '/../../test/resources/html-with-base64image.html', 'utf8');
  var options = {
    wrap_line_length: 80
  };

  //warm-up
  beautifier.html(github_html, options);
  beautifier.html(data_attr, options);

  var suite = new Benchmark.Suite();

  suite.add("html-beautify (index.html)", function() {
      beautifier.html(index_html, options);
    })
    .add("html-beautify (base64 image)", function() {
      beautifier.html(data_attr, options);
    })
    .add("html-beautify (github.html)", function() {
      beautifier.html(github_html, options);
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
