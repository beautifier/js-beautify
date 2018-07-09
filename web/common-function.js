var the = {
  use_codemirror: !window.location.href.match(/without-codemirror/),
  beautifier_file: window.location.href.match(/debug/) ? 'beautifier' : './beautifier.min',
  beautifier: null,
  beautify_in_progress: false,
  editor: null // codemirror editor
};

requirejs.config({
  //By default load any module IDs from js/lib
  baseUrl: 'js/lib',
  paths: {
    'beautifier': the.beautifier_file,
  }
});

requirejs(['beautifier'],
  function(beautifier) {
    the.beautifier = beautifier;
  });

function any(a, b) {
  return a || b;
}

function run_tests() {
  $.when($.getScript("js/test/sanitytest.js"),
      $.getScript("js/test/generated/beautify-javascript-tests.js"),
      $.getScript("js/test/generated/beautify-css-tests.js"),
      $.getScript("js/test/generated/beautify-html-tests.js"))
    .done(function() {
      var st = new SanityTest();
      run_javascript_tests(st, Urlencoded, the.beautifier.js, the.beautifier.html, the.beautifier.css);
      run_css_tests(st, Urlencoded, the.beautifier.js, the.beautifier.html, the.beautifier.css);
      run_html_tests(st, Urlencoded, the.beautifier.js, the.beautifier.html, the.beautifier.css);
      JavascriptObfuscator.run_tests(st);
      P_A_C_K_E_R.run_tests(st);
      Urlencoded.run_tests(st);
      MyObfuscate.run_tests(st);
      var results = st.results_raw()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/ /g, '&nbsp;')
        .replace(/\r/g, '·')
        .replace(/\n/g, '<br>');
      $('#testresults').html(results).show();
    });
}

function read_settings_from_cookie() {
  $('#tabsize').val(any(Cookies.get('tabsize'), '4'));
  $('#brace-style').val(any(Cookies.get('brace-style'), 'collapse'));
  $('#detect-packers').prop('checked', Cookies.get('detect-packers') !== 'off');
  $('#max-preserve-newlines').val(any(Cookies.get('max-preserve-newlines'), '5'));
  $('#keep-array-indentation').prop('checked', Cookies.get('keep-array-indentation') === 'on');
  $('#break-chained-methods').prop('checked', Cookies.get('break-chained-methods') === 'on');
  $('#indent-scripts').val(any(Cookies.get('indent-scripts'), 'normal'));
  $('#additional-options').val(any(Cookies.get('additional-options'), '{}'));
  $('#space-before-conditional').prop('checked', Cookies.get('space-before-conditional') !== 'off');
  $('#wrap-line-length').val(any(Cookies.get('wrap-line-length'), '0'));
  $('#unescape-strings').prop('checked', Cookies.get('unescape-strings') === 'on');
  $('#jslint-happy').prop('checked', Cookies.get('jslint-happy') === 'on');
  $('#end-with-newline').prop('checked', Cookies.get('end-with-newline') === 'on');
  $('#indent-inner-html').prop('checked', Cookies.get('indent-inner-html') === 'on');
  $('#comma-first').prop('checked', Cookies.get('comma-first') === 'on');
  $('#e4x').prop('checked', Cookies.get('e4x') === 'on');
  $('#language').val(any(Cookies.get('language'), 'auto'));
}

function store_settings_to_cookie() {
  var opts = {
    expires: 360
  };
  Cookies.set('tabsize', $('#tabsize').val(), opts);
  Cookies.set('brace-style', $('#brace-style').val(), opts);
  Cookies.set('detect-packers', $('#detect-packers').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('max-preserve-newlines', $('#max-preserve-newlines').val(), opts);
  Cookies.set('keep-array-indentation', $('#keep-array-indentation').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('break-chained-methods', $('#break-chained-methods').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('space-before-conditional', $('#space-before-conditional').prop('checked') ? 'on' : 'off',
    opts);
  Cookies.set('unescape-strings', $('#unescape-strings').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('jslint-happy', $('#jslint-happy').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('end-with-newline', $('#end-with-newline').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('wrap-line-length', $('#wrap-line-length').val(), opts);
  Cookies.set('indent-scripts', $('#indent-scripts').val(), opts);
  Cookies.set('additional-options', $('#additional-options').val(), opts);
  Cookies.set('indent-inner-html', $('#indent-inner-html').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('comma-first', $('#comma-first').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('e4x', $('#e4x').prop('checked') ? 'on' : 'off', opts);
  Cookies.set('language', $('#language').val(), opts);

}

function unpacker_filter(source) {
  var trailing_comments = '',
    comment = '',
    unpacked = '',
    found = false;

  // cut trailing comments
  do {
    found = false;
    if (/^\s*\/\*/.test(source)) {
      found = true;
      comment = source.substr(0, source.indexOf('*/') + 2);
      source = source.substr(comment.length).replace(/^\s+/, '');
      trailing_comments += comment + "\n";
    } else if (/^\s*\/\//.test(source)) {
      found = true;
      comment = source.match(/^\s*\/\/.*/)[0];
      source = source.substr(comment.length).replace(/^\s+/, '');
      trailing_comments += comment + "\n";
    }
  } while (found);

  var unpackers = [P_A_C_K_E_R, Urlencoded, JavascriptObfuscator /*, MyObfuscate*/ ];
  for (var i = 0; i < unpackers.length; i++) {
    if (unpackers[i].detect(source)) {
      unpacked = unpackers[i].unpack(source);
      if (unpacked != source) {
        source = unpacker_filter(unpacked);
      }
    }
  }

  return trailing_comments + source;
}


function beautify() {
  if (the.beautify_in_progress) return;

  store_settings_to_cookie();

  the.beautify_in_progress = true;

  var source = the.editor ? the.editor.getValue() : $('#source').val(),
    output,
    opts = {};
  the.lastInput = source;

  var additional_options = $('#additional-options').val();

  var language = $('#language').val();
  the.language = $('#language option:selected').text();

  opts.indent_size = $('#tabsize').val();
  opts.indent_char = opts.indent_size == 1 ? '\t' : ' ';
  opts.max_preserve_newlines = $('#max-preserve-newlines').val();
  opts.preserve_newlines = opts.max_preserve_newlines !== "-1";
  opts.keep_array_indentation = $('#keep-array-indentation').prop('checked');
  opts.break_chained_methods = $('#break-chained-methods').prop('checked');
  opts.indent_scripts = $('#indent-scripts').val();
  opts.brace_style = $('#brace-style').val() + ($('#brace-preserve-inline').prop('checked') ? ",preserve-inline" : "");
  opts.space_before_conditional = $('#space-before-conditional').prop('checked');
  opts.unescape_strings = $('#unescape-strings').prop('checked');
  opts.jslint_happy = $('#jslint-happy').prop('checked');
  opts.end_with_newline = $('#end-with-newline').prop('checked');
  opts.wrap_line_length = $('#wrap-line-length').val();
  opts.indent_inner_html = $('#indent-inner-html').prop('checked');
  opts.comma_first = $('#comma-first').prop('checked');
  opts.e4x = $('#e4x').prop('checked');

  $('#additional-options-error').hide();
  $('#open-issue').hide();

  if (additional_options && additional_options !== '{}') {
    try {
      additional_options = JSON.parse(additional_options);
      opts = mergeObjects(opts, additional_options);
    } catch (e) {
      $('#additional-options-error').show();
    }
  }

  var selectedOptions = JSON.stringify(opts, null, 2);
  $('#options-selected').val(selectedOptions);

  if (language === 'html' || (language === 'auto' && looks_like_html(source))) {
    output = the.beautifier.html(source, opts);
  } else if (language === 'css') {
    output = the.beautifier.css(source, opts);
  } else {
    if ($('#detect-packers').prop('checked')) {
      source = unpacker_filter(source);
    }
    output = the.beautifier.js(source, opts);
  }

  if (the.editor) {
    the.editor.setValue(output);
  } else {
    $('#source').val(output);
  }

  $('#open-issue').show();

  the.lastOutput = output;
  the.lastOpts = selectedOptions;

  the.beautify_in_progress = false;
}

function looks_like_html(source) {
  // <foo> - looks like html
  var trimmed = source.replace(/^[ \t\n\r]+/, '');
  return trimmed && (trimmed.substring(0, 1) === '<');
}

function mergeObjects(allOptions, additionalOptions) {
  var finalOpts = {};
  var name;

  for (name in allOptions) {
    finalOpts[name] = allOptions[name];
  }
  for (name in additionalOptions) {
    finalOpts[name] = additionalOptions[name];
  }
  return finalOpts;
}

function submitIssue() {
  var url = 'https://github.com/beautify-web/js-beautify/issues/new?';
  var submit_body = [
    '# Description',
    '> NOTE:',
    '> * Check the list of open issues before filing a new issue.',
    '> * Please update the expect output section to match how you would prefer the code to look.',
    '',
    '# Input',
    'The code looked like this before beautification:',
    '```',
    the.lastInput,
    '```',
    '',
    '# Current Output',
    'The  code actually looked like this after beautification:',
    '```',
    the.lastOutput,
    '```',
    '',
    '# Expected Output',
    'The code should have looked like this after beautification:',
    '```',
    '/*Adjust the code to look how you prefer the output to be.*/',
    the.lastInput,
    '```',
    '',
    '## Environment',
    'Browser User Agent:',
    navigator.userAgent,
    '',
    'Language Selected:',
    the.language,
    '',
    '## Settings',
    'Example:',
    '```json',
    the.lastOpts,
    '```',
    ''];

  var encoded = encodeURIComponent(submit_body.join('\n'));
  url += 'body=' + encoded;

  console.log(url);
  window.open(url, '_blank').focus();
}