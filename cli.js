#!/usr/bin/env node

var fs = require('fs'),
    beautify = require('./beautify').js_beautify,
    options = {},
    argv = require('optimist')
        .usage("Reformat JS files in idiomatic style.\n\nUsage:\n  $0 [options] path/to/file [...]")
        .options({
            // cli options
            "f": {
                "alias": "file",
                "type": "string",
                "description": "Input file (Pass '-' for stdin)"
            },
            "i": {
                "alias": "in-place",
                "type": "boolean",
                "description": "Write output in-place (replacing input)"
            },
            "o": {
                "alias": "outfile",
                "type": "string",
                "description": "Write output to file (default stdout)"
            },
            // beautify options
            "s": {
                "alias": "indent-size",
                "type": "number",
                "default": 4,
                "description": "Indentation size"
            },
            "c": {
                "alias": "indent-char",
                "type": "string",
                "default": " ",
                "description": "Indentation character"
            },
            "l": {
                "alias": "indent-level",
                "type": "number",
                "default": 0,
                "description": "Initial indentation level"
            },
            "t": {
                "alias": "indent-with-tabs",
                "type": "boolean",
                "description": "Indent with tabs, overrides -s and -c"
            },
            "p": {
                "alias": "preserve-newlines",
                "type": "boolean",
                "default": true,
                "description": "Do not preserve existing line-breaks"
            },
            "m": {
                "alias": "max-preserve-newlines",
                "type": "number",
                "default": 10,
                "description": "Maximum number of line-breaks to be preserved in one chunk"
            },
            "j": {
                "alias": "jslint-happy",
                "type": "boolean",
                "description": "Enable jslint-stricter mode"
            },
            "b": {
                "alias": "brace-style",
                "type": "string",
                "default": "collapse",
                "description": "Brace style [collapse|expand|end-expand|expand-strict]"
            },
            "k": {
                "alias": "keep-array-indentation",
                "type": "boolean",
                "description": "Preserve array indentation"
            },
            "a": {
                "alias": "indent-case",
                "type": "boolean",
                "description": "Indent case inside switch"
            },
            "x": {
                "alias": "unescape-strings",
                "type": "boolean",
                "description": "Decode printable characters encoded in xNN notation"
            }
        })
        .check(function (argv) {
            if (argv.file) {
                // might pass multiple -f args
                if (Array.isArray(argv.file)) {
                    argv._ = argv._.concat(argv.file);
                }
                else {
                    argv._.push(argv.file);
                }
            }

            if (!argv._.length) {
                throw 'Must define at least one file.';
            }

            argv._.forEach(function (filepath) {
                try {
                    fs.statSync(filepath);
                } catch (err) {
                    throw 'Unable to open path "' + filepath + '"';
                }
            });
        })
        .argv;

if (argv["indent-with-tabs"]) {
    argv["indent-size"] = 1;
    argv["indent-char"] = "\t";
}

// translate dashed options into weird python underscored keys
Object.keys(argv).forEach(function (key) {
    if (key.length > 1) {
        options[key.replace(/-/g, '_')] = argv[key];
    }
});

argv._.forEach(function (filepath) {
    var data = '',
        stream = fs.createReadStream(filepath, { encoding: 'utf8' });

    stream.on('data', function (chunk) {
        data += chunk;
    });

    stream.on('end', function () {
        var pretty = beautify(data, options);
        console.log(pretty);
    });
});
