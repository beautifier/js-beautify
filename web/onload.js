/*jshint node:false, jquery:true, strict:false */
$(function() {

  read_settings_from_cookie();
  $.getJSON("./package.json", function(data) {
    $('#version-number').text('(v' + data.version + ')');
  });

  var default_text =
    "// This is just a sample script. Paste your real code (javascript or HTML) here.\n\nif ('this_is'==/an_example/){of_beautifier();}else{var a=b?(c%d):e[f];}";
  var textArea = $('#source')[0];
  $('#source').val(default_text);

  if (the.use_codemirror && typeof CodeMirror !== 'undefined') {

    the.editor = CodeMirror.fromTextArea(textArea, {
      lineNumbers: true
    });

    set_editor_mode();
    the.editor.focus();

    $('.CodeMirror').click(function() {
      if (the.editor.getValue() === default_text) {
        the.editor.setValue('');
      }
    });
  } else {
    $('#source').bind('click focus', function() {
      if ($(this).val() === default_text) {
        $(this).val('');
      }
    }).bind('blur', function() {
      if (!$(this).val()) {
        $(this).val(default_text);
      }
    });
  }

  setPreferredColorScheme();

  $(window).bind('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.keyCode === 13) {
      beautify();
    }
  });

  if (typeof window.navigator !== "undefined" && typeof window.navigator.platform === "string" && window.navigator.platform.includes("Mac")) {
    $(".submit em").text("(cmd-enter)");
  }

  $('.submit').click(beautify);
  $('select').change(beautify);
  $(':checkbox').change(beautify);
  $('#additional-options').change(beautify);


});
