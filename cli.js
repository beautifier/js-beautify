#!/usr/bin/env node

var fs = require('fs'),
    beautify = require('./beautify').js_beautify,
    options = require('./config/defaults'),
    argv = require('optimist')
        .usage("Reformat JS files in idiomatic style.\n\nUsage:\n  $0 [options] path/to/file [...]")
        .options(require('./config/options'))
        .check(function (argv) {
            if (argv.file) {
                if (Array.isArray(argv.file)) {
                    // might pass multiple -f args
                    argv._ = argv._.concat(argv.file);
                }
                else if ('string' === typeof argv.file) {
                    // `cat foo.js | cli.js -f -`, avoid ['-', true]
                    argv._.push(argv.file);
                }
            }

            if ('string' === typeof argv.outfile && !argv._.length) {
                // use outfile as input when no other files passed in args
                argv._.push(argv.outfile);
                // operation is now an implicit overwrite
                argv.replace = true;
            }

            if (!argv._.length) {
                throw 'Must define at least one file.';
            }

            argv._.forEach(function (filepath) {
                try {
                    if (filepath !== "-") {
                        fs.statSync(filepath);
                    }
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

// translate dashed options into weird python underscored keys,
// avoiding single character aliases.
Object.keys(argv).forEach(function (key) {
    if (key.length > 1) {
        options[key.replace(/-/g, '_')] = argv[key];
    }
});

argv._.forEach(function (filepath) {
    var data = '',
        input;

    if (filepath === '-') {
        input = process.stdin;
        input.resume();
        input.setEncoding('utf8');
    } else {
        input = fs.createReadStream(filepath, { encoding: 'utf8' });
    }

    input.on('data', function (chunk) {
        data += chunk;
    });

    input.on('end', function () {
        var pretty = beautify(data, options),
            output;

        // -o passed with no value overwrites
        if (options.outfile === true || options.replace) {
            options.outfile = filepath;
        }

        if (options.outfile) {
            output = fs.createWriteStream(options.outfile, {
                flags: "w",
                encoding: "utf8",
                mode: 0644
            });
        } else {
            output = process.stdout;
        }

        // ensure newline at end of beautified output
        pretty += '\n';

        output.write(pretty);

        if (options.outfile) {
            output.end();
        }
    });
});
