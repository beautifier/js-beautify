# JS Beautifier

...or, more specifically, all of the code powering
[jsbeautifier.org](http://jsbeautifier.org/).

This little beautifier will reformat and reindent bookmarklets, ugly
JavaScript, unpack scripts packed by Dean Edward’s popular packer,
as well as deobfuscate scripts processed by
[javascriptobfuscator.com](http://javascriptobfuscator.com/).

To beautify from the command-line you can use provided python script/library.

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

You are free to use this in any way you want, in case you find this
useful or working for you.

Written by Einar Lielmanis, <einar@jsbeautifier.org>
Python version flourished by Stefano Sanfilippo <a.little.coder@gmail.com>

Thanks to Jason Diamond, Patrick Hof, Nochum Sossonko, Andreas Schneider, Dave
Vasilevsky, Vital Batmanov, Ron Baldwin, Gabriel Harrison, Chris J. Hull,
Mathias Bynens and others.
