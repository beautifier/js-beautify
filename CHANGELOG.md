# Changelog

## v1.14.7
* Doc: Updates web browser implementation examples ([#2107](https://github.com/beautify-web/js-beautify/pull/2107))
* HTML formatter breaks layout by introducing newlines ([#1989](https://github.com/beautify-web/js-beautify/issues/1989))

## v1.14.6
* Globs no longer work on Windows in 1.14.5 ([#2093](https://github.com/beautify-web/js-beautify/issues/2093))

## v1.14.5
* Dependency updates and UI tweaks ([#2088](https://github.com/beautify-web/js-beautify/pull/2088))
* Bump terser from 5.12.1 to 5.14.2 ([#2084](https://github.com/beautify-web/js-beautify/pull/2084))
* new layout breaks everything on long lines ([#2071](https://github.com/beautify-web/js-beautify/issues/2071))
* Dark mode ([#2057](https://github.com/beautify-web/js-beautify/issues/2057))

## v1.14.4
* Extra space before `!important` added ([#2056](https://github.com/beautify-web/js-beautify/issues/2056))
* css format removes space after quoted value  ([#2051](https://github.com/beautify-web/js-beautify/issues/2051))
* Add grid-template-areas to NON\_SEMICOLON\_NEWLINE\_PROPERTY list ([#2035](https://github.com/beautify-web/js-beautify/pull/2035))
* CSS formatter removes useful space ([#2024](https://github.com/beautify-web/js-beautify/issues/2024))
* CHANGELOG.md file was wiped out in v1.14.2 ([#2022](https://github.com/beautify-web/js-beautify/issues/2022))
* Fails to recognize Handlebars block with whitespace control, e.g. {{~#if true ~}} ([#1988](https://github.com/beautify-web/js-beautify/issues/1988))
* Support new sass `@use` syntax ([#1976](https://github.com/beautify-web/js-beautify/issues/1976))
* Do not remove whitespace after number ([#1950](https://github.com/beautify-web/js-beautify/issues/1950))
* html formatter doesn't support handlebars partial blocks (`#>`) ([#1869](https://github.com/beautify-web/js-beautify/issues/1869))
* in keyword in class method causes indentation problem ([#1846](https://github.com/beautify-web/js-beautify/issues/1846))
* space\_after\_named\_function not working inside an ES6 class ([#1622](https://github.com/beautify-web/js-beautify/issues/1622))
* Restyle website ([#1444](https://github.com/beautify-web/js-beautify/issues/1444))
* improper line concatenation between 'return' and a prefix expression ([#1095](https://github.com/beautify-web/js-beautify/issues/1095))

## v1.14.3
* [LESS] Fixing issues with spacing when an object literal lives inside a mixin ([#2017](https://github.com/beautify-web/js-beautify/pull/2017))
* Overindentation when using "class" as a key in an object ([#1838](https://github.com/beautify-web/js-beautify/issues/1838))
* CSS Grid template formatting is broken when adding track size after line names ([#1817](https://github.com/beautify-web/js-beautify/issues/1817))
* SCSS module system @use problem ([#1798](https://github.com/beautify-web/js-beautify/issues/1798))
* JS "space\_in\_empty\_paren" failing for class methods ([#1151](https://github.com/beautify-web/js-beautify/issues/1151))
* LESS mixins gets formatted strangely ([#722](https://github.com/beautify-web/js-beautify/issues/722))

## v1.14.2
* Why put npm in dependencies? ([#2005](https://github.com/beautify-web/js-beautify/issues/2005))
* [Bug] Logical assignments in JS are incorrectly beautified  ([#1991](https://github.com/beautify-web/js-beautify/issues/1991))

## v1.14.1
* feature request: cmd+enter hotkey for mac users ([#1985](https://github.com/beautify-web/js-beautify/issues/1985))
* Wrong indentation when the last line in a case is a right brace ([#1683](https://github.com/beautify-web/js-beautify/issues/1683))

## v1.14.0
* import.meta appears on newline ([#1978](https://github.com/beautify-web/js-beautify/issues/1978))
* Added buttons to website ([#1930](https://github.com/beautify-web/js-beautify/pull/1930))
* Logical assignment operators; Fix parsing of optional chaining ([#1888](https://github.com/beautify-web/js-beautify/issues/1888))
* Numbers should be allowed to contain underscores ([#1836](https://github.com/beautify-web/js-beautify/issues/1836))
* Use native mkdirSync instead of 'mkdirp' package ([#1833](https://github.com/beautify-web/js-beautify/pull/1833))
*  selector\_separator\_newline adds erroneous newline on @extend SCSS statements ([#1799](https://github.com/beautify-web/js-beautify/issues/1799))

## v1.13.13
* IE11 compatibility failure v>1.13.5 ([#1918](https://github.com/beautify-web/js-beautify/issues/1918))

## v1.13.11
* Support short PHP tags ([#1840](https://github.com/beautify-web/js-beautify/issues/1840))

## v1.13.6
* Fix space-before-conditional: false to work on switch-case statement ([#1881](https://github.com/beautify-web/js-beautify/pull/1881))
* Optional chaining obj?.[expr] ([#1801](https://github.com/beautify-web/js-beautify/issues/1801))

## v1.13.5

## v1.13.1
* Option 'max\_preserve\_newlines' not working on beautify\_css.js CSS Beautifier ([#1863](https://github.com/beautify-web/js-beautify/issues/1863))
* React Fragment Short Syntax <></> issue ([#1854](https://github.com/beautify-web/js-beautify/issues/1854))
* add  viewport meta tag to index.html ([#1843](https://github.com/beautify-web/js-beautify/pull/1843))
* Add basic smarty templating support ([#1820](https://github.com/beautify-web/js-beautify/issues/1820))
* Tagged Template literals ([#1244](https://github.com/beautify-web/js-beautify/issues/1244))

## v1.13.0
* (internal) Refactor python cssbeautifier to reuse jsbeautifier CLI methods ([#1832](https://github.com/beautify-web/js-beautify/pull/1832))
* (internal) Switch from node-static to serve ([#1831](https://github.com/beautify-web/js-beautify/pull/1831))
* Fixed pip install cssbeautifier ([#1830](https://github.com/beautify-web/js-beautify/pull/1830))

## v1.12.0
* Python jsbeautifier fails for special chars ([#1809](https://github.com/beautify-web/js-beautify/issues/1809))
* pip install cssbeautifier fails ([#1808](https://github.com/beautify-web/js-beautify/issues/1808))
* Add expand brace-style option to css beautifier ([#1796](https://github.com/beautify-web/js-beautify/pull/1796))
* Support nullish-coalescing ([#1794](https://github.com/beautify-web/js-beautify/issues/1794))
* Upgrade ga.js to analytics.js ([#1777](https://github.com/beautify-web/js-beautify/issues/1777))
* Newline rule not working with css-like files ([#1776](https://github.com/beautify-web/js-beautify/issues/1776))
* no new line after self closing tag ([#1718](https://github.com/beautify-web/js-beautify/issues/1718))
* HTML format, no break after <label>? ([#1365](https://github.com/beautify-web/js-beautify/issues/1365))
* Does this extension still supports applying Allman style to CSS? ([#1353](https://github.com/beautify-web/js-beautify/issues/1353))
* Add brace\_style option for CSS ([#1259](https://github.com/beautify-web/js-beautify/issues/1259))

## v1.11.0
* Please bump mkdirp to fix mkdirp@0.5.1 vulnerability ([#1768](https://github.com/beautify-web/js-beautify/issues/1768))
* Incorrect indentation of Handlebars inline partials ([#1756](https://github.com/beautify-web/js-beautify/issues/1756))
* Support optional-chaining ([#1727](https://github.com/beautify-web/js-beautify/issues/1727))
* Please support es module ([#1706](https://github.com/beautify-web/js-beautify/issues/1706))
* Support new js proposals: optional-chaining & pipeline-operator ([#1530](https://github.com/beautify-web/js-beautify/issues/1530))
* Optional <p> closing not implemented ([#1503](https://github.com/beautify-web/js-beautify/issues/1503))

## v1.10.3
* Unquoted href causes wrong indentation ([#1736](https://github.com/beautify-web/js-beautify/issues/1736))
* Broken private fields in classes (JS) ([#1734](https://github.com/beautify-web/js-beautify/issues/1734))
* Fix for python 2.7 and cli parameters ([#1712](https://github.com/beautify-web/js-beautify/pull/1712))
* Search (ctrl+f) works only in view field in CodeMirror ([#1696](https://github.com/beautify-web/js-beautify/issues/1696))

## v1.10.2
* Please update CodeMirror Addon ([#1695](https://github.com/beautify-web/js-beautify/issues/1695))
* Nested braces indentation ([#223](https://github.com/beautify-web/js-beautify/issues/223))

## v1.10.1
* javascript fails to format when <?php > is first text inside <script> tag ([#1687](https://github.com/beautify-web/js-beautify/issues/1687))
* 414 Request-URI Too Large ([#1640](https://github.com/beautify-web/js-beautify/issues/1640))

## v1.10.0
* beautifying scss selector with colon in it adds space ([#1667](https://github.com/beautify-web/js-beautify/issues/1667))
* Javascript multiline comments duplicates ([#1663](https://github.com/beautify-web/js-beautify/issues/1663))
* Tokenizer crashes if the input terminates with a dot character. ([#1658](https://github.com/beautify-web/js-beautify/issues/1658))
* stop reformatting valid css \\! into invalid \\ ! ([#1656](https://github.com/beautify-web/js-beautify/pull/1656))
* wrong indent for unclosed <? - need to support disabling templating ([#1647](https://github.com/beautify-web/js-beautify/issues/1647))
* Beautify inserts space before exclamation mark in comment <!-- in css <style> ([#1641](https://github.com/beautify-web/js-beautify/issues/1641))
* 'less' mixins parameter formatting problem ([#1582](https://github.com/beautify-web/js-beautify/issues/1582))
* Change css tests to use 4 space indenting instead of tabs ([#1527](https://github.com/beautify-web/js-beautify/issues/1527))
* Braces after case get pushed onto new line ([#1357](https://github.com/beautify-web/js-beautify/issues/1357))
* Extra space in pseudo-elements and pseudo-classes selectors ([#1233](https://github.com/beautify-web/js-beautify/issues/1233))
* LESS formatting - mixins with multiple variables ([#1018](https://github.com/beautify-web/js-beautify/issues/1018))
* Bug in less format ([#842](https://github.com/beautify-web/js-beautify/issues/842))

## v1.9.1
* nested table not beautified correctly ([#1649](https://github.com/beautify-web/js-beautify/issues/1649))
* Add an option to preserve indentation on empty lines ([#1322](https://github.com/beautify-web/js-beautify/issues/1322))

## v1.9.0
* Incorrect indentation of `^` inverted section tags in Handlebars/Mustache code ([#1623](https://github.com/beautify-web/js-beautify/issues/1623))
* PHP In HTML Attributes ([#1620](https://github.com/beautify-web/js-beautify/issues/1620))
* DeanEdward python unpacker offset problem ([#1616](https://github.com/beautify-web/js-beautify/issues/1616))
* CLI on Windows doesn't accept -f - for stdin? ([#1609](https://github.com/beautify-web/js-beautify/issues/1609))
* HTML type attribute breaks JavaScript beautification? ([#1606](https://github.com/beautify-web/js-beautify/issues/1606))
* Use of global MODE before declaration caused uglify problem ([#1604](https://github.com/beautify-web/js-beautify/issues/1604))
* When building html tags using Mustache variables, extra whitespace is added after opening arrow ([#1602](https://github.com/beautify-web/js-beautify/issues/1602))
* <script type="text/html">isnot abled to be beautified ([#1591](https://github.com/beautify-web/js-beautify/issues/1591))
* \_get\_full\_indent undefined ([#1590](https://github.com/beautify-web/js-beautify/issues/1590))
* Website "autodetect" setting doesn't distinguish css vs javascript ([#1565](https://github.com/beautify-web/js-beautify/issues/1565))
* Add setting to keep HTML tag text content unformatted or ignore custom delimiters ([#1560](https://github.com/beautify-web/js-beautify/issues/1560))
* HTML auto formatting using spaces instead of tabs ([#1551](https://github.com/beautify-web/js-beautify/issues/1551))
* Unclosed single quote in php tag causes formatting changes which break php code ([#1377](https://github.com/beautify-web/js-beautify/issues/1377))
* Using tabs when wrapping attributes and wrapping if needed ([#1294](https://github.com/beautify-web/js-beautify/issues/1294))
* HTML --wrap-attributes doesn't respect --wrap-line-length ([#1238](https://github.com/beautify-web/js-beautify/issues/1238))
* Bad indent level(HTML) ([#1213](https://github.com/beautify-web/js-beautify/issues/1213))
* js-beautify produces invalid code for variables with Unicode escape sequences ([#1211](https://github.com/beautify-web/js-beautify/issues/1211))
* support vuejs ([#1154](https://github.com/beautify-web/js-beautify/issues/1154))
* Go templates in HTML ([#881](https://github.com/beautify-web/js-beautify/issues/881))
* Better behavior for javascript --wrap-line-length ([#284](https://github.com/beautify-web/js-beautify/issues/284))

## v1.8.9
* Won't run from CLI - bad option name `files` ([#1583](https://github.com/beautify-web/js-beautify/issues/1583))
* in the .vue file `space\_after\_anon\_function` is invalid ([#1425](https://github.com/beautify-web/js-beautify/issues/1425))
* Add function default\_options() to beautifier.js ([#1364](https://github.com/beautify-web/js-beautify/issues/1364))
* fix: Missing space before function parentheses ? ([#1077](https://github.com/beautify-web/js-beautify/issues/1077))
* Support globs in CLI ([#787](https://github.com/beautify-web/js-beautify/issues/787))

## v1.8.8
*  async function in object wrong indentation ([#1573](https://github.com/beautify-web/js-beautify/issues/1573))

## v1.8.7
* Add tests for html  `indent\_scripts` option ([#1518](https://github.com/beautify-web/js-beautify/issues/1518))
* Support dynamic import ([#1197](https://github.com/beautify-web/js-beautify/issues/1197))
* HTML: add an option to preserve manual wrapping of attributes ([#1125](https://github.com/beautify-web/js-beautify/issues/1125))
* js-beautify adds a space between # and include ([#1114](https://github.com/beautify-web/js-beautify/issues/1114))
* space\_after\_anon\_function doesn't work with anon async functions ([#1034](https://github.com/beautify-web/js-beautify/issues/1034))
* Space before function arguments (space-after-function) (space-after-named-function) ([#608](https://github.com/beautify-web/js-beautify/issues/608))

## v1.8.6
* JS beautify break the angular compile ([#1544](https://github.com/beautify-web/js-beautify/issues/1544))
* base64 string is broken with v1.8.4 ([#1535](https://github.com/beautify-web/js-beautify/issues/1535))
* Bookmarklet becomes totally useless ([#1408](https://github.com/beautify-web/js-beautify/issues/1408))
* HTTPS ([#1399](https://github.com/beautify-web/js-beautify/issues/1399))
* Beautify breaks when js starts with space followed by multi-line comment ([#789](https://github.com/beautify-web/js-beautify/issues/789))

## v1.8.4
* Multiple newlines added between empty textarea and "unformatted" inline elements  ([#1534](https://github.com/beautify-web/js-beautify/issues/1534))
* unindent\_chained\_methods broken ([#1533](https://github.com/beautify-web/js-beautify/issues/1533))

## v1.8.3
* Missing Bower Assets ([#1521](https://github.com/beautify-web/js-beautify/issues/1521))
* Javascript ternary breaked with `await` ([#1519](https://github.com/beautify-web/js-beautify/issues/1519))
* Object property indented after `await` ([#1517](https://github.com/beautify-web/js-beautify/issues/1517))
* Handlebars formatting problems ([#870](https://github.com/beautify-web/js-beautify/issues/870))
* beautify.js doesn't have indent\_level option ([#724](https://github.com/beautify-web/js-beautify/issues/724))

## v1.8.1
* Why npm is a dependency? ([#1516](https://github.com/beautify-web/js-beautify/issues/1516))
* indent\_inner\_html not working in v1.8.0 ([#1514](https://github.com/beautify-web/js-beautify/issues/1514))

## v1.8.0
* list items of nested lists get indented backwards ([#1501](https://github.com/beautify-web/js-beautify/issues/1501))
* Make beautifier auto-convert options with dashes into underscores ([#1497](https://github.com/beautify-web/js-beautify/issues/1497))
* ReferenceError: token is not defined ([#1496](https://github.com/beautify-web/js-beautify/issues/1496))
* Publish v1.8.0 ([#1495](https://github.com/beautify-web/js-beautify/issues/1495))
* still probem #1439 / #1337 ([#1491](https://github.com/beautify-web/js-beautify/issues/1491))
* Duplicating HTML Code Nested In PHP ([#1483](https://github.com/beautify-web/js-beautify/issues/1483))
* Handlebars - `if` tags are broken when using helper with `textarea` ([#1482](https://github.com/beautify-web/js-beautify/issues/1482))
* TypeError: Cannot read property '1' of null ([#1481](https://github.com/beautify-web/js-beautify/issues/1481))
* Space in Self Closing Tag Issue ([#1478](https://github.com/beautify-web/js-beautify/issues/1478))
* Weird Formatting in VSCode ([#1475](https://github.com/beautify-web/js-beautify/issues/1475))
* Indent with tab issue on website ([#1470](https://github.com/beautify-web/js-beautify/issues/1470))
* Contents of hbs tags are converted to lowercase ([#1464](https://github.com/beautify-web/js-beautify/issues/1464))
* HTML tags are indented wrongly when attributes are present ([#1462](https://github.com/beautify-web/js-beautify/issues/1462))
* hbs tags are stripped when there is a comment below or inline ([#1461](https://github.com/beautify-web/js-beautify/issues/1461))
* Spaces added to handlebars with '=' ([#1460](https://github.com/beautify-web/js-beautify/issues/1460))
* jsbeautifier.org don't works ([#1445](https://github.com/beautify-web/js-beautify/issues/1445))
* Commenting code and then beautifying removes line breaks ([#1440](https://github.com/beautify-web/js-beautify/issues/1440))
* Less: Where is my space? ([#1411](https://github.com/beautify-web/js-beautify/issues/1411))
* No newline after @import ([#1406](https://github.com/beautify-web/js-beautify/issues/1406))
* "html.format.wrapAttributes": "force-aligned" adds empty line on long attributes ([#1403](https://github.com/beautify-web/js-beautify/issues/1403))
* HTML: wrap\_line\_length is handled incorrectly ([#1401](https://github.com/beautify-web/js-beautify/issues/1401))
* js-beautify is breaking code by adding space after import ([#1393](https://github.com/beautify-web/js-beautify/issues/1393))
* JS-Beautify should format XML tags inside HTML files ([#1383](https://github.com/beautify-web/js-beautify/issues/1383))
* python unpacker can not handle if radix given as [] and not as a number ([#1381](https://github.com/beautify-web/js-beautify/issues/1381))
* unindent\_chained\_methods breaks indentation for if statements without brackets  ([#1378](https://github.com/beautify-web/js-beautify/issues/1378))
* function parameters merged into single line when starting with ! or [ ([#1374](https://github.com/beautify-web/js-beautify/issues/1374))
* CSS selector issue (header > div[class~="div-all"]) in SCSS file ([#1373](https://github.com/beautify-web/js-beautify/issues/1373))
* Add "Create Issue for Unexpected Output" button to website ([#1371](https://github.com/beautify-web/js-beautify/issues/1371))
* Add combobox to control type of beautification ([#1370](https://github.com/beautify-web/js-beautify/issues/1370))
* Add Options textbox to website for debugging ([#1369](https://github.com/beautify-web/js-beautify/issues/1369))

## v1.7.5
* Strict mode: js\_source\_text is not defined [CSS] ([#1286](https://github.com/beautify-web/js-beautify/issues/1286))
* Made brace\_style option more inclusive ([#1277](https://github.com/beautify-web/js-beautify/pull/1277))
* White space before"!important" tag missing in CSS beautify ([#1273](https://github.com/beautify-web/js-beautify/issues/1273))

## v1.7.4
* Whitespace after ES7 `async` keyword for arrow functions ([#896](https://github.com/beautify-web/js-beautify/issues/896))

## v1.7.3
* Version 1.7.0 fail to install through pip ([#1250](https://github.com/beautify-web/js-beautify/issues/1250))
* Installing js-beautify fails ([#1247](https://github.com/beautify-web/js-beautify/issues/1247))

## v1.7.0
* undindent-chained-methods option. Resolves #482 ([#1240](https://github.com/beautify-web/js-beautify/pull/1240))
* Add test and tools folder to npmignore ([#1239](https://github.com/beautify-web/js-beautify/issues/1239))
* incorrect new-line insertion after "yield" ([#1206](https://github.com/beautify-web/js-beautify/issues/1206))
* Do not modify built-in objects ([#1205](https://github.com/beautify-web/js-beautify/issues/1205))
* Fix label checking incorrect box when clicked ([#1169](https://github.com/beautify-web/js-beautify/pull/1169))
* Webpack ([#1149](https://github.com/beautify-web/js-beautify/pull/1149))
* daisy-chain indentation leads to over-indentation ([#482](https://github.com/beautify-web/js-beautify/issues/482))

## v1.6.12
* CSS: Preserve Newlines ([#537](https://github.com/beautify-web/js-beautify/issues/537))

## v1.6.11
* On beautify, new line before next CSS selector ([#1142](https://github.com/beautify-web/js-beautify/issues/1142))

## v1.6.10

## v1.6.9
* Wrong HTML beautification starting with v1.6.5 ([#1115](https://github.com/beautify-web/js-beautify/issues/1115))
* Ignore linebreak when meet handlebar ([#1104](https://github.com/beautify-web/js-beautify/pull/1104))
* Lines are not un-indented correctly when attributes are wrapped ([#1103](https://github.com/beautify-web/js-beautify/issues/1103))
* force-aligned is not aligned when indenting with tabs ([#1102](https://github.com/beautify-web/js-beautify/issues/1102))
* Python package fails to publish  ([#1101](https://github.com/beautify-web/js-beautify/issues/1101))
* Explaination of 'operator\_position' is absent from README.md ([#1047](https://github.com/beautify-web/js-beautify/issues/1047))

## v1.6.8
* Incorrect indentation after loop with comment ([#1090](https://github.com/beautify-web/js-beautify/issues/1090))
* Extra newline is inserted after beautifying code with anonymous function ([#1085](https://github.com/beautify-web/js-beautify/issues/1085))
* end brace with next comment line make bad indent ([#1043](https://github.com/beautify-web/js-beautify/issues/1043))
* Javascript comment in last line doesn't beautify well ([#964](https://github.com/beautify-web/js-beautify/issues/964))
* indent doesn't work with comment (jsdoc) ([#913](https://github.com/beautify-web/js-beautify/issues/913))
* Wrong indentation, when new line between chained methods ([#892](https://github.com/beautify-web/js-beautify/issues/892))
* Comments in a non-semicolon style have extra indent ([#815](https://github.com/beautify-web/js-beautify/issues/815))
* [bug] Incorrect indentation due to commented line(s) following a function call with a function argument. ([#713](https://github.com/beautify-web/js-beautify/issues/713))
* Wrong indent formatting ([#569](https://github.com/beautify-web/js-beautify/issues/569))

## v1.6.7
* HTML pre code indentation ([#928](https://github.com/beautify-web/js-beautify/issues/928))
* Beautify script/style tags but ignore their inner JS/CSS content ([#906](https://github.com/beautify-web/js-beautify/issues/906))

## v1.6.6
* Wrong indentation for comment after nested unbraced control constructs ([#1079](https://github.com/beautify-web/js-beautify/issues/1079))
* Should prefer breaking the line after operator ? instead of before operator < ([#1073](https://github.com/beautify-web/js-beautify/issues/1073))
* New option "force-expand-multiline" for "wrap\_attributes" ([#1070](https://github.com/beautify-web/js-beautify/pull/1070))
* Breaks if html file starts with comment ([#1068](https://github.com/beautify-web/js-beautify/issues/1068))
* collapse-preserve-inline restricts users to collapse brace\_style ([#1057](https://github.com/beautify-web/js-beautify/issues/1057))
* Parsing failure on numbers with "e" ([#1054](https://github.com/beautify-web/js-beautify/issues/1054))
* Issue with Browser Instructions ([#1053](https://github.com/beautify-web/js-beautify/issues/1053))
* Add preserve inline function for expand style braces ([#1052](https://github.com/beautify-web/js-beautify/issues/1052))
* Update years in LICENSE ([#1038](https://github.com/beautify-web/js-beautify/issues/1038))
* JS. Switch with template literals. Unexpected indentation. ([#1030](https://github.com/beautify-web/js-beautify/issues/1030))
* The object with spread object formatted not correctly ([#1023](https://github.com/beautify-web/js-beautify/issues/1023))
* Bad output generator function in class ([#1013](https://github.com/beautify-web/js-beautify/issues/1013))
* Support editorconfig for stdin ([#1012](https://github.com/beautify-web/js-beautify/issues/1012))
* Publish to cdnjs ([#992](https://github.com/beautify-web/js-beautify/issues/992))
* breaks if handlebars comments contain handlebars tags ([#930](https://github.com/beautify-web/js-beautify/issues/930))
* Using jsbeautifyrc is broken ([#929](https://github.com/beautify-web/js-beautify/issues/929))
* Option to put HTML attributes on their own lines, aligned ([#916](https://github.com/beautify-web/js-beautify/issues/916))
* Erroneously changes CRLF to LF on Windows in HTML and CSS ([#899](https://github.com/beautify-web/js-beautify/issues/899))
* Weird space in {get } vs { normal } ([#888](https://github.com/beautify-web/js-beautify/issues/888))
* Bad for-of formatting with constant Array ([#875](https://github.com/beautify-web/js-beautify/issues/875))
* Problems with filter property in css and scss ([#755](https://github.com/beautify-web/js-beautify/issues/755))
* Add "collapse-one-line" option for non-collapse brace styles  ([#487](https://github.com/beautify-web/js-beautify/issues/487))

## v1.6.4
* css-beautify sibling combinator space issue ([#1001](https://github.com/beautify-web/js-beautify/issues/1001))
* Bug: Breaks when the source code it found an unclosed multiline comment. ([#996](https://github.com/beautify-web/js-beautify/issues/996))
* CSS: Preserve white space before pseudo-class and pseudo-element selectors ([#985](https://github.com/beautify-web/js-beautify/pull/985))
* Spelling error in token definition ([#984](https://github.com/beautify-web/js-beautify/issues/984))
* collapse-preserve-inline does not preserve simple, single line ("return") statements ([#982](https://github.com/beautify-web/js-beautify/issues/982))
* Publish the library via cdn ([#971](https://github.com/beautify-web/js-beautify/issues/971))
* Bug with css calc() function ([#957](https://github.com/beautify-web/js-beautify/issues/957))
* &:first-of-type:not(:last-child) when prettified insert erroneous white character ([#952](https://github.com/beautify-web/js-beautify/issues/952))
* Shorthand generator functions are formatting strangely ([#941](https://github.com/beautify-web/js-beautify/issues/941))
* Add handlebars support on cli for html ([#935](https://github.com/beautify-web/js-beautify/pull/935))
* Do not put a space within `yield*` generator functions. ([#920](https://github.com/beautify-web/js-beautify/issues/920))
* Possible to add an indent\_inner\_inner\_html option? (Prevent indenting second-level tags) ([#917](https://github.com/beautify-web/js-beautify/issues/917))
* Messing up jsx formatting multi-line attribute ([#914](https://github.com/beautify-web/js-beautify/issues/914))
* Bug report: Closing 'body' tag isn't formatted correctly ([#900](https://github.com/beautify-web/js-beautify/issues/900))
* { throw … } not working with collapse-preserve-inline ([#898](https://github.com/beautify-web/js-beautify/issues/898))
* ES6 concise method not propely indented ([#889](https://github.com/beautify-web/js-beautify/issues/889))
* CSS beautify changing symantics ([#883](https://github.com/beautify-web/js-beautify/issues/883))
* Dojo unsupported script types. ([#874](https://github.com/beautify-web/js-beautify/issues/874))
* Readme version comment  ([#868](https://github.com/beautify-web/js-beautify/issues/868))
* Extra space after pseudo-elements within :not() ([#618](https://github.com/beautify-web/js-beautify/issues/618))
* space in media queries after colon &: selectors ([#565](https://github.com/beautify-web/js-beautify/issues/565))
* Integrating editor config ([#551](https://github.com/beautify-web/js-beautify/issues/551))
* Preserve short expressions/statements on single line ([#338](https://github.com/beautify-web/js-beautify/issues/338))

## v1.6.3
* CLI broken when output path is not set ([#933](https://github.com/beautify-web/js-beautify/issues/933))
* huge memory leak ([#909](https://github.com/beautify-web/js-beautify/issues/909))
* don't print unpacking errors on stdout (python) ([#884](https://github.com/beautify-web/js-beautify/pull/884))
* Fix incomplete list of non-positionable operators (python lib) ([#878](https://github.com/beautify-web/js-beautify/pull/878))
* Fix Issue #844 ([#873](https://github.com/beautify-web/js-beautify/pull/873))
* assignment exponentiation operator ([#864](https://github.com/beautify-web/js-beautify/issues/864))
* Bug in Less mixins ([#844](https://github.com/beautify-web/js-beautify/issues/844))
* Can't Nest Conditionals ([#680](https://github.com/beautify-web/js-beautify/issues/680))
* ternary operations ([#670](https://github.com/beautify-web/js-beautify/issues/670))
* Support newline before logical or ternary operator ([#605](https://github.com/beautify-web/js-beautify/issues/605))
* Provide config files for format and linting ([#336](https://github.com/beautify-web/js-beautify/issues/336))

## v1.6.2
* Add missing 'collapse-preserve-inline' option to js module ([#861](https://github.com/beautify-web/js-beautify/pull/861))

## v1.6.1
* Inconsistent formatting for arrays of objects ([#860](https://github.com/beautify-web/js-beautify/issues/860))
* Publish v1.6.1 ([#859](https://github.com/beautify-web/js-beautify/issues/859))
* Space added to "from++" due to ES6 keyword  ([#858](https://github.com/beautify-web/js-beautify/issues/858))
* Changelog generator doesn't sort versions above 9 right ([#778](https://github.com/beautify-web/js-beautify/issues/778))
* space-after-anon-function not applied to object properties ([#761](https://github.com/beautify-web/js-beautify/issues/761))
* Separating 'input' elements adds whitespace ([#580](https://github.com/beautify-web/js-beautify/issues/580))
* Inline Format ([#572](https://github.com/beautify-web/js-beautify/issues/572))
* Preserve attributes line break in HTML ([#455](https://github.com/beautify-web/js-beautify/issues/455))
* Multiline Array ([#406](https://github.com/beautify-web/js-beautify/issues/406))

## v1.6.0
* Individual tests pollute options object ([#855](https://github.com/beautify-web/js-beautify/issues/855))
* Object attribute assigned fat arrow function with implicit return of a ternary causes next line to indent ([#854](https://github.com/beautify-web/js-beautify/issues/854))
* Treat php tags as single in html ([#850](https://github.com/beautify-web/js-beautify/pull/850))
* Read piped input by default ([#849](https://github.com/beautify-web/js-beautify/pull/849))
* Replace makefile dependency with bash script ([#848](https://github.com/beautify-web/js-beautify/pull/848))
* list of HTML inline elements incomplete; wraps inappropriately ([#840](https://github.com/beautify-web/js-beautify/issues/840))
* Beautifying bracket-less if/elses ([#838](https://github.com/beautify-web/js-beautify/issues/838))
* <col> elements within a <colgroup> are getting indented incorrectly ([#836](https://github.com/beautify-web/js-beautify/issues/836))
* single attribute breaks jsx beautification ([#834](https://github.com/beautify-web/js-beautify/issues/834))
* Improve Python packaging ([#831](https://github.com/beautify-web/js-beautify/pull/831))
* Erroneously changes CRLF to LF on Windows. ([#829](https://github.com/beautify-web/js-beautify/issues/829))
* Can't deal with XHTML5 ([#828](https://github.com/beautify-web/js-beautify/issues/828))
* HTML after PHP is indented ([#826](https://github.com/beautify-web/js-beautify/issues/826))
* exponentiation operator ([#825](https://github.com/beautify-web/js-beautify/issues/825))
* Add support for script type "application/ld+json" ([#821](https://github.com/beautify-web/js-beautify/issues/821))
* package.json: Remove "preferGlobal" option ([#820](https://github.com/beautify-web/js-beautify/pull/820))
* Don't use array.indexOf() to support legacy browsers ([#816](https://github.com/beautify-web/js-beautify/pull/816))
* ES6 Object Shortand Indenting Weirdly Sometimes ([#810](https://github.com/beautify-web/js-beautify/issues/810))
* Implicit Return Function on New Line not Preserved ([#806](https://github.com/beautify-web/js-beautify/issues/806))
* Misformating "0b" Binary Strings ([#803](https://github.com/beautify-web/js-beautify/issues/803))
* Beautifier breaks ES6 nested template strings ([#797](https://github.com/beautify-web/js-beautify/issues/797))
* Misformating "0o" Octal Strings ([#792](https://github.com/beautify-web/js-beautify/issues/792))
* Do not use hardcoded directory for tests ([#788](https://github.com/beautify-web/js-beautify/pull/788))
* Handlebars {{else}} tag not given a newline ([#784](https://github.com/beautify-web/js-beautify/issues/784))
* Wrong indentation for XML header (<?xml version="1.0"?>) ([#783](https://github.com/beautify-web/js-beautify/issues/783))
* is\_whitespace for loop incrementing wrong variable ([#777](https://github.com/beautify-web/js-beautify/pull/777))
* Newline is inserted after comment with comma\_first ([#775](https://github.com/beautify-web/js-beautify/issues/775))
* Cannot copy more than 1000 characters out of CodeMirror buffer ([#768](https://github.com/beautify-web/js-beautify/issues/768))
* Missing 'var' in beautify-html.js; breaks strict mode ([#763](https://github.com/beautify-web/js-beautify/issues/763))
* Fix typo in the example javascript code of index.html ([#753](https://github.com/beautify-web/js-beautify/pull/753))

## v1.5.10
* Preserve directive doesn't work as intended ([#723](https://github.com/beautify-web/js-beautify/issues/723))

## v1.5.7
* Support for legacy JavaScript versions (e.g. WSH+JScript & Co) ([#720](https://github.com/beautify-web/js-beautify/pull/720))
* Is \\n hard coded into CSS Beautifier logic? ([#715](https://github.com/beautify-web/js-beautify/issues/715))
* Spaces and linebreaks after # and around { } messing up interpolation/mixins (SASS/SCSS) ([#689](https://github.com/beautify-web/js-beautify/issues/689))
* Calls to functions get completely messed up in Sass (*.scss) ([#675](https://github.com/beautify-web/js-beautify/issues/675))
* No new line after selector in scss files ([#666](https://github.com/beautify-web/js-beautify/issues/666))
* using html-beautify on handlebars template deletes unclosed tag if on second line ([#623](https://github.com/beautify-web/js-beautify/issues/623))
* more Extra space after scss pseudo classes ([#557](https://github.com/beautify-web/js-beautify/issues/557))
* Unnecessary spaces in PHP code ([#490](https://github.com/beautify-web/js-beautify/issues/490))
* Some underscore.js template tags are broken ([#417](https://github.com/beautify-web/js-beautify/issues/417))
* Selective ignore using comments (feature request) ([#384](https://github.com/beautify-web/js-beautify/issues/384))

## v1.5.6
* Fix tokenizer's bracket pairs' open stack ([#693](https://github.com/beautify-web/js-beautify/pull/693))
* Indentation is incorrect for HTML5 void tag <source> ([#692](https://github.com/beautify-web/js-beautify/issues/692))
* Line wrapping breaks at the wrong place when the line is indented. ([#691](https://github.com/beautify-web/js-beautify/issues/691))
* Publish v1.5.6 ([#687](https://github.com/beautify-web/js-beautify/issues/687))
* Replace existing file fails using python beautifier ([#686](https://github.com/beautify-web/js-beautify/issues/686))
* Pseudo-classes formatted incorrectly and inconsistently with @page ([#661](https://github.com/beautify-web/js-beautify/issues/661))
* doc: add end\_with\_newline option ([#650](https://github.com/beautify-web/js-beautify/pull/650))
* Improve support for xml parts of jsx (React) => spaces, spread attributes and nested objects break the process ([#646](https://github.com/beautify-web/js-beautify/issues/646))
* html-beautify formats handlebars comments but does not format html comments ([#635](https://github.com/beautify-web/js-beautify/issues/635))
* Support for ES7 async ([#630](https://github.com/beautify-web/js-beautify/issues/630))
* css beautify adding an extra newline after a comment line in a css block ([#609](https://github.com/beautify-web/js-beautify/issues/609))
* No option to "Indent with tabs" for HTML files ([#587](https://github.com/beautify-web/js-beautify/issues/587))
* Function body is indented when followed by a comment ([#583](https://github.com/beautify-web/js-beautify/issues/583))
* JSX support ([#425](https://github.com/beautify-web/js-beautify/issues/425))
* Alternative Newline Characters ([#260](https://github.com/beautify-web/js-beautify/issues/260))

## v1.5.5
* Add GUI support for `--indent-inner-html`. ([#633](https://github.com/beautify-web/js-beautify/pull/633))
* Publish v1.5.5 ([#629](https://github.com/beautify-web/js-beautify/issues/629))
* CSS: Updating the documentation for the 'newline\_between\_rules' ([#615](https://github.com/beautify-web/js-beautify/pull/615))
* Equal Sign Removed from Filter Properties Alpha Opacity Assignment ([#599](https://github.com/beautify-web/js-beautify/issues/599))
* Keep trailing spaces on comments ([#598](https://github.com/beautify-web/js-beautify/issues/598))
* only print the file names of changed files ([#597](https://github.com/beautify-web/js-beautify/issues/597))
*  CSS: support add newline between rules ([#574](https://github.com/beautify-web/js-beautify/pull/574))
* elem[array]++ changes to elem[array] ++ inserting unnecessary gap ([#570](https://github.com/beautify-web/js-beautify/issues/570))
* add support to less functions paramters braces ([#568](https://github.com/beautify-web/js-beautify/pull/568))
* selector\_separator\_newline: true for Sass doesn't work ([#563](https://github.com/beautify-web/js-beautify/issues/563))
* yield statements are being beautified to their own newlines since 1.5.2 ([#560](https://github.com/beautify-web/js-beautify/issues/560))
* HTML beautifier inserts extra newline into `<li>`s ending with `<code>` ([#524](https://github.com/beautify-web/js-beautify/issues/524))
* Add wrap\_attributes option ([#476](https://github.com/beautify-web/js-beautify/issues/476))
* Add or preserve empty line between CSS rules ([#467](https://github.com/beautify-web/js-beautify/issues/467))
* Support comma first style of variable declaration ([#245](https://github.com/beautify-web/js-beautify/issues/245))

## v1.5.4
* TypeScript oddly formatted with 1.5.3 ([#552](https://github.com/beautify-web/js-beautify/issues/552))
* HTML beautifier inserts double spaces between adjacent tags ([#525](https://github.com/beautify-web/js-beautify/issues/525))
* Keep space in font rule ([#491](https://github.com/beautify-web/js-beautify/issues/491))
* [Brackets plug in] Space after </a> disappears ([#454](https://github.com/beautify-web/js-beautify/issues/454))
* Support nested pseudo-classes and parent reference (LESS) ([#427](https://github.com/beautify-web/js-beautify/pull/427))
* Alternate approach: preserve single spacing and treat img as inline element ([#415](https://github.com/beautify-web/js-beautify/pull/415))

## v1.5.3
* [TypeError: Cannot read property 'type' of undefined] ([#548](https://github.com/beautify-web/js-beautify/issues/548))
* Bug with RegExp ([#547](https://github.com/beautify-web/js-beautify/issues/547))
* Odd behaviour on less ([#520](https://github.com/beautify-web/js-beautify/issues/520))
* css beauitify ([#506](https://github.com/beautify-web/js-beautify/issues/506))
* Extra space after scss pseudo classes. ([#500](https://github.com/beautify-web/js-beautify/issues/500))
* Generates invalid scss when formatting ampersand selectors ([#498](https://github.com/beautify-web/js-beautify/issues/498))
* bad formatting of .less files using @variable or &:hover syntax ([#489](https://github.com/beautify-web/js-beautify/issues/489))
* Incorrect beautifying of CSS comment including an url. ([#466](https://github.com/beautify-web/js-beautify/issues/466))
* Handle SASS parent reference &: ([#414](https://github.com/beautify-web/js-beautify/issues/414))
* Js-beautify breaking selectors in less code.  ([#410](https://github.com/beautify-web/js-beautify/issues/410))
* Problem with "content" ([#364](https://github.com/beautify-web/js-beautify/issues/364))
* Space gets inserted between function and paren for function in Define  ([#313](https://github.com/beautify-web/js-beautify/issues/313))
* beautify-html returns null on broken html ([#301](https://github.com/beautify-web/js-beautify/issues/301))
* Indentation of functions inside conditionals not passing jslint ([#298](https://github.com/beautify-web/js-beautify/issues/298))

## v1.5.2
* Allow custom elements to be unformatted ([#540](https://github.com/beautify-web/js-beautify/pull/540))
* Need option to ignore brace style ([#538](https://github.com/beautify-web/js-beautify/issues/538))
* Refactor to Output and OutputLine classes ([#536](https://github.com/beautify-web/js-beautify/pull/536))
* Recognize ObjectLiteral on open brace ([#535](https://github.com/beautify-web/js-beautify/pull/535))
* Refactor to fully tokenize before formatting ([#530](https://github.com/beautify-web/js-beautify/pull/530))
* Cleanup checked in six.py file ([#527](https://github.com/beautify-web/js-beautify/pull/527))
* Changelog.md? ([#526](https://github.com/beautify-web/js-beautify/issues/526))
* New line added between each css declaration ([#523](https://github.com/beautify-web/js-beautify/issues/523))
* Kendo Template scripts get messed up! ([#516](https://github.com/beautify-web/js-beautify/issues/516))
* SyntaxError: Unexpected token ++ ([#514](https://github.com/beautify-web/js-beautify/issues/514))
* space appears before open square bracket when the object name is "set" ([#508](https://github.com/beautify-web/js-beautify/issues/508))
* Unclosed string problem ([#505](https://github.com/beautify-web/js-beautify/issues/505))
* "--n" and "++n" are not indented like "n--" and "n++" are... ([#495](https://github.com/beautify-web/js-beautify/issues/495))
* Allow `<style>` and `<script>` tags to be unformatted ([#494](https://github.com/beautify-web/js-beautify/pull/494))
* Preserve new line at end of file ([#492](https://github.com/beautify-web/js-beautify/issues/492))
* Line wraps breaking numbers (causes syntax error) ([#488](https://github.com/beautify-web/js-beautify/issues/488))
* jsBeautify acts differently when handling different kinds of function expressions ([#485](https://github.com/beautify-web/js-beautify/issues/485))
* AttributeError: 'NoneType' object has no attribute 'groups' ([#479](https://github.com/beautify-web/js-beautify/issues/479))
* installation doco for python need update -- pip install six? ([#478](https://github.com/beautify-web/js-beautify/issues/478))
* Move einars/js-beautify to beautify-web/js-beautify ([#475](https://github.com/beautify-web/js-beautify/issues/475))
* Bring back space\_after\_anon\_function ([#474](https://github.com/beautify-web/js-beautify/pull/474))
* fix for #453, Incompatible handlebar syntax ([#468](https://github.com/beautify-web/js-beautify/pull/468))
* Python: missing explicit dependency on "six" package ([#465](https://github.com/beautify-web/js-beautify/issues/465))
* function declaration inside array, adds extra line.  ([#464](https://github.com/beautify-web/js-beautify/issues/464))
* [es6] yield a array ([#458](https://github.com/beautify-web/js-beautify/issues/458))
* Publish v1.5.2 ([#452](https://github.com/beautify-web/js-beautify/issues/452))
* Port css colon character fix to python  ([#446](https://github.com/beautify-web/js-beautify/issues/446))
* Cannot declare object literal properties with unquoted reserved words ([#440](https://github.com/beautify-web/js-beautify/issues/440))
* Do not put a space within `function*` generator functions. ([#428](https://github.com/beautify-web/js-beautify/issues/428))
* beautification of "nth-child" css fails csslint ([#418](https://github.com/beautify-web/js-beautify/issues/418))
