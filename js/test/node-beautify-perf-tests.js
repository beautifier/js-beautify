/*global js_beautify: true */
/*jshint node:true */
/*jshint unused:false */

'use strict';

var fs = require('fs'),
  SanityTest = require('./sanitytest'),
  Benchmark = require('benchmark'),
  Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
  beautifier = require('../src/index');

function node_beautifier_tests() {
  console.log('Testing performance...');
  var data = fs.readFileSync(__dirname + '/../../test/resources/underscore.js', 'utf8');
  var data_min = fs.readFileSync(__dirname + '/../../test/resources/underscore-min.js', 'utf8');
  var github_min = fs.readFileSync(__dirname + '/../../test/resources/github-min.js', 'utf8');
  var options = {
    wrap_line_length: 80
  };

  //warm-up
  beautifier.js(data, options);
  beautifier.js(data_min, options);

  var suite = new Benchmark.Suite();

  suite.add("js-beautify (underscore)", function() {
      beautifier.js(data, options);
    })
    .add("js-beautify (underscore-min)", function() {
      beautifier.js(data_min, options);
    })
    .add("js-beautify (github-min)", function() {
      beautifier.js(github_min, options);
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
  process.exit(node_beautifier_tests());
}
