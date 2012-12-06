#!/usr/bin/env node

var debug = process.env.DEBUG_JSBEAUTIFY || process.env.JSBEAUTIFY_DEBUG
    ? function () { console.error.apply(console, arguments); }
    : function () {};

var fs = require('fs'),
    cc = require('config-chain'),
    beautify = require('./beautify').js_beautify,
    nopt = require('nopt'),
    path = require('path'),
    knownOpts = {
        // Beautifier
        "indent_size": Number,
        "indent_char": String,
        "indent_level": Number,
        "indent_with_tabs": Boolean,
        "preserve_newlines": Boolean,
        "max_preserve_newlines": Number,
        "jslint_happy": Boolean,
        "brace_style": ["collapse", "expand", "end-expand", "expand-strict"],
        "break_chained_methods": Boolean,
        "keep_array_indentation": Boolean,
        "unescape_strings": Boolean,
        // CLI
        "version": Boolean,
        "help": Boolean,
        "files": [path, Array],
        "outfile": path,
        "replace": Boolean,
        "config": path
    },
    // dasherizeShorthands provides { "indent-size": ["--indent_size"] }
    // translation, allowing more convenient dashes in CLI arguments
    shortHands = dasherizeShorthands({
        // Beautifier
        "s": ["--indent_size"],
        "c": ["--indent_char"],
        "l": ["--indent_level"],
        "t": ["--indent_with_tabs"],
        "p": ["--preserve_newlines"],
        "m": ["--max_preserve_newlines"],
        "j": ["--jslint_happy"],
        "b": ["--brace_style"],
        "B": ["--break_chained_methods"],
        "k": ["--keep_array_indentation"],
        "x": ["--unescape_strings"],
        // non-dasherized hybrid shortcuts
        "good-stuff": [
            "--keep_array_indentation",
            "--keep_function_indentation",
            "--jslint_happy"
        ],
        // CLI
        "v": ["--version"],
        "h": ["--help"],
        "f": ["--files"],
        "o": ["--outfile"],
        "r": ["--replace"]
        // no shorthand for "config"
    }),
    parsed = nopt(knownOpts, shortHands);

if (parsed.version) {
    console.log(require('./package.json').version);
    process.exit(0);
}
else if (parsed.help) {
    usage();
    process.exit(0);
}

var cfg = cc(
    parsed,
    cleanOptions(cc.env('jsbeautify_'), knownOpts),
    parsed.config,
    cc.find('.jsbeautifyrc'),
    __dirname + '/config/defaults.json'
).snapshot;

try {
    checkFiles(cfg);
    checkIndent(cfg);
    debug(cfg);
}
catch (ex) {
    debug(cfg);
    usage(ex);
    process.exit(1);
}


cfg.files.forEach(processInput, { cfg: cfg });


function usage(err) {
    var msg = [
        'js-beautify@' + require('./package.json').version,
        '',
        'CLI Options:',
        '  -f, --file                    Input file(s) (Pass \'-\' for stdin)',
        '  -r, --replace                 Write output in-place, replacing input',
        '  -o, --outfile                 Write output to file (default stdout)',
        '  --config                      Path to config file',
        '  -h, --help                    Show this help',
        '  -v, --version                 Show the version',
        '',
        'Beautifier Options:',
        '  -s, --indent-size             Indentation size [4]',
        '  -c, --indent-char             Indentation character [" "]',
        '  -l, --indent-level            Initial indentation level [0]',
        '  -t, --indent-with-tabs        Indent with tabs, overrides -s and -c',
        '  -p, --preserve-newlines       Preserve existing line-breaks (--no-preserve-newlines disables)',
        '  -m, --max-preserve-newlines   Number of line-breaks to be preserved in one chunk [10]',
        '  -j, --jslint-happy            Enable jslint-stricter mode',
        '  -b, --brace-style             [collapse|expand|end-expand|expand-strict] ["collapse"]',
        '  -B, --break-chained-methods   Break chained method calls across subsequent lines',
        '  -k, --keep-array-indentation  Preserve array indentation',
        '  -x, --unescape-strings        Decode printable characters encoded in xNN notation',
        '  -g, --good-stuff              Warm the cockles of Crockford\'s heart',
        ''
    ];

    if (err) {
        msg.push(err);
        msg.push('');
        console.error(msg.join('\n'));
    } else {
        console.log(msg.join('\n'));
    }
}

// main iterator, {cfg} passed as thisArg of forEach call
function processInput(filepath) {
    var data = '',
        config = this.cfg,
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
            outfile = config.outfile,
            output;

        // -o passed with no value overwrites
        if (outfile === true || config.replace) {
            outfile = filepath;
        }

        if (outfile) {
            output = fs.createWriteStream(outfile, {
                flags: "w",
                encoding: "utf8",
                mode: '644'
            });

            // catch possible errors
            output.on('error', onOutputError);
        } else {
            output = process.stdout;
        }

        // ensure newline at end of beautified output
        pretty += '\n';

        if (output.writable) {
            output.write(pretty);

            if (outfile) {
                output.end();
            }
        }
    });
}

// workaround the fact that nopt.clean doesn't return the object passed in :P
function cleanOptions(data, types) {
    nopt.clean(data, types);
    return data;
}

// error handler for output stream that swallows errors silently,
// allowing the loop to continue over unwritable files.
function onOutputError(err) {
    if (err.code === 'EACCES') {
        console.error(err.path + " is not writable. Skipping!");
    }
}

// turn "--foo_bar" into "foo-bar"
function dasherizeFlag(str) {
    return str.replace(/^\-+/, '').replace(/_/g, '-');
}

// translate weird python underscored keys into dashed argv,
// avoiding single character aliases.
function dasherizeShorthands(hash) {
    // operate in-place
    Object.keys(hash).forEach(function (key) {
        // each key value is an array
        var val = hash[key][0];
        // only dasherize one-character shorthands
        if (key.length === 1 && val.indexOf('_') > -1) {
            hash[dasherizeFlag(val)] = val;
        }
    });

    return hash;
}

function checkIndent(parsed) {
    if (parsed["indent_with_tabs"]) {
        parsed["indent_size"] = 1;
        parsed["indent_char"] = "\t";
    }

    return parsed;
}

function checkFiles(parsed) {
    var argv = parsed.argv;

    if (!parsed.files) {
        parsed.files = [];
    } else {
        if (argv.cooked.indexOf('-') > -1) {
            // strip stdin path eagerly added by nopt in '-f -' case
            parsed.files.some(removeDashedPath);
        }
    }

    if (argv.remain.length) {
        // assume any remaining args are files
        argv.remain.forEach(function (f) {
            parsed.files.push(path.resolve(f));
        });
    }

    if ('string' === typeof parsed.outfile && !parsed.files.length) {
        // use outfile as input when no other files passed in args
        parsed.files.push(parsed.outfile);
        // operation is now an implicit overwrite
        parsed.replace = true;
    }

    if (argv.original.indexOf('-') > -1) {
        // ensure '-' without '-f' still consumes stdin
        parsed.files.push('-');
    }

    if (!parsed.files.length) {
        throw 'Must define at least one file.';
    }

    parsed.files.forEach(testFilePath);

    return parsed;
}

function removeDashedPath(filepath, i, arr) {
    var found = filepath.lastIndexOf('-') === (filepath.length - 1);
    if (found) {
        arr.splice(i, 1);
    }
    return found;
}

function testFilePath(filepath) {
    try {
        if (filepath !== "-") {
            fs.statSync(filepath);
        }
    } catch (err) {
        throw 'Unable to open path "' + filepath + '"';
    }
}
