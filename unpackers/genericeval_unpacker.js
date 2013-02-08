//
// simple unpacker/deobfuscator for anything eval-based
//
// written by Einar Lielmanis <einar@jsbeautifier.org>
//
// usage:
//
// if (GenericEval.detect(some_string)) {
//     var unpacked = GenericEval.unpack(some_string);
// }
//
//

var GenericEval = {
    detect: function (str) {
        if (GenericEval.starts_with(str, 'eval(')) {
            return true;
        }
        return false;
    },

    unpack: function (str) {
        if (GenericEval.detect(str)) {
            var modified_source = 'eval = function (s) { unpacked_source += s; }\n' + str;
            var unpacked_source = '';
            eval(modified_source);
            return unpacked_source ? unpacked_source : str;
        }
        return str;
    },

    starts_with: function (str, what) {
        return str.substr(0, what.length) === what;
    },

    ends_with: function (str, what) {
        return str.substr(str.length - what.length, what.length) === what;
    },

    run_tests: function (sanity_test) {
        var t = sanity_test || new SanityTest();

        return t;
    }


}
