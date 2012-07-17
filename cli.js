#!/usr/bin/env node

var fs = require('fs'),
    beautify = require('./beautify').js_beautify,
    config,
    options;

// only node v0.5+ can require json
if (parseFloat(process.version.substr(1)) < 0.5) {
    config  = JSON.parse(fs.readFileSync('./config/defaults.json', 'utf8'));
    options = JSON.parse(fs.readFileSync('./config/options.json', 'utf8'));
} else {
    config  = require('./config/defaults.json');
    options = require('./config/options.json');
}

var argv = require('optimist')
        .usage("Reformat JS files in idiomatic style.\n\nUsage:\n  $0 [options] path/to/file [...]")
        .options(options)
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

// translate dashed argv into weird python underscored keys,
// avoiding single character aliases.
Object.keys(argv).forEach(function (key) {
    if (key.length > 1) {
        config[key.replace(/-/g, '_')] = argv[key];
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
        var pretty = beautify(data, config),
            output;

        // -o passed with no value overwrites
        if (config.outfile === true || config.replace) {
            config.outfile = filepath;
        }

        if (config.outfile) {
            output = fs.createWriteStream(config.outfile, {
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

        if (config.outfile) {
            output.end();
        }
    });
});
