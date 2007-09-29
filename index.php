<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!--

  (c) 2006: Einars "elfz" Lielmanis, 
            elfz@laacz.lv
            http://elfz.laacz.lv/

-->
<?
function get_raw($name) {
    return trim((!empty($_GET[$name]) ? $_GET[$name] : ( !empty($_POST[$name]) ? $_POST[$name] : '' )));
}

require('beautify.php');

remove_magic_quotes();

function remove_magic_quotes() {
    if( get_magic_quotes_gpc() ) {
        if (is_array($_GET)) {
            while( list($k, $v) = each($_GET) ) {
                if( is_array($_GET[$k]) ) {
                    while( list($k2, $v2) = each($_GET[$k]) ) {
                        $_GET[$k][$k2] = stripslashes($v2);
                    }
                    reset($_GET[$k]);
                } else
                    $_GET[$k] = stripslashes($v);
            }
            reset($_GET);
        }

        if( is_array($_POST) ) {
            while( list($k, $v) = each($_POST) ) {
                if( is_array($_POST[$k]) ) {
                    while( list($k2, $v2) = each($_POST[$k]) )
                        $_POST[$k][$k2] = stripslashes($v2);
                    reset($_POST[$k]);
                } else
                    $_POST[$k] = stripslashes($v);
            }
            reset($_POST);
        }

        if( is_array($_COOKIE) ) {
            while( list($k, $v) = each($_COOKIE) ) {
                if( is_array($_COOKIE[$k]) ) {
                    while( list($k2, $v2) = each($_COOKIE[$k]) )
                        $_COOKIE[$k][$k2] = stripslashes($v2);
                    reset($_COOKIE[$k]);
                } else
                    $_COOKIE[$k] = stripslashes($v);
            }
            reset($_COOKIE);
        }
    }
}

?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>Online beautifier for JavaScript | js beautify, pretty-print</title>
<script type="text/javascript">
window.onload = function() {
    var c = document.forms[0].content;
    c && c.setSelectionRange && c.setSelectionRange(0, 0);
    c && c.focus && c.focus();
}
</script>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
form {
    margin: 0 10px 0 10px;
}
textarea {
    width: 100%;
    height: 320px;
    border: 1px solid #ccc;
    padding: 3px;
    font-family: consolas, courier new, courier, monospace;
    font-size: 12px;
}
h1 {
    color: #666;
}
button { width: 100%;}
code, .code {
    font-family: consolas, lucida console, courier new, courier, monospace;
    font-size: 12px;
}
</style>
</head>
<body>
  <h1>My Great Online Beautifier for JavaScript</h1>
  <form method="post" action="?">
      <textarea rows="30" cols="30" name="content"><?php 

$c = get_raw('content');
echo $c ? 
     htmlspecialchars(js_beautify($c)) : 
     preg_replace("/\n([^ ])/u", "\$1",
"/*   paste in your own code and press Beautify button   */
var nosemicolon=2 var test={regexp=/^[a-z\/]+%/;/^test$/.match(test);
d:function(x){return x}}
var latest_changes=new Object(
{'2007-09-28':
'Better handling of switch cases and lines not ending with semicolon; 
                   UTF supported in strings and comments (мелочь, но приятно).',
'2007-05-26':
'Fixed regular expression detection at the start of line',
'2007-05-18':
'Uninitialized string offset at the end of script bug fixed',
'2007-03-13':
'Gave the code away',
'2007-02-08':
'Initial release'});");

?></textarea><br />
      <button type="submit">Beautify</button>
      <p>Completely reformat the javascript source code to my liking so that it becomes a little bit readable.<br />
      It can be useful to explore the scripts compacted in one line (<a href="http://createwebapp.com/">(now-ex) CAPXOUS</a> comes to my mind as <a href="http://createwebapp.com/javascripts/autocomplete.js">an example</a>).<br />
      At least that's what I wrote it for&mdash;all the other beautifiers sucked and seemed to be written by guys who haven't seen any javascript lately.</p>
      <p>PHP source for the curious can be <a href="beautify.phps">downloaded here</a>. It's messy&mdash;you've been warned.</p>
      <p>In case of strange glitches you may wish to tell me about them&mdash;<code>elfz<span style="color:#999">[at]</span>laacz<span style="color:#999">[dot]</span>lv</code></p>
  </form>
<?php 
    printf('<img src="http://edev.uk.to/tmp/track?beautify&amp;ref=%s" style="display:none" alt="my tracker" />', isset($_SERVER['HTTP_REFERER']) ? urlencode($_SERVER['HTTP_REFERER']) : '');
?>
</body>
</html>
