/*
  The MIT License (MIT)

  Copyright (c) 2007-2018 Einar Lielmanis, Liam Newman, and contributors.

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
    { name: "indent_size", value: "4" },
    { name: "indent_char", value: "' '" },
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
      ]
    }, {
      name: "Support Indent Level Options and Base Indent Autodetection",
      description: "If user specifies indent level, use it. If not, autodetect indent level from starting whitespace.",
      matrix: [{
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "false" }
        ],
        input_start_indent: '   ',
        output_start_of_base: '   ',
        i: '    '
      }, {
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "false" },
          { name: "indent_level", value: "0" }
        ],
        input_start_indent: '   ',
        output_start_of_base: '   ',
        i: '    '
      }, {
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "false" },
          { name: "indent_level", value: "1" }
        ],
        input_start_indent: '   ',
        output_start_of_base: '    ',
        i: '    '
      }, {
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "false" },
          { name: "indent_level", value: "2" }
        ],
        input_start_indent: '',
        output_start_of_base: '        ',
        i: '    '
      }, {
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "true" },
          { name: "indent_level", value: "2" }
        ],
        input_start_indent: '',
        output_start_of_base: '\t\t',
        i: '\t'
      }, {
        options: [
          { name: "indent_size", value: "4" },
          { name: "indent_char", value: "' '" },
          { name: "indent_with_tabs", value: "false" },
          { name: "indent_level", value: "0" }
        ],
        input_start_indent: '\t   ',
        output_start_of_base: '\t   ',
        i: '    '
      }],
      tests: [
        { fragment: true, input: '{{input_start_indent}}a', output: '{{output_start_of_base}}a' },
        {
          fragment: true,
          input: [
            '{{input_start_indent}}.a {',
            '  text-align: right;',
            '}'
          ],
          output: [
            '{{output_start_of_base}}.a {',
            '{{output_start_of_base}}{{i}}text-align: right;',
            '{{output_start_of_base}}}'
          ]
        }, {
          fragment: true,
          input: [
            '{{input_start_indent}}// This is a random comment',
            '.a {',
            '  text-align: right;',
            '}'
          ],
          output: [
            '{{output_start_of_base}}// This is a random comment',
            '{{output_start_of_base}}.a {',
            '{{output_start_of_base}}{{i}}text-align: right;',
            '{{output_start_of_base}}}'
          ]
        }
      ]
    }, {
      name: "Empty braces",
      description: "",
      tests: [
        { input: '.tabs{}', output: '.tabs {}' },
        { input: '.tabs { }', output: '.tabs {}' },
        { input: '.tabs    {    }', output: '.tabs {}' },
        // When we support preserving newlines this will need to change
        { input: '.tabs    \n{\n    \n  }', output: '.tabs {}' }
      ]
    }, {
      name: "",
      description: "",
      tests: [{
        input: '#cboxOverlay {\n    background: url(images/overlay.png) repeat 0 0;\n    opacity: 0.9;\n    filter: alpha(opacity = 90);\n}',
        output: '#cboxOverlay {\n    background: url(images/overlay.png) repeat 0 0;\n    opacity: 0.9;\n    filter: alpha(opacity=90);\n}'
      }, {
        comment: 'simple data uri base64 test',
        input: 'a { background: url(data:image/gif;base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=); }',
        output: 'a {\n    background: url(data:image/gif;base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=);\n}'
      }, {
        comment: 'non-base64 data',
        input: 'a { background: url(data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E); }',
        output: 'a {\n    background: url(data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E);\n}'
      }, {
        comment: 'Beautifier does not fix or mitigate bad data uri',
        input: 'a { background: url(data:  image/gif   base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=); }',
        output: 'a {\n    background: url(data:  image/gif   base64,R0lGODlhCwALAJEAAAAAAP///xUVFf///yH5BAEAAAMALAAAAAALAAsAAAIPnI+py+0/hJzz0IruwjsVADs=);\n}'
      }]
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
          c: '     '
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
            '    width: calc(100% + 45px);',
            '}'
          ]
        },
        {
          input: 'a ~ b{width: calc(100% + 45px);}',
          output: [
            'a{{space}}~{{space}}b {',
            '    width: calc(100% + 45px);',
            '}'
          ]
        },
        {
          input: 'a + b{width: calc(100% + 45px);}',
          output: [
            'a{{space}}+{{space}}b {',
            '    width: calc(100% + 45px);',
            '}'
          ]
        },
        {
          input: 'a + b > c{width: calc(100% + 45px);}',
          output: [
            'a{{space}}+{{space}}b{{space}}>{{space}}c {',
            '    width: calc(100% + 45px);',
            '}'
          ]
        }
      ]
    }, {
      name: "Issue 1373 -- Correct spacing around [attribute~=value]",
      description: "",
      tests: [{
        unchanged: 'header>div[class~="div-all"]'
      }]
    }, {
      name: 'Selector Separator',
      description: '',
      matrix: [{
        options: [
          { name: 'selector_separator_newline', value: 'false' },
          { name: 'selector_separator', value: '" "' },
          { name: "newline_between_rules", value: "true" }
        ],
        separator: ' ',
        separator1: ' ',
        new_rule: '\n',
        first_nested_rule: ''
      }, {
        options: [
          { name: 'selector_separator_newline', value: 'false' },
          { name: 'selector_separator', value: '" "' },
          { name: "newline_between_rules", value: "false" }
        ],
        separator: ' ',
        separator1: ' ',
        new_rule: '',
        first_nested_rule: ''
      }, {
        options: [
          { name: 'selector_separator_newline', value: 'false' },
          { name: 'selector_separator', value: '"  "' },
          { name: "newline_between_rules", value: "false" }
        ],
        // BUG: #713
        separator: ' ',
        separator1: ' ',
        new_rule: '',
        first_nested_rule: ''
      }, {
        options: [
          { name: 'selector_separator_newline', value: 'true' },
          { name: 'selector_separator', value: '" "' },
          { name: "newline_between_rules", value: "true" }
        ],
        separator: '\\n',
        separator1: '\\n\    ',
        new_rule: '\n',
        first_nested_rule: '\n' // bug #1489
      }, {
        options: [
          { name: 'selector_separator_newline', value: 'true' },
          { name: 'selector_separator', value: '" "' },
          { name: "newline_between_rules", value: "false" }
        ],
        separator: '\\n',
        separator1: '\\n\    ',
        new_rule: '',
        first_nested_rule: ''
      }, {
        options: [
          { name: 'selector_separator_newline', value: 'true' },
          { name: 'selector_separator', value: '"  "' },
          { name: "newline_between_rules", value: "false" }
        ],
        separator: '\\n',
        separator1: '\\n\    ',
        new_rule: '',
        new_rule_bug: ''
      }],
      tests: [
        { input: '#bla, #foo{color:green}', output: '#bla,{{separator}}#foo {\n    color: green\n}' },
        { input: '#bla, #foo{color:green}\n#bla, #foo{color:green}', output: '#bla,{{separator}}#foo {\n    color: green\n}{{new_rule}}\n#bla,{{separator}}#foo {\n    color: green\n}' },
        { input: '@media print {.tab{}}', output: '@media print {\n    .tab {}\n}' },

        {
          comment: 'This is bug #1489',
          input: '@media print {.tab,.bat{}}',
          output: '@media print {\n{{first_nested_rule}}    .tab,{{separator1}}.bat {}\n}'
        },
        {
          comment: 'This is bug #1489',
          input: '@media print {// comment\n//comment 2\n.bat{}}',
          output: '@media print {\n{{new_rule}}    // comment\n    //comment 2\n    .bat {}\n}'
        },
        { input: '#bla, #foo{color:black}', output: '#bla,{{separator}}#foo {\n    color: black\n}' }, {
          input: 'a:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}\na:first-child,a:first-child{color:red;div:first-child,div:hover{color:black;}}',
          output: 'a:first-child,{{separator}}a:first-child {\n    color: red;{{new_rule}}\n    div:first-child,{{separator1}}div:hover {\n        color: black;\n    }\n}\n{{new_rule}}a:first-child,{{separator}}a:first-child {\n    color: red;{{new_rule}}\n    div:first-child,{{separator1}}div:hover {\n        color: black;\n    }\n}'
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
        separator_output: '\\n\\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" }
        ],
        separator_input: '\\n\\n',
        separator_output: '\\n'
      }],
      tests: [
        { input: '.div {}{{separator_input}}.span {}', output: '.div {}{{separator_output}}.span {}' },
        { input: '#bla, #foo{\n    color:black;{{separator_input}}    font-size: 12px;\n}', output: '#bla,\n#foo {\n    color: black;{{separator_output}}    font-size: 12px;\n}' }
      ]
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
        { input: '#bla, #foo{\n    color:black;\n    font-size: 12px;\n}', output: '#bla,\n#foo {\n    color: black;\n    font-size: 12px;\n}' },
        { input: '#bla, #foo{\n    color:black;\n\n\n    font-size: 12px;\n}', output: '#bla,\n#foo {\n    color: black;\n\n\n    font-size: 12px;\n}' },
        { unchanged: '#bla,\n\n#foo {\n    color: black;\n    font-size: 12px;\n}' },
        { unchanged: 'a {\n    b: c;\n\n\n    d: {\n        e: f;\n    }\n}' },
        { unchanged: '.div {}\n\n.span {}' },
        { unchanged: 'html {}\n\n/*this is a comment*/' },
        { unchanged: '.div {\n    a: 1;\n\n\n    b: 2;\n}\n\n\n\n.span {\n    a: 1;\n}' },
        { unchanged: '.div {\n\n\n    a: 1;\n\n\n    b: 2;\n}\n\n\n\n.span {\n    a: 1;\n}' },
        { unchanged: '@media screen {\n    .div {\n        a: 1;\n\n\n        b: 2;\n    }\n\n\n\n    .span {\n        a: 1;\n    }\n}\n\n.div {}\n\n.span {}' }
      ]
    }, {
      name: "Preserve Newlines and add tabs",
      options: [{ name: "preserve_newlines", value: "true" }],
      description: "",
      tests: [{
        input: '.tool-tip {\n    position: relative;\n\n        \n    .tool-tip-content {\n        &>* {\n            margin-top: 0;\n        }\n        \n\n        .mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n        padding: 1rem;\n        position: absolute;\n        z-index: 10;\n    }\n}',
        output: '.tool-tip {\n    position: relative;\n\n\n    .tool-tip-content {\n        &>* {\n            margin-top: 0;\n        }\n\\n\\n        .mixin-box-shadow(.2rem .2rem .5rem rgba(0, 0, 0, .15));\n        padding: 1rem;\n        position: absolute;\n        z-index: 10;\n    }\n}'
      }]
    }, {
      name: "Issue #1338 -- Preserve Newlines within CSS rules",
      options: [{ name: "preserve_newlines", value: "true" }],
      description: "",
      tests: [{
        unchanged: 'body {\n    grid-template-areas:\n        "header header"\n        "main   sidebar"\n        "footer footer";\n}'
      }]
    }, {
      name: "Newline Between Rules",
      description: "",
      matrix: [{
        options: [
          { name: "newline_between_rules", value: "true" }
        ],
        new_rule: '\n'
      }, {
        options: [
          { name: "newline_between_rules", value: "false" }
        ],
        new_rule: ''
      }],
      tests: [
        { input: '.div {}\n.span {}', output: '.div {}\n{{new_rule}}.span {}' },
        { input: '.div{}\n   \n.span{}', output: '.div {}\n{{new_rule}}.span {}' },
        { input: '.div {}    \n  \n.span { } \n', output: '.div {}\n{{new_rule}}.span {}' },
        { input: '.div {\n    \n} \n  .span {\n }  ', output: '.div {}\n{{new_rule}}.span {}' },
        {
          input: '.selector1 {\n    margin: 0; /* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n.div{height:15px;}',
          output: '.selector1 {\n    margin: 0;\n    /* This is a comment including an url http://domain.com/path/to/file.ext */\n}\n{{new_rule}}.div {\n    height: 15px;\n}'
        },
        { input: '.tabs{width:10px;//end of line comment\nheight:10px;//another\n}\n.div{height:15px;}', output: '.tabs {\n    width: 10px; //end of line comment\n    height: 10px; //another\n}\n{{new_rule}}.div {\n    height: 15px;\n}' },
        { input: '#foo {\n    background-image: url(foo@2x.png);\n    @font-face {\n        font-family: "Bitstream Vera Serif Bold";\n        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n    }\n}\n.div{height:15px;}', output: '#foo {\n    background-image: url(foo@2x.png);\n{{new_rule}}    @font-face {\n        font-family: "Bitstream Vera Serif Bold";\n        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n    }\n}\n{{new_rule}}.div {\n    height: 15px;\n}' },
        { input: '@media screen {\n    #foo:hover {\n        background-image: url(foo@2x.png);\n    }\n    @font-face {\n        font-family: "Bitstream Vera Serif Bold";\n        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n    }\n}\n.div{height:15px;}', output: '@media screen {\n    #foo:hover {\n        background-image: url(foo@2x.png);\n    }\n{{new_rule}}    @font-face {\n        font-family: "Bitstream Vera Serif Bold";\n        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n    }\n}\n{{new_rule}}.div {\n    height: 15px;\n}' },
        { input: '@font-face {\n    font-family: "Bitstream Vera Serif Bold";\n    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n@media screen {\n    #foo:hover {\n        background-image: url(foo.png);\n    }\n    @media screen and (min-device-pixel-ratio: 2) {\n        @font-face {\n            font-family: "Helvetica Neue"\n        }\n        #foo:hover {\n            background-image: url(foo@2x.png);\n        }\n    }\n}', output: '@font-face {\n    font-family: "Bitstream Vera Serif Bold";\n    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");\n}\n{{new_rule}}@media screen {\n    #foo:hover {\n        background-image: url(foo.png);\n    }\n{{new_rule}}    @media screen and (min-device-pixel-ratio: 2) {\n        @font-face {\n            font-family: "Helvetica Neue"\n        }\n{{new_rule}}        #foo:hover {\n            background-image: url(foo@2x.png);\n        }\n    }\n}' },
        { input: 'a:first-child{color:red;div:first-child{color:black;}}\n.div{height:15px;}', output: 'a:first-child {\n    color: red;\n{{new_rule}}    div:first-child {\n        color: black;\n    }\n}\n{{new_rule}}.div {\n    height: 15px;\n}' },
        { input: 'a:first-child{color:red;div:not(.peq){color:black;}}\n.div{height:15px;}', output: 'a:first-child {\n    color: red;\n{{new_rule}}    div:not(.peq) {\n        color: black;\n    }\n}\n{{new_rule}}.div {\n    height: 15px;\n}' },
        {
          input_: [
            '.list-group {',
            '    .list-group-item {',
            '    }',
            '',
            '    .list-group-icon {',
            '    }',
            '}',
            '',
            '.list-group-condensed {',
            '}'
          ],
          output: [
            '.list-group {',
            '    .list-group-item {}',
            '{{new_rule}}    .list-group-icon {}',
            '}',
            '{{new_rule}}.list-group-condensed {}'
          ]
        },
        {
          input_: [
            '.list-group {',
            '    .list-group-item {',
            '        a:1',
            '    }',
            '    .list-group-item {',
            '        a:1',
            '    }',
            '    .list-group-icon {',
            '    }',
            '    .list-group-icon {',
            '    }',
            '}',
            '.list-group-condensed {',
            '}'
          ],
          output: [
            '.list-group {',
            '    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    .list-group-icon {}',
            '{{new_rule}}    .list-group-icon {}',
            '}',
            '{{new_rule}}.list-group-condensed {}'
          ]
        },
        {
          input_: [
            '.list-group {',
            '    .list-group-item {',
            '        a:1',
            '    }',
            '    //this is my pre-comment',
            '    .list-group-item {',
            '        a:1',
            '    }',
            '    //this is a comment',
            '    .list-group-icon {',
            '    }',
            '    //this is also a comment',
            '    .list-group-icon {',
            '    }',
            '}',
            '.list-group-condensed {',
            '}'
          ],
          output: [
            '.list-group {',
            '    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    //this is my pre-comment',
            '    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    //this is a comment',
            '    .list-group-icon {}',
            '{{new_rule}}    //this is also a comment',
            '    .list-group-icon {}',
            '}',
            '{{new_rule}}.list-group-condensed {}'
          ]
        },
        {
          input_: [
            '.list-group {',
            '    color: #38a0e5;',
            '    .list-group-item {',
            '        a:1',
            '    }',
            '    color: #38a0e5;',
            '    .list-group-item {',
            '        a:1',
            '    }',
            'color: #38a0e5;',
            '    .list-group-icon {',
            '    }',
            '    color: #38a0e5;',
            '    .list-group-icon {',
            '    }',
            '}',
            'color: #38a0e5;',
            '.list-group-condensed {',
            '}'
          ],
          output: [
            '.list-group {',
            '    color: #38a0e5;',
            '{{new_rule}}    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    color: #38a0e5;',
            '{{new_rule}}    .list-group-item {',
            '        a: 1',
            '    }',
            '{{new_rule}}    color: #38a0e5;',
            '{{new_rule}}    .list-group-icon {}',
            '{{new_rule}}    color: #38a0e5;',
            '{{new_rule}}    .list-group-icon {}',
            '}',
            '{{new_rule}}color: #38a0e5;',
            '{{new_rule}}.list-group-condensed {}'
          ]
        },
        {
          input_: [
            '@media only screen and (max-width: 40em) {',
            'header {',
            '    margin: 0 auto;',
            '    padding: 10px;',
            '    background: red;',
            '    }',
            'main {',
            '    margin: 20px auto;',
            '    padding: 4px;',
            '    background: blue;',
            '    }',
            '}'
          ],
          output: [
            '@media only screen and (max-width: 40em) {',
            '    header {',
            '        margin: 0 auto;',
            '        padding: 10px;',
            '        background: red;',
            '    }',
            '{{new_rule}}    main {',
            '        margin: 20px auto;',
            '        padding: 4px;',
            '        background: blue;',
            '    }',
            '}'
          ]
        },
        {
          input_: [
            '.preloader {',
            '    height: 20px;',
            '    .line {',
            '        width: 1px;',
            '        height: 12px;',
            '        background: #38a0e5;',
            '        margin: 0 1px;',
            '        display: inline-block;',
            '        &.line-1 {',
            '            animation-delay: 800ms;',
            '        }',
            '        &.line-2 {',
            '            animation-delay: 600ms;',
            '        }',
            '    }',
            '    div {',
            '        color: #38a0e5;',
            '        font-family: "Arial", sans-serif;',
            '        font-size: 10px;',
            '        margin: 5px 0;',
            '    }',
            '}'
          ],
          output: [
            '.preloader {',
            '    height: 20px;',
            '{{new_rule}}    .line {',
            '        width: 1px;',
            '        height: 12px;',
            '        background: #38a0e5;',
            '        margin: 0 1px;',
            '        display: inline-block;',
            '{{new_rule}}        &.line-1 {',
            '            animation-delay: 800ms;',
            '        }',
            '{{new_rule}}        &.line-2 {',
            '            animation-delay: 600ms;',
            '        }',
            '    }',
            '{{new_rule}}    div {',
            '        color: #38a0e5;',
            '        font-family: "Arial", sans-serif;',
            '        font-size: 10px;',
            '        margin: 5px 0;',
            '    }',
            '}'
          ]
        }
      ]
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
        { input: '.tabs  (t, t2)  \n{\n  key: val(p1  ,p2);  \n  }', output: '.tabs (t, t2) {\n    key: val(p1, p2);\n}' },
        { unchanged: '.box-shadow(@shadow: 0 1px 3px rgba(0, 0, 0, .25)) {\n    -webkit-box-shadow: @shadow;\n    -moz-box-shadow: @shadow;\n    box-shadow: @shadow;\n}' }
      ]
    }, {
      name: "Beautify preserve formatting",
      description: "Allow beautifier to preserve sections",
      options: [
        { name: "indent_size", value: "4" },
        { name: "indent_char", value: "' '" },
        { name: "preserve_newlines", value: "true" }
      ],
      tests: [
        // Preserve not yet supported
        // { unchanged: "/* beautify preserve:start */\n/* beautify preserve:end */" },
        // { unchanged: "/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */" },
        // { unchanged: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */" },
        // { unchanged: "/* beautify preserve:start */     {asdklgh;y;;{}dd2d}/* beautify preserve:end */" },
        // {
        //   input_: "var a =  1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */",
        //   output: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */"
        // },
        // {
        //   input_: "var a = 1;\n /* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */",
        //   output: "var a = 1;\n/* beautify preserve:start */\n   var a = 1;\n/* beautify preserve:end */"
        // },
        // {
        //   unchanged: [
        //     'var a = {',
        //     '    /* beautify preserve:start */',
        //     '    one   :  1',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '    /* beautify preserve:end */',
        //     '};'
        //   ]
        // },
        // {
        //   input: [
        //     'var a = {',
        //     '/* beautify preserve:start */',
        //     '    one   :  1,',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '/* beautify preserve:end */',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /* beautify preserve:start */',
        //     '    one   :  1,',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '/* beautify preserve:end */',
        //     '};'
        //   ]
        // },
        // {
        //   comment: 'one space before and after required, only single spaces inside.',
        //   input: [
        //     'var a = {',
        //     '/*  beautify preserve:start  */',
        //     '    one   :  1,',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /*  beautify preserve:start  */',
        //     '    one: 1,',
        //     '    two: 2,',
        //     '    three: 3,',
        //     '    ten: 10',
        //     '};'
        //   ]
        // },
        // {
        //   input: [
        //     'var a = {',
        //     '/*beautify preserve:start*/',
        //     '    one   :  1,',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /*beautify preserve:start*/',
        //     '    one: 1,',
        //     '    two: 2,',
        //     '    three: 3,',
        //     '    ten: 10',
        //     '};'
        //   ]
        // },
        // {
        //   input: [
        //     'var a = {',
        //     '/*beautify  preserve:start*/',
        //     '    one   :  1,',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '    ten   : 10',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /*beautify  preserve:start*/',
        //     '    one: 1,',
        //     '    two: 2,',
        //     '    three: 3,',
        //     '    ten: 10',
        //     '};'
        //   ]
        // },

        {
          comment: 'Directive: ignore',
          unchanged: "/* beautify ignore:start */\n/* beautify ignore:end */"
        },
        { unchanged: "/* beautify ignore:start */\n   var a,,,{ 1;\n .div {}/* beautify ignore:end */" },
        { unchanged: ".div {}\n\n/* beautify ignore:start */\n   .div {}var a = 1;\n/* beautify ignore:end */" },
        {
          comment: 'ignore starts _after_ the start comment, ends after the end comment',
          unchanged: "/* beautify ignore:start */     {asdklgh;y;+++;dd2d}/* beautify ignore:end */"
        },
        { unchanged: "/* beautify ignore:start */  {asdklgh;y;+++;dd2d}    /* beautify ignore:end */" },
        {
          input_: ".div {}/* beautify ignore:start */\n   .div {}var a,,,{ 1;\n/*beautify ignore:end*/",
          output: ".div {}\n/* beautify ignore:start */\n   .div {}var a,,,{ 1;\n/*beautify ignore:end*/"
        },
        {
          input_: ".div {}\n  /* beautify ignore:start */\n   .div {}var a,,,{ 1;\n/* beautify ignore:end */",
          output: ".div {}\n/* beautify ignore:start */\n   .div {}var a,,,{ 1;\n/* beautify ignore:end */"
        },
        {
          unchanged: [
            '.div {',
            '    /* beautify ignore:start */',
            '    one   :  1',
            '    two   :  2,',
            '    three :  {',
            '    ten   : 10',
            '    /* beautify ignore:end */',
            '}'
          ]
        },
        {
          input: [
            '.div {',
            '/* beautify ignore:start */',
            '    one   :  1',
            '    two   :  2,',
            '    three :  {',
            '    ten   : 10',
            '/* beautify ignore:end */',
            '}'
          ],
          output: [
            '.div {',
            '    /* beautify ignore:start */',
            '    one   :  1',
            '    two   :  2,',
            '    three :  {',
            '    ten   : 10',
            '/* beautify ignore:end */',
            '}'
          ]
        },
        // {
        //   comment: 'Directives - multiple and interacting',
        //   input: [
        //     'var a = {',
        //     '/* beautify preserve:start */',
        //     '/* beautify preserve:start */',
        //     '    one   :  1,',
        //     '  /* beautify preserve:end */',
        //     '    two   :  2,',
        //     '    three :  3,',
        //     '/* beautify preserve:start */',
        //     '    ten   : 10',
        //     '/* beautify preserve:end */',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /* beautify preserve:start */',
        //     '/* beautify preserve:start */',
        //     '    one   :  1,',
        //     '  /* beautify preserve:end */',
        //     '    two: 2,',
        //     '    three: 3,',
        //     '    /* beautify preserve:start */',
        //     '    ten   : 10',
        //     '/* beautify preserve:end */',
        //     '};'
        //   ]
        // },
        {
          input: [
            '.div {',
            '/* beautify ignore:start */',
            '    one   :  1',
            ' /* beautify ignore:end */',
            '    two   :  2,',
            '/* beautify ignore:start */',
            '    three :  {',
            '    ten   : 10',
            '/* beautify ignore:end */',
            '}'
          ],
          output: [
            '.div {',
            '    /* beautify ignore:start */',
            '    one   :  1',
            ' /* beautify ignore:end */',
            '    two : 2,',
            '    /* beautify ignore:start */',
            '    three :  {',
            '    ten   : 10',
            '/* beautify ignore:end */',
            '}'
          ]
        }
        // ,{
        //   comment: 'Starts can occur together, ignore:end must occur alone.',
        //   input: [
        //     '.div {',
        //     '/* beautify ignore:start */',
        //     '    one   :  1',
        //     '    NOTE: ignore end block does not support starting other directives',
        //     '    This does not match the ending the ignore...',
        //     ' /* beautify ignore:end preserve:start */',
        //     '    two   :  2,',
        //     '/* beautify ignore:start */',
        //     '    three :  {',
        //     '    ten   : 10',
        //     '    ==The next comment ends the starting ignore==',
        //     '/* beautify ignore:end */',
        //     '}'
        //   ],
        //   output: [
        //     '.div {',
        //     '    /* beautify ignore:start */',
        //     '    one   :  1',
        //     '    NOTE: ignore end block does not support starting other directives',
        //     '    This does not match the ending the ignore...',
        //     ' /* beautify ignore:end preserve:start */',
        //     '    two   :  2,',
        //     '/* beautify ignore:start */',
        //     '    three :  {',
        //     '    ten   : 10',
        //     '    ==The next comment ends the starting ignore==',
        //     '/* beautify ignore:end */',
        //     '}'
        //   ]
        // },
        // {
        //   input: [
        //     '.div {',
        //     '/* beautify ignore:start preserve:start */',
        //     '    one   :  {',
        //     ' /* beautify ignore:end */',
        //     '    two   :  2,',
        //     '  /* beautify ignore:start */',
        //     '    three :  {',
        //     '/* beautify ignore:end */',
        //     '    ten   : 10',
        //     '   // This is all preserved',
        //     '}'
        //   ],
        //   output: [
        //     '.div {',
        //     '    /* beautify ignore:start preserve:start */',
        //     '    one   :  {',
        //     ' /* beautify ignore:end */',
        //     '    two   :  2,',
        //     '  /* beautify ignore:start */',
        //     '    three :  {',
        //     '/* beautify ignore:end */',
        //     '    ten   : 10',
        //     '   // This is all preserved',
        //     '}'
        //   ]
        // },
        // {
        //   input: [
        //     'var a = {',
        //     '/* beautify ignore:start preserve:start */',
        //     '    one   :  {',
        //     ' /* beautify ignore:end */',
        //     '    two   :  2,',
        //     '  /* beautify ignore:start */',
        //     '    three :  {',
        //     '/* beautify ignore:end */',
        //     '    ten   : 10,',
        //     '/* beautify preserve:end */',
        //     '     eleven: 11',
        //     '};'
        //   ],
        //   output: [
        //     'var a = {',
        //     '    /* beautify ignore:start preserve:start */',
        //     '    one   :  {',
        //     ' /* beautify ignore:end */',
        //     '    two   :  2,',
        //     '  /* beautify ignore:start */',
        //     '    three :  {',
        //     '/* beautify ignore:end */',
        //     '    ten   : 10,',
        //     '/* beautify preserve:end */',
        //     '    eleven: 11',
        //     '};'
        //   ]
        // }
      ]
    },
    {
      name: "Comments",
      description: "With preserve newlines option on",
      template: "< >",
      matrix: [{
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '',
        i1: '\n',
        o: '\n',
        new_rule: '\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '\n\n\n',
        i1: '\n\n\n',
        o: '\n',
        new_rule: '\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '\n        \n    \n',
        i1: '\n            \n   \n',
        o: '\n',
        new_rule: '\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '',
        i1: '\n',
        o: '\n',
        new_rule: '\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '\n',
        i1: '\n',
        o: '\n',
        new_rule: '\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '\n        \n    \n',
        i1: '\n            \n   \n',
        o: '\n\n\n',
        new_rule: '\n\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "false" }
        ],
        i: '\n\n\n',
        i1: '\n\n\n',
        o: '\n\n\n',
        new_rule: '\n\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '',
        i1: '\n',
        o: '\n',
        new_rule: '\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '\n\n\n',
        i1: '\n\n\n',
        o: '\n',
        new_rule: '\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "false" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '\n        \n    \n',
        i1: '\n            \n   \n',
        o: '\n',
        new_rule: '\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '',
        i1: '\n',
        o: '\n',
        new_rule: '\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '\n',
        i1: '\n',
        o: '\n',
        new_rule: '\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '\n\n\n',
        i1: '\n\n\n',
        o: '\n\n\n',
        new_rule: '\n\n\n'
      }, {
        options: [
          { name: "preserve_newlines", value: "true" },
          { name: "newline_between_rules", value: "true" }
        ],
        i: '\n        \n    \n',
        i1: '\n            \n   \n',
        o: '\n\n\n',
        new_rule: '\n\n\n'
      }],
      tests: [
        { unchanged: '/* header comment newlines on */' },
        {
          input: [
            '@import "custom.css";<i>.rule{}'
          ],
          output: [
            '@import "custom.css";<new_rule>.rule {}'
          ]
        },
        { input: '.tabs{<i>/* test */<i>}', output: '.tabs {<o>    /* test */<o>}' },
        {
          comment: '#1185',
          input: '/* header */<i>.tabs{}',
          output: '/* header */<o>.tabs {}'
        },
        { input: '.tabs {<i>/* non-header */<i>width:10px;<i>}', output: '.tabs {<o>    /* non-header */<o>    width: 10px;<o>}' },
        { unchanged: '/* header' },
        { unchanged: '// comment' },
        { unchanged: '/*' },
        { unchanged: '//' },
        {
          input: '.selector1 {<i>margin: 0;<i>/* This is a comment including an url http://domain.com/path/to/file.ext */<i>}',
          output: '.selector1 {<o>    margin: 0;<o>    /* This is a comment including an url http://domain.com/path/to/file.ext */<o>}'
        },

        {
          comment: "single line comment support (less/sass)",
          input: '.tabs{<i>// comment<i1>width:10px;<i>}',
          output: '.tabs {<o>    // comment<o>    width: 10px;<o>}'
        },
        { input: '.tabs{<i>// comment<i1>width:10px;<i>}', output: '.tabs {<o>    // comment<o>    width: 10px;<o>}' },
        { input: '//comment<i1>.tabs{<i>width:10px;<i>}', output: '//comment<o>.tabs {<o>    width: 10px;<o>}' },
        { input: '.tabs{<i>//comment<i1>//2nd single line comment<i1>width:10px;<i>}', output: '.tabs {<o>    //comment<o>    //2nd single line comment<o>    width: 10px;<o>}' },
        { input: '.tabs{<i>width:10px;//end of line comment<i1>}', output: '.tabs {<o>    width: 10px; //end of line comment<o>}' },
        { input: '.tabs{<i>width:10px;//end of line comment<i1>height:10px;<i>}', output: '.tabs {<o>    width: 10px; //end of line comment<o>    height: 10px;<o>}' },
        { input: '.tabs{<i>width:10px;//end of line comment<i1>height:10px;//another nl<i1>}', output: '.tabs {<o>    width: 10px; //end of line comment<o>    height: 10px; //another nl<o>}' },
        {
          input: '.tabs{<i>width: 10px;   // comment follows rule<i1>// another comment new line<i1>}',
          output: '.tabs {<o>    width: 10px; // comment follows rule<o>    // another comment new line<o>}'
        },
        {
          comment: '#1165',
          input: '.tabs{<i>width: 10px;<i1>        // comment follows rule<i1>// another comment new line<i1>}',
          output: '.tabs {<o>    width: 10px;<o>    // comment follows rule<o>    // another comment new line<o>}'
        },

        {
          comment: "#736",
          input: '/*\n * comment\n */<i>/* another comment */<i>body{}<i>',
          output: '/*\n * comment\n */<o>/* another comment */<o>body {}'
        },
        {
          comment: "#1348",
          input: '.demoa1 {<i>text-align:left; //demoa1 instructions for LESS note visibility only<i1>}<i>.demob {<i>text-align: right;<i>}',
          output: '.demoa1 {<o>    text-align: left; //demoa1 instructions for LESS note visibility only<o>}<new_rule>.demob {<o>    text-align: right;<o>}'
        },
        {
          comment: "#1440",
          input: [
            '#search-text {',
            '  width: 43%;',
            '  // height: 100%;',
            '  border: none;',
            '}'
          ],
          output: [
            '#search-text {',
            '    width: 43%;',
            '    // height: 100%;',
            '    border: none;',
            '}'
          ]
        },
        {
          input: '.demoa2 {<i>text-align:left;<i>}<i>//demob instructions for LESS note visibility only<i1>.demob {<i>text-align: right}',
          output: '.demoa2 {<o>    text-align: left;<o>}<new_rule>//demob instructions for LESS note visibility only<o>.demob {<o>    text-align: right\n}'
        },
        {
          comment: 'new lines between rules - #531 and #857',
          input: '.div{}<i1>.span {<i>}',
          output: '.div {}<new_rule>.span {}'
        },
        {
          input: '/**/<i>/**/<i>//<i1>/**/<i>.div{}<i>/**/<i>/**/<i>//<i1>/**/<i>.span {<i>}',
          output: '/**/<o>/**/<o>//<o>/**/<o>.div {}<new_rule>/**/<o>/**/<o>//<o>/**/<o>.span {}'
        },
        {
          input: '//<i1>.div{}<i>//<i1>.span {<i>}',
          output: '//<o>.div {}<new_rule>//<o>.span {}'
        },
        {
          input: '.selector1 {<i>margin: 0; <i>/* This is a comment including an url http://domain.com/path/to/file.ext */<i>}<i1>.div{<i>height:15px;<i>}',
          output: '.selector1 {<o>    margin: 0;<o>    /* This is a comment including an url http://domain.com/path/to/file.ext */<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        },
        {
          input: '.tabs{<i>width:10px;//end of line comment<i1>height:10px;//another<i1>}<i>.div{<i>height:15px;<i>}',
          output: '.tabs {<o>    width: 10px; //end of line comment<o>    height: 10px; //another<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        },
        {
          input: '#foo {<i>background-image: url(foo@2x.png);<i>    @font-face {<i>        font-family: "Bitstream Vera Serif Bold";<i>        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<i>    }<i>}<i>.div{<i>height:15px;<i>}',
          output: '#foo {<o>    background-image: url(foo@2x.png);<new_rule>    @font-face {<o>        font-family: "Bitstream Vera Serif Bold";<o>        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<o>    }<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        },
        {
          input: '@media screen {<i>    #foo:hover {<i>        background-image: url(foo@2x.png);<i>    }<i>    @font-face {<i>        font-family: "Bitstream Vera Serif Bold";<i>        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<i>    }<i>}<i>.div{<i>height:15px;<i>}',
          output: '@media screen {<o>    #foo:hover {<o>        background-image: url(foo@2x.png);<o>    }<new_rule>    @font-face {<o>        font-family: "Bitstream Vera Serif Bold";<o>        src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<o>    }<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        },
        {
          input: '@font-face {<i>    font-family: "Bitstream Vera Serif Bold";<i>    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<i>}<i1>@media screen {<i>    #foo:hover {<i>        background-image: url(foo.png);<i>    }<i>    @media screen and (min-device-pixel-ratio: 2) {<i>        @font-face {<i>            font-family: "Helvetica Neue";<i>        }<i>        #foo:hover {<i>            background-image: url(foo@2x.png);<i>        }<i>    }<i>}',
          output: '@font-face {<o>    font-family: "Bitstream Vera Serif Bold";<o>    src: url("http://developer.mozilla.org/@api/deki/files/2934/=VeraSeBd.ttf");<o>}<new_rule>@media screen {<o>    #foo:hover {<o>        background-image: url(foo.png);<o>    }<new_rule>    @media screen and (min-device-pixel-ratio: 2) {<o>        @font-face {<o>            font-family: "Helvetica Neue";<o>        }<new_rule>        #foo:hover {<o>            background-image: url(foo@2x.png);<o>        }<o>    }<o>}'
        },
        {
          input: 'a:first-child{<i>color:red;<i>div:first-child{<i>color:black;<i>}<i>}<i>.div{<i>height:15px;<i>}',
          output: 'a:first-child {<o>    color: red;<new_rule>    div:first-child {<o>        color: black;<o>    }<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        },
        {
          input: 'a:first-child{<i>color:red;<i>div:not(.peq){<i>color:black;<i>}<i>}<i>.div{<i>height:15px;<i>}',
          output: 'a:first-child {<o>    color: red;<new_rule>    div:not(.peq) {<o>        color: black;<o>    }<o>}<new_rule>.div {<o>    height: 15px;<o>}'
        }
      ]
    },
    {
      name: "Handle LESS property name interpolation",
      description: "",
      tests: [
        { unchanged: 'tag {\n    @{prop}: none;\n}' },
        { input: 'tag{@{prop}:none;}', output: 'tag {\n    @{prop}: none;\n}' },
        { input: 'tag{ @{prop}: none;}', output: 'tag {\n    @{prop}: none;\n}' },
        {
          comment: "can also be part of property name",
          unchanged: 'tag {\n    dynamic-@{prop}: none;\n}'
        },
        { input: 'tag{dynamic-@{prop}:none;}', output: 'tag {\n    dynamic-@{prop}: none;\n}' },
        { input: 'tag{ dynamic-@{prop}: none;}', output: 'tag {\n    dynamic-@{prop}: none;\n}' }
      ]
    }, {
      name: "Handle LESS property name interpolation, test #631",
      description: "",
      tests: [
        { unchanged: '.generate-columns(@n, @i: 1) when (@i =< @n) {\n    .column-@{i} {\n        width: (@i * 100% / @n);\n    }\n    .generate-columns(@n, (@i + 1));\n}' },
        {
          input: '.generate-columns(@n,@i:1) when (@i =< @n){.column-@{i}{width:(@i * 100% / @n);}.generate-columns(@n,(@i + 1));}',
          output: '.generate-columns(@n, @i: 1) when (@i =< @n) {\n    .column-@{i} {\n        width: (@i * 100% / @n);\n    }\n    .generate-columns(@n, (@i + 1));\n}'
        }
      ]
    }, {
      name: "Handle LESS function parameters",
      description: "",
      tests: [
        { input: 'div{.px2rem(width,12);}', output: 'div {\n    .px2rem(width, 12);\n}' },
        //mixin next to 'background: url("...")' should not add a linebreak after the comma
        { unchanged: 'div {\n    background: url("//test.com/dummy.png");\n    .px2rem(width, 12);\n}' }
      ]
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
      ]
    }, {
      name: "Issue 1411 -- LESS Variable Assignment Spacing",
      description: "",
      tests: [{
          unchanged: [
            '@set: {',
            '    one: blue;',
            '    two: green;',
            '    three: red;',
            '}',
            '.set {',
            '    each(@set, {',
            '            @{key}-@{index}: @value;',
            '        }',
            '    );',
            '}'
          ]
        },
        { unchanged: '@light-blue: @nice-blue + #111;' }
      ]
    }, {
      name: "SASS/SCSS",
      description: "",
      tests: [{
          comment: "Basic Interpolation",
          unchanged: 'p {\n    $font-size: 12px;\n    $line-height: 30px;\n    font: #{$font-size}/#{$line-height};\n}'
        },
        { unchanged: 'p.#{$name} {}' }, {
          unchanged: [
            '@mixin itemPropertiesCoverItem($items, $margin) {',
            '    width: calc((100% - ((#{$items} - 1) * #{$margin}rem)) / #{$items});',
            '    margin: 1.6rem #{$margin}rem 1.6rem 0;',
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
            '    &:not(:first-of-type) {',
            '        background: red;',
            '    }',
            '}'
          ]
        }

      ]
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
            '    color: #87D1FF;',
            '}'
          ]
        },
        {
          unchanged: [
            'div [attr] :not(.class) {',
            '    color: red;',
            '}'
          ]
        },
        {
          comment: "Issue #1233",
          unchanged: [
            '.one {',
            '    color: #FFF;',
            '    // pseudo-element',
            '    span:not(*::selection) {',
            '        margin-top: 0;',
            '    }',
            '}',
            '.two {',
            '    color: #000;',
            '    // pseudo-class',
            '    span:not(*:active) {',
            '        margin-top: 0;',
            '    }',
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
          '    .selector::after {',
          '        /* property: value */',
          '    }',
          '    .other-selector {',
          '        /* property: value */',
          '    }',
          '}'
        ]
      }, {
        unchanged: [
          '.fa-rotate-270 {',
          '    filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);',
          '}'
        ]
      }]
    }, {
      name: "Issue #645, #1233",
      description: "",
      options: [
        { name: "selector_separator_newline", value: "true" },
        { name: "preserve_newlines", value: "true" },
        { name: "newline_between_rules", value: "true" }

      ],
      tests: [{
          unchanged: [
            '/* Comment above first rule */',
            '',
            'body {',
            '    display: none;',
            '}',
            '',
            '/* Comment between rules */',
            '',
            'ul,',
            '',
            '/* Comment between selectors */',
            '',
            'li {',
            '    display: none;',
            '}',
            '',
            '/* Comment after last rule */'
          ]
        },
        {
          input: [
            '.one  {',
            '    color: #FFF;',
            '    // pseudo-element',
            '    span:not(*::selection) {',
            '        margin-top: 0;',
            '    }',
            '}',
            '.two {',
            '    color: #000;',
            '    // pseudo-class',
            '    span:not(*:active) {',
            '        margin-top: 0;',
            '    }',
            '}'
          ],
          output: [
            '.one {',
            '    color: #FFF;',
            '',
            '    // pseudo-element',
            '    span:not(*::selection) {',
            '        margin-top: 0;',
            '    }',
            '}',
            '',
            '.two {',
            '    color: #000;',
            '',
            '    // pseudo-class',
            '    span:not(*:active) {',
            '        margin-top: 0;',
            '    }',
            '}'
          ]
        }
      ]
    }, {
      name: "Extend Tests",
      description: "Test for '@extend'",
      options: [],
      tests: [{
        unchanged: [
          '.btn-group-radios {',
          '    .btn:hover {',
          '        &:hover,',
          '        &:focus {',
          '            @extend .btn-blue:hover;',
          '        }',
          '    }',
          '}'
        ]
      }, {
        unchanged: [
          '.item-warning {',
          '    @extend btn-warning:hover;',
          '}',
          '.item-warning-wrong {',
          '    @extend btn-warning: hover;',
          '}'
        ]
      }]
    }, {
      name: "Import Tests",
      description: "Test for '@import'",
      options: [],
      tests: [{
        input: [
          '@import "custom.css";.rule{}',
          'a, p {}'
        ],
        output: [
          '@import "custom.css";',
          '.rule {}',
          'a,',
          'p {}'
        ]
      }, {
        input: [
          '@import url("bluish.css") projection,tv;.rule{}',
          'a, p {}'
        ],
        output: [
          '@import url("bluish.css") projection, tv;',
          '.rule {}',
          'a,',
          'p {}'
        ]
      }]
    }, {
      name: "Important",
      description: "Spacing of !important",
      options: [],
      tests: [{
        input: 'a {\n    color: blue  !important;\n}',
        output: 'a {\n    color: blue !important;\n}'
      }, {
        input: 'a {\n    color: blue!important;\n}',
        output: 'a {\n    color: blue !important;\n}'
      }, {
        unchanged: 'a {\n    color: blue !important;\n}'
      }, {
        unchanged: '.blue\\\\! {\n    color: blue !important;\n}'
      }]
    }, {
      name: "Escape",
      description: "",
      options: [],
      tests: [{
        unchanged: 'a:not(.color\\\\:blue) {\n    color: blue !important;\n}'
      }, {
        unchanged: '.blue\\\\:very {\n    color: blue !important;\n}'
      }, {
        fragment: true,
        unchanged: 'a:not(.color\\\\'
      }, {
        fragment: true,
        unchanged: 'a:not\\\\'
      }]
    }, {
      name: "indent_empty_lines true",
      description: "",
      options: [
        { name: "indent_empty_lines", value: "true" },
        //Necessary to test
        { name: "preserve_newlines", value: "true" }
      ],
      tests: [{
        fragment: true,
        input: [
          'a {',
          '',
          'width: auto;',
          '',
          'height: auto;',
          '',
          '}'
        ],
        output: [
          'a {',
          '    ',
          '    width: auto;',
          '    ',
          '    height: auto;',
          '    ',
          '}'
        ]
      }]
    }, {
      name: "indent_empty_lines false",
      description: "",
      options: [
        { name: "indent_empty_lines", value: "false" },
        //Necessary to test
        { name: "preserve_newlines", value: "true" }
      ],
      tests: [{
        fragment: true,
        unchanged: [
          'a {',
          '',
          '    width: auto;',
          '',
          '    height: auto;',
          '',
          '}'
        ]
      }]
    }, {
      name: "LESS mixins",
      description: "",
      tests: [{
        unchanged: [
          '.btn {',
          '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);',
          '}',
          '.mymixin(@color: #ccc; @border-width: 1px) {',
          '    border: @border-width solid @color;',
          '}',
          'strong {',
          '    &:extend(a:hover);',
          '}'
        ]
      }, {
        comment: 'Ensure simple closing parens do not break behavior',
        unchanged: [
          'strong {',
          '    &:extend(a:hover));',
          '}',
          '.btn {',
          '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);',
          '}',
          '.mymixin(@color: #ccc; @border-width: 1px) {',
          '    border: @border-width solid @color;',
          '}',
          'strong {',
          '    &:extend(a:hover);',
          '}'
        ]
      }, {
        comment: 'indent multi-line parens',
        unchanged: [
          '.btn {',
          '    .generate-animation(@mykeyframes, 1.4s,',
          '        .5s, 1, ease-out);',
          '}',
          '.mymixin(@color: #ccc;',
          '    @border-width: 1px) {',
          '    border: @border-width solid @color;',
          '}'
        ]
      }, {
        comment: 'format inside mixin parens',
        input: [
          '.btn {',
          '    .generate-animation(@mykeyframes,1.4s,.5s,1,ease-out);',
          '}',
          '.mymixin(@color:#ccc;@border-width:1px) {',
          '    border:@border-width solid @color;',
          '}'
        ],
        output: [
          '.btn {',
          '    .generate-animation(@mykeyframes, 1.4s, .5s, 1, ease-out);',
          '}',
          '.mymixin(@color: #ccc; @border-width: 1px) {',
          '    border: @border-width solid @color;',
          '}'
        ]
      }]
    }, {

    }
  ]
};
