/*global js_beautify: true */
/*jshint node:true */

var requirejs = require('requirejs'),
    SanityTest = require('./sanitytest'),
    Urlencoded = require('../lib/unpackers/urlencode_unpacker'),
    run_beautifier_tests = require('./beautify-tests').run_beautifier_tests;

requirejs.config({
	paths: {
	    'beautify': "../lib"
	}
});

function amd_beautifier_tests(k) {
    requirejs([
        'beautify/beautify',
        'beautify/beautify-html',
        'beautify/beautify-css'],
    function(
        js_beautify,
        html_beautify,
        css_beautify)
    {
        var results = run_beautifier_tests(
            new SanityTest(),
            Urlencoded,
            js_beautify,
            html_beautify.html_beautify,
            css_beautify.css_beautify);
        
        console.log(results.results_raw());
        k(results);
    });
}

if (require.main === module) {
    amd_beautifier_tests(function(results) {
        process.exit(results.get_exitcode());
    });
}

exports.amd_beautifier_tests = amd_beautifier_tests;
