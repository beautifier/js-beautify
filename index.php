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
<title>Online beautifier for javascript (js beautify, pretty-print)</title>
<script type="text/javascript">
window.onload = function() {
    var c = document.forms[0].content;
    c && c.setSelectionRange && c.setSelectionRange(0, 0);
    c && c.focus && c.focus();
}
</script>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
form     { margin: 0 10px 0 10px }
textarea { width: 100%; height: 320px; border: 1px solid #ccc; padding: 3px; font-family: liberation mono, consolas, courier new, courier, monospace; font-size: 12px; }
h1       { font-family: trebuchet ms, arial, sans-serif; font-weight: normal; font-size: 28px; color: #666; margin-bottom: 15px; border-bottom: 1px solid #666; }
select   { width: 19%; }
button   { width: 79%; cursor: pointer;}
code, .code { font-family: liberation mono, consolas, lucida console, courier new, courier, monospace; font-size: 12px; }
pre      { font-size: 12px; font-family: liberation mono, consolas, courier new, courier, monospace; margin-left: 20px; color: #777; }

</style>
</head>
<body>
  <h1>Beautify Javascript</h1>
  <form method="post" action="?">
      <textarea rows="30" cols="30" name="content"><?php 

$c = get_raw('content');
echo $c ? 
     htmlspecialchars(js_beautify($c, $tab_size, $tab_char)) : 
     preg_replace("/\n([^ ])/u", "\$1",
         <<<HTML
/*   paste in your own code and press Beautify button   */
var latest_changes=new Object(
{
'2007-10-17':
'Many, many fixes and improvements. Processing speed is also back.',
'... who cares ...',
'2007-02-08':
'Initial release'});
var a=b?(c%d):e[f];
HTML
);

?></textarea><br />
      <button type="submit">Beautify</button>
<select name="tabsize">
  <option value="1" <?php echo $tab_size == 1 ?'selected="selected"' : ''?>>indent with tab character</option>
  <option value="2" <?php echo $tab_size == 2 ?'selected="selected"' : ''?>>indent with 2 spaces</option>
  <option value="4" <?php echo $tab_size == 4 ?'selected="selected"' : ''?>>indent with 4 spaces</option>
  <option value="8" <?php echo $tab_size == 8 ?'selected="selected"' : ''?>>indent with 8 spaces</option>
</select>
      <p>This script was intended to explore ugly javascripts, e.g <a href="http://createwebapp.com/javascripts/autocomplete.js">compacted in one line</a>.</p>
      <p>PHP source can be <a href="beautify.phps">seen online here</a> or fetched from subversion repository at <a href="svn://edev.uk.to/beautify/">svn://edev.uk.to/beautify</a>. Feel free to use and abuse.</p>
      <p>In case of glitches you may wish to tell me about them&mdash;<code>elfz<span style="color:#999">[at]</span>laacz<span style="color:#999">[dot]</span>lv</code></p>
      <p>If anyone would volunteer to convert current version to javascript, it would be also cool. There's really no reason for the converter to be server-side php, if it could be client-side (probably firefox-integratable) javascript.</p>
  </form>
<?php 
if (file_exists('.svnlog')) {
    printf("<pre>Latest commits from svn://edev.uk.to/beautify/:\n%s</pre>", 
        htmlspecialchars(file_get_contents('.svnlog')));
}

?>
<script src="/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-2816767-1";
if (window.urchinTracker) urchinTracker();
</script>
</body>
</html>
