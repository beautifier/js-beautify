# JS Beautifier
[![Build Status](https://api.travis-ci.org/beautify-web/js-beautify.svg?branch=master)](http://travis-ci.org/beautify-web/js-beautify)
[![Build status](https://ci.appveyor.com/api/projects/status/5bxmpvew5n3e58te/branch/master?svg=true)](https://ci.appveyor.com/project/beautify-web/js-beautify/branch/master)

[![PyPI version](https://img.shields.io/pypi/v/jsbeautifier.svg)](https://pypi.python.org/pypi/jsbeautifier)
[![CDNJS version](https://img.shields.io/cdnjs/v/js-beautify.svg)](https://cdnjs.com/libraries/js-beautify)
[![NPM version](https://img.shields.io/npm/v/js-beautify.svg)](https://www.npmjs.com/package/js-beautify)
[![Download stats](https://img.shields.io/npm/dm/js-beautify.svg)](https://www.npmjs.com/package/js-beautify)

[![Join the chat at https://gitter.im/beautify-web/js-beautify](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/beautify-web/js-beautify?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Twitter Follow](https://img.shields.io/twitter/follow/js_beautifier.svg?style=social&label=Follow)](https://twitter.com/intent/user?screen_name=js_beautifier)

[![NPM stats](https://nodei.co/npm/js-beautify.svg?downloadRank=true&downloads=true)](https://www.npmjs.org/package/js-beautify)


This little beautifier will reformat and re-indent bookmarklets, ugly
JavaScript, unpack scripts packed by Dean Edward’s popular packer,
as well as deobfuscate scripts processed by
[javascriptobfuscator.com](http://javascriptobfuscator.com/).

# Contributors Needed
I'm putting this front and center above because existing owners have very limited time to work on this project currently.
This is a popular project and widely used but it desperately needs contributors who have time to commit to fixing both
customer facing bugs and underlying problems with the internal design and implementation.  

If you are interested, please take a look at the [CONTRIBUTING.md](https://github.com/beautify-web/js-beautify/blob/master/CONTRIBUTING.md) then fix an issue marked with the ["Good first issue"](https://github.com/beautify-web/js-beautify/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) label and submit a PR. Repeat as often as possible.  Thanks!


# Usage
You can beautify javascript using JS Beautifier in your web browser, or on the command-line using node.js or python.

JS Beautifier is hosted on two CDN services: [cdnjs](https://cdnjs.com/libraries/js-beautify) and rawgit.

To pull from one of these services include one set of the script tags below in your document:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify-css.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify-html.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify-css.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.7.5/beautify-html.min.js"></script>

<script src="https://cdn.rawgit.com/beautify-web/js-beautify/v1.7.5/js/lib/beautify.js"></script>
<script src="https://cdn.rawgit.com/beautify-web/js-beautify/v1.7.5/js/lib/beautify-css.js"></script>
<script src="https://cdn.rawgit.com/beautify-web/js-beautify/v1.7.5/js/lib/beautify-html.js"></script>
```
Disclaimer: These are free services, so there are [no uptime or support guarantees](https://github.com/rgrove/rawgit/wiki/Frequently-Asked-Questions#i-need-guaranteed-100-uptime-should-i-use-cdnrawgitcom).

## Web Browser
Open [jsbeautifier.org](http://jsbeautifier.org/).  Options are available via the UI.

## Python
To beautify using python:

```bash
$ pip install jsbeautifier
$ js-beautify file.js
```

Beautified output goes to `stdout`.

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
opts.space_in_empty_paren = True
res = jsbeautifier.beautify('some javascript', opts)
```
The configuration option names are the same as the CLI names but with underscores instead of dashes.  The example above would be set on the command-line as `--indent-size 2 --space-in-empty-paren`.


## JavaScript

As an alternative to the Python script, you may install the NPM package `js-beautify`. When installed globally, it provides an executable `js-beautify` script. As with the Python script, the beautified result is sent to `stdout` unless otherwise configured.

```bash
$ npm -g install js-beautify
$ js-beautify foo.js
```

You can also use `js-beautify` as a `node` library (install locally, the `npm` default):

```bash
$ npm install js-beautify
```

Import and call the appropriate beautifier method for javascript (js), css, or html.  All three method signatures are `beautify(code, options)`. `code` is the string of code to be beautified. options is an object with the settings you would like used to beautify the code.  

The configuration option names are the same as the CLI names but with underscores instead of dashes.  For example, `--indent-size 2 --space-in-empty-paren` would be `{ indent_size: 2, space_in_empty_paren: true }`.

```js
var beautify = require('js-beautify').js,
    fs = require('fs');

fs.readFile('foo.js', 'utf8', function (err, data) {
    if (err) {
        throw err;
    }
    console.log(beautify(data, { indent_size: 2, space_in_empty_paren: true }));
});
```


## Options

These are the command-line flags for both Python and JS scripts:

```text
CLI Options:
  -f, --file       Input file(s) (Pass '-' for stdin)
  -r, --replace    Write output in-place, replacing input
  -o, --outfile    Write output to file (default stdout)
  --config         Path to config file
  --type           [js|css|html] ["js"]
  -q, --quiet      Suppress logging to stdout
  -h, --help       Show this help
  -v, --version    Show the version

Beautifier Options:
  -s, --indent-size                 Indentation size [4]
  -c, --indent-char                 Indentation character [" "]
  -t, --indent-with-tabs            Indent with tabs, overrides -s and -c
  -e, --eol                         Character(s) to use as line terminators.
                                    [first newline in file, otherwise "\n]
  -n, --end-with-newline            End output with newline
  --editorconfig                    Use EditorConfig to set up the options
  -l, --indent-level                Initial indentation level [0]
  -p, --preserve-newlines           Preserve line-breaks (--no-preserve-newlines disables)
  -m, --max-preserve-newlines       Number of line-breaks to be preserved in one chunk [10]
  -P, --space-in-paren              Add padding spaces within paren, ie. f( a, b )
  -E, --space-in-empty-paren        Add a single space inside empty paren, ie. f( )
  -j, --jslint-happy                Enable jslint-stricter mode
  -a, --space-after-anon-function   Add a space before an anonymous function's parens, ie. function ()
  -b, --brace-style                 [collapse|expand|end-expand|none][,preserve-inline] [collapse,preserve-inline]
  -u, --unindent-chained-methods    Don't indent chained method calls
  -B, --break-chained-methods       Break chained method calls across subsequent lines
  -k, --keep-array-indentation      Preserve array indentation
  -x, --unescape-strings            Decode printable characters encoded in xNN notation
  -w, --wrap-line-length            Wrap lines at next opportunity after N characters [0]
  -X, --e4x                         Pass E4X xml literals through untouched
  --good-stuff                      Warm the cockles of Crockford's heart
  -C, --comma-first                 Put commas at the beginning of new line instead of end
  -O, --operator-position           Set operator position (before-newline|after-newline|preserve-newline) [before-newline]
```

Which correspond to the underscored option keys for both library interfaces

**defaults per CLI options**
```json
{
    "indent_size": 4,
    "indent_char": " ",
    "indent_with_tabs": false,
    "eol": "\n",
    "end_with_newline": false,
    "indent_level": 0,
    "preserve_newlines": true,
    "max_preserve_newlines": 10,
    "space_in_paren": false,
    "space_in_empty_paren": false,
    "jslint_happy": false,
    "space_after_anon_function": false,
    "brace_style": "collapse",
    "unindent_chained_methods": false,
    "break_chained_methods": false,
    "keep_array_indentation": false,
    "unescape_strings": false,
    "wrap_line_length": 0,
    "e4x": false,
    "comma_first": false,
    "operator_position": "before-newline"
}
```

**defaults not exposed in the cli**
```json
{
  "eval_code": false,
  "space_before_conditional": true
}
```

Notice not all defaults are exposed via the CLI.  Historically, the Python and
JS APIs have not been 100% identical. For example, `space_before_conditional` is
currently JS-only, and not addressable from the CLI script. There are still a
few other additional cases keeping us from 100% API-compatibility.


### Loading settings from environment or .jsbeautifyrc (JavaScript-Only)

In addition to CLI arguments, you may pass config to the JS executable via:

 * any `jsbeautify_`-prefixed environment variables
 * a `JSON`-formatted file indicated by the `--config` parameter
 * a `.jsbeautifyrc` file containing `JSON` data at any level of the filesystem above `$PWD`

Configuration sources provided earlier in this stack will override later ones.

### Setting inheritance and Language-specific overrides

The settings are a shallow tree whose values are inherited for all languages, but
can be overridden.  This works for settings passed directly to the API in either implementation.
In the Javascript implementation, settings loaded from a config file, such as .jsbeautifyrc, can also use inheritance/overriding.  

Below is an example configuration tree showing all the supported locations
for language override nodes.  We'll use `indent_size` to discuss how this configuration would behave, but any number of settings can be inherited or overridden:

```json
{
    "indent_size": 4,
    "html": {
        "end_with_newline": true,
        "js": {
            "indent_size": 2
        },
        "css": {
            "indent_size": 2
        }
    },
    "css": {
        "indent_size": 1
    },
    "js": {
       "preserve-newlines": true
    }
}
```

Using the above example would have the following result:

* HTML files
  * Inherit `indent_size` of 4 spaces from the top-level setting.  
  * The files would also end with a newline.
  * JavaScript and CSS inside HTML
    * Inherit the HTML `end_with_newline` setting.
    * Override their indentation to 2 spaces.
* CSS files
  * Override the top-level setting to an `indent_size` of 1 space.
* JavaScript files
  * Inherit `indent_size` of 4 spaces from the top-level setting.
  * Set `preserve-newlines` to `true`.

### CSS & HTML

In addition to the `js-beautify` executable, `css-beautify` and `html-beautify`
are also provided as an easy interface into those scripts. Alternatively,
`js-beautify --css` or `js-beautify --html` will accomplish the same thing, respectively.

```js
// Programmatic access
var beautify_js = require('js-beautify'); // also available under "js" export
var beautify_css = require('js-beautify').css;
var beautify_html = require('js-beautify').html;

// All methods accept two arguments, the string to be beautified, and an options object.
```

The CSS & HTML beautifiers are much simpler in scope, and possess far fewer options.

```text
CSS Beautifier Options:
  -s, --indent-size                  Indentation size [4]
  -c, --indent-char                  Indentation character [" "]
  -t, --indent-with-tabs             Indent with tabs, overrides -s and -c
  -e, --eol                          Character(s) to use as line terminators. (default newline - "\\n")
  -n, --end-with-newline             End output with newline
  -L, --selector-separator-newline   Add a newline between multiple selectors
  -N, --newline-between-rules        Add a newline between CSS rules

HTML Beautifier Options:
  -s, --indent-size                  Indentation size [4]
  -c, --indent-char                  Indentation character [" "]
  -t, --indent-with-tabs             Indent with tabs, overrides -s and -c
  -e, --eol                          Character(s) to use as line terminators. (default newline - "\\n")
  -n, --end-with-newline             End output with newline
  -p, --preserve-newlines            Preserve existing line-breaks (--no-preserve-newlines disables)
  -m, --max-preserve-newlines        Maximum number of line-breaks to be preserved in one chunk [10]
  -I, --indent-inner-html            Indent <head> and <body> sections. Default is false.
  -b, --brace-style                  [collapse-preserve-inline|collapse|expand|end-expand|none] ["collapse"]
  -S, --indent-scripts               [keep|separate|normal] ["normal"]
  -w, --wrap-line-length             Maximum characters per line (0 disables) [250]
  -A, --wrap-attributes              Wrap attributes to new lines [auto|force|force-aligned|force-expand-multiline] ["auto"]
  -i, --wrap-attributes-indent-size  Indent wrapped attributes to after N characters [indent-size] (ignored if wrap-attributes is "force-aligned")
  -U, --unformatted                  List of tags (defaults to inline) that should not be reformatted
  -T, --content_unformatted          List of tags (defaults to pre) whose content should not be reformatted
  -E, --extra_liners                 List of tags (defaults to [head,body,/html] that should have an extra newline before them.
  -K, --keep_collapsed_whitespace    Don't add a newline before tag which has a direct previous sibling tag. Default is false.
  --editorconfig                     Use EditorConfig to set up the options
```

## Directives to Ignore or Preserve sections (Javascript only)

Beautifier for  supports directives in comments inside the file.
This allows you to tell the beautifier to preserve the formatting of or completely ignore part of a file.
The example input below will remain changed after beautification

```js
// Use preserve when the content is not javascript, but you don't want it reformatted.
/* beautify preserve:start */
{
    browserName: 'internet explorer',
    platform:    'Windows 7',
    version:     '8'
}
/* beautify preserve:end */

// Use ignore when the content is not parsable as javascript.
var a =  1;
/* beautify ignore:start */
 {This is some strange{template language{using open-braces?
/* beautify ignore:end */
```

# License

You are free to use this in any way you want, in case you find this useful or working for you but you must keep the copyright notice and license. (MIT)

# Credits

* Created by Einar Lielmanis, <einar@jsbeautifier.org>
* Python version flourished by Stefano Sanfilippo <a.little.coder@gmail.com>
* Command-line for node.js by Daniel Stockman <daniel.stockman@gmail.com>
* Maintained and expanded by Liam Newman <bitwiseman@gmail.com>

Thanks also to Jason Diamond, Patrick Hof, Nochum Sossonko, Andreas Schneider, Dave
Vasilevsky, Vital Batmanov, Ron Baldwin, Gabriel Harrison, Chris J. Shull,
Mathias Bynens, Vittorio Gambaletta and others.

(README.md: js-beautify@1.7.5)
