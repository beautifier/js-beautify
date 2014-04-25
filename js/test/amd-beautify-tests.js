/*global js_beautify: true */
/*jshint node:true */

var requirejs = require('requirejs'),
    SanityTest = require('./sanitytest'),
    Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
    run_beautifier_tests = require('./beautify-tests').run_beautifier_tests;

requirejs.config({
	paths: {
	    'beautify': "..",
	    'beautify-lib': "../lib"
	}
});

function amd_beautifier_tests() {
    console.log('Testing with node.js Require.js...');
    var beautify = requirejs('beautify/index');
    var results = run_beautifier_tests(
            new SanityTest(),
            Urlencoded,
            beautify.js,
            beautify.html,
            beautify.css);
    console.log(results.results_raw());
    if (results.get_exitcode() !== 0) {
        return results;
    }
    
    var js_beautify = requirejs('beautify-lib/beautify'),
        css_beautify = requirejs('beautify-lib/beautify-css'),
        html_beautify = requirejs('beautify-lib/beautify-html');
    
    results = run_beautifier_tests(
            new SanityTest(),
            Urlencoded,
            js_beautify.js_beautify,
            html_beautify.html_beautify,
            css_beautify.css_beautify);
    console.log(results.results_raw());
    return results;
}

if (require.main === module) {
    process.exit(amd_beautifier_tests().results_raw());
}

exports.amd_beautifier_tests = amd_beautifier_tests;
