/*global js_beautify: true */
/*jshint node:true */

var SanityTest = require('./sanitytest'),
    Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
    js_beautify = require('../index').js_beautify,
    run_beautifier_tests = require('./beautify-tests').run_beautifier_tests;

function node_beautifier_tests() {
    var results = run_beautifier_tests(new SanityTest(), Urlencoded, js_beautify);
    console.log(results.results_raw());
    return results;
}

if (require.main === module) {
    process.exit(node_beautifier_tests().get_exitcode());
}

exports.node_beautifier_tests = node_beautifier_tests;
