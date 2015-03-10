/*global js_beautify: true */

function run_html_tests(test_obj, Urlencoded, js_beautify, html_beautify, css_beautify)
{

    var opts = {
        indent_size: 4,
        indent_char: ' ',
        preserve_newlines: true,
        jslint_happy: false,
        keep_array_indentation: false,
        brace_style: 'collapse',
        space_before_conditional: true,
        break_chained_methods: false,
        selector_separator: '\n',
        end_with_newline: false
    };

    function test_html_beautifier(input)
    {
        return html_beautify(input, opts);
    }

    var sanitytest;

    // test the input on beautifier with the current flag settings
    // does not check the indentation / surroundings as bt() does
    function test_fragment(input, expected)
    {
        expected = expected || expected === '' ? expected : input;
        sanitytest.expect(input, expected);
        // if the expected is different from input, run it again
        // expected output should be unchanged when run twice.
        if (expected !== input) {
            sanitytest.expect(expected, expected);
        }
    }

    // test html
    function bth(input, expectation)
    {
        var wrapped_input, wrapped_expectation, field_input, field_expectation;

        expectation = expectation || expectation === '' ? expectation : input;
        sanitytest.test_function(test_html_beautifier, 'html_beautify');
        test_fragment(input, expectation);

        if (opts.indent_size === 4 && input) {
            wrapped_input = '<div>\n' + input.replace(/^(.+)$/mg, '    $1') + '\n    <span>inline</span>\n</div>';
            wrapped_expectation = '<div>\n' + expectation.replace(/^(.+)$/mg, '    $1') + '\n    <span>inline</span>\n</div>';
            if (opts.end_with_newline) {
                wrapped_expectation += '\n';
            }
            test_fragment(wrapped_input, wrapped_expectation);
        }

        // Test that handlebars non-block {{}} tags act as content and do not
        // get any spacing or line breaks.
        if (input.indexOf('content') != -1) {
            // Just {{field}}
            field_input = input.replace(/content/g, '{{field}}');
            field_expectation = expectation.replace(/content/g, '{{field}}');
            test_fragment(field_input, field_expectation);

            // handlebars comment
            field_input = input.replace(/content/g, '{{! comment}}');
            field_expectation = expectation.replace(/content/g, '{{! comment}}');
            test_fragment(field_input, field_expectation);

            // issue 635 test that handlebars comments including multi-line remain unformatted
            if (opts.indent_handlebars) {
                field_input = input.replace(/content/g, '{{! \n mult-line\ncomment \n}}');
                field_expectation = expectation.replace(/content/g, '{{! \n mult-line\ncomment \n}}');
                test_fragment(field_input, field_expectation);
            }

            // mixed {{field}} and content
            field_input = input.replace(/content/g, 'pre{{field1}} {{field2}} {{field3}}post');
            field_expectation = expectation.replace(/content/g, 'pre{{field1}} {{field2}} {{field3}}post');
            test_fragment(field_input, field_expectation);
        }
    }

    function unicode_char(value) {
        return String.fromCharCode(value)
    }

    function beautifier_tests()
    {
        sanitytest = test_obj;

        bth('');

        opts.indent_size = 4;
        opts.indent_char = ' ';
        opts.preserve_newlines = true;
        opts.jslint_happy = false;
        opts.keep_array_indentation = false;
        opts.brace_style = 'collapse';

        // End With Newline - (eof = "\n")
        opts.end_with_newline = true;
        test_fragment('', '\n');
        test_fragment('<div></div>', '<div></div>\n');
        test_fragment('\n');

        // End With Newline - (eof = "")
        opts.end_with_newline = false;
        test_fragment('');
        test_fragment('<div></div>');
        test_fragment('\n', '');

        // Attribute Wrap - (eof = "\n", indent_attr = "    ", over80 = "\n")
        opts.wrap_attributes = 'force';
        test_fragment('<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>', '<div attr0\n    attr1="123"\n    data-attr2="hello    t here">This is some text</div>');
        test_fragment('<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>', '<div lookatthissuperduperlongattributenamewhoahcrazy0="true"\n    attr0\n    attr1="123"\n    data-attr2="hello    t here"\n    heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>');
        test_fragment('<img attr0 attr1="123" data-attr2="hello    t here"/>', '<img attr0\n    attr1="123"\n    data-attr2="hello    t here" />');

        // Attribute Wrap - (eof = "\n", indent_attr = "    ", over80 = "\n")
        opts.wrap_attributes = 'force';
        opts.wrap_line_length = 80;
        test_fragment('<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>', '<div attr0\n    attr1="123"\n    data-attr2="hello    t here">This is some text</div>');
        test_fragment('<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>', '<div lookatthissuperduperlongattributenamewhoahcrazy0="true"\n    attr0\n    attr1="123"\n    data-attr2="hello    t here"\n    heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>');
        test_fragment('<img attr0 attr1="123" data-attr2="hello    t here"/>', '<img attr0\n    attr1="123"\n    data-attr2="hello    t here" />');

        // Attribute Wrap - (eof = "\n", indent_attr = "        ", over80 = "\n")
        opts.wrap_attributes = 'force';
        opts.wrap_attributes_indent_size = 8;
        test_fragment('<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>', '<div attr0\n        attr1="123"\n        data-attr2="hello    t here">This is some text</div>');
        test_fragment('<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>', '<div lookatthissuperduperlongattributenamewhoahcrazy0="true"\n        attr0\n        attr1="123"\n        data-attr2="hello    t here"\n        heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>');
        test_fragment('<img attr0 attr1="123" data-attr2="hello    t here"/>', '<img attr0\n        attr1="123"\n        data-attr2="hello    t here" />');

        // Attribute Wrap - (eof = " ", indent_attr = "", over80 = "\n")
        opts.wrap_attributes = 'auto';
        opts.wrap_line_length = 80;
        test_fragment('<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>');
        test_fragment('<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>', '<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here"\nheymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>');
        test_fragment('<img attr0 attr1="123" data-attr2="hello    t here"/>', '<img attr0 attr1="123" data-attr2="hello    t here" />');

        // Attribute Wrap - (eof = " ", indent_attr = "", over80 = " ")
        opts.wrap_attributes = 'auto';
        opts.wrap_line_length = 0;
        test_fragment('<div attr0 attr1="123" data-attr2="hello    t here">This is some text</div>');
        test_fragment('<div lookatthissuperduperlongattributenamewhoahcrazy0="true" attr0 attr1="123" data-attr2="hello    t here" heymanimreallylongtoowhocomesupwiththesenames="false">This is some text</div>');
        test_fragment('<img attr0 attr1="123" data-attr2="hello    t here"/>', '<img attr0 attr1="123" data-attr2="hello    t here" />');

        // New Test Suite

        opts.end_with_newline = true;
        test_fragment('', '\n');
        test_fragment('<div></div>\n');
        test_fragment('<div></div>\n\n\n', '<div></div>\n');
        test_fragment('<head>\n' +
            '    <script>\n' +
            '        mocha.setup("bdd");\n' +
            '\n' +
            '    </script>\n' +
            '</head>\n');


        opts.end_with_newline = false;
        // error cases need love too
        bth('<img title="Bad food!" src="foo.jpg" alt="Evil" ">');
        bth("<!-- don't blow up if a comment is not complete"); // -->

        test_fragment(
            '<head>\n' +
            '    <script>\n' +
            '        mocha.setup("bdd");\n' +
            '    </script>\n' +
            '</head>');

        test_fragment('<div></div>\n', '<div></div>');
        bth('<div></div>');
        bth('<div>content</div>');
        bth('<div><div></div></div>',
            '<div>\n' +
            '    <div></div>\n' +
            '</div>');
        bth('<div><div>content</div></div>',
            '<div>\n' +
            '    <div>content</div>\n' +
            '</div>');
        bth('<div>\n' +
            '    <span>content</span>\n' +
            '</div>');
        bth('<div>\n' +
            '</div>');
        bth('<div>\n' +
            '    content\n' +
            '</div>');
        bth('<div>\n' +
            '    </div>',
            '<div>\n' +
            '</div>');
        bth('    <div>\n' +
            '    </div>',
            '<div>\n' +
            '</div>');
        bth('<div>\n' +
            '</div>\n' +
            '    <div>\n' +
            '    </div>',
            '<div>\n' +
            '</div>\n' +
            '<div>\n' +
            '</div>');
        bth('    <div>\n' +
            '</div>',
            '<div>\n' +
            '</div>');
        bth('<div        >content</div>',
            '<div>content</div>');
        bth('<div     thinger="preserve  space  here"   ></div  >',
            '<div thinger="preserve  space  here"></div>');
        bth('content\n' +
            '    <div>\n' +
            '    </div>\n' +
            'content',
            'content\n' +
            '<div>\n' +
            '</div>\n' +
            'content');
        bth('<li>\n' +
            '    <div>\n' +
            '    </div>\n' +
            '</li>');
        bth('<li>\n' +
            '<div>\n' +
            '</div>\n' +
            '</li>',
            '<li>\n' +
            '    <div>\n' +
            '    </div>\n' +
            '</li>');
        bth('<li>\n' +
            '    content\n' +
            '</li>\n' +
            '<li>\n' +
            '    content\n' +
            '</li>');

        bth('<img>content');
        bth('<img> content');
        bth('<img>   content', '<img> content');

        bth('<img><img>content');
        bth('<img> <img>content');
        bth('<img>   <img>content', '<img> <img>content');

        bth('<img><b>content</b>');
        bth('<img> <b>content</b>');
        bth('<img>   <b>content</b>', '<img> <b>content</b>');

        bth('<div>content<img>content</div>');
        bth('<div> content <img> content</div>');
        bth('<div>    content <img>    content </div>',
            '<div> content <img> content </div>');
        bth('Text <a href="#">Link</a> Text');


        // START tests for issue 453
        bth('<script type="text/unknown"><div></div></script>',
            '<script type="text/unknown">\n' +
            '    <div></div>\n' +
            '</script>');
        bth('<script type="text/javascript"><div></div></script>',
            '<script type="text/javascript">\n' +
            '    < div > < /div>\n' +
            '</script>');
        bth('<script><div></div></script>',
            '<script>\n' +
            '    < div > < /div>\n' +
            '</script>');
        bth('<script type="text/javascript">var foo = "bar";</script>',
            '<script type="text/javascript">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script type="application/javascript">var foo = "bar";</script>',
            '<script type="application/javascript">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script type="application/javascript;version=1.8">var foo = "bar";</script>',
            '<script type="application/javascript;version=1.8">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script type="application/x-javascript">var foo = "bar";</script>',
            '<script type="application/x-javascript">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script type="application/ecmascript">var foo = "bar";</script>',
            '<script type="application/ecmascript">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script type="text/javascript1.5">var foo = "bar";</script>',
            '<script type="text/javascript1.5">\n' +
            '    var foo = "bar";\n' +
            '</script>');
        bth('<script>var foo = "bar";</script>',
            '<script>\n' +
            '    var foo = "bar";\n' +
            '</script>');

        bth('<style type="text/unknown"><tag></tag></style>',
            '<style type="text/unknown">\n' +
            '    <tag></tag>\n' +
            '</style>');
        bth('<style type="text/css"><tag></tag></style>',
            '<style type="text/css">\n' +
            '    <tag></tag>\n' +
            '</style>');
        bth('<style><tag></tag></style>',
            '<style>\n' +
            '    <tag></tag>\n' +
            '</style>');
        bth('<style type="text/css">.selector {font-size:12px;}</style>',
            '<style type="text/css">\n' +
            '    .selector {\n' +
            '        font-size: 12px;\n' +
            '    }\n'+
            '</style>');
        bth('<style>.selector {font-size:12px;}</style>',
            '<style>\n' +
            '    .selector {\n' +
            '        font-size: 12px;\n' +
            '    }\n'+
            '</style>');
        // END tests for issue 453

        var unformatted = opts.unformatted;
        opts.unformatted = ['script', 'style'];
        bth('<script id="javascriptTemplate" type="text/x-kendo-template">\n' +
            '  <ul>\n' +
            '  # for (var i = 0; i < data.length; i++) { #\n' +
            '    <li>#= data[i] #</li>\n' +
            '  # } #\n' +
            '  </ul>\n' +
            '</script>');
        bth('<style>\n' +
            '  body {background-color:lightgrey}\n' +
            '  h1   {color:blue}\n' +
            '</style>');
        opts.unformatted = unformatted;

        unformatted = opts.unformatted;
        opts.unformatted = ['custom-element'];
        test_fragment('<div>should <custom-element>not</custom-element>' +
                      ' insert newlines</div>',
                      '<div>should <custom-element>not</custom-element>' +
                      ' insert newlines</div>');
        opts.unformatted = unformatted;

        // Tests that don't pass, but probably should.
        // bth('<div><span>content</span></div>');

        // Handlebars tests
        // Without the indent option on, handlebars are treated as content.
        opts.indent_handlebars = false;
        bth('{{#if 0}}\n' +
            '    <div>\n' +
            '    </div>\n' +
            '{{/if}}',
            '{{#if 0}}\n' +
            '<div>\n' +
            '</div>\n' +
            '{{/if}}');
        bth('<div>\n' +
            '{{#each thing}}\n' +
            '    {{name}}\n' +
            '{{/each}}\n' +
            '</div>',
            '<div>\n' +
            '    {{#each thing}} {{name}} {{/each}}\n' +
            '</div>');

        opts.indent_handlebars = true;
        bth('{{#if 0}}{{/if}}');
        bth('{{#if 0}}content{{/if}}');
        bth('{{#if 0}}\n' +
            '{{/if}}');
        bth('{{#if     words}}{{/if}}',
            '{{#if words}}{{/if}}');
        bth('{{#if     words}}content{{/if}}',
            '{{#if words}}content{{/if}}');
        bth('{{#if     words}}content{{/if}}',
            '{{#if words}}content{{/if}}');
        bth('{{#if 1}}\n' +
            '    <div>\n' +
            '    </div>\n' +
            '{{/if}}');
        bth('{{#if 1}}\n' +
            '<div>\n' +
            '</div>\n' +
            '{{/if}}',
            '{{#if 1}}\n' +
            '    <div>\n' +
            '    </div>\n' +
            '{{/if}}');
        bth('<div>\n' +
            '    {{#if 1}}\n' +
            '    {{/if}}\n' +
            '</div>');
        bth('<div>\n' +
            '{{#if 1}}\n' +
            '{{/if}}\n' +
            '</div>',
            '<div>\n' +
            '    {{#if 1}}\n' +
            '    {{/if}}\n' +
            '</div>');
        bth('{{#if}}\n' +
            '{{#each}}\n' +
            '{{#if}}\n' +
            'content\n' +
            '{{/if}}\n' +
            '{{#if}}\n' +
            'content\n' +
            '{{/if}}\n' +
            '{{/each}}\n' +
            '{{/if}}',
            '{{#if}}\n' +
            '    {{#each}}\n' +
            '        {{#if}}\n' +
            '            content\n' +
            '        {{/if}}\n' +
            '        {{#if}}\n' +
            '            content\n' +
            '        {{/if}}\n' +
            '    {{/each}}\n' +
            '{{/if}}');
        bth('{{#if 1}}\n' +
            '    <div>\n' +
            '    </div>\n' +
            '{{/if}}');

        // Test {{else}} aligned with {{#if}} and {{/if}}
        bth('{{#if 1}}\n' +
            '    content\n' +
            '    {{else}}\n' +
            '    content\n' +
            '{{/if}}',
            '{{#if 1}}\n' +
            '    content\n' +
            '{{else}}\n' +
            '    content\n' +
            '{{/if}}');
        bth('{{#if 1}}\n' +
            '    {{else}}\n' +
            '    {{/if}}',
            '{{#if 1}}\n' +
            '{{else}}\n' +
            '{{/if}}');
        bth('{{#if thing}}\n' +
            '{{#if otherthing}}\n' +
            '    content\n' +
            '    {{else}}\n' +
            'content\n' +
            '    {{/if}}\n' +
            '       {{else}}\n'+
            'content\n' +
            '{{/if}}',
            '{{#if thing}}\n' +
            '    {{#if otherthing}}\n' +
            '        content\n' +
            '    {{else}}\n' +
            '        content\n' +
            '    {{/if}}\n' +
            '{{else}}\n'+
            '    content\n' +
            '{{/if}}');

        // Test {{}} inside of <> tags, which should be separated by spaces
        // for readability, unless they are inside a string.
        bth('<div{{somestyle}}></div>',
            '<div {{somestyle}}></div>');
        bth('<div{{#if test}}class="foo"{{/if}}>content</div>',
            '<div {{#if test}} class="foo" {{/if}}>content</div>');
        bth('<div{{#if thing}}{{somestyle}}class="{{class}}"{{else}}class="{{class2}}"{{/if}}>content</div>',
            '<div {{#if thing}} {{somestyle}} class="{{class}}" {{else}} class="{{class2}}" {{/if}}>content</div>');
        bth('<span{{#if condition}}class="foo"{{/if}}>content</span>',
            '<span {{#if condition}} class="foo" {{/if}}>content</span>');
        bth('<div unformatted="{{#if}}content{{/if}}">content</div>');
        bth('<div unformatted="{{#if  }}    content{{/if}}">content</div>');

        // Quotes found inside of Handlebars expressions inside of quoted
        // strings themselves should not be considered string delimiters.
        bth('<div class="{{#if thingIs "value"}}content{{/if}}"></div>');
        bth('<div class="{{#if thingIs \'value\'}}content{{/if}}"></div>');
        bth('<div class=\'{{#if thingIs "value"}}content{{/if}}\'></div>');
        bth('<div class=\'{{#if thingIs \'value\'}}content{{/if}}\'></div>');

        opts.wrap_line_length = 0;
        //...---------1---------2---------3---------4---------5---------6---------7
        //...1234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some text that should not wrap at all.</div>',
            /* expected */
            '<div>Some text that should not wrap at all.</div>');

        // A value of 0 means no max line length, and should not wrap.
        //...---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        //...12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all.</div>',
            /* expected */
            '<div>Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all.</div>');

        opts.wrap_line_length = "0";
        //...---------1---------2---------3---------4---------5---------6---------7
        //...1234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some text that should not wrap at all.</div>',
            /* expected */
            '<div>Some text that should not wrap at all.</div>');

        // A value of "0" means no max line length, and should not wrap
        //...---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12--------13--------14--------15--------16--------17--------18--------19--------20--------21--------22--------23--------24--------25--------26--------27--------28--------29
        //...12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all.</div>',
            /* expected */
            '<div>Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all. Some text that should not wrap at all.</div>');

        //BUGBUG: This should wrap before 40 not after.
        opts.wrap_line_length = 40;
        //...---------1---------2---------3---------4---------5---------6---------7
        //...1234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some test text that should wrap_inside_this section here.</div>',
            /* expected */
            '<div>Some test text that should wrap_inside_this\n' +
            '    section here.</div>');

        opts.wrap_line_length = "40";
        //...---------1---------2---------3---------4---------5---------6---------7
        //...1234567890123456789012345678901234567890123456789012345678901234567890
        bth('<div>Some test text that should wrap_inside_this section here.</div>',
            /* expected */
            '<div>Some test text that should wrap_inside_this\n' +
            '    section here.</div>');

        opts.indent_size = 1;
        opts.indent_char = '\t';
        opts.preserve_newlines = false;
        bth('<div>\n\tfoo\n</div>', '<div> foo </div>');

        opts.preserve_newlines = true;
        bth('<div>\n\tfoo\n</div>');



        // test preserve_newlines and max_preserve_newlines
        opts.preserve_newlines = false;
        bth('<div>Should not</div>\n\n\n' +
            '<div>preserve newlines</div>',
            '<div>Should not</div>\n' +
            '<div>preserve newlines</div>');

        opts.preserve_newlines = true;
        opts.max_preserve_newlines  = 0;
        bth('<div>Should</div>\n\n\n' +
            '<div>preserve zero newlines</div>',
            '<div>Should</div>\n' +
            '<div>preserve zero newlines</div>');

        opts.max_preserve_newlines  = 1;
        bth('<div>Should</div>\n\n\n' +
            '<div>preserve one newline</div>',
            '<div>Should</div>\n\n' +
            '<div>preserve one newline</div>');

        opts.max_preserve_newlines  = null;
        bth('<div>Should</div>\n\n\n' +
            '<div>preserve one newline</div>',
            '<div>Should</div>\n\n\n' +
            '<div>preserve one newline</div>');
    }

    beautifier_tests();
}

if (typeof exports !== "undefined") {
    exports.run_html_tests = run_html_tests;
}
