# Changelog
## v1.5.1

### Description
Highlights:
* Fixes var declaration of objects and arrays to indent correctly (#256, #430)
* Support keywords as IdentifierNames such as foo.catch() (#309, #351,#368, #378)
* Improved indenting for statements (#289)
* Improved ES6 support - let, const, template strings, and "fat arrow"
* Support for non-ASCII characters in variable names (#305)
* Multiple fixes to requirejs support and added tests to protect in future
* Improved LESS support (still plenty of room for improvement in this area)
* Do not add space after !!

https://github.com/einars/js-beautify/compare/v1.4.2...v1.5.1

### Closed Issues
* Nested if statements not displayed correctly ([#450](https://github.com/beautify-web/js-beautify/issues/450))
* preserve_newlines always true ([#449](https://github.com/beautify-web/js-beautify/issues/449))
* line wrapping breaks in weird places ([#438](https://github.com/beautify-web/js-beautify/issues/438))
* Update dependencies to current versions ([#437](https://github.com/beautify-web/js-beautify/pull/437))
* Add support for ES6 template strings ([#434](https://github.com/beautify-web/js-beautify/pull/434))
* Fix #402: support ES6 fat arrow ([#433](https://github.com/beautify-web/js-beautify/pull/433))
* Ending brace missaligned when part of first definition in var line ([#430](https://github.com/beautify-web/js-beautify/issues/430))
* fixing disabled line wrapping for HTML ([#429](https://github.com/beautify-web/js-beautify/pull/429))
* Missing semi colon ([#420](https://github.com/beautify-web/js-beautify/issues/420))
* Fixed require.js support ([#416](https://github.com/beautify-web/js-beautify/pull/416))
* should not split the es6 operator '=>' ([#402](https://github.com/beautify-web/js-beautify/issues/402))
* fixed relative paths for require.js ([#387](https://github.com/beautify-web/js-beautify/pull/387))
* Support reserved words as property names ([#378](https://github.com/beautify-web/js-beautify/issues/378))
* Make the AMD API match the rest of the APIs ([#376](https://github.com/beautify-web/js-beautify/pull/376))
* Preserve newlines in html related to issue #307 ([#375](https://github.com/beautify-web/js-beautify/pull/375))
* Multi-line statements ([#374](https://github.com/beautify-web/js-beautify/issues/374))
* Reserved words used as property/function/variable identifiers are formatted incorrectly ([#368](https://github.com/beautify-web/js-beautify/issues/368))
* fixed problems with colon character ([#363](https://github.com/beautify-web/js-beautify/pull/363))
* require.JS paths are hardcoded in beautify-html.js  ([#359](https://github.com/beautify-web/js-beautify/issues/359))
* Regression in p.a.c.ked file detection ([#357](https://github.com/beautify-web/js-beautify/issues/357))
* Fix Issue #339 ([#354](https://github.com/beautify-web/js-beautify/pull/354))
* Added single line comment support in less/sass for javascript parser ([#353](https://github.com/beautify-web/js-beautify/pull/353))
* Function named 'in' not formatting correctly ([#351](https://github.com/beautify-web/js-beautify/issues/351))
* CSS Pseudo element ([#346](https://github.com/beautify-web/js-beautify/issues/346))
* array closing brace error for return statements with keep_array_indentation ([#340](https://github.com/beautify-web/js-beautify/issues/340))
* CSS Beautifier: breaks :before and :after (regression) ([#339](https://github.com/beautify-web/js-beautify/issues/339))
* Publish v1.5.0  ([#335](https://github.com/beautify-web/js-beautify/issues/335))
* "keep array indentation" not working ([#333](https://github.com/beautify-web/js-beautify/issues/333))
* CSS Beautifier: support LESS/SASS line comments ([#326](https://github.com/beautify-web/js-beautify/issues/326))
* Incorrect formating with semicolon-less code ([#323](https://github.com/beautify-web/js-beautify/issues/323))


## v1.4.2 

### Description
Release quick fix for python errno error that has started being more heavily reported
Initial release of css beautifier ported to python
Additional minor fixes and enhancements



### Closed Issues
* global name 'errno' is not defined ([#352](https://github.com/beautify-web/js-beautify/issues/352))
* import errno for errno.EEXIST ([#349](https://github.com/beautify-web/js-beautify/pull/349))
* Added bower.json ([#343](https://github.com/beautify-web/js-beautify/pull/343))
* HTML wrap-line-length: 0 doesn't work ([#342](https://github.com/beautify-web/js-beautify/issues/342))
* Make beautify.js, beautify-html.js, beautify-css.js available in bower ([#341](https://github.com/beautify-web/js-beautify/issues/341))
* Making .jsbeautifyrc resolve work (in general and for Windows re home dir) ([#334](https://github.com/beautify-web/js-beautify/pull/334))
* windows 8 error: path.js:204         throw new TypeError('Arguments to path.join must be strings'); ([#300](https://github.com/beautify-web/js-beautify/issues/300))
* Port beautify-css to python ([#204](https://github.com/beautify-web/js-beautify/issues/204))


## v1.4.1

### Description
Incremental fixes and improvements 


### Closed Issues
* Tests borked when running from web ([#332](https://github.com/beautify-web/js-beautify/issues/332))
* wrap_line_length isn't enforced for property values ([#331](https://github.com/beautify-web/js-beautify/issues/331))
* Have no empty line between comment and function ([#329](https://github.com/beautify-web/js-beautify/issues/329))
* Add new line at the end of the file (html-beautify) ([#325](https://github.com/beautify-web/js-beautify/issues/325))
* Space in empty parentheses ([#322](https://github.com/beautify-web/js-beautify/pull/322))
* Handlebars ([#321](https://github.com/beautify-web/js-beautify/pull/321))
* Space in empty parentheses ([#320](https://github.com/beautify-web/js-beautify/issues/320))
* The indent_with_tabs option did not work when required in node, only CLI. ([#319](https://github.com/beautify-web/js-beautify/pull/319))
* add option to indent "inner HTML"... ([#312](https://github.com/beautify-web/js-beautify/pull/312))
* Wrong format of HTML textnode containing multipe words ([#306](https://github.com/beautify-web/js-beautify/issues/306))
* Repair to work in windows ([#304](https://github.com/beautify-web/js-beautify/pull/304))
* make export object the same with common and amd methods ([#303](https://github.com/beautify-web/js-beautify/pull/303))
* jshint cleanup and make require.js optimizable ([#302](https://github.com/beautify-web/js-beautify/pull/302))
* E4X xml-literal allowed xml-characters ([#294](https://github.com/beautify-web/js-beautify/pull/294))
* Publish 1.4.1 ([#292](https://github.com/beautify-web/js-beautify/issues/292))
* Blank line inserted between function and preceding comment ([#291](https://github.com/beautify-web/js-beautify/issues/291))
* Add tests for beautify-html.js ([#211](https://github.com/beautify-web/js-beautify/issues/211))


## v1.4.0

### Description
Given the breadth of the changes in the code and api, bump to 1.4.0 for the next release.

https://github.com/einars/js-beautify/compare/v1.3.4...v1.4.0

### Closed Issues
* Fix major performance degradation from minimal indenting ([#288](https://github.com/beautify-web/js-beautify/issues/288))
* Minimal indenting ([#286](https://github.com/beautify-web/js-beautify/pull/286))
* Empty lines are removed in HTML and CSS, and also adds trailing spaces ([#285](https://github.com/beautify-web/js-beautify/issues/285))
* npmjs cli options incomplete ([#283](https://github.com/beautify-web/js-beautify/issues/283))
* Publish 1.4.0 ([#282](https://github.com/beautify-web/js-beautify/issues/282))
* Blocks, arrays, and expressions over indented ([#281](https://github.com/beautify-web/js-beautify/issues/281))
* Keeping New lines inside markup ([#280](https://github.com/beautify-web/js-beautify/issues/280))
* E4X xml-literal small fixes ([#279](https://github.com/beautify-web/js-beautify/pull/279))
* Add support for Asynchronous Module Definition (AMD) API ([#274](https://github.com/beautify-web/js-beautify/pull/274))
* fixed broken run tests script ([#255](https://github.com/beautify-web/js-beautify/pull/255))
* Ending parenthesis in function call ([#239](https://github.com/beautify-web/js-beautify/issues/239))
* Preventing line breaks around Unformatted tags ([#105](https://github.com/beautify-web/js-beautify/issues/105))
* IE conditional HTML comments don't play well with the rest of the document ([#91](https://github.com/beautify-web/js-beautify/issues/91))


## v1.3.4

### Description
1.3.3 introduced an change to function formatting.  This fixes primarily that but also a few other tweaks.

### Closed Issues
* Broken indentation ([#277](https://github.com/beautify-web/js-beautify/issues/277))
* Nested inline statements (if, while, do, for) should start new line ([#276](https://github.com/beautify-web/js-beautify/issues/276))
* Bare expression followed immediately by function definition should not indent ([#275](https://github.com/beautify-web/js-beautify/issues/275))
* bug fix for "js-beautify does not create directory automatically when use '-o' parameter" ([#272](https://github.com/beautify-web/js-beautify/pull/272))
* js-beautify does not create directory automatically when use '-o' parameter ([#270](https://github.com/beautify-web/js-beautify/issues/270))
* Problem with indentation inside function ([#268](https://github.com/beautify-web/js-beautify/issues/268))
* added a deindent() function . ([#267](https://github.com/beautify-web/js-beautify/pull/267))


## v1.3.3

### Description
Another good set of fixes. 

### Closed Issues
* Nested arrays indentation with --good-stuff ([#273](https://github.com/beautify-web/js-beautify/issues/273))
* Keep Array Indentation doesn't always work ([#263](https://github.com/beautify-web/js-beautify/issues/263))
* Whitespace issue with function call with object literal + other arguments. ([#262](https://github.com/beautify-web/js-beautify/issues/262))
* Implement wider fix to Indenting within parenthesis frames ([#259](https://github.com/beautify-web/js-beautify/issues/259))
* Block formatting within function call parameters. ([#258](https://github.com/beautify-web/js-beautify/issues/258))
* make python accept -w or --wrap-line-lengthmake python accept -w or --wrap-line-length ([#252](https://github.com/beautify-web/js-beautify/pull/252))
* Beautifying function call chains that end with a callback results in incorrect formatting ([#241](https://github.com/beautify-web/js-beautify/pull/241))
* Keeping New lines  ([#96](https://github.com/beautify-web/js-beautify/issues/96))


## v1.3.2

### Description
Seems like there are enough features on `master` to justify a patch revision. To wit:

* Removal of `expand-strict` value for `--brace-style` option.
* Added `--space-in-paren` option.
* E4X
* Functions as sub-array literals (#246)
* Minor updates to `p_a_c_k_e_r` unpacking.

https://github.com/einars/js-beautify/compare/v1.3.1...master

### Closed Issues
* Why removed support for global object? ([#249](https://github.com/beautify-web/js-beautify/issues/249))
* Incorrect indentation of functions in array ([#246](https://github.com/beautify-web/js-beautify/issues/246))
* E4X for Python ([#243](https://github.com/beautify-web/js-beautify/issues/243))
* Single line comments on "case:" lines forced to next line ([#242](https://github.com/beautify-web/js-beautify/issues/242))
* Remove expand-strict ([#240](https://github.com/beautify-web/js-beautify/pull/240))
* empty braces should always collapse to {} on the same line ([#237](https://github.com/beautify-web/js-beautify/issues/237))
* braces "expand-strict", return { } should be on same line ([#236](https://github.com/beautify-web/js-beautify/issues/236))
* Option for different formatting of spaces in parens ([#235](https://github.com/beautify-web/js-beautify/pull/235))
* E4X ([#234](https://github.com/beautify-web/js-beautify/pull/234))
* -h option in cli.js ([#233](https://github.com/beautify-web/js-beautify/pull/233))
* Globally installed npm js-beautify will never catch .jsbeautifyrc in /home ([#228](https://github.com/beautify-web/js-beautify/issues/228))
* html conditional tag treated as open tag "<!--[if IE 8]>" ([#222](https://github.com/beautify-web/js-beautify/issues/222))
* Document package release process ([#214](https://github.com/beautify-web/js-beautify/issues/214))
* Add basic tests for beautify command line ([#209](https://github.com/beautify-web/js-beautify/issues/209))
* Index.html - "Preserve empty lines" does not describe the behavior ([#199](https://github.com/beautify-web/js-beautify/issues/199))
* Bug: <![CDATA[ ([#152](https://github.com/beautify-web/js-beautify/issues/152))
* New options proposal: spaces around arguments ([#126](https://github.com/beautify-web/js-beautify/issues/126))
* Add option to put single-statement blocks into a new line ([#116](https://github.com/beautify-web/js-beautify/issues/116))
* [Feature request] --disable-preserve-newlines to one line ([#74](https://github.com/beautify-web/js-beautify/issues/74))


