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
    { name: "indent_with_tabs", value: "false" },
    { name: "preserve_newlines", value: "true" },
    { name: "jslint_happy", value: "false" },
    { name: "keep_array_indentation", value: "false" },
    { name: "brace_style", value: "'collapse'" },
    { name: "extra_liners", value: "['html', 'head', '/html']" }
  ],
  groups: [{
    name: "Unicode Support",
    description: "",
    tests: [{
      unchanged: "<p>Hello' + unicode_char(160) + unicode_char(3232) + '_' + unicode_char(3232) + 'world!</p>"
    }]
  }, {
    name: "Handle inline and block elements differently",
    description: "",
    matrix: [{}],
    tests: [{
      fragment: true,
      input: '<body><h1>Block</h1></body>',
      output: [
        '<body>',
        '    <h1>Block</h1>',
        '</body>'
      ]
    }, {
      fragment: true,
      unchanged: '<body><i>Inline</i></body>'
    }]
  }, {
    name: "End With Newline",
    description: "",
    matrix: [{
        options: [
          { name: "end_with_newline", value: "true" }
        ],
        eof: '\n'
      }, {
        options: [
          { name: "end_with_newline", value: "false" }
        ],
        eof: ''
      }

    ],
    tests: [
      { fragment: true, input: '', output: '{{eof}}' },
      { fragment: true, input: '<div></div>', output: '<div></div>{{eof}}' },
      // { fragment: true, input: '   \n\n<div></div>\n\n\n\n', output: '   <div></div>{{eof}}' },
      { fragment: true, input: '\n', output: '{{eof}}' }
    ]
  }, {
    name: "Support Indent Level Options and Base Indent Autodetection",
    description: "If user specifies indent level, use it; otherwise start at zero indent.",
    matrix: [{
      options: [],
      input_start_indent: '   ',
      output_start_of_base: '   ',
      i: '    '
    }, {
      options: [
        { name: "indent_level", value: "0" }
      ],
      input_start_indent: '   ',
      output_start_of_base: '   ',
      i: '    '
    }, {
      options: [
        { name: "indent_level", value: "1" }
      ],
      input_start_indent: '   ',
      output_start_of_base: '    ',
      i: '    '
    }, {
      options: [
        { name: "indent_level", value: "2" }
      ],
      input_start_indent: '',
      output_start_of_base: '        ',
      i: '    '
    }, {
      options: [
        { name: "indent_with_tabs", value: "true" },
        { name: "indent_level", value: "2" }
      ],
      input_start_indent: '',
      output_start_of_base: '\t\t',
      i: '\t'
    }, {
      options: [
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
          '{{input_start_indent}}<div>',
          '  <p>This is my sentence.</p>',
          '</div>'
        ],
        output: [
          '{{output_start_of_base}}<div>',
          '{{output_start_of_base}}{{i}}<p>This is my sentence.</p>',
          '{{output_start_of_base}}</div>'
        ]
      }, {
        fragment: true,
        input: [
          '{{input_start_indent}}// This is a random comment',
          '<div>',
          '  <p>This is my sentence.</p>',
          '</div>'
        ],
        output: [
          '{{output_start_of_base}}// This is a random comment',
          '{{output_start_of_base}}<div>',
          '{{output_start_of_base}}{{i}}<p>This is my sentence.</p>',
          '{{output_start_of_base}}</div>'
        ]
      }
    ]
  }, {
    name: "Custom Extra Liners (empty)",
    description: "",
    matrix: [{
        options: [
          { name: "extra_liners", value: "[]" }
        ]
      }

    ],
    tests: [{
      fragment: true,
      input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
      output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n        <p>x</p>\n    </div>\n</body>\n</html>'
    }]
  }, {
    name: "Custom Extra Liners (default)",
    description: "",
    matrix: [{
        options: [
          { name: "extra_liners", value: "null" }
        ]
      }

    ],
    tests: [{
      fragment: true,
      input: '<html><head></head><body></body></html>',
      output: '<html>\n\n<head></head>\n\n<body></body>\n\n</html>'
    }]
  }, {
    name: "Custom Extra Liners (p, string)",
    description: "",
    matrix: [{
        options: [
          { name: "extra_liners", value: "'p,/p'" }
        ]
      }

    ],
    tests: [{
      fragment: true,
      input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
      output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
    }]
  }, {
    name: "Custom Extra Liners (p)",
    description: "",
    matrix: [{
        options: [
          { name: "extra_liners", value: "['p', '/p']" }
        ]
      }

    ],
    tests: [{
      fragment: true,
      input: '<html><head><meta></head><body><div><p>x</p></div></body></html>',
      output: '<html>\n<head>\n    <meta>\n</head>\n<body>\n    <div>\n\n        <p>x\n\n        </p>\n    </div>\n</body>\n</html>'
    }]
  }, {
    name: "Tests for script and style Commented and cdata wapping (#1641)",
    description: "Repect comment and cdata wrapping regardless of beautifier",
    tests: [{
      input: [
        '<style><!----></style>'
      ],
      output: [
        '<style>',
        '    <!--',
        '    -->',
        '</style>'
      ]
    }, {
      input: [
        '<style><!--',
        '--></style>'
      ],
      output: [
        '<style>',
        '    <!--',
        '    -->',
        '</style>'
      ]
    }, {
      input: [
        '<style><!-- the rest of this   line is   ignored',
        '',
        '',
        '',
        '--></style>'
      ],
      output: [
        '<style>',
        '    <!-- the rest of this   line is   ignored',
        '    -->',
        '</style>'
      ]
    }, {
      input: [
        '<style type="test/null"><!--',
        '',
        '\t  ',
        '',
        '--></style>'
      ],
      output: [
        '<style type="test/null">',
        '    <!--',
        '    -->',
        '</style>'
      ]
    }, {
      input: [
        '<script><!--',
        'console.log("</script>" + "</style>");',
        '--></script>'
      ],
      output: [
        '<script>',
        '    <!--',
        '    console.log("</script>" + "</style>");',
        '    -->',
        '</script>'
      ]
    }, {
      fragment: true,
      comment: 'If wrapping is incomplete, print remaining unchanged.',
      input: [
        '<div>',
        '<script><!--',
        'console.log("</script>" + "</style>");',
        ' </script>',
        '</div>'
      ],
      output: [
        '<div>',
        '    <script><!--',
        'console.log("</script>" + "</style>");',
        ' </script>',
        '</div>'
      ]
    }, {
      input: [
        '<style><!--',
        '.selector {',
        '    font-family: "</script></style>";',
        '    }',
        '--></style>'
      ],
      output: [
        '<style>',
        '    <!--',
        '    .selector {',
        '        font-family: "</script></style>";',
        '    }',
        '    -->',
        '</style>'
      ]
    }, {
      input: [
        '<script type="test/null">',
        '    <!--',
        '   console.log("</script>" + "</style>");',
        '    console.log("</script>" + "</style>");',
        '--></script>'
      ],
      output: [
        '<script type="test/null">',
        '    <!--',
        '    console.log("</script>" + "</style>");',
        '     console.log("</script>" + "</style>");',
        '    -->',
        '</script>'
      ]
    }, {
      input: [
        '<script type="test/null"><!--',
        ' console.log("</script>" + "</style>");',
        '      console.log("</script>" + "</style>");',
        '--></script>'
      ],
      output: [
        '<script type="test/null">',
        '    <!--',
        '    console.log("</script>" + "</style>");',
        '         console.log("</script>" + "</style>");',
        '    -->',
        '</script>'
      ]
    }, {
      input: [
        '<script><![CDATA[',
        'console.log("</script>" + "</style>");',
        ']]></script>'
      ],
      output: [
        '<script>',
        '    <![CDATA[',
        '    console.log("</script>" + "</style>");',
        '    ]]>',
        '</script>'
      ]
    }, {
      input: [
        '<style><![CDATA[',
        '.selector {',
        '    font-family: "</script></style>";',
        '    }',
        ']]></style>'
      ],
      output: [
        '<style>',
        '    <![CDATA[',
        '    .selector {',
        '        font-family: "</script></style>";',
        '    }',
        '    ]]>',
        '</style>'
      ]
    }, {
      input: [
        '<script type="test/null">',
        '    <![CDATA[',
        '   console.log("</script>" + "</style>");',
        '    console.log("</script>" + "</style>");',
        ']]></script>'
      ],
      output: [
        '<script type="test/null">',
        '    <![CDATA[',
        '    console.log("</script>" + "</style>");',
        '     console.log("</script>" + "</style>");',
        '    ]]>',
        '</script>'
      ]
    }, {
      input: [
        '<script type="test/null"><![CDATA[',
        ' console.log("</script>" + "</style>");',
        '      console.log("</script>" + "</style>");',
        ']]></script>'
      ],
      output: [
        '<script type="test/null">',
        '    <![CDATA[',
        '    console.log("</script>" + "</style>");',
        '         console.log("</script>" + "</style>");',
        '    ]]>',
        '</script>'
      ]
    }]
  }, {
    name: "Tests for script and style types (issue 453, 821)",
    description: "Only format recognized script types",
    tests: [{
        unchanged: '<script type="text/unknown"><div></div></script>'
      }, {
        unchanged: '<script type="text/unknown">Blah Blah Blah</script>'
      }, {
        input: '<script type="text/unknown">    Blah Blah Blah   </script>',
        output: '<script type="text/unknown"> Blah Blah Blah   </script>'
      }, {
        input: '<script type="text/javascript"><div></div></script>',
        output: [
          '<script type="text/javascript">',
          '    < div > < /div>',
          '</script>'
        ]
      }, {
        input: '<script><div></div></script>',
        output: [
          '<script>',
          '    < div > < /div>',
          '</script>'
        ]
      }, {
        comment: 'text/html should beautify as html',
        input: '<script type="text/html">\n<div>\n<div></div><div></div></div></script>',
        output: [
          '<script type="text/html">',
          '    <div>',
          '        <div></div>',
          '        <div></div>',
          '    </div>',
          '</script>'
        ]
      }, {
        comment: 'null beatifier behavior - should still indent',
        fragment: true,
        input: '<script type="test/null">\n    <div>\n  <div></div><div></div></div></script>',
        output: [
          '<script type="test/null">',
          '    <div>',
          '      <div></div><div></div></div>',
          '</script>'
        ]
      }, {
        input: '<script type="test/null">\n   <div>\n     <div></div><div></div></div></script>',
        output: [
          '<script type="test/null">',
          '    <div>',
          '      <div></div><div></div></div>',
          '</script>'
        ]
      }, {
        input: '<script type="test/null">\n<div>\n<div></div><div></div></div></script>',
        output: [
          '<script type="test/null">',
          '    <div>',
          '    <div></div><div></div></div>',
          '</script>'
        ]
      }, {
        input: '<script>var foo = "bar";</script>',
        output: [
          '<script>',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        comment: 'Issue #1606 - type attribute on other element',
        input: [
          '<script>',
          'console.log(1  +  1);',
          '</script>',
          '',
          '<input type="submit"></input>'
        ],
        output: [
          '<script>',
          '    console.log(1 + 1);',
          '</script>',
          '',
          '<input type="submit"></input>'
        ]
      }, {
        input: '<script type="text/javascript">var foo = "bar";</script>',
        output: [
          '<script type="text/javascript">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="application/javascript">var foo = "bar";</script>',
        output: [
          '<script type="application/javascript">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="application/javascript;version=1.8">var foo = "bar";</script>',
        output: [
          '<script type="application/javascript;version=1.8">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="application/x-javascript">var foo = "bar";</script>',
        output: [
          '<script type="application/x-javascript">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="application/ecmascript">var foo = "bar";</script>',
        output: [
          '<script type="application/ecmascript">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="dojo/aspect">this.domNode.style.display="none";</script>',
        output: [
          '<script type="dojo/aspect">',
          '    this.domNode.style.display = "none";',
          '</script>'
        ]
      }, {
        input: '<script type="dojo/method">this.domNode.style.display="none";</script>',
        output: [
          '<script type="dojo/method">',
          '    this.domNode.style.display = "none";',
          '</script>'
        ]
      }, {
        input: '<script type="text/javascript1.5">var foo = "bar";</script>',
        output: [
          '<script type="text/javascript1.5">',
          '    var foo = "bar";',
          '</script>'
        ]
      }, {
        input: '<script type="application/json">{"foo":"bar"}</script>',
        output: [
          '<script type="application/json">',
          '    {',
          '        "foo": "bar"',
          '    }',
          '</script>'
        ]
      }, {
        input: '<script type="application/ld+json">{"foo":"bar"}</script>',
        output: [
          '<script type="application/ld+json">',
          '    {',
          '        "foo": "bar"',
          '    }',
          '</script>'
        ]
      }, {
        unchanged: '<style type="text/unknown"><tag></tag></style>'
      }, {
        input: '<style type="text/css"><tag></tag></style>',
        output: [
          '<style type="text/css">',
          '    <tag></tag>',
          '</style>'
        ]
      }, {
        input: '<style><tag></tag></style>',
        output: [
          '<style>',
          '    <tag></tag>',
          '</style>'
        ]
      }, {
        input: '<style>.selector {font-size:12px;}</style>',
        output: [
          '<style>',
          '    .selector {',
          '        font-size: 12px;',
          '    }',
          '</style>'
        ]
      }, {
        input: '<style type="text/css">.selector {font-size:12px;}</style>',
        output: [
          '<style type="text/css">',
          '    .selector {',
          '        font-size: 12px;',
          '    }',
          '</style>'
        ]
      }

    ]
  }, {
    name: "Attribute Wrap alignment with spaces and tabs",
    description: "Ensure attributes are internally aligned with spaces when the indent_character is set to tab",
    template: "^^^ $$$",
    matrix: [{
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" },
        { name: "indent_with_tabs", value: "true" }
      ],
      indent_attr: '\t   ',
      indent_div_attr: '\t '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force'" },
        { name: "indent_with_tabs", value: "true" }
      ],
      indent_attr: '\t',
      indent_div_attr: '\t'
    }],
    tests: [{
        fragment: true,
        input: '<div><div a="1" b="2"><div>test</div></div></div>',
        output: '<div>\n\t<div a="1"\n\t^^^indent_div_attr$$$b="2">\n\t\t<div>test</div>\n\t</div>\n</div>'
      },
      {
        fragment: true,
        unchanged: [
          '<input type="radio"',
          '^^^indent_attr$$$name="garage"',
          '^^^indent_attr$$$id="garage-02"',
          '^^^indent_attr$$$class="ns-e-togg__radio ns-js-form-binding"',
          '^^^indent_attr$$$value="02"',
          '^^^indent_attr$$${{#ifCond data.antragsart "05"}}',
          '^^^indent_attr$$$checked="checked"',
          '^^^indent_attr$$${{/ifCond}}>'
        ]
      },
      {
        fragment: true,
        unchanged: [
          '<div>',
          '\t<input type="radio"',
          '\t^^^indent_attr$$$name="garage"',
          '\t^^^indent_attr$$$id="garage-02"',
          '\t^^^indent_attr$$$class="ns-e-togg__radio ns-js-form-binding"',
          '\t^^^indent_attr$$$value="02"',
          '\t^^^indent_attr$$${{#ifCond data.antragsart "05"}}',
          '\t^^^indent_attr$$$checked="checked"',
          '\t^^^indent_attr$$${{/ifCond}}>',
          '</div>'
        ]
      },
      {
        fragment: true,
        unchanged: [
          '---',
          'layout: mainLayout.html',
          'page: default.html',
          '---',
          '',
          '<div>',
          '\t{{> componentXYZ my.data.key}}',
          '\t{{> componentABC my.other.data.key}}',
          '\t<span>Hello World</span>',
          '\t<p>Your paragraph</p>',
          '</div>'
        ]
      }
    ]
  }, {
    name: "Attribute Wrap de-indent",
    description: "Tags de-indent when attributes are wrapped",
    matrix: [{
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" },
        { name: "indent_with_tabs", value: "false" }
      ]
    }],
    tests: [{
        input: '<div a="1" b="2"><div>test</div></div>',
        output: '<div a="1"\n     b="2">\n    <div>test</div>\n</div>'
      },
      {
        input: '<p>\n    <a href="/test/" target="_blank"><img src="test.jpg" /></a><a href="/test/" target="_blank"><img src="test.jpg" /></a>\n</p>',
        output: '<p>\n    <a href="/test/"\n       target="_blank"><img src="test.jpg" /></a><a href="/test/"\n       target="_blank"><img src="test.jpg" /></a>\n</p>'
      },
      {
        input: '<p>\n    <span data-not-a-href="/test/" data-totally-not-a-target="_blank"><img src="test.jpg" /></span><span data-not-a-href="/test/" data-totally-not-a-target="_blank"><img src="test.jpg" /></span>\n</p>',
        output: '<p>\n    <span data-not-a-href="/test/"\n          data-totally-not-a-target="_blank"><img src="test.jpg" /></span><span data-not-a-href="/test/"\n          data-totally-not-a-target="_blank"><img src="test.jpg" /></span>\n</p>'
      }
    ]
  }, {
    name: "Issue #1403 -- no extra newlines in force-aligned wrap_attributes",
    description: "",
    matrix: [{
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" }
      ]
    }],
    tests: [{
      fragment: true,
      input: '<button class="btn btn-primary" ng-click="shipment.editSendDate = false;sampleTracking.updateShipmentDates({shipment_id: shipment.shipment_id, sent_timestamp: shipment.sending_date})" type="button">Save</button>',
      output: [
        '<button class="btn btn-primary"',
        '        ng-click="shipment.editSendDate = false;sampleTracking.updateShipmentDates({shipment_id: shipment.shipment_id, sent_timestamp: shipment.sending_date})"',
        '        type="button">Save</button>'
      ]
    }]
  }, {
    name: "unformatted_content_delimiter ^^",
    description: "keep delimited together",
    options: [
      { name: "wrap_line_length", value: "80" },
      { name: "unformatted_content_delimiter", value: "'^^'" }
    ],
    tests: [{
      fragment: true,
      input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 ^^09 0010 0011 0012 0013 0014 0015 ^^16 0017 0018 0019 0020</span>',
      output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008\n    ^^09 0010 0011 0012 0013 0014 0015 ^^16 0017 0018 0019 0020</span>'
    }, {
      fragment: true,
      input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020</span>',
      output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014\n    0015 0016 0017 0018 0019 0020</span>'
    }, {
      fragment: true,
      input: '<span>0   0001   0002   0003   0004   0005   0006   0007   0008   0009   ^^10   0011   0012   0013   0014   0015   0016   0^^7   0018   0019   0020</span>',
      output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009\n    ^^10   0011   0012   0013   0014   0015   0016   0^^7 0018 0019 0020</span>'
    }, {
      fragment: true,
      input: '<span>0   0001   0002   0003   0004   0005   0006   0007   0008   0009   0^^0   0011   0012   0013   0014   0015   0016   0^^7   0018   0019   0020</span>',
      output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0^^0 0011 0012 0013 0014\n    0015 0016 0^^7 0018 0019 0020</span>'
    }]
  }, {
    name: "Attribute Wrap",
    description: "Wraps attributes inside of html tags",
    matrix: [{
      options: [
        { name: "wrap_attributes", value: "'force'" }
      ],
      indent_attr: '\n    ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n    '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force'" },
        { name: "wrap_line_length", value: "80" }
      ],
      indent_attr: '\n    ',
      indent_attr_first: ' ',
      indent_attr_first_link: '\n    ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: '\n    ',
      indent_over80: '\n    '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force'" },
        { name: "wrap_attributes_indent_size", value: "8" }
      ],
      indent_attr: '\n        ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n        '
    }, {
      options: [
        { name: "wrap_attributes", value: "'auto'" },
        { name: "wrap_line_length", value: "80" },
        { name: "wrap_attributes_indent_size", value: "0" }
      ],
      indent_attr: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: '\n',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: '\n    ',
      indent_content80: '\n    ',
      indent_over80: '\n'
    }, {
      options: [
        { name: "wrap_attributes", value: "'auto'" },
        { name: "wrap_line_length", value: "80" },
        { name: "wrap_attributes_indent_size", value: "4" }
      ],
      indent_attr: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: '\n    ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: '\n    ',
      indent_content80: '\n    ',
      indent_over80: '\n    '
    }, {
      options: [
        { name: "wrap_attributes", value: "'auto'" },
        { name: "wrap_line_length", value: "0" }
      ],
      indent_attr: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: ' '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" }
      ],
      indent_attr: '\n     ',
      indent_attr_faligned: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n     '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" },
        { name: "wrap_line_length", value: "80" }
      ],
      indent_attr: '\n     ',
      indent_attr_faligned: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: '\n    ',
      indent_over80: '\n     '
    }, {
      options: [
        { name: "wrap_attributes", value: "'aligned-multiple'" },
        { name: "wrap_line_length", value: "80" }
      ],
      indent_attr: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_attr_aligned: ' ',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: '\n    ',
      indent_content80: '\n    ',
      indent_over80: '\n     '
    }, {
      options: [
        { name: "wrap_attributes", value: "'aligned-multiple'" }
      ],
      indent_attr: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: ' '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-aligned'" },
        { name: "wrap_attributes_indent_size", value: "8" }
      ],
      indent_attr: '\n     ',
      indent_attr_faligned: ' ',
      indent_attr_first: ' ',
      indent_attr_first_link: ' ',
      indent_end: '',
      indent_end_selfclosing: ' ',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n     '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_attributes_indent_size", value: "4" }
      ],
      indent_attr: '\n    ',
      indent_attr_first: '\n    ',
      indent_attr_first_link: '\n    ',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n    '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_attributes_indent_size", value: "4" },
        { name: "wrap_line_length", value: "80" }
      ],
      indent_attr: '\n    ',
      indent_attr_first: '\n    ',
      indent_attr_first_link: '\n    ',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: '\n    ',
      indent_over80: '\n    '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_attributes_indent_size", value: "8" }
      ],
      indent_attr: '\n        ',
      indent_attr_first: '\n        ',
      indent_attr_first_link: '\n        ',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n        '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_attributes_indent_size", value: "4" },
        { name: "indent_with_tabs", value: 'true' }
      ],
      indent_attr: '\n\t',
      indent_attr_first: '\n\t',
      indent_attr_first_link: '\n\t',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n\t'
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_attributes_indent_size", value: "7" },
        { name: "indent_with_tabs", value: 'true' }
      ],
      indent_attr: '\n\t   ',
      indent_attr_first: '\n\t   ',
      indent_attr_first_link: '\n\t   ',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: ' ',
      indent_over80: '\n\t   '
    }, {
      options: [
        { name: "wrap_attributes", value: "'force-expand-multiline'" },
        { name: "wrap_line_length", value: "80" },
        { name: "indent_with_tabs", value: 'true' }
      ],
      indent_attr: '\n\t',
      indent_attr_first: '\n\t',
      indent_attr_first_link: '\n\t',
      indent_end: '\n',
      indent_end_selfclosing: '\n',
      indent_content80_selfclosing: ' ',
      indent_content80: '\n\t',
      indent_over80: '\n\t'
    }],
    tests: [{
        input: '<div  >This is some text</div>',
        output: '<div>This is some text</div>'
      }, {
        fragment: true,
        input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020</span>',
        output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014{{indent_content80}}0015 0016 0017 0018 0019 0020</span>'
      }, {
        fragment: true,
        input: '<span>0   0001   0002   0003   0004   0005   0006   0007   0008   0009   0010   0011   0012   0013   0014   0015   0016   0017   0018   0019   0020</span>',
        output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014{{indent_content80}}0015 0016 0017 0018 0019 0020</span>'
      }, {
        fragment: true,
        input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014\t0015 0016 0017 0018 0019 0020</span>',
        output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014{{indent_content80}}0015 0016 0017 0018 0019 0020</span>'
      }, {
        comment: "issue #869",
        fragment: true,
        input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014&nbsp;0015 0016 0017 0018 0019 0020</span>',
        output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013{{indent_content80}}0014&nbsp;0015 0016 0017 0018 0019 0020</span>'
      }, {
        comment: "issue #1324",
        fragment: true,
        input: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009  0010 <span>&nbsp;</span>&nbsp;0015 0016 0017 0018 0019 0020</span>',
        output: '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010{{indent_content80}}<span>&nbsp;</span>&nbsp;0015 0016 0017 0018 0019 0020</span>'
      }, {
        comment: "issue #1496 - respect unicode non-breaking space",
        fragment: true,
        input: "<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011  unic 0013 0014' + unicode_char(160) + '0015 0016 0017 0018 0019 0020</span>",
        output: "<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 unic 0013{{indent_content80}}0014' + unicode_char(160) + '0015 0016 0017 0018 0019 0020</span>"
      }, {
        comment: "issue #1496 and #1324 - respect unicode non-breaking space",
        fragment: true,
        input: "<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011  unic <span>' + unicode_char(160) + '</span>' + unicode_char(160) + '0015 0016 0017 0018 0019 0020</span>",
        output: "<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 unic{{indent_content80}}<span>' + unicode_char(160) + '</span>' + unicode_char(160) + '0015 0016 0017 0018 0019 0020</span>"
      }, {
        fragment: true,
        comment: 'Issue 1222 -- P tags are formatting correctly',
        input: '<p>Our forms for collecting address-related information follow a standard design. Specific input elements willl vary according to the form’s audience and purpose.</p>',
        output: '<p>Our forms for collecting address-related information follow a standard{{indent_content80}}design. Specific input elements willl vary according to the form’s audience{{indent_content80}}and purpose.</p>'
      }, {
        input: '<div attr="123"  >This is some text</div>',
        output: '<div attr="123">This is some text</div>'
      }, {
        fragment: true,
        input: '<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>',
        output: '<div{{indent_attr_first}}attr0{{indent_attr}}attr1="123"{{indent_attr}}data-attr2="hello    t here"{{indent_end}}>This is some text</div>'
      }, {
        fragment: true,
        input: '<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is text</div>',
        output: '<div{{indent_attr_first}}lookatthissuperduperlongattributenamewhoahcrazy0="true"{{indent_attr}}attr0{{indent_attr}}attr1="123"{{indent_over80}}data-attr2="hello    t here"{{indent_over80}}heymanimreallylongtoowhocomesupwiththesenames="false"{{indent_end}}>This is text</div>'
      }, {
        fragment: true,
        input: '<img attr0 attr1="123" data-attr2="hello    t here"/>',
        output: '<img{{indent_attr_first}}attr0{{indent_attr}}attr1="123"{{indent_attr}}data-attr2="hello    t here"{{indent_end_selfclosing}}/>'
      }, {
        fragment: true,
        input: '<?xml version="1.0" encoding="UTF-8" ?><root attr1="foo" attr2="bar"/>',
        output: '<?xml version="1.0" encoding="UTF-8" ?>\n<root{{indent_attr_first}}attr1="foo"{{indent_attr}}{{indent_attr_faligned}}attr2="bar"{{indent_end_selfclosing}}/>'
      }, {
        comment: "Issue #1094 - Beautify correctly without quotes and with extra spaces",
        fragment: true,
        input: '<div lookatthissuperduperlongattributenamewhoahcrazy0 =    "true" attr0 attr1=  12345 data-attr2   ="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is text</div>',
        output: '<div{{indent_attr_first}}lookatthissuperduperlongattributenamewhoahcrazy0="true"{{indent_attr}}attr0{{indent_attr}}attr1=12345{{indent_over80}}data-attr2="hello    t here"{{indent_over80}}heymanimreallylongtoowhocomesupwiththesenames="false"{{indent_end}}>This is text</div>'
      },
      {
        fragment: true,
        input: '<?xml version="1.0" encoding="UTF-8" ?><root attr1   =   foo12   attr2  ="bar"    />',
        output: '<?xml version="1.0" encoding="UTF-8" ?>\n<root{{indent_attr_first}}attr1=foo12{{indent_attr}}{{indent_attr_faligned}}attr2="bar"{{indent_end_selfclosing}}/>'
      },
      // Not ready
      // {
      //   fragment: true,
      //   input: '<?xml version=    "1.0"    encoding = "UTF-8" ?><root attr1   =   foo   attr2="bar"/>',
      //   output: '<?xml version="1.0" encoding="UTF-8" ?>\n<root{{indent_attr_first}}attr1=foo{{indent_attr}}{{indent_attr_faligned}}attr2="bar"{{indent_end_selfclosing}}/>'
      // },
      {
        input: '<link href="//fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,700,300&amp;subset=latin" rel="stylesheet" type="text/css">',
        output: '<link{{indent_attr_first_link}}href="//fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,400,600,700,300&amp;subset=latin"{{indent_over80}}{{indent_attr_faligned}}{{indent_attr_aligned}}rel="stylesheet"{{indent_attr}}{{indent_attr_faligned}}type="text/css"{{indent_end}}>'
      }
    ]
  }, {
    name: "Issue #1335 -- <button> Bug with force-expand-multiline formatting",
    description: "",
    template: "^^^ $$$",
    options: [
      { name: "wrap_attributes", value: "'force-expand-multiline'" }
    ],
    tests: [{
      fragment: true,
      unchanged: [
        '<button',
        '    class="my-class"',
        '    id="id1"',
        '>',
        '    Button 1',
        '</button>',
        '',
        '<button',
        '    class="my-class"',
        '    id="id2"',
        '>',
        '    Button 2',
        '</button>'
      ]
    }, {
      input_: [
        '<button>',
        '    <span>foo</span>',
        '<p>bar</p>',
        '</button>'
      ],
      output: [
        '<button>',
        '    <span>foo</span>',
        '    <p>bar</p>',
        '</button>'
      ]
    }]
  }, {
    name: "Issue #1125 -- Add preserve and preserve_aligned attribute options",
    description: "",
    template: "^^^ $$$",
    matrix: [{
      options: [
        { name: "wrap_attributes", value: "'preserve-aligned'" }
      ],
      indent_attr: '       '
    }, {
      options: [
        { name: "wrap_attributes", value: "'preserve'" }
      ],
      indent_attr: '    '
    }],
    tests: [{
      input: [
        '<input type="text"     class="form-control"  autocomplete="off"',
        '[(ngModel)]="myValue"          [disabled]="isDisabled" [placeholder]="placeholder"',
        '[typeahead]="suggestionsSource" [typeaheadOptionField]="suggestionValueField" [typeaheadItemTemplate]="suggestionTemplate"   [typeaheadWaitMs]="300"',
        '(typeaheadOnSelect)="onSuggestionSelected($event)" />'
      ],
      output: [
        '<input type="text" class="form-control" autocomplete="off"',
        '^^^indent_attr$$$[(ngModel)]="myValue" [disabled]="isDisabled" [placeholder]="placeholder"',
        '^^^indent_attr$$$[typeahead]="suggestionsSource" [typeaheadOptionField]="suggestionValueField" [typeaheadItemTemplate]="suggestionTemplate" [typeaheadWaitMs]="300"',
        '^^^indent_attr$$$(typeaheadOnSelect)="onSuggestionSelected($event)" />'
      ]
    }]
  }, {
    name: "Handlebars Indenting Off",
    description: "Test handlebar behavior when indenting is off",
    template: "^^^ $$$",
    options: [
      { name: "indent_handlebars", value: "false" }
    ],
    tests: [{
        fragment: true,
        input_: '{{#if 0}}\n' + '    <div>\n' + '    </div>\n' + '{{/if}}',
        output: '{{#if 0}}\n' + '<div>\n' + '</div>\n' + '{{/if}}'
      }, {
        fragment: true,
        input_: '<div>\n' + '{{#each thing}}\n' + '    {{name}}\n' + '{{/each}}\n' + '</div>',
        output: '<div>\n' + '    {{#each thing}}\n' + '    {{name}}\n' + '    {{/each}}\n' + '</div>'
      },
      {
        input_: [
          '{{em-input label="Some Labe" property="amt" type="text" placeholder=""}}',
          '   {{em-input label="Type*" property="type" type="text" placeholder="(LTD)"}}',
          '       {{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ],
        output: [
          '{{em-input label="Some Labe" property="amt" type="text" placeholder=""}}',
          '{{em-input label="Type*" property="type" type="text" placeholder="(LTD)"}}',
          '{{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ]
      },
      {
        comment: "Issue #1469 - preserve newlines inside handlebars, including first one. Just treated as text here.",
        input_: [
          '{{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '   {{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '       {{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ],
        output: [
          '{{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '{{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '{{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ]
      },
      {
        input_: [
          '<div>',
          '{{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '   {{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '       {{em-input label="Place*" property="place" type="text" placeholder=""}}',
          '</div>'
        ],
        output: [
          '<div>',
          '    {{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '    {{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '    {{em-input label="Place*" property="place" type="text" placeholder=""}}',
          '</div>'
        ]
      },
      {
        input_: [
          '{{#if callOn}}',
          '{{#unless callOn}}',
          '      {{translate "onText"}}',
          '   {{else}}',
          '{{translate "offText"}}',
          '{{/unless callOn}}',
          '   {{else if (eq callOn false)}}',
          '{{translate "offText"}}',
          '        {{/if}}'
        ],
        output: [
          '{{#if callOn}}',
          '{{#unless callOn}}',
          '{{translate "onText"}}',
          '{{else}}',
          '{{translate "offText"}}',
          '{{/unless callOn}}',
          '{{else if (eq callOn false)}}',
          '{{translate "offText"}}',
          '{{/if}}'
        ]
      }
    ]
  }, {
    name: "Handlebars Indenting On",
    description: "Test handlebar formatting",
    template: "^^^ $$$",
    matrix: [{
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{field}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{em-input label="Some Labe" property="amt" type="text" placeholder=""}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{! comment}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{!-- comment--}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{Hello "woRld"}} {{!-- comment--}} {{heLloWorlD}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{pre{{field1}} {{field2}} {{field3}}post',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{! \n mult-line\ncomment  \n     with spacing\n}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{!-- \n mult-line\ncomment  \n     with spacing\n--}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" }
      ],
      content: '{{!-- \n mult-line\ncomment \n{{#> component}}\n mult-line\ncomment  \n     with spacing\n {{/ component}}--}}',
      indent_over80: ' '
    }, {
      options: [
        { name: "indent_handlebars", value: "true" },
        { name: "wrap_line_length", value: "80" }
      ],
      content: 'content',
      indent_over80: '\n    ',
      wrap_over80: '\n    ',
      wrap_content_over80: '\n        '
    }],
    tests: [
      { unchanged: '{{page-title}}' },
      {
        unchanged: [
          '{{page-title}}',
          '{{a}}',
          '{{value-title}}'
        ]
      },
      {
        input: [
          '{{textarea value=someContent}}',
          '',
          '^^^&content$$$',
          '{{#if condition}}',
          '    <div  class="some">{{helper "hello"}}<strong>{{helper "world"}}</strong></div>',
          '{{/if}}',
          '^^^&content$$$'
        ],
        output: [
          '{{textarea value=someContent}}',
          '',
          '^^^&content$$$',
          '{{#if condition}}',
          '    <div class="some">{{helper "hello"}}<strong>{{helper "world"}}</strong>^^^wrap_over80$$$</div>',
          '{{/if}}',
          '^^^&content$$$'
        ]
      },
      {
        input: [
          '{{textarea value=someContent}}',
          '',
          '^^^&content$$$',
          '{{#if condition}}',
          '    <div  class="some-class-detail">{{helper "hello"}}<strong>{{helper "world"}}</strong>{{helper "hello"}}<strong>{{helper "world"}}</strong></div>',
          '{{/if}}',
          '^^^&content$$$'
        ],
        output: [
          '{{textarea value=someContent}}',
          '',
          '^^^&content$$$',
          '{{#if condition}}',
          '    <div class="some-class-detail">^^^wrap_content_over80$$${{helper "hello"}}<strong>{{helper "world"}}</strong>{{helper "hello"}}<strong>{{helper "world"}}</strong>^^^wrap_over80$$$</div>',
          '{{/if}}',
          '^^^&content$$$'
        ]
      },
      {
        comment: "error case",
        unchanged: [
          '{{page-title}}',
          '{{ myHelper someValue}}',
          '^^^&content$$$',
          '{{value-title}}'
        ]
      },
      {
        comment: "Issue #1469 - preserve newlines inside handlebars, including first one. BUG: does not fix indenting inside handlebars.",
        input_: [
          '{{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '^^^&content$$$',
          '   {{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '       {{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ],
        output: [
          '{{em-input',
          '  label="Some Labe" property="amt"',
          '  type="text" placeholder=""}}',
          '^^^&content$$$',
          '{{em-input label="Type*"',
          'property="type" type="text" placeholder="(LTD)"}}',
          '{{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ]
      },
      {
        unchanged: [
          '{{em-input label="Some Labe" property="amt" type="text" placeholder=""}}',
          '^^^&content$$$',
          '{{em-input label="Type*" property="type" type="text" placeholder="(LTD)"}}',
          '{{em-input label="Place*" property="place" type="text" placeholder=""}}'
        ]
      },
      { unchanged: '{{#if 0}}{{/if}}' },
      { unchanged: '{{#if 0}}^^^&content$$${{/if}}' },
      { unchanged: '{{#if 0}}\n{{/if}}' }, {
        input_: '{{#if     words}}{{/if}}',
        output: '{{#if words}}{{/if}}'
      }, {
        input_: '{{#if     words}}^^^&content$$${{/if}}',
        output: '{{#if words}}^^^&content$$${{/if}}'
      }, {
        input_: '{{#if     words}}^^^&content$$${{/if}}',
        output: '{{#if words}}^^^&content$$${{/if}}'
      }, {
        unchanged: '{{#if 1}}\n' + '    <div>\n' + '    </div>\n' + '{{/if}}'
      }, {
        input_: '{{#if 1}}\n' + '<div>\n' + '</div>\n' + '{{/if}}',
        output: '{{#if 1}}\n' + '    <div>\n' + '    </div>\n' + '{{/if}}'
      }, {
        unchanged: '<div>\n' + '    {{#if 1}}\n' + '    {{/if}}\n' + '</div>'
      }, {
        input_: '<div>\n' + '{{#if 1}}\n' + '{{/if}}\n' + '</div>',
        output: '<div>\n' + '    {{#if 1}}\n' + '    {{/if}}\n' + '</div>'
      }, {
        input_: '{{#if}}\n' + '{{#each}}\n' + '{{#if}}\n' + '^^^&content$$$\n' + '{{/if}}\n' + '{{#if}}\n' + '^^^&content$$$\n' + '{{/if}}\n' + '{{/each}}\n' + '{{/if}}',
        output: '{{#if}}\n' + '    {{#each}}\n' + '        {{#if}}\n' + '            ^^^&content$$$\n' + '        {{/if}}\n' + '        {{#if}}\n' + '            ^^^&content$$$\n' + '        {{/if}}\n' + '    {{/each}}\n' + '{{/if}}'
      }, {
        unchanged: '{{#if 1}}\n' + '    <div>\n' + '    </div>\n' + '{{/if}}'
      },

      // Issue #576 -- Indent Formatting with Handlebars
      {
        input_: [
          '<div>',
          '    <small>SMALL TEXT</small>',
          '    <span>',
          '        {{#if isOwner}}',
          '    <span><i class="fa fa-close"></i></span>',
          '        {{else}}',
          '            <span><i class="fa fa-bolt"></i></span>',
          '        {{/if}}',
          '    </span>',
          '    <strong>{{userName}}:&nbsp;</strong>{{text}}',
          '</div>'
        ],
        output: [
          '<div>',
          '    <small>SMALL TEXT</small>',
          '    <span>',
          '        {{#if isOwner}}',
          '            <span><i class="fa fa-close"></i></span>',
          '        {{else}}',
          '            <span><i class="fa fa-bolt"></i></span>',
          '        {{/if}}',
          '    </span>',
          '    <strong>{{userName}}:&nbsp;</strong>{{text}}',
          '</div>'
        ]
      }, {
        unchanged: [
          '<div>',
          '    <small>SMALL TEXT</small>',
          '    <span>',
          '        {{#if isOwner}}',
          '            <span><i class="fa fa-close"></i></span>',
          '        {{else}}',
          '            <span><i class="fa fa-bolt"></i></span>',
          '        {{/if}}',
          '    </span>',
          '    <strong>{{userName}}:&nbsp;</strong>{{text}}',
          '</div>'
        ]
      },

      // Issue #1040 -- Ignore expressions in handlebar tags
      {
        unchanged: [
          '{{#if `this.customerSegment == "Active"`}}',
          '    ...',
          '{{/if}}'
        ]
      },

      // Issue #1415 -- Indent Formatting with Handlebars and &nbsp
      {
        input_: [
          '{{#isDealLink}}',
          '&nbsp;&nbsp;<a target="_blank" href="{{dealLink}}" class="weak">See</a>',
          '{{/isDealLink}}'
        ],
        output: [
          '{{#isDealLink}}',
          '    &nbsp;&nbsp;<a target="_blank" href="{{dealLink}}" class="weak">See</a>',
          '{{/isDealLink}}'
        ]
      },

      // Test {{else}} aligned with {{#if}} and {{/if}}
      {
        input_: '{{#if 1}}\n' + '    ^^^&content$$$\n' + '    {{else}}\n' + '    ^^^&content$$$\n' + '{{/if}}',
        output: '{{#if 1}}\n' + '    ^^^&content$$$\n' + '{{else}}\n' + '    ^^^&content$$$\n' + '{{/if}}'
      }, {
        input_: '{{#if 1}}\n' + '    {{else}}\n' + '    {{/if}}',
        output: '{{#if 1}}\n' + '{{else}}\n' + '{{/if}}'
      }, {
        input_: '{{#if thing}}\n' + '{{#if otherthing}}\n' + '    ^^^&content$$$\n' + '    {{else}}\n' + '^^^&content$$$\n' + '    {{/if}}\n' + '       {{else}}\n' + '^^^&content$$$\n' + '{{/if}}',
        output: '{{#if thing}}\n' + '    {{#if otherthing}}\n' + '        ^^^&content$$$\n' + '    {{else}}\n' + '        ^^^&content$$$\n' + '    {{/if}}\n' + '{{else}}\n' + '    ^^^&content$$$\n' + '{{/if}}'
      },
      {
        comment: 'ISSUE #800 and #1123: else if and #unless',
        input_: [
          '{{#if callOn}}',
          '{{#unless callOn}}',
          '      ^^^&content$$$',
          '   {{else}}',
          '{{translate "offText"}}',
          '{{/unless callOn}}',
          '   {{else if (eq callOn false)}}',
          '^^^&content$$$',
          '        {{/if}}'
        ],
        output: [
          '{{#if callOn}}',
          '    {{#unless callOn}}',
          '        ^^^&content$$$',
          '    {{else}}',
          '        {{translate "offText"}}',
          '    {{/unless callOn}}',
          '{{else if (eq callOn false)}}',
          '    ^^^&content$$$',
          '{{/if}}'
        ]
      },
      // Test {{}} inside of <> tags, which should be separated by spaces
      // for readability, unless they are inside a string.
      {
        input_: '<div {{someStyle}}>  </div>',
        output: '<div {{someStyle}}> </div>'
      }, {
        comment: 'only partial support for complex templating in attributes',
        input_: '<dIv {{#if test}}class="foo"{{/if}}>^^^&content$$$</dIv>',
        output: '<dIv {{#if test}}class="foo" {{/if}}>^^^&content$$$</dIv>'
      }, {
        fragment: true,
        input_: '<diV {{#if thing}}{{somestyle}}class_spacing_for="{{class}}"{{else}}class="{{class2}}"{{/if}}>^^^&content$$$</diV>',
        output: '<diV {{#if thing}}{{somestyle}}class_spacing_for="{{class}}"^^^&indent_over80$$${{else}}class="{{class2}}" {{/if}}>^^^&content$$$</diV>'
      },
      // {
      //   fragment: true,
      //   input_: '<div>\n<diV{{#if thing}}{{somestyle}}class_spacing_for="{{class}}"{{else}}class="{{class2}}"{{/if}}>^^^&content$$$</diV>\n<span />\n</div>',
      //   output: '<div>\n    <diV {{#if thing}} {{somestyle}} class_spacing_for="{{class}}" {{else}}^^^&indent_over80$$$class="{{class2}}" {{/if}}>^^^&content$$$</diV>\n    <span />\n</div>'
      // },
      {
        comment: 'partiial support for templating in attributes',
        input_: '<span {{#if condition}}class="foo"{{/if}}>^^^&content$$$</span>',
        output: '<span {{#if condition}}class="foo" {{/if}}>^^^&content$$$</span>'
      }, {
        unchanged: '<{{ele}} unformatted="{{#if}}^^^&content$$${{/if}}">^^^&content$$$</{{ele}}>'
      }, {
        unchanged: '<div unformatted="{{#if}}^^^&content$$${{/if}}">^^^&content$$$</div>'
      }, {
        unchanged: '<div unformatted="{{#if  }}    ^^^&content$$${{/if}}">^^^&content$$$</div>'
      },

      // Quotes found inside of Handlebars expressions inside of quoted
      // strings themselves should not be considered string delimiters.
      {
        unchanged: '<div class="{{#if thingIs "value"}}^^^&content$$${{/if}}"></div>'
      }, {
        unchanged: '<div class="{{#if thingIs \\\'value\\\'}}^^^&content$$${{/if}}"></div>'
      }, {
        unchanged: '<div class=\\\'{{#if thingIs "value"}}^^^&content$$${{/if}}\\\'></div>'
      }, {
        unchanged: '<div class=\\\'{{#if thingIs \\\'value\\\'}}^^^&content$$${{/if}}\\\'></div>'
      }, {
        unchanged: '<span>{{condition < 0 ? "result1" : "result2"}}</span>'
      }, {
        unchanged: '<span>{{condition1 && condition2 && condition3 && condition4 < 0 ? "resForTrue" : "resForFalse"}}</span>'
      }
    ]
  }, {
    name: "Handlebars Else If, Each, and Inverted Section tag indenting",
    description: "Handlebar Else If, Each, and Inverted Section handling tags should be newlined after formatted tags",
    template: "^^^ $$$",
    options: [
      { name: "indent_handlebars", value: "true" }
    ],
    tests: [{
        input_: '{{#if test}}<div></div>{{else}}<div></div>{{/if}}',
        output: '{{#if test}}\n' + '    <div></div>\n' + '{{else}}\n' + '    <div></div>\n' + '{{/if}}'
      }, {
        unchanged: '{{#if test}}<span></span>{{else}}<span></span>{{/if}}'
      },
      // Else if handling
      {
        input: ['<a class="navbar-brand">',
          '    {{#if connected}}',
          '        <i class="fa fa-link" style="color:green"></i> {{else if sleep}}',
          '        <i class="fa fa-sleep" style="color:yellow"></i>',
          '    {{else}}',
          '        <i class="fa fa-unlink" style="color:red"></i>',
          '    {{/if}}',
          '</a>'
        ],
        output: ['<a class="navbar-brand">',
          '    {{#if connected}}',
          '        <i class="fa fa-link" style="color:green"></i>',
          '    {{else if sleep}}',
          '        <i class="fa fa-sleep" style="color:yellow"></i>',
          '    {{else}}',
          '        <i class="fa fa-unlink" style="color:red"></i>',
          '    {{/if}}',
          '</a>'
        ]
      },
      // Each handling
      {
        unchanged: [
          '{{#each clinics as |clinic|}}',
          '    <p>{{clinic.name}}</p>',
          '{{else}}',
          '    <p>Unfortunately no clinics found.</p>',
          '{{/each}}'
        ]
      },
      // Inverted section handling.
      {
        comment: "Issue #1623 - Fix indentation of `^` inverted section tags in Handlebars/Mustache code",
        unchanged: [
          '{{^inverted-condition}}',
          '    <p>Unfortunately this condition is false.</p>',
          '{{/inverted-condition}}'
        ]
      }
    ]
  }, {
    name: "Unclosed html elements",
    description: "Unclosed elements should not indent",
    options: [],
    tests: [
      { unchanged: '<source>\n<source>' },
      { unchanged: '<br>\n<br>' },
      { unchanged: '<input>\n<input>' },
      { unchanged: '<meta>\n<meta>' },
      { unchanged: '<link>\n<link>' },
      { unchanged: '<colgroup>\n    <col>\n    <col>\n</colgroup>' },
      { input: '<source>\n    <source>', output: '<source>\n<source>' },
      { input: '<br>\n    <br>', output: '<br>\n<br>' },
      { input: '<input>\n    <input>', output: '<input>\n<input>' },
      { input: '<meta>\n    <meta>', output: '<meta>\n<meta>' },
      { input: '<link>\n    <link>', output: '<link>\n<link>' },
      { input: '<colgroup>\n        <col>\n        <col>\n</colgroup>', output: '<colgroup>\n    <col>\n    <col>\n</colgroup>' }
    ]
  }, {
    name: "Optional html elements",
    description: "Optional elements should not indent",
    options: [],
    tests: [{
      fragment: true,
      unchanged: [
        '<li>test content',
        '<li>test content',
        '<li>test content'
      ]
    }, {
      unchanged: [
        '<ol>',
        '    <li>test content',
        '    <li>test content',
        '    <li>test content',
        '</ol>'
      ]
    }, {
      unchanged: [
        '<ol>',
        '    <li>',
        '        test content',
        '    <li>',
        '        <ul>',
        '            <li> extra text',
        '            <li> depth check',
        '        </ul>',
        '    <li> test content',
        '    <li>',
        '        test content',
        '</ol>'
      ]
    }, {
      unchanged: [
        '<dl>',
        '    <dt>',
        '        test content',
        '    <dt>',
        '        test content',
        '    <dd>',
        '        test content',
        '    <dd>',
        '        test content',
        '    <dt>',
        '        test content',
        '    <dd>',
        '        <dl>',
        '            <dt>',
        '                test content',
        '            <dt>',
        '                test content',
        '            <dd>',
        '                test content',
        '        </dl>',
        '</dl>'
      ]
    }, {
      unchanged: [
        '<select>',
        '    <optgroup>',
        '        test content',
        '    <optgroup>',
        '        test content',
        '        <option>',
        '            test content',
        '        <option>',
        '            test content',
        '    <optgroup>',
        '        test content',
        '        <option>',
        '            test content',
        '        <option>',
        '            test content',
        '</select>'
      ]
    }, {
      comment: "Regression test for #1649",
      unchanged: [
        '<table>',
        '    <tbody>',
        '        <tr>',
        '            <td>',
        '                <table>',
        '                    <thead>',
        '                        <th>',
        '                        </th>',
        '                    </thead>',
        '                    <tbody>',
        '                        <tr>',
        '                            <td>',
        '                            </td>',
        '                        </tr>',
        '                    </tbody>',
        '                </table>',
        '            </td>',
        '        </tr>',
        '    </tbody>',
        '</table>'
      ]
    }, {
      unchanged: [
        '<table>',
        '    <caption>37547 TEE Electric Powered Rail Car Train Functions (Abbreviated)',
        '    <colgroup>',
        '        <col>',
        '        <col>',
        '        <col>',
        '    <thead>',
        '        <tr>',
        '            <th>Function',
        '            <th>Control Unit',
        '            <th>Central Station',
        '    <tbody>',
        '        <tr>',
        '            <td>Headlights',
        '            <td>✔',
        '            <td>✔',
        '        <tr>',
        '            <td>Interior Lights',
        '            <td>✔',
        '            <td>✔',
        '        <tr>',
        '            <td>Electric locomotive operating sounds',
        '            <td>✔',
        '                <table>',
        '                    <caption>37547 TEE Electric Powered Rail Car Train Functions (Abbreviated)',
        '                    <colgroup>',
        '                        <col>',
        '                        <col>',
        '                        <col>',
        '                    <thead>',
        '                        <tr>',
        '                            <th>Function',
        '                            <th>Control Unit',
        '                            <th>Central Station',
        '                    <tbody>',
        '                        <tr>',
        '                            <td>Headlights',
        '                            <td>✔',
        '                            <td>✔',
        '                        <tr>',
        '                            <td>Interior Lights',
        '                            <td>✔',
        '                            <td>✔',
        '                        <tr>',
        '                            <td>Electric locomotive operating sounds',
        '                            <td>✔',
        '                            <td>✔',
        '                        <tr>',
        '                            <td>Engineer’s cab lighting',
        '                            <td>',
        '                            <td>✔',
        '                        <tr>',
        '                            <td>Station Announcements - Swiss',
        '                            <td>',
        '                            <td>✔',
        '                    <tfoot>',
        '                        <tr>',
        '                            <td>Station Announcements - Swiss',
        '                            <td>',
        '                            <td>✔',
        '                </table>',
        '            <td>✔',
        '        <tr>',
        '            <td>Engineer’s cab lighting',
        '            <td>',
        '            <td>✔',
        '        <tr>',
        '            <td>Station Announcements - Swiss',
        '            <td>',
        '            <td>✔',
        '    <tfoot>',
        '        <tr>',
        '            <td>Station Announcements - Swiss',
        '            <td>',
        '            <td>✔',
        '</table>'
      ]
    }, {
      comment: 'Regression test for #1213',
      input: [
        '<ul><li>ab<li>cd</li><li>cd</li></ul><dl><dt>ef<dt>gh</dt><dt>gh</dt></dl>',
        '<ul><li>ab</li><li>cd<li>cd</li></ul><dl><dt>ef</dt><dt>gh<dt>gh</dt></dl>'
      ],
      output: [
        '<ul>',
        '    <li>ab',
        '    <li>cd</li>',
        '    <li>cd</li>',
        '</ul>',
        '<dl>',
        '    <dt>ef',
        '    <dt>gh</dt>',
        '    <dt>gh</dt>',
        '</dl>',
        '<ul>',
        '    <li>ab</li>',
        '    <li>cd',
        '    <li>cd</li>',
        '</ul>',
        '<dl>',
        '    <dt>ef</dt>',
        '    <dt>gh',
        '    <dt>gh</dt>',
        '</dl>'
      ]
    }]
  }, {
    name: "Unformatted tags",
    description: "Unformatted tag behavior",
    options: [],
    tests: [{
        input: '<ol>\n    <li>b<pre>c</pre></li>\n</ol>',
        output: [
          '<ol>',
          '    <li>b',
          '        <pre>c</pre>',
          '    </li>',
          '</ol>'
        ]
      },
      { unchanged: '<ol>\n    <li>b<code>c</code></li>\n</ol>' },
      { unchanged: '<ul>\n    <li>\n        <span class="octicon octicon-person"></span>\n        <a href="/contact/">Kontakt</a>\n    </li>\n</ul>' },
      { unchanged: '<div class="searchform"><input type="text" value="" name="s" id="s" /><input type="submit" id="searchsubmit" value="Search" /></div>' },
      { unchanged: '<div class="searchform"><input type="text" value="" name="s" id="s"><input type="submit" id="searchsubmit" value="Search"></div>' },
      { unchanged: '<p>\n    <a href="/test/"><img src="test.jpg" /></a>\n</p>' },
      { unchanged: '<p>\n    <a href="/test/"><img src="test.jpg" /></a><a href="/test/"><img src="test.jpg" /></a>\n</p>' },
      { unchanged: '<p>\n    <a href="/test/"><img src="test.jpg" /></a><a href="/test/"><img src="test.jpg" /></a><a href="/test/"><img src="test.jpg" /></a><a href="/test/"><img src="test.jpg" /></a>\n</p>' },
      { unchanged: '<p>\n    <span>image: <img src="test.jpg" /></span><span>image: <img src="test.jpg" /></span>\n</p>' },
      { unchanged: '<p>\n    <strong>image: <img src="test.jpg" /></strong><strong>image: <img src="test.jpg" /></strong>\n</p>' }
    ]
  }, {
    name: "File starting with comment",
    description: "Unformatted tag behavior",
    options: [],
    tests: [{
      unchanged: [
        '<!--sample comment -->',
        '',
        '<html>',
        '<body>',
        '    <span>a span</span>',
        '</body>',
        '',
        '</html>'
      ]
    }]
  }, {
    name: "ISSUE #545 and #944 Ignore directive works in html",
    description: "",
    options: [],
    tests: [{
      comment: 'ignore starts _after_ the start comment, ends after the end comment',
      unchanged: [
        '<div>',
        '    <!-- beautify ignore:start -->',
        '@{',
        '',
        '    ViewBag.Title = "Dashboard";',
        '    string firstName = string.Empty;',
        '    string userId = ViewBag.UserId;',
        '',
        '    if( !string.IsNullOrEmpty(ViewBag.FirstName ) ) {',
        '',
        '         firstName = "<h2>Hi " + ViewBag.FirstName + "</h2>";',
        '',
        '    }',
        '',
        '}',
        ' <!-- beautify ignore:end -->',
        '',
        '    <header class="layout-header">',
        '',
        '        <h2 id="logo"><a href="/">Logo</a></h2>',
        '',
        '        <ul class="social">',
        '',
        '            <li class="facebook"><a href="#">Facebook</a></li>',
        '            <li class="twitter"><a href="#">Twitter</a></li>',
        '',
        '        </ul>',
        '',
        '    </header>',
        '</div>'
      ]
    }]
  }, {
    name: "Issue 1478 - Space handling inside self closing tag",
    description: "Properly indent following text after self closing tags regardless of space",
    options: [],
    tests: [{
      input: [
        '<div>',
        '    <br/>',
        '    <br />',
        '</div>'
      ],
      output: [
        '<div>',
        '    <br />',
        '    <br />',
        '</div>'
      ]
    }]
  }, {
    name: "Single line comment after closing tag",
    description: "Keep single line comments as they are after closing tags",
    options: [],
    tests: [{
      input: [
        '<div class="col">',
        '    <div class="row">',
        '        <div class="card">',
        '',
        '            <h1>Some heading</h1>',
        '            <p>Some text for the card.</p>',
        '            <img src="some/image.jpg" alt="">',
        '',
        '            </div>    <!-- /.card -->',
        '    </div>',
        '            <!-- /.row -->',
        '</div> <!-- /.col -->'
      ],
      output: [
        '<div class="col">',
        '    <div class="row">',
        '        <div class="card">',
        '',
        '            <h1>Some heading</h1>',
        '            <p>Some text for the card.</p>',
        '            <img src="some/image.jpg" alt="">',
        '',
        '        </div> <!-- /.card -->',
        '    </div>',
        '    <!-- /.row -->',
        '</div> <!-- /.col -->'
      ]
    }]
  }, {
    name: "Regression Tests",
    description: "Regression Tests",
    options: [],
    tests: [{
        comment: '#1202',
        unchanged: '<a class="js-open-move-from-header" href="#">5A - IN-SPRINT TESTING</a>'
      },
      { fragment: true, unchanged: '<a ">9</a">' },
      { unchanged: '<a href="javascript:;" id="_h_url_paid_pro3" onmousedown="_h_url_click_paid_pro(this);" rel="nofollow" class="pro-title" itemprop="name">WA GlassKote</a>' },
      { unchanged: '<a href="/b/yergey-brewing-a-beer-has-no-name/1745600">"A Beer Has No Name"</a>' },
      {
        comment: '#1304',
        unchanged: '<label>Every</label><input class="scheduler__minutes-input" type="text">'
      },
      {
        comment: '#1377',
        unchanged: [
          '<a href=\\\'\\\' onclick=\\\'doIt("<?php echo str_replace("\\\'", "\\\\ ", $var); ?>  "); \\\'>',
          '    Test',
          '</a>',
          '',
          '<?php include_once $_SERVER[\\\'DOCUMENT_ROOT\\\'] . "/shared/helpModal.php";  ?>'
        ]
      }
    ]
  }, {
    name: "minimal template handling",
    description: "treated as content.",
    template: "^^^ $$$",
    matrix: [

      // Php (<?php ... ?> and <?= ... ?>) =.
      {
        s: '<?php',
        e: '?>'
      },
      {
        s: '<?=',
        e: '?>'
      },
      // erb, ejs, asp: <% ... %>
      {
        s: '<%',
        e: '%>'
      },
      // django {{ ... }} and {# ... #} and {% ... %}
      {
        s: '{{',
        e: '}}'
      },
      {
        s: '{#',
        e: '#}'
      },
      {
        s: '{%',
        e: '%}'
      },
      // handlebars {{ ... }} and {{# ... }} and {{! ... }} and {{!-- --}}
      {
        options: [
          { name: "indent_handlebars", value: "false" }
        ],
        s: '{{',
        e: '}}'
      },
      {
        options: [
          { name: "indent_handlebars", value: "false" }
        ],
        s: '{{#',
        e: '}}'
      },
      {
        options: [
          { name: "indent_handlebars", value: "false" }
        ],
        s: '{{!',
        e: '}}'
      },
      {
        options: [
          { name: "indent_handlebars", value: "false" }
        ],
        s: '{{!--',
        e: '--}}'
      }

    ],
    tests: [{
      input: '<h1  class="content-page-header">^^^s$$$$view["name"]; ^^^e$$$</h1>',
      output: '<h1 class="content-page-header">^^^s$$$$view["name"]; ^^^e$$$</h1>'
    }, {
      unchanged: [
        '^^^s$$$',
        'for($i = 1; $i <= 100; $i++;) {',
        '    #count to 100!',
        '    echo($i . "</br>");',
        '}',
        '^^^e$$$'
      ]
    }, {
      fragment: true,
      unchanged: [
        '^^^s$$$ ^^^e$$$',
        '<!DOCTYPE html>',
        '',
        '<html>',
        '',
        '<head></head>',
        '',
        '<body></body>',
        '',
        '</html>'
      ]
    }, {
      unchanged: [
        '^^^s$$$ "A" ^^^e$$$abc^^^s$$$ "D" ^^^e$$$',
        '^^^s$$$ "B" ^^^e$$$',
        '^^^s$$$ "C" ^^^e$$$'
      ]
    }, {
      unchanged: [
        '^^^s$$$',
        'echo "A";',
        '^^^e$$$',
        '<span>Test</span>'
      ]
    }, {
      unchanged: [
        '<^^^s$$$ html_element(); ^^^e$$$ ^^^s$$$language_attributes();^^^e$$$>abc</^^^s$$$ html_element(); ^^^e$$$>'
      ]
    }, {
      unchanged: [
        '<input type="text" value="^^^s$$$$x["test"] . $x[\\\'test\\\']^^^e$$$">'
      ]
    }]
  }, {
    name: "Support simple language specific option inheritance/overriding",
    description: "Support simple language specific option inheritance/overriding",
    matrix: [{
        options: [
          { name: "js", value: "{ 'indent_size': 3 }" },
          { name: "css", value: "{ 'indent_size': 5 }" }
        ],
        h: '    ',
        c: '     ',
        j: '   ',
        dhc: '    ',
        dhj: '    ',
        dc: '     ',
        dj: '   '
      },
      {
        options: [
          { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 } }" }
        ],
        h: '    ',
        c: '     ',
        j: '   ',
        dhc: '    ',
        dhj: '    ',
        dc: '     ',
        dj: '   '
      },
      {
        options: [
          { name: "indent_size", value: "9" },
          { name: "js", value: "{ 'indent_size': 5 }" },
          { name: "css", value: "{ 'indent_size': 3 }" }
        ],
        h: '         ',
        c: '   ',
        j: '     ',
        dhc: '         ',
        dhj: '         ',
        dc: '   ',
        dj: '     '
      },
      {
        options: [
          { name: "indent_size", value: "9" },
          { name: "js", value: "{ 'indent_size': 5, 'disabled': true }" },
          { name: "css", value: "{ 'indent_size': 3 }" }
        ],
        h: '         ',
        c: '   ',
        j: '     ',
        dhc: '         ',
        dhj: '',
        dc: '   ',
        dj: ''
      },
      {
        options: [
          { name: "indent_size", value: "9" },
          { name: "js", value: "{ 'indent_size': 5 }" },
          { name: "css", value: "{ 'indent_size': 3, 'disabled': true }" }
        ],
        h: '         ',
        c: '   ',
        j: '     ',
        dhc: '',
        dhj: '         ',
        dc: '',
        dj: '     '
      },
      {
        options: [
          { name: "indent_size", value: "9" },
          { name: "html", value: "{ 'js': { 'indent_size': 3 }, 'css': { 'indent_size': 5 }, 'indent_size': 2}" },
          { name: "js", value: "{ 'indent_size': 5 }" },
          { name: "css", value: "{ 'indent_size': 3 }" }
        ],
        h: '  ',
        c: '     ',
        j: '   ',
        dhc: '  ',
        dhj: '  ',
        dc: '     ',
        dj: '   '
      },
      {
        options: [
          { name: "indent_size", value: "9" },
          { name: "html", value: "{ 'js': { 'indent_size': 3, 'disabled': true }, 'css': { 'indent_size': 5 }, 'indent_size': 2}" },
          { name: "js", value: "{ 'indent_size': 5 }" },
          { name: "css", value: "{ 'indent_size': 3 }" }
        ],
        h: '  ',
        c: '     ',
        j: '   ',
        dhc: '  ',
        dhj: '',
        dc: '     ',
        dj: ''
      }
    ],
    tests: [{
        fragment: true,
        unchanged: [
          '<head>',
          '{{h}}<script>',
          '{{h}}{{h}}if (a == b) {',
          '{{h}}{{h}}{{j}}test();',
          '{{h}}{{h}}}',
          '{{h}}</script>',
          '{{h}}<style>',
          '{{h}}{{h}}.selector {',
          '{{h}}{{h}}{{c}}font-size: 12px;',
          '{{h}}{{h}}}',
          '{{h}}</style>',
          '</head>'
        ]
      }, {
        fragment: true,
        input: [
          '<head>',
          '<script>',
          'if (a == b) {',
          'test();',
          '}',
          '</script>',
          '<style>',
          '.selector {',
          'font-size: 12px;',
          '}',
          '</style>',
          '</head>'
        ],
        output: [
          '<head>',
          '{{h}}<script>',
          '{{h}}{{h}}if (a == b) {',
          '{{dhj}}{{dhj}}{{dj}}test();',
          '{{dhj}}{{dhj}}}',
          '{{h}}</script>',
          '{{h}}<style>',
          '{{h}}{{h}}.selector {',
          '{{dhc}}{{dhc}}{{dc}}font-size: 12px;',
          '{{dhc}}{{dhc}}}',
          '{{h}}</style>',
          '</head>'
        ]
      },
      {
        fragment: true,
        unchanged: [
          '<body>',
          '{{h}}<script src="one.js"></script> <!-- one -->',
          '{{h}}<script src="two.js"></script> <!-- two-->',
          '</body>'
        ]
      }
    ]
  }, {
    name: "Tests script indent behavior",
    description: "Tests script indenting behavior",
    matrix: [{
        options: [
          { name: "indent_scripts", value: "'normal'" }
        ],
        h: '    ',
        c: '    ',
        j: '    ',
        hscript: '        '
      },
      {
        options: [
          { name: "indent_scripts", value: "'keep'" }
        ],
        h: '    ',
        c: '    ',
        j: '    ',
        hscript: '    '
      },
      {
        options: [
          { name: "indent_scripts", value: "'separate'" }
        ],
        h: '    ',
        c: '    ',
        j: '    ',
        hscript: ''
      }
    ],
    tests: [{
        fragment: true,
        input: [
          '<head>',
          '<script>',
          'if (a == b) {',
          'test();',
          '}',
          '</script>',
          '<style>',
          '.selector {',
          'font-size: 12px;',
          '}',
          '</style>',
          '</head>'
        ],
        output: [
          '<head>',
          '{{h}}<script>',
          '{{hscript}}if (a == b) {',
          '{{hscript}}{{j}}test();',
          '{{hscript}}}',
          '{{h}}</script>',
          '{{h}}<style>',
          '{{hscript}}.selector {',
          '{{hscript}}{{c}}font-size: 12px;',
          '{{hscript}}}',
          '{{h}}</style>',
          '</head>'
        ]
      },
      {
        fragment: true,
        unchanged: [
          '<body>',
          '{{h}}<script src="one.js"></script> <!-- one -->',
          '{{h}}<script src="two.js"></script> <!-- two-->',
          '</body>'
        ]
      }
    ]
  }, {
    name: "ASP(X) and JSP directives <%@ indent formatting",
    description: "",
    options: [],
    tests: [{
      unchanged: [
        '<%@Master language="C#"%>',
        '<%@Register TagPrefix="a" Namespace="a" Assembly="a"%>',
        '<%@Register TagPrefix="b" Namespace="a" Assembly="a"%>',
        '<%@Register TagPrefix="c" Namespace="a" Assembly="a"%>',
        '<!DOCTYPE html>',
        '',
        '<html>',
        '',
        '<some-content />',
        '',
        '</html>'
      ]
    }]
  }, {
    name: "Issue #1027 -- Formatting SVG files",
    description: "",
    options: [],
    tests: [{
      input: [
        '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"',
        '     viewBox="0 0 36 36" style="enable-background:new 0 0 36 36;" xml:space="preserve">',
        '                    <rect id="XMLID_20_" x="-7"',
        '                          class="st0"',
        '                          width="49" height="36"/>',
        '</svg>'
      ],
      output: [
        '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 36 36" style="enable-background:new 0 0 36 36;" xml:space="preserve">',
        '    <rect id="XMLID_20_" x="-7" class="st0" width="49" height="36" />',
        '</svg>'
      ]
    }]
  }, {
    name: "Linewrap length",
    description: "",
    options: [{ name: "wrap_line_length", value: "80" }],
    tests: [{
        comment: "This test shows how line wrapping is still not correct.",
        fragment: true,
        input: [
          '<body>',
          '    <div>',
          '        <div>',
          '            <p>Reconstruct the schematic editor the EDA system <a href="http://www.jedat.co.jp/eng/products.html"><i>AlphaSX</i></a> series</p>',
          '        </div>',
          '    </div>',
          '</body>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<body>',
          '    <div>',
          '        <div>',
          '            <p>Reconstruct the schematic editor the EDA system <a',
          '                    href="http://www.jedat.co.jp/eng/products.html"><i>AlphaSX</i></a>',
          '                series</p>',
          '        </div>',
          '    </div>',
          '</body>'
        ]
      }, {
        fragment: true,
        input: [
          '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014 0015 0016 0017 0018 0019 0020</span>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<span>0 0001 0002 0003 0004 0005 0006 0007 0008 0009 0010 0011 0012 0013 0014',
          '    0015 0016 0017 0018 0019 0020</span>'
        ]
      }, {
        fragment: true,
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        unchanged: [
          '<div>----1---------2---------3---------4---------5---------6---------7----</div>'
        ]
      }, {
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        unchanged: [
          '<span>----1---------2---------3---------4---------5---------6---------7----</span>'
        ]
      }, {
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        unchanged: [
          '<span>----1---------2---------3---------4---------5---------6---------7----<br /></span>'
        ]
      }, {
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----',
          '</div>'
        ]
      }, {
        fragment: true,
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----<br /></div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>',
          '    ----1---------2---------3---------4---------5---------6---------7-----<br />',
          '</div>'
        ]
      }, {
        fragment: true,
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----<hr /></div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----',
          '    <hr />',
          '</div>'
        ]
      }, {
        fragment: true,
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----<hr />-</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>----1---------2---------3---------4---------5---------6---------7-----',
          '    <hr />-</div>'
        ]
      }, {
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7 --------81 ----2---------3---------4---------5---------6---------7-----</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>----1---------2---------3---------4---------5---------6---------7',
          '    --------81 ----2---------3---------4---------5---------6---------7-----',
          '</div>'
        ]
      }, {
        input: [
          '<span>---1---------2---------3---------4---------5---------6---------7 --------81 ----2---------3---------4---------5---------6</span>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<span>---1---------2---------3---------4---------5---------6---------7',
          '    --------81 ----2---------3---------4---------5---------6</span>'
        ]
      }, {
        input: [
          '<p>---------1---------2---------3---------4 ---------1---------2---------3---------4</p>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          // BUGBUG Input should result in this, but doesn't
          // '<p>---------1---------2---------3---------4',
          // '    ---------1---------2---------3---------4',
          // '</p>'
          '<p>---------1---------2---------3---------4',
          '    ---------1---------2---------3---------4</p>'
        ]
      }, {
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7 --------81 ----2---------3---------4---------5---------6</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          // BUGBUG Input should result in this, but doesn't
          // '<div>----1---------2---------3---------4---------5---------6---------7',
          // '    --------81 ----2---------3---------4---------5---------6',
          // '</div>'
          '<div>----1---------2---------3---------4---------5---------6---------7',
          '    --------81 ----2---------3---------4---------5---------6</div>'
        ]
      }, {
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7 --------81 ----2---------3---------4---------5---------6<br /></div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          // BUGBUG Input should result in this, but doesn't
          // '<div>----1---------2---------3---------4---------5---------6---------7',
          // '    --------81 ----2---------3---------4---------5---------6<br />',
          // '</div>'
          '<div>----1---------2---------3---------4---------5---------6---------7',
          '    --------81 ----2---------3---------4---------5---------6<br /></div>'
        ]
      }, {
        input: [
          '<div>----1---------2---------3---------4---------5---------6---------7 --------81 ----2---------3---------4---------5---------6<hr /></div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>----1---------2---------3---------4---------5---------6---------7',
          '    --------81 ----2---------3---------4---------5---------6',
          '    <hr />',
          '</div>'
        ]
      },
      {
        comment: "#1238  Fixed",
        input: [
          '<span uib-tooltip="[[firstName]] [[lastName]]" tooltip-enable="showToolTip">',
          '   <ng-letter-avatar charCount="2" data="[[data]]"',
          '        shape="round" fontsize="[[font]]" height="[[height]]" width="[[width]]"',
          '   avatarcustombgcolor="[[bgColor]]" dynamic="true"></ng-letter-avatar>',
          '     </span>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<span uib-tooltip="[[firstName]] [[lastName]]" tooltip-enable="showToolTip">',
          '    <ng-letter-avatar charCount="2" data="[[data]]" shape="round"',
          '        fontsize="[[font]]" height="[[height]]" width="[[width]]"',
          '        avatarcustombgcolor="[[bgColor]]" dynamic="true"></ng-letter-avatar>',
          '</span>'
        ]
      }, {
        comment: "Issue #1122",
        fragment: true,
        input: [
          '<div>',
          '<div>',
          '<p>',
          '    В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов и глубина зондирования), текущие',
          '    отсчеты сохраняются в контроллере при нажатии кнопки «ПУСК». Одновременно, они распечатываются',
          '    на минипринтере. Управлять контроллером для записи данных зондирования можно при помощи <link_row to="РК.05.01.01">Радиокнопки РК-11</link_row>.',
          '</p>',
          '</div>',
          '</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>',
          '    <div>',
          '        <p>',
          '            В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов',
          '            и глубина зондирования), текущие',
          '            отсчеты сохраняются в контроллере при нажатии кнопки «ПУСК».',
          '            Одновременно, они распечатываются',
          '            на минипринтере. Управлять контроллером для записи данных',
          '            зондирования можно при помощи <link_row to="РК.05.01.01">Радиокнопки',
          '                РК-11</link_row>.',
          '        </p>',
          '    </div>',
          '</div>'
        ]
      }, {
        comment: "Issue #1122",
        fragment: true,
        input: [
          '<div>',
          '<div>',
          '<p>',
          '    В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов и глубина зондирования), текущие отсчеты сохраняются в контроллере при нажатии кнопки «ПУСК». Одновременно, они распечатываются на минипринтере. Управлять контроллером для записи данных зондирования можно при помощи <link_row to="РК.05.01.01">Радиокнопки РК-11</link_row>.',
          '</p>',
          '</div>',
          '</div>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<div>',
          '    <div>',
          '        <p>',
          '            В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов',
          '            и глубина зондирования), текущие отсчеты сохраняются в контроллере',
          '            при нажатии кнопки «ПУСК». Одновременно, они распечатываются на',
          '            минипринтере. Управлять контроллером для записи данных зондирования',
          '            можно при помощи <link_row to="РК.05.01.01">Радиокнопки РК-11',
          '            </link_row>.',
          '        </p>',
          '    </div>',
          '</div>'
        ]
      }, {
        comment: "#607 - preserve-newlines makes this look a bit odd now, but it much better",
        fragment: true,
        input: [
          '<p>В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов и глубина зондирования), текущие',
          '    отсчеты сохраняются в контроллере при нажатии кнопки «ПУСК». Одновременно, они распечатываются',
          '    на минипринтере. Управлять контроллером для записи данных зондирования можно при помощи <link_row to="РК.05.01.01">Радиокнопки РК-11</link_row>.</p>'
        ],
        //.---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        output: [
          '<p>В РАБОЧЕМ РЕЖИМЕ, после ввода параметров опыта (номер, шаг отсчетов и глубина',
          '    зондирования), текущие',
          '    отсчеты сохраняются в контроллере при нажатии кнопки «ПУСК». Одновременно,',
          '    они распечатываются',
          '    на минипринтере. Управлять контроллером для записи данных зондирования можно',
          '    при помощи <link_row to="РК.05.01.01">Радиокнопки РК-11</link_row>.</p>'
        ]
      }
    ]
  }, {
    name: "Indent with tabs",
    description: "Use one tab instead of several spaces for indentation",
    template: "^^^ $$$",
    options: [
      { name: "indent_with_tabs", value: "true" }
    ],
    tests: [{
      fragment: true,
      input_: '<div>\n' +
        '<div>\n' +
        '</div>\n' +
        '</div>',
      output: '<div>\n' +
        '\t<div>\n' +
        '\t</div>\n' +
        '</div>'
    }]
  }, {
    name: "Indent without tabs",
    description: "Use several spaces for indentation",
    template: "^^^ $$$",
    options: [
      { name: "indent_with_tabs", value: "false" }
    ],
    tests: [{
      fragment: true,
      input_: '<div>\n' + '<div>\n' + '</div>\n' + '</div>',
      output: '<div>\n' + '    <div>\n' + '    </div>\n' + '</div>'
    }]
  }, {
    name: "Do not indent html inner html by default",
    description: "",
    tests: [{
      fragment: true,
      input: '<html>\n<body>\n<div></div>\n</body>\n\n</html>',
      output: '<html>\n<body>\n    <div></div>\n</body>\n\n</html>'
    }]
  }, {
    name: "indent_inner_html set to true indents html inner html",
    description: "",
    options: [
      { name: 'indent_inner_html', value: "true" }
    ],
    tests: [{
      fragment: true,
      unchanged: '<html>\n    <body>\n        <div></div>\n    </body>\n\n</html>'
    }]
  }, {
    name: "Indent body inner html by default",
    description: "",
    tests: [{
      fragment: true,
      input: '<html>\n<body>\n<div></div>\n</body>\n\n</html>',
      output: '<html>\n<body>\n    <div></div>\n</body>\n\n</html>'
    }]
  }, {
    name: "indent_body_inner_html set to false prevents indent of body inner html",
    description: "",
    options: [
      { name: 'indent_body_inner_html', value: "false" }
    ],
    tests: [{
      fragment: true,
      unchanged: '<html>\n<body>\n<div></div>\n</body>\n\n</html>'
    }]
  }, {
    name: "Indent head inner html by default",
    description: "",
    tests: [{
      fragment: true,
      input: '<html>\n\n<head>\n<meta>\n</head>\n\n</html>',
      output: '<html>\n\n<head>\n    <meta>\n</head>\n\n</html>'
    }]
  }, {
    name: "indent_head_inner_html set to false prevents indent of head inner html",
    description: "",
    options: [
      { name: 'indent_head_inner_html', value: "false" }
    ],
    tests: [{
      fragment: true,
      unchanged: '<html>\n\n<head>\n<meta>\n</head>\n\n</html>'
    }]
  }, {
    name: "Inline tags formatting",
    description: "",
    template: "^^^ $$$",
    tests: [{
      input: '<div><span></span></div><span><div></div></span>',
      output: '<div><span></span></div><span>\n    <div></div>\n</span>'
    }, {
      input: '<div><div><span><span>Nested spans</span></span></div></div>',
      output: [
        '<div>',
        '    <div><span><span>Nested spans</span></span></div>',
        '</div>'
      ]
    }, {
      input: '<p>Should remove <span><span \n\nclass="some-class">attribute</span></span> newlines</p>',
      output: [
        '<p>Should remove <span><span class="some-class">attribute</span></span> newlines</p>'
      ]
    }, {
      unchanged: '<div><span>All</span> on <span>one</span> line</div>'
    }, {
      unchanged: '<span class="{{class_name}}">{{content}}</span>'
    }, {
      unchanged: '{{#if 1}}<span>{{content}}</span>{{/if}}'
    }]
  }, {
    name: "Preserve newlines false",
    description: "",
    options: [
      { name: 'indent_size', value: "2" },
      { name: 'preserve_newlines', value: "false" }
    ],
    tests: [{
      input: '<div>\n\tfoo\n</div>',
      output: '<div> foo </div>'
    }, {
      input_: '<div>Should not</div>\n\n\n' + '<div>preserve newlines</div>',
      output: '<div>Should not</div>\n' + '<div>preserve newlines</div>'
    }, {
      input: [
        '<header>',
        '  <h1>',
        '',
        '',
        '    <ul>',
        '',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '',
        '',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ],
      output: [
        '<header>',
        '  <h1>',
        '    <ul>',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ]
    }]
  }, {
    name: "Preserve newlines true",
    description: "",
    options: [
      { name: 'indent_size', value: "1" },
      { name: 'indent_char', value: '"\t"' },
      { name: 'preserve_newlines', value: "true" }
    ],
    tests: [{
      fragment: true,
      unchanged: '<div>\n\tfoo\n</div>'
    }]
  }, {
    name: "Preserve newlines true with zero max newline",
    description: "",
    options: [
      { name: 'preserve_newlines', value: "true" },
      { name: 'max_preserve_newlines', value: "0" },
      { name: 'indent_size', value: "2" }
    ],
    tests: [{
      input_: '<div>Should</div>\n\n\n' + '<div>preserve zero newlines</div>',
      output: '<div>Should</div>\n' + '<div>preserve zero newlines</div>'
    }, {
      input: [
        '<header>',
        '  <h1>',
        '',
        '',
        '    <ul>',
        '',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '',
        '',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ],
      output: [
        '<header>',
        '  <h1>',
        '    <ul>',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ]
    }]
  }, {
    name: "Preserve newlines true with 1 max newline",
    description: "",
    options: [
      { name: 'preserve_newlines', value: "true" },
      { name: 'indent_size', value: "2" },
      { name: 'max_preserve_newlines', value: "1" }
    ],
    tests: [{
      input_: '<div>Should</div>\n\n\n' + '<div>preserve one newline</div>',
      output: '<div>Should</div>\n\n' + '<div>preserve one newline</div>'
    }, {
      input: [
        '<header>',
        '  <h1>',
        '',
        '',
        '    <ul>',
        '',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '',
        '',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ],
      output: [
        '<header>',
        '  <h1>',
        '',
        '    <ul>',
        '',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ]
    }]
  }, {
    name: "Preserve newlines true with null max newline",
    description: "",
    options: [
      { name: 'preserve_newlines', value: "true" },
      { name: 'indent_size', value: "2" },
      { name: 'max_preserve_newlines', value: "null" }
    ],
    tests: [{
      unchanged: '<div>Should</div>\n\n\n' + '<div>preserve zero newlines</div>'
    }, {
      unchanged: [
        '<header>',
        '  <h1>',
        '',
        '',
        '    <ul>',
        '',
        '      <li class="menuactive menuparent">',
        '        <a>',
        '          <span>Anita Koppe</span>',
        '        </a>',
        '',
        '',
        '      </li>',
        '    </ul>',
        '  </h1>',
        '</header>'
      ]
    }]
  }, {
    name: "unformatted to prevent formatting changes",
    description: "",
    options: [
      { name: 'unformatted', value: "['u', 'span', 'textarea']" }
    ],
    tests: [{
      unchanged: '<u><div><div>Ignore block tags in unformatted regions</div></div></u>'
    }, {
      unchanged: '<div><u>Don\\\'t wrap unformatted regions with extra newlines</u></div>'
    }, {
      input_: '<u>  \n\n\n  Ignore extra """whitespace mostly  \n\n\n  </u>',
      output: '<u>\n\n\n  Ignore extra """whitespace mostly  \n\n\n  </u>'
    }, {
      unchanged: '<u><div \n\t\nclass=""">Ignore whitespace in attributes\t</div></u>'
    }, {
      comment: 'Regression test #1534 - interaction between unformatted, content_unformatted, and inline',
      unchanged: [
        '<div>',
        '    <textarea></textarea>',
        '    <textarea>',
        '',
        '</textarea>',
        '    <span></span>',
        '    <span>',
        '',
        '</span>',
        '</div>'
      ]
    }, {
      input_: '<u \n\n\t\t  class="">Ignore whitespace\nin\tattributes</u>',
      output: '<u\n\n\t\t  class="">Ignore whitespace\nin\tattributes</u>'
    }]
  }, {
    name: "content_unformatted to prevent formatting content",
    description: "NOTE: for this test textarea is still content_unformatted but pre is not",
    options: [

      { name: 'content_unformatted', value: "['?php', 'script', 'style', 'p', 'span', 'br', 'meta', 'textarea']" }
    ],
    tests: [{
      fragment: true,
      input: '<html><body><h1>A</h1><script>if(1){f();}</script><style>.a{display:none;}</style></body></html>',
      output: [
        '<html>',
        '<body>',
        '    <h1>A</h1>',
        '    <script>if(1){f();}</script>',
        '    <style>.a{display:none;}</style>',
        '</body>',
        '',
        '</html>'
      ]
    }, {
      input: '<div><p>Beautify me</p></div><p><div>But not me</div></p>',
      output: [
        '<div>',
        '    <p>Beautify me</p>',
        '</div>',
        '<p><div>But not me</div></p>'
      ]
    }, {
      input: '<div><p\n  class="beauty-me"\n>Beautify me</p></div><p><div\n  class="iamalreadybeauty"\n>But not me</div></p>',
      output: [
        '<div>',
        '    <p class="beauty-me">Beautify me</p>',
        '</div>',
        '<p><div',
        '  class="iamalreadybeauty"',
        '>But not me</div></p>'
      ]
    }, {
      unchanged: '<div><span>blabla<div>something here</div></span></div>'
    }, {
      unchanged: '<div><br /></div>'
    }, {
      unchanged: '<div><br></div>'
    }, {
      input: [
        '<div>',
        '<br>',
        '<br />',
        '<br></div>'
      ],
      output: [
        '<div>',
        '    <br>',
        '    <br />',
        '    <br></div>'
      ]
    }, {
      comment: 'Regression test #1534 - interaction between unformatted, content_unformatted, and inline',
      unchanged: [
        '<div>',
        '    <textarea></textarea>',
        '    <textarea>',
        '',
        '</textarea>',
        '    <span></span>',
        '    <span>',
        '',
        '</span>',
        '</div>'
      ]
    }, {
      input: [
        '<div>',
        '<meta>',
        '<meta />',
        '<meta></div>'
      ],
      output: [
        '<div>',
        '    <meta>',
        '    <meta />',
        '    <meta>',
        '</div>'
      ]
    }, {
      input: '<div><pre>var a=1;\nvar b=a;</pre></div>',
      output: [
        '<div>',
        '    <pre>var a=1;',
        '        var b=a;</pre>',
        '</div>'
      ]
    }, {
      unchanged: [
        '<?php',
        '/**',
        ' * Comment',
        ' */',
        '',
        '?>',
        '<div class="">',
        '',
        '</div>'
      ]
    }, {
      input: '<div><pre>\nvar a=1;\nvar b=a;\n</pre></div>',
      output: [
        '<div>',
        '    <pre>',
        '        var a=1;',
        '        var b=a;',
        '    </pre>',
        '</div>'
      ]
    }]
  }, {
    name: "default content_unformatted and inline element test",
    description: "",
    options: [],
    tests: [{
      fragment: true,
      input: '<html><body><h1>A</h1><script>if(1){f();}</script><style>.a{display:none;}</style></body></html>',
      output: [
        '<html>',
        '<body>',
        '    <h1>A</h1>',
        '    <script>',
        '        if (1) {',
        '            f();',
        '        }',
        '    </script>',
        '    <style>',
        '        .a {',
        '            display: none;',
        '        }',
        '    </style>',
        '</body>',
        '',
        '</html>'
      ]
    }, {
      input: '<div><p>Beautify me</p></div><p><p>But not me</p></p>',
      output: [
        '<div>',
        '    <p>Beautify me</p>',
        '</div>',
        '<p>',
        '    <p>But not me</p>',
        '</p>'
      ]
    }, {
      input: '<div><p\n  class="beauty-me"\n>Beautify me</p></div><p><p\n  class="iamalreadybeauty"\n>But not me</p></p>',
      output: [
        '<div>',
        '    <p class="beauty-me">Beautify me</p>',
        '</div>',
        '<p>',
        '    <p class="iamalreadybeauty">But not me</p>',
        '</p>'
      ]
    }, {
      unchanged: '<div><span>blabla<div>something here</div></span></div>'
    }, {
      unchanged: '<div><br /></div>'
    }, {
      comment: 'Regression test #1534 - interaction between unformatted, content_unformatted, and inline',
      unchanged: [
        '<div>',
        '    <textarea></textarea>',
        '    <textarea>',
        '',
        '</textarea>',
        '    <span></span>',
        '    <span>',
        '',
        '    </span>',
        '</div>'
      ]
    }, {
      input: '<div><pre>var a=1;\nvar b=a;</pre></div>',
      output: [
        '<div>',
        '    <pre>var a=1;',
        'var b=a;</pre>',
        '</div>'
      ]
    }, {
      input: '<div><pre>\nvar a=1;\nvar b=a;\n</pre></div>',
      output: [
        '<div>',
        '    <pre>',
        'var a=1;',
        'var b=a;',
        '</pre>',
        '</div>'
      ]
    }, {
      comment: "Test for #1041",
      input: [
        '<p><span class="foo">foo <span class="bar">bar</span></span></p>',
        '',
        '<aside><p class="foo">foo <span class="bar">bar</span></p></aside>',
        '<p class="foo"><span class="bar">bar</span></p>'
      ],
      output: [
        '<p><span class="foo">foo <span class="bar">bar</span></span></p>',
        '',
        '<aside>',
        '    <p class="foo">foo <span class="bar">bar</span></p>',
        '</aside>',
        '<p class="foo"><span class="bar">bar</span></p>'
      ]
    }, {
      comment: "Test for #869 - not exactly what the user wants but no longer horrible",
      unchanged: [
        '<div><input type="checkbox" id="j" name="j" value="foo">&nbsp;<label for="j">Foo</label></div>'
      ]
    }, {
      comment: "Test for #1167",
      unchanged: [
        '<span>',
        '    <span><img src="images/off.svg" alt=""></span>',
        '    <span><img src="images/on.svg" alt=""></span>',
        '</span>'
      ]
    }, {
      comment: "Test for #882",
      input: '<tr><th><h3>Name</h3></th><td class="full-width"></td></tr>',
      output: [
        '<tr>',
        '    <th>',
        '        <h3>Name</h3>',
        '    </th>',
        '    <td class="full-width"></td>',
        '</tr>'
      ]
    }, {
      comment: "Test for #1184",
      input: '<div><div></div>Connect</div>',
      output: [
        '<div>',
        '    <div></div>Connect',
        '</div>'
      ]
    }, {
      comment: "Test for #1383",
      input: [
        '<p class="newListItem">',
        '  <svg height="40" width="40">',
        '              <circle cx="20" cy="20" r="18" stroke="black" stroke-width="0" fill="#bddffa" />',
        '              <text x="50%" y="50%" text-anchor="middle" stroke="#1b97f3" stroke-width="2px" dy=".3em">1</text>',
        '            </svg> This is a paragraph after an SVG shape.',
        '</p>'
      ],
      output: [
        '<p class="newListItem">',
        '    <svg height="40" width="40">',
        '        <circle cx="20" cy="20" r="18" stroke="black" stroke-width="0" fill="#bddffa" />',
        '        <text x="50%" y="50%" text-anchor="middle" stroke="#1b97f3" stroke-width="2px" dy=".3em">1</text>',
        '    </svg> This is a paragraph after an SVG shape.',
        '</p>'
      ]
    }]
  }, {
    name: "indent_empty_lines true",
    description: "",
    options: [
      { name: "indent_empty_lines", value: "true" }
    ],
    tests: [{
      fragment: true,
      input: [
        '<div>',
        '',
        '    <div>',
        '',
        '    </div>',
        '',
        '</div>'
      ],
      output: [
        '<div>',
        '    ',
        '    <div>',
        '        ',
        '    </div>',
        '    ',
        '</div>'
      ]
    }]
  }, {
    name: "indent_empty_lines false",
    description: "",
    options: [
      { name: "indent_empty_lines", value: "false" }
    ],
    tests: [{
      fragment: true,
      unchanged: [
        '<div>',
        '',
        '    <div>',
        '',
        '    </div>',
        '',
        '</div>'
      ]
    }]
  }, {
    name: "New Test Suite"
  }]
};
