# JS Beautifier

...or, more specifically, all of the code powering
[jsbeautifier.org](http://jsbeautifier.org/).

This little beautifier will reformat and reindent bookmarklets, ugly
JavaScript, unpack scripts packed by Dean Edward’s popular packer,
as well as deobfuscate scripts processed by
[javascriptobfuscator.com](http://javascriptobfuscator.com/).

## Usage

To beautify from the command-line you can use the provided Python script/library or [npm](http://npmjs.org/) package.

### Python

`./js-beautify file.js` beautifies a file, output goes to `stdout`.

To use `jsbeautifier` as a library is simple:

``` python
import jsbeautifier
res = jsbeautifier.beautify('your javascript string')
res = jsbeautifier.beautify_file('some_file.js')
```

...or, to specify some options:

``` python
opts = jsbeautifier.default_options()
opts.indent_size = 2
res = jsbeautifier.beautify('some javascript', opts)
```

### JavaScript

As an alternative to the Python script, you may install the NPM package `js-beautify`. When installed globally, it provides an executable `jsbeautify` script. As with the Python script, the beautified result is sent to `stdout` unless otherwise configured.

```js
jsbeautify foo.js
```

You can also use `js-beautify` as a `node` library:

```js
var beautify = require('js-beautify').js_beautify,
    fs = require('fs');

fs.readFile('foo.js', 'utf8', function (err, data) {
    if (err) {
        throw err;
    }
    console.log(beautify(data, { indent_size: 2 }));
});
```

### Options

These are the command-line flags for both Python and JS scripts:

    CLI Options:
      -f, --file                    Input file(s) (Pass '-' for stdin). These can also be passed directly.
      -r, --replace                 Write output in-place, replacing input
      -o, --outfile                 Write output to file (default stdout)
    
    Beautifier Options:
      -s, --indent-size             Indentation size [default: 4]
      -c, --indent-char             Indentation character [default: " "]
      -l, --indent-level            Initial indentation level [default: 0]
      -t, --indent-with-tabs        Indent with tabs, overrides -s and -c
      -p, --preserve-newlines       Preserve existing line-breaks (--no-preserve-newlines disables) [default: true]
      -m, --max-preserve-newlines   Maximum number of line-breaks to be preserved in one chunk [default: 10]
      -j, --jslint-happy            Enable jslint-stricter mode
      -b, --brace-style             Brace style [collapse|expand|end-expand|expand-strict] [default: "collapse"]
      -k, --keep-array-indentation  Preserve array indentation
      -a, --indent-case             Indent case inside switch
      -x, --unescape-strings        Decode printable characters encoded in xNN notation

These correspond to underscored option keys for both library interfaces:

    defaults = {
        indent_size: 4,
        indent_char: " ",
        indent_level: 0,
        indent_with_tabs: false,
        preserve_newlines: true,
        max_preserve_newlines: 10,
        jslint_happy: false,
        brace_style: "collapse",
        keep_array_indentation: false,
        indent_case: false,
        unescape_strings: false
    }

## License

You are free to use this in any way you want, in case you find this
useful or working for you.

## Credits

Written by Einar Lielmanis, <einar@jsbeautifier.org>
Python version flourished by Stefano Sanfilippo <a.little.coder@gmail.com>

Thanks to Jason Diamond, Patrick Hof, Nochum Sossonko, Andreas Schneider, Dave
Vasilevsky, Vital Batmanov, Ron Baldwin, Gabriel Harrison, Chris J. Shull,
Mathias Bynens, Vittorio Gambaletta and others.
