#!/bin/sh

DESTINATION=opera_userscript.js

echo '// ==UserScript==
// @name        Scripts beautifier for Opera
// @author      Rafal Chlodnicki
// @version     1.0
// @JSBeautifierversion 16 May 2009
// @include *
// ==/UserScript==

(function(){

var beautify = 
' > $DESTINATION
cat ../beautify.js >> $DESTINATION

echo '
  var toString = Function.prototype.toString;
  Function.prototype.tidy = function(){ return beautify( toString.call(this) ) };
  String.prototype.tidy = function(){ return beautify(this); };

  // tidy scripts if special window property set
  if ( window.tidyScripts ) 
  {
    opera.addEventListener('BeforeScript', tidyScript, false);
    function tidyScript(ev) 
    {
      ev.element.text = Function.prototype.tidy.call(ev.element.text);
    }
  }

})();
' >> $DESTINATION
