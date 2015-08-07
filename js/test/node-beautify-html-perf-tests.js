/*global js_beautify: true */
/*jshint node:true */

var fs = require('fs'),
    SanityTest = require('./sanitytest'),
    Benchmark = require('benchmark'),
    Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
    js_beautify = require('../index').js_beautify,
    css_beautify = require('../index').css_beautify,
    html_beautify = require('../index').html_beautify;

function node_beautifier_html_tests() {
    console.log('Testing performance...');
    var data_attr = fs.readFileSync(__dirname + '/../../test/base.64.still.almost.breaking.js', 'utf8');
    var options = {
        wrap_line_length: 80
    };

    //warm-up
    html_beautify(data_attr, options);
    
    var suite = new Benchmark.Suite;

    suite.add("html-beautify (base64 image)", function () {
        html_beautify(data_attr, options);
    })
    // add listeners
    .on('cycle', function(event) {
      console.log(String(event.target));
    })
    .on('error', function(event) {
      return 1;
    })
    .on('complete', function(event) {
    })
    .run()
    return 0;
}




if (require.main === module) {
    process.exit(node_beautifier_html_tests());
}
