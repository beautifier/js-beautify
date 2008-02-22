<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!--

  (c) 2006-2007: Einars "elfz" Lielmanis, 
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

$tab_size = (int)get_raw('tabsize');
$tab_char = ' ';
if ($tab_size <= 0) $tab_size = 4;
if ($tab_size == 1) $tab_char = "\t";

?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Online beautifier for javascript (js beautify, pretty-print)</title>
<script type="text/javascript">
window.onload = function() {
    var c = document.forms[0].content;
    c && c.setSelectionRange && c.setSelectionRange(0, 0);
    c && c.focus && c.focus();
}
function do_js_beautify()
{
    document.getElementById('beautify').disabled = true;
    js_source = document.getElementById('content').value;
    tabsize = document.getElementById('tabsize').value;
    tabchar = ' ';
    if (tabsize == 1) tabchar = '\t'; 
    
    var start = new Date();
    document.getElementById('content').value = js_beautify(js_source, tabsize, tabchar);
    var end = new Date();
    document.getElementById('timing').innerHTML = '' + (end - start) + ' ms';
    
    document.getElementById('beautify').disabled = false;
    return false;
}
</script>
<script type="text/javascript" src="beautify.js" ></script>
<script type="text/javascript" src="beautify-tests.js" ></script>

<style type="text/css">
form     { margin: 0 10px 0 10px }
textarea { width: 100%; height: 320px; border: 1px solid #ccc; padding: 3px; font-family: liberation mono, consolas, courier new, courier, monospace; font-size: 12px; }
h1       { font-family: trebuchet ms, arial, sans-serif; font-weight: normal; font-size: 28px; color: #666; margin-bottom: 15px; border-bottom: 1px solid #666; }
select   { width: 19%; }
button   { width: 40%; cursor: pointer;}
code, .code { font-family: liberation mono, consolas, lucida console, courier new, courier, monospace; font-size: 12px; }
pre      { font-size: 12px; font-family: liberation mono, consolas, courier new, courier, monospace; margin-left: 20px; color: #777; }

</style>
</head>
<body>
  <h1>Beautify Javascript</h1>
  <form method="post" action="?">
      <textarea rows="30" cols="30" name="content" id="content"><?php 

$c = get_raw('content');
echo $c ? 
     htmlspecialchars(js_beautify($c, $tab_size, $tab_char)) : 
     preg_replace("/\n([^ ])/u", "\$1",
         <<<HTML
/*   paste in your own code and press Beautify button   */
var latest_changes=new Object(
{
'2008-02-22':
'Javascript beautifier rewrite in javascript.',
'... boring history ...',
'2007-02-08':
'Initial release'});
var a=b?(c%d):e[f];
HTML
);

?></textarea><br />
      <button onclick="return do_js_beautify()" id="beautify">Beautify (Javascript)</button>
      <button type="submit" style="color:#666">Beautify (PHP version)</button>
<select name="tabsize" id="tabsize">
  <option value="1" <?php echo $tab_size == 1 ?'selected="selected"' : ''?>>indent with tab character</option>
  <option value="2" <?php echo $tab_size == 2 ?'selected="selected"' : ''?>>indent with 2 spaces</option>
  <option value="4" <?php echo $tab_size == 4 ?'selected="selected"' : ''?>>indent with 4 spaces</option>
  <option value="8" <?php echo $tab_size == 8 ?'selected="selected"' : ''?>>indent with 8 spaces</option>
</select>
      <p><span id="timing"></span> This script was intended to explore ugly javascripts, e.g <a href="http://createwebapp.com/javascripts/autocomplete.js">compacted in one line</a>, or just make scripts look more readable.</p>
      <p>With <big>big</big> and awesome thanks to <a href="http://my.opera.com/Vital/blog/2007/11/21/javascript-beautify-on-javascript-translated">Vital,</a> there is now a pure javascript version of beautifier!</p>
      <p>Files of possible interest:</p>
      <ul>
<li><a href="beautify.js">beautify.js,</a> javascript beautifier in javascript;</li>
<li><a href="beautify.phps">beautify.phps,</a> javascript beautifier in php;</li>
<li><a href="beautify-tests.js">beautify-tests.js,</a> beautifier tests, to make sure it's running as it should;</li>
<li><a href="beautify-tests.phps">beautify-tests.phps,</a> beautifier tests in php.</li>
</ul>
      <p>You can also always fetch the latest versions from subversion repository at <a href="svn://edev.uk.to/beautify/">svn://edev.uk.to/beautify</a>.</p>
      <p>In case of glitches you may wish to tell me about them&mdash;<code>elfz<span style="color:#999">[at]</span>laacz<span style="color:#999">[dot]</span>lv</code></p>
  </form>
<pre id="testresults">
   <a href="#" onclick="document.getElementById('testresults').innerHTML=test_js_beautify(); return false;">Run tests on javascript version</a>
<?php 
if (file_exists('.svnlog')) {
    printf("<pre>Latest commits from svn://edev.uk.to/beautify/:\n%s</pre>", 
        htmlspecialchars(file_get_contents('.svnlog')));
}

?>
</pre>

<script src="/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-2816767-1";
if (window.urchinTracker) urchinTracker();
</script>
</body>
</html>
