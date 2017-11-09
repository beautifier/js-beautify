/*
  The MIT License (MIT)

  Copyright (c) 2007-2017 Einar Lielmanis, Liam Newman, and contributors.

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation files
  (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*/

exports.test_data = {
    default_options: [
        { name: "indent_size", value: "1" },
        { name: "indent_char", value: "'\\t'" },
        { name: "selector_separator_newline", value: "true" },
        { name: "end_with_newline", value: "false" },
        { name: "newline_between_rules", value: "false" },
        { name: "space_around_combinator", value: "false" },
        { name: "preserve_newlines", value: "false" },
        // deprecated
        { name: "space_around_selector_separator", value: "false" }
    ],
    groups: [{
            name: "End With Newline",
            description: "",
            matrix: [{
                options: [
                    { name: "end_with_newline", value: "true" }
                ],
                eof: '\\n'
            }, {
                options: [
                    { name: "end_with_newline", value: "false" }
                ],
                eof: ''
            }],
            tests: [
                { fragment: true, input: '', output: '{{eof}}' },
                { fragment: true, input: '   .tabs{}', output: '   .tabs {}{{eof}}' },
                { fragment: true, input: '   \n\n.tabs{}\n\n\n\n', output: '   .tabs {}{{eof}}' },
                { fragment: true, input: '\n', output: '{{eof}}' }
            ],
        }, {
            name: "Empty braces",
            description: "",
            tests: [
                { input: '.tabs{}', output: '.tabs {}' },
                { input: '.tabs { }', output: '.tabs {}' },
                { input: '.tabs    {    }', output: '.tabs {}' },
                // When we support preserving newlines this will need to change
                { input: '.tabs    \n{\n    \n  }', output: '.tabs {}' }
            ],
        }, {
            name: "",
            description: "",
            tests: [{
                input: '#cboxOverlay {\n\tbackground: url(images/overlay.png) repeat 0 0;\n\topacity: 0.9;\n\tfilter: alpha(opacity = 90);\n}',
                output: '#cboxOverlay {\n\tbackground: url(images/overlay.png) repeat 0 0;\n\topacity: 0.9;\n\tfilter: alpha(opacity=90);\n}'
            }, ],
        }, {
            name: "Support simple language specific option inheritance/overriding",
            description: "Support simple language specific option inheritance/overriding",
            matrix: [{
                    options: [
                        { name: "indent_char", value: "' '" },
                        { name: "indent_size", value: "4" },
                        { name: "js", value: "{ 'indent_size': 3 }" },
                        { name: "css", value: "{ 'indent_size': 5 }" }
                    ],
                    c: '     ',
                },
                {
                    options: [
                        { name: "indent_char", value: "' '" },
                        { name: "indent_size", value: "4" },
                        { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 } }" }
                    ],
                    c: '    '
                },
                {
                    options: [
                        { name: "indent_char", value: "' '" },
                        { name: "indent_size", value: "9" },
                        { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 8 }, 'indent_size': 2}" },
                        { name: "js", value: "{ 'indent_size': 5 }" },
                        { name: "css", value: "{ 'indent_size': 3 }" }
                    ],
                    c: '   '
                }
            ],
            tests: [{
                unchanged: [
                    '.selector {',
                    '{{c}}font-size: 12px;',
                    '}'
                ]
            }]
        }, {
            name: "Space Around Combinator",
            description: "",
            matrix: [{
                options: [{ name: "space_around_combinator", value: "true" }],
                space: ' '
            }, {
                options: [{ name: "space_around_combinator", value: "false" }],
                space: ''
            }, {
                // space_around_selector_separator is deprecated, but needs to keep working for now.
                options: [{ name: "space_around_selector_separator", value: "true" }],
                space: ' '
            }],
            tests: [
                { input: 'a>b{}', output: 'a{{space}}>{{space}}b {}' },
                { input: 'a~b{}', output: 'a{{space}}~{{space}}b {}' },
                { input: 'a+b{}', output: 'a{{space}}+{{space}}b {}' },
                { input: 'a+b>c{}', output: 'a{{space}}+{{space}}b{{space}}>{{space}}c {}' },
                { input: 'a > b{}', output: 'a{{space}}>{{space}}b {}' },
                { input: 'a ~ b{}', output: 'a{{space}}~{{space}}b {}' },
                { input: 'a + b{}', output: 'a{{space}}+{{space}}b {}' },
                { input: 'a + b > c{}', output: 'a{{space}}+{{space}}b{{space}}>{{space}}c {}' },
                {
                    input: 'a > b{width: calc(100% + 45px);}',
                    output: [
                        'a{{space}}>{{space}}b {',
                        '\twidth: calc(100% + 45px);',
                        '}'
                    ]
                },
                {
                    input: 'a ~ b{width: calc(100% + 45px);}',
                    output: [
                        'a{{space}}~{{space}}b {',
                        '\twidth: calc(100% + 45px);',
                        '}'
                    ]
                },
                {
                    input: 'a + b{width: calc(100% + 45px);}',
                    output: [
                        'a{{space}}+{{space}}b {',
                        '\twidth: calc(100% + 45px);',
                        '}'
                    ]
                },
                {
                    input: 'a + b > c{width: calc(100% + 45px);}',
                    output: [
                        'a{{space}}+{{space}}b{{space}}>{{space}}c {',
                        '\twidth: calc(100% + 45px);',
                        '}'
                    ]
                }
            ]
        }, {
            name: 'Selector Separator',
            description: '',
            matrix: [{
                options: [
                    { name: 'selector_separator_newline', value: 'false' },
                    { name: 'selector_separator', value: '" "' }
                ],
                separator: ' ',
                separator1: ' '
            }, {
                options: [
                    { name: 'selector_separator_newline', value: 'false' },
                    { name: 'selector_separator', value: '"  "' }
                ],
                // BUG: #713
                separator: ' ',
                separator1: ' '
            }, {
                options: [
                    { name: 'selector_separator_newline', value: 'true' },
                    { name: 'selector_separator', value: '" "' }
                ],
                separator: '\\n',
                separator1: '\\n\\t'
            }, {
                options: [
                    { name: 'selector_separator_newline', value: 'true' },
                    { name: 'selector_separator', value: '"  "' }
                ],
                separator: '\\n',
                separator1: '\\n\\t'
            }],
            tests: [
                { input: '#bla, #foo{color:green}', output: '#bla,{{separator}}#foo {\n\tcolor: green\n}' },
                { input: '@media print {.tab{}}', output: '@media print {\n\t.tab {}\n}' },
                { input: '@media print {.tab,.bat{}}', output: '@media print {\n\t.tab,{{separator1}}.bat {}\n}' },
                { input: '#bla, #foo{color:black}', output: '#bla,{{separator}}#foo {\n\tcolor: black\n}' }, {
                    input: 'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
                    output: 'a:first-child,{{separator}}a:first-child {\n\tcolor: red;\n\tdiv:first-child,{{separator1}}div:hover {\n\t\tcolor: black;\n\t}\n}'
                }
            ]
        }, {
            name: "Preserve Newlines",
            description: "",
            matrix: [{
                options: [
                    { name: "preserve_newlines", value: "true" }
                ],
                separator_input: '\\n\\n',
                separator_output: '\\n\\n',
            }, {
                options: [
                    { name: "preserve_newlines", value: "false" }
                ],
                separator_input: '\\n\\n',
                separator_output: '\\n',
            }],
            tests: [
                { input: '.div {}{{separator_input}}.span {}', output: '.div {}{{separator_output}}.span {}' },
                { input: '#bla, #foo{\n\tcolor:black;{{separator_input}}\tfont-size: 12px;\n}', output: '#bla,\n#foo {\n\tcolor: black;{{separator_output}}\tfont-size: 12px;\n}' }
            ],
        },
        {
            name: "Preserve Newlines and newline_between_rules",
            description: "",
            options: [
                { name: "preserve_newlines", value: "true" },
                { name: "newline_between_rules", value: "true" }
            ],
            tests: [
                { input: '.div {}.span {}', output: '.div {}\n\n.span {}' },
                { input: '#bla, #foo{\n\tcolor:black;\n\tfont-size: 12px;\n}', output: '#bla,\n#foo {\n\tcolor: black;\n\tfont-size: 12px;\n}' },
                { input: '#bla, #foo{\n\tcolor:black;\n\n\n\tfont-size: 12px;\n}', output: '#bla,\n#foo {\n\tcolor: black;\n\n\n\tfont-size: 12px;\n}' },
                { unchanged: '#bla,\n\n#foo {\n\tcolor: black;\n\tfont-size: 12px;\n}' },
                { unchanged: 'a {\n\tb: c;\n\n\n\td: {\n\t\te: f;\n\t}\n}' },
                { unchanged: '.div {}\n\n.span {}' },
                { unchanged: 'html {}\n\n/*this is a comment*/' },
                { unchanged: '.div {\n\ta: 1;\n\n\n\tb: 2;\n}\n\n\n\n.span {\n\ta: 1;\n}' },
                { unchanged: '.div {\n\n\n\ta: 1;\n\n\n\tb: 2;\n}\n\n\n\n.span {\n\ta: 1;\n}' },
                { unchanged: '@media screen {\n\t.div {\n\t\ta: 1;\n\n\n\t\tb: 2;\n\t}\n\n\n\n\t.span {\n\t\ta: 1;\n\t}\n}\n\n.div {}\n\n.span {}' },
            ],
        }, {
            name: "Preserve Newlines and add tabs",
            options: [{ name: "preserve_newlines", value: "true" }],
            description: "",
            tests: [{
                input: '.tool-tip {\n\tposition: relative;\n\n\t\t\n\t.tool-tip-content {\n\t\t&>* {\n\t\t\tmargin-top: 0;\n\t\t}\n\t\t\n\n\t\t.mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n\t\tpadding: 1rem;\n\t\tposition: absolute;\n\t\tz-index: 10;\n\t}\n}',
                output: '.tool-tip {\n\tposition: relative;\n\n\n\t.tool-tip-content {\n\t\t&>* {\n\t\t\tmargin-top: 0;\n\t\t}\n\\n\\n\t\t.mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n\t\tpadding: 1rem;\n\t\tposition: absolute;\n\t\tz-index: 10;\n\t}\n}'
            }],
        }, {
            name: "Newline Between Rules",
            description: "",
            matrix: [{
                options: [
                    { name: "newline_between_rules", value: "true" }
                ],
                separator: '\\n'
            }, {
                options: [
                    { name: "newline_between_rules", value: "false" }
                ],
                separator: ''
            }],
            tests: [
                { input: '.div {}\n.span {}', output: '.div {}\n{{separator}}.span {}' },
                { input: '.div{}\n   \n.span{}', output: '.div {}\n{{separator}}.span {}' },
                { input: '.div {}    \n  \n.span { } \n', output: '.div {}\n{{separator}}.span {}' },
                { input: '.div {\n    \n} \n  .span {\n }  ', output: '.div {}\n{{separator}}.span {}' },
                { input: '.selector1 {\n\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n.div{height:15px;}', output: '.selector1 {\n\tmargin: 0;\n\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
                { input: '.tabs{width:10px;//end of line comment\nheight:10px;//another\n}\n.div{height:15px;}', output: '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px; //another\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
                { input: '#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', output: '#foo {\n\tbackground-image: url(foo@2x.png);\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
                { input: '@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n.div{height:15px;}', output: '@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo@2x.png);\n\t}\n\t@font-face {\n\t\tfont-family: "Bitstream Vera Serif Bold";\n\t\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n\t}\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
                { input: '@font-face {\n\tfont-family: "Bitstream Vera Serif Bold";\n\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: "Helvetica Neue"\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}', output: '@font-face {\n\tfont-family: "Bitstream Vera Serif Bold";\n\tsrc: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n{{separator}}@media screen {\n\t#foo:hover {\n\t\tbackground-image: url(foo.png);\n\t}\n\t@media screen and (min-device-pixel-ratio: 2) {\n\t\t@font-face {\n\t\t\tfont-family: "Helvetica Neue"\n\t\t}\n\t\t#foo:hover {\n\t\t\tbackground-image: url(foo@2x.png);\n\t\t}\n\t}\n}' },
                { input: 'a:first-child{color:red;div:first-child{color:black;}}\n.div{height:15px;}', output: 'a:first-child {\n\tcolor: red;\n\tdiv:first-child {\n\t\tcolor: black;\n\t}\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
                { input: 'a:first-child{color:red;div:not(.peq){color:black;}}\n.div{height:15px;}', output: 'a:first-child {\n\tcolor: red;\n\tdiv:not(.peq) {\n\t\tcolor: black;\n\t}\n}\n{{separator}}.div {\n\theight: 15px;\n}' },
            ],
        }, {
            name: "Functions braces",
            description: "",
            tests: [
                { input: '.tabs(){}', output: '.tabs() {}' },
                { input: '.tabs (){}', output: '.tabs () {}' },
                { input: '.tabs (pa, pa(1,2)), .cols { }', output: '.tabs (pa, pa(1, 2)),\n.cols {}' },
                { input: '.tabs(pa, pa(1,2)), .cols { }', output: '.tabs(pa, pa(1, 2)),\n.cols {}' },
                { input: '.tabs (   )   {    }', output: '.tabs () {}' },
                { input: '.tabs(   )   {    }', output: '.tabs() {}' },
                { input: '.tabs  (t, t2)  \n{\n  key: val(p1  ,p2);  \n  }', output: '.tabs (t, t2) {\n\tkey: val(p1, p2);\n}' },
                { unchanged: '.box-shadow(@shadow: 0 1px 3px rgba(0, 0, 0, .25)) {\n\t-webkit-box-shadow: @shadow;\n\t-moz-box-shadow: @shadow;\n\tbox-shadow: @shadow;\n}' }
            ],
        }, {
            name: "Comments",
            description: "",
            tests: [
                { unchanged: '/* test */' },
                { input: '.tabs{/* test */}', output: '.tabs {\n\t/* test */\n}' },
                { input: '.tabs{/* test */}', output: '.tabs {\n\t/* test */\n}' },
                { input: '/* header */.tabs {}', output: '/* header */\n\n.tabs {}' },
                { input: '.tabs {\n/* non-header */\nwidth:10px;}', output: '.tabs {\n\t/* non-header */\n\twidth: 10px;\n}' },
                { unchanged: '/* header' },
                { unchanged: '// comment' }, {
                    input: '.selector1 {\n\tmargin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}',
                    output: '.selector1 {\n\tmargin: 0;\n\t/* This is a comment including an url http://domain.com/path/to/file.ext */\n}'
                },

                {
                    comment: "single line comment support (less/sass)",
                    input: '.tabs{\n// comment\nwidth:10px;\n}',
                    output: '.tabs {\n\t// comment\n\twidth: 10px;\n}'
                },
                { input: '.tabs{// comment\nwidth:10px;\n}', output: '.tabs {\n\t// comment\n\twidth: 10px;\n}' },
                { input: '//comment\n.tabs{width:10px;}', output: '//comment\n.tabs {\n\twidth: 10px;\n}' },
                { input: '.tabs{//comment\n//2nd single line comment\nwidth:10px;}', output: '.tabs {\n\t//comment\n\t//2nd single line comment\n\twidth: 10px;\n}' },
                { input: '.tabs{width:10px;//end of line comment\n}', output: '.tabs {\n\twidth: 10px; //end of line comment\n}' },
                { input: '.tabs{width:10px;//end of line comment\nheight:10px;}', output: '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px;\n}' },
                { input: '.tabs{width:10px;//end of line comment\nheight:10px;//another\n}', output: '.tabs {\n\twidth: 10px; //end of line comment\n\theight: 10px; //another\n}' }
            ],
        }, {
            name: "Handle LESS property name interpolation",
            description: "",
            tests: [
                { unchanged: 'tag {\n\t@{prop}: none;\n}' },
                { input: 'tag{@{prop}:none;}', output: 'tag {\n\t@{prop}: none;\n}' },
                { input: 'tag{ @{prop}: none;}', output: 'tag {\n\t@{prop}: none;\n}' },
                {
                    comment: "can also be part of property name",
                    unchanged: 'tag {\n\tdynamic-@{prop}: none;\n}'
                },
                { input: 'tag{dynamic-@{prop}:none;}', output: 'tag {\n\tdynamic-@{prop}: none;\n}' },
                { input: 'tag{ dynamic-@{prop}: none;}', output: 'tag {\n\tdynamic-@{prop}: none;\n}' },
            ],
        }, {
            name: "Handle LESS property name interpolation, test #631",
            description: "",
            tests: [
                { unchanged: '.generate-columns(@n, @i: 1) when (@i =< @n) {\n\t.column-@{i} {\n\t\twidth: (@i * 100% / @n);\n\t}\n\t.generate-columns(@n, (@i + 1));\n}' },
                {
                    input: '.generate-columns(@n,@i:1) when (@i =< @n){.column-@{i}{width:(@i * 100% / @n);}.generate-columns(@n,(@i + 1));}',
                    output: '.generate-columns(@n, @i: 1) when (@i =< @n) {\n\t.column-@{i} {\n\t\twidth: (@i * 100% / @n);\n\t}\n\t.generate-columns(@n, (@i + 1));\n}'
                }
            ],
        }, {
            name: "Psuedo-classes vs Variables",
            description: "",
            tests: [
                { unchanged: '@page :first {}' }, {
                    comment: "Assume the colon goes with the @name. If we're in LESS, this is required regardless of the at-string.",
                    input: '@page:first {}',
                    output: '@page: first {}'
                },
                { unchanged: '@page: first {}' }
            ],
        }, {
            name: "SASS/SCSS",
            description: "",
            tests: [{
                    comment: "Basic Interpolation",
                    unchanged: 'p {\n\t$font-size: 12px;\n\t$line-height: 30px;\n\tfont: #{$font-size}/#{$line-height};\n}'
                },
                { unchanged: 'p.#{$name} {}' }, {
                    unchanged: [
                        '@mixin itemPropertiesCoverItem($items, $margin) {',
                        '\twidth: calc((100% - ((#{$items} - 1) * #{$margin}rem)) / #{$items});',
                        '\tmargin: 1.6rem #{$margin}rem 1.6rem 0;',
                        '}'
                    ]
                },
                {
                    comment: "Multiple filed issues in LESS due to not(:blah)",
                    unchanged: '&:first-of-type:not(:last-child) {}'
                },
                {
                    unchanged: [
                        'div {',
                        '\t&:not(:first-of-type) {',
                        '\t\tbackground: red;',
                        '\t}',
                        '}',
                    ]
                }

            ],
        }, {
            name: "Proper handling of colon in selectors",
            description: "Space before a colon in a selector must be preserved, as it means pseudoclass/pseudoelement on any child",
            options: [{ name: "selector_separator_newline", value: "false" }],
            tests: [
                { unchanged: 'a :b {}' },
                { unchanged: 'a ::b {}' },
                { unchanged: 'a:b {}' },
                { unchanged: 'a::b {}' },
                {
                    input: 'a {}, a::b {}, a   ::b {}, a:b {}, a   :b {}',
                    output: 'a {}\n, a::b {}\n, a ::b {}\n, a:b {}\n, a :b {}'
                },
                {
                    unchanged: [
                        '.card-blue ::-webkit-input-placeholder {',
                        '\tcolor: #87D1FF;',
                        '}'
                    ]
                },
                {
                    unchanged: [
                        'div [attr] :not(.class) {',
                        '\tcolor: red;',
                        '}'
                    ]
                }
            ]
        }, {
            name: "Regresssion Tests",
            description: "General Regression tests for known issues",
            options: [{ name: "selector_separator_newline", value: "false" }],
            tests: [{
                unchanged: [
                    '@media(min-width:768px) {',
                    '\t.selector::after {',
                    '\t\t/* property: value */',
                    '\t}',
                    '\t.other-selector {',
                    '\t\t/* property: value */',
                    '\t}',
                    '}'
                ]
            }, {
                unchanged: [
                    '.fa-rotate-270 {',
                    '\tfilter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);',
                    '}'
                ]
            }]
        }, {
            name: "Important ",
            description: "Spacing of !important",
            options: [],
            tests: [{
                input: 'a {\n\tcolor: blue  !important;\n}',
                output: 'a {\n\tcolor: blue !important;\n}'
            }, {
                input: 'a {\n\tcolor: blue!important;\n}',
                output: 'a {\n\tcolor: blue !important;\n}'
            }, {
                unchanged: 'a {\n\tcolor: blue !important;\n}'
            }]
        }, {

        }
    ]
};