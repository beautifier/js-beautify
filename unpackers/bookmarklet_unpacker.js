//
// trivial bookmarklet/escaped script detector for the javascript beautifier
// written by Einar Lielmanis <einar@jsbeautifier.org>
//
// usage:
//
// if (EscapedBookmarklet.detect(some_string)) {
//     var unpacked = EscapedBookmarklet.unpack(some_string);
// }
// 
//

var EscapedBookmarklet = {
    detect: function (str) {
        // the fact that script doesn't contain any space, but has %20 instead
        // should be sufficient check for now.
        return str.indexOf('%20') != -1 && str.indexOf(' ') == -1;
    },

    unpack: function (str) {
        if (EscapedBookmarklet.detect(str)) {
            return unescape(str);
        }
        return str;
    },



    run_tests: function (sanity_test) {
        var t = sanity_test || new SanityTest();
        t.test_function(EscapedBookmarklet.detect, "EscapedBookmarklet.detect");
        t.expect('', false);
        t.expect('var a = b', false);
        t.expect('var%20a=b', true);
        t.test_function(EscapedBookmarklet.unpack, 'EscapedBookmarklet.unpack');
        t.expect('', '');
        t.expect('abcd', 'abcd');
        t.expect('var a = b', 'var a = b');
        t.expect('var%20a=b', 'var a=b');
        return t;
    }


}
