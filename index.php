<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!--

  (c) 2006-2008: Einars "elfz" Lielmanis, 
            elfz@laacz.lv
            http://elfz.laacz.lv/

-->
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Online beautifier for javascript</title>
<script type="text/javascript">
window.onload = function() {
    var c = document.forms[0].content;
    c && c.setSelectionRange && c.setSelectionRange(0, 0);
    c && c.focus && c.focus();
}
function do_js_beautify()
{
    document.getElementById('beautify').disabled = true;
    js_source = document.getElementById('content').value.replace(/^\s+/, '');
    tabsize = document.getElementById('tabsize').value;
    tabchar = ' ';
    if (tabsize == 1) {
        tabchar = '\t'; 
    }

    if (js_source && js_source[0] === '<') { 
        document.getElementById('content').value = style_html(js_source, tabsize, tabchar, 80);
    } else {
        document.getElementById('content').value = js_beautify(js_source, tabsize, tabchar);
    }
    
    document.getElementById('beautify').disabled = false;
    return false;
}
</script>
<script type="text/javascript" src="beautify.js" ></script>
<script type="text/javascript" src="beautify-tests.js" ></script>
<script type="text/javascript" src="HTML-Beautify.js" ></script>

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
      <textarea rows="30" cols="30" name="content" id="content">
/*   paste in your own code and press Beautify button   */
var latest_changes=new Object({'2008-02-22':'Javascript beautifier rewrite in javascript.','... boring history ...','2007-02-08':'Initial release'});var a=b?(c%d):e[f];
</textarea><br />
      <button onclick="return do_js_beautify()" id="beautify">Beautify</button>
<select name="tabsize" id="tabsize">
  <option value="1">indent with tab character</option>
  <option value="2">indent with 2 spaces</option>
  <option value="4" selected="selected">indent with 4 spaces</option>
  <option value="8">indent with 8 spaces</option>
</select>
      <p>This script was intended to explore ugly javascripts, e.g <a href="http://createwebapp.com/javascripts/autocomplete.js">compacted in one line</a>, or just make scripts look more readable.</p>
      <p>Now you can try to paste in code with &lt;script&gt; tags and (well-formed) HTML as well - say thanks to Nochum and his <a href="HTML-Beautify.js">experimental HTML beautifier!</a></p>
      <p>Thanks to <a href="http://my.opera.com/Vital/blog/2007/11/21/javascript-beautify-on-javascript-translated">Vital,</a> there is now a pure javascript version of beautifier. It's now the only one: php version is not supported anymore.</p>
      <ul>
<li><a href="beautify.js">beautify.js,</a> javascript beautifier in javascript;</li>
<li><a href="HTML-Beautify.js">HTML-Beautify.js,</a> Nochum's experimental HTML beautifier in javascript;</li>
<li><a href="beautify-tests.js">beautify-tests.js,</a> beautifier tests, to make sure it's running as it should;</li>
</ul>
      <p>You can also always fetch the latest versions from subversion repository at <a href="svn://edev.uk.to/beautify/">svn://edev.uk.to/beautify</a>.</p>
      <p>If you're writing javascript, <a href="http://jslint.com/">JSLint</a> is a really fine piece of software, too. You should at least understand what and why it says about your code &mdash; to be a better person. Even if it hurts your feelings.</p>
      <p>In case of glitches you may wish to tell me about them&mdash;<code>elfz<span style="color:#999">[at]</span>laacz<span style="color:#999">[dot]</span>lv</code></p>
  </form>
<pre id="testresults">
   <a href="#" onclick="document.getElementById('testresults').innerHTML=test_js_beautify(); return false;">Run tests</a>
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
