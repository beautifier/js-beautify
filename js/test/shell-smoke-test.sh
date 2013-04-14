#!/bin/bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

test_cli_common()
{
  echo ----------------------------------------
  echo Testing common cli behavior...
  CLI_SCRIPT=${1:?missing_param}
  echo Script: $CLI_SCRIPT

  # should find the minimal help output
  $SCRIPT_DIR/../bin/$CLI_SCRIPT.js 2>&1 | grep -q "Must define at least one file\." || {
      echo "[$CLI_SCRIPT.js] Output should be help message."
      exit 1
  }

  $SCRIPT_DIR/../bin/$CLI_SCRIPT.js 2> /dev/null && {
      echo "[$CLI_SCRIPT.js (with no parameters)] Return code should be error."
      exit 1
  }

  $SCRIPT_DIR/../bin/$CLI_SCRIPT.js -invalidParameter 2> /dev/null && {
      echo "[$CLI_SCRIPT.js -invalidParameter] Return code should be error."
      exit 1
  }

  $SCRIPT_DIR/../bin/$CLI_SCRIPT.js -h > /dev/null || {
      echo "[$CLI_SCRIPT.js -h] Return code should be success."
      exit 1
  }

  $SCRIPT_DIR/../bin/$CLI_SCRIPT.js -v > /dev/null || {
      echo "[$CLI_SCRIPT.js -v] Return code should be success."
      exit 1
  }

}

test_cli_js_beautify()
{
  echo ----------------------------------------
  echo Testing js-beautify cli behavior...
  $SCRIPT_DIR/../bin/js-beautify.js $SCRIPT_DIR/../bin/js-beautify.js > /dev/null || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected succeed."
      exit 1
  }

  $SCRIPT_DIR/../bin/js-beautify.js $SCRIPT_DIR/../bin/css-beautify.js > /dev/null || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/css-beautify.js was expected succeed."
      exit 1
  }

  $SCRIPT_DIR/../bin/js-beautify.js $SCRIPT_DIR/../bin/js-beautify.js | diff $SCRIPT_DIR/../bin/js-beautify.js - || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected to be unchanged."
      exit 1
  }

  $SCRIPT_DIR/../bin/js-beautify.js $SCRIPT_DIR/../bin/css-beautify.js | diff -q $SCRIPT_DIR/../bin/css-beautify.js - && {
      echo "js-beautify output for $SCRIPT_DIR/../bin/css-beautify.js was expected to be different."
      exit 1
  }

}

test_cli_common css-beautify
test_cli_common html-beautify
test_cli_common js-beautify

test_cli_js_beautify

echo ----------------------------------------
echo $0 - PASSED.
echo ----------------------------------------
