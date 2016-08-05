#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"


test_cli_common()
{
  echo ----------------------------------------
  echo Testing common cli behavior...
  CLI_SCRIPT_NAME=${1:?missing_param}.js
  CLI_SCRIPT=$SCRIPT_DIR/../bin/$CLI_SCRIPT_NAME
  echo Script: $CLI_SCRIPT

  # should find the minimal help output
  $CLI_SCRIPT 2>&1 | grep -q "Must pipe input or define at least one file\." || {
      $CLI_SCRIPT 2>&1
      echo "[$CLI_SCRIPT_NAME] Output should be help message."
      exit 1
  }

  $CLI_SCRIPT 2> /dev/null && {
      echo "[$CLI_SCRIPT_NAME (with no parameters)] Return code should be error."
      exit 1
  }

  $CLI_SCRIPT -Z 2> /dev/null && {
      echo "[$CLI_SCRIPT_NAME -Z] Return code for invalid parameter should be error."
      exit 1
  }

  $CLI_SCRIPT -h > /dev/null || {
      echo "[$CLI_SCRIPT_NAME -h] Return code should be success."
      exit 1
  }

  $CLI_SCRIPT -v > /dev/null || {
      echo "[$CLI_SCRIPT_NAME -v] Return code should be success."
      exit 1
  }

  MISSING_FILE="$SCRIPT_DIR/../../../js/bin/missing_file"
  MISSING_FILE_MESSAGE="Unable to open path"
  $CLI_SCRIPT $MISSING_FILE 2> /dev/null && {
      echo "[$CLI_SCRIPT_NAME $MISSING_FILE] Return code should be error."
      exit 1
  }

  $CLI_SCRIPT $MISSING_FILE 2>&1 | grep -q "$MISSING_FILE_MESSAGE" || {
      echo "[$CLI_SCRIPT_NAME $MISSING_FILE] Stderr should have useful message."
      exit 1
  }

  if [ "`$CLI_SCRIPT $MISSING_FILE 2> /dev/null`" != "" ]; then
      echo "[$CLI_SCRIPT_NAME $MISSING_FILE] Stdout should have no text."
      exit 1
  fi

}

setup_temp()
{
    mkdir -p target
    TEST_TEMP=$PWD/`mktemp -d target/test_temp_XXXX`
    echo Created $TEST_TEMP...
}

cleanup()
{
    rm -rf $TEST_TEMP && echo Removed $TEST_TEMP...
    test -z $1 || exit $1
}


test_cli_js_beautify()
{
  echo ----------------------------------------
  echo Testing js-beautify cli behavior...
  CLI_SCRIPT=$SCRIPT_DIR/../bin/js-beautify.js

  $CLI_SCRIPT $SCRIPT_DIR/../bin/js-beautify.js > /dev/null || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected succeed."
      exit 1
  }

  $CLI_SCRIPT $SCRIPT_DIR/../bin/css-beautify.js > /dev/null || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/css-beautify.js was expected succeed."
      exit 1
  }

  $CLI_SCRIPT $SCRIPT_DIR/../bin/js-beautify.js | diff $SCRIPT_DIR/../bin/js-beautify.js - || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected to be unchanged."
      exit 1
  }

  cat $SCRIPT_DIR/../bin/js-beautify.js | $CLI_SCRIPT | diff $SCRIPT_DIR/../bin/js-beautify.js - || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected to be unchanged."
      exit 1
  }

  cat $SCRIPT_DIR/../bin/js-beautify.js | $CLI_SCRIPT - | diff $SCRIPT_DIR/../bin/js-beautify.js - || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js was expected to be unchanged."
      exit 1
  }


  # EditorConfig related tests
  export EDITORCONFIG_RESOURCE=js/test/resources/editorconfig
  cd js/test/resources/editorconfig
  $CLI_SCRIPT --editorconfig $SCRIPT_DIR/../bin/js-beautify.js \
  > /dev/null || {
      echo "Invalid editorconfig file will not report error (consistent with the EditorConfig)."
      exit 1
  }
  $CLI_SCRIPT --editorconfig example.js \
  | diff -q example.js - && {
      echo "EditorConfig settings overides indent_size (to 2), hence causing diff."
      exit 1
  }
  cd -
  # End EditorConfig

  setup_temp
  $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $SCRIPT_DIR/../bin/js-beautify.js && diff $SCRIPT_DIR/../bin/js-beautify.js $TEST_TEMP/js-beautify.js || {
      echo "js-beautify output for $SCRIPT_DIR/../bin/js-beautify.js should have been created in $TEST_TEMP/js-beautify.js."
      cleanup 1
  }

  # ensure new line settings work
  $CLI_SCRIPT -o $TEST_TEMP/js-beautify-n.js --eol '\n' $SCRIPT_DIR/../bin/js-beautify.js
  $CLI_SCRIPT -o $TEST_TEMP/js-beautify-rn.js --eol '\r\n' $TEST_TEMP/js-beautify-n.js

  diff -q $TEST_TEMP/js-beautify-n.js $TEST_TEMP/js-beautify-rn.js && {
      diff $TEST_TEMP/js-beautify-n.js $TEST_TEMP/js-beautify-rn.js | cat -t -e
      echo "js-beautify output for $TEST_TEMP/js-beautify-n.js and $TEST_TEMP/js-beautify-rn.js was expected to be different."
      cleanup 1
  }

  $CLI_SCRIPT $TEST_TEMP/js-beautify-n.js | diff -q $TEST_TEMP/js-beautify-n.js - || {
      echo "js-beautify output for $TEST_TEMP/js-beautify-n.js was expected to be unchanged."
      cleanup 1
  }

  $CLI_SCRIPT --eol 'auto' $TEST_TEMP/js-beautify-rn.js | diff -q $TEST_TEMP/js-beautify-rn.js - || {
      echo "js-beautify output for $TEST_TEMP/js-beautify-rn.js was expected to be unchanged."
      cleanup 1
  }

  # ensure unchanged files are not overwritten
  $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $SCRIPT_DIR/../bin/js-beautify.js
  cp -p $TEST_TEMP/js-beautify.js $TEST_TEMP/js-beautify-old.js
  touch $TEST_TEMP/js-beautify.js
  sleep 2
  touch $TEST_TEMP/js-beautify-old.js
  $CLI_SCRIPT -r $TEST_TEMP/js-beautify.js && test $TEST_TEMP/js-beautify.js -nt $TEST_TEMP/js-beautify-old.js && {
      echo "js-beautify should not replace unchanged file $TEST_TEMP/js-beautify.js when using -r"
      cleanup 1
  }

  $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $TEST_TEMP/js-beautify.js && test $TEST_TEMP/js-beautify.js -nt $TEST_TEMP/js-beautify-old.js && {
      echo "js-beautify should not replace unchanged file $TEST_TEMP/js-beautify.js when using -o and same file name"
      cleanup 1
  }

  $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $TEST_TEMP/js-beautify-old.js && test $TEST_TEMP/js-beautify.js -nt $TEST_TEMP/js-beautify-old.js && {
      echo "js-beautify should not replace unchanged file $TEST_TEMP/js-beautify.js when using -o and different file name"
      cleanup 1
  }

  $CLI_SCRIPT $SCRIPT_DIR/../bin/css-beautify.js | diff -q $SCRIPT_DIR/../bin/css-beautify.js - && {
      echo "js-beautify output for $SCRIPT_DIR/../bin/css-beautify.js was expected to be different."
      cleanup 1
  }

  unset HOME
  unset USERPROFILE
  $CLI_SCRIPT -o $TEST_TEMP/example1-default.js $SCRIPT_DIR/resources/example1.js || exit 1

  $CLI_SCRIPT -o $TEST_TEMP/example1-sanity.js $TEST_TEMP/example1-default.js || exit 1
  diff -q $TEST_TEMP/example1-default.js $TEST_TEMP/example1-sanity.js || {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be identical after no change in settings."
      cleanup 1
  }

  cd $SCRIPT_DIR/resources/configerror
  $CLI_SCRIPT $TEST_TEMP/example1-default.js 2>&1 |  grep -q "Error while loading beautifier configuration file\." || {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be configration load error message."
      cleanup 1
  }

  cd $SCRIPT_DIR/resources/indent11chars
  $CLI_SCRIPT $TEST_TEMP/example1-default.js | diff -q $TEST_TEMP/example1-default.js - && {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be different based on CWD settings."
      cleanup 1
  }

  cd $SCRIPT_DIR/resources/indent11chars/subDir1/subDir2
  $CLI_SCRIPT $TEST_TEMP/example1-default.js | diff -q $TEST_TEMP/example1-default.js - && {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be different based on CWD parent folder settings."
      cleanup 1
  }
  cd $SCRIPT_DIR

  export HOME=$SCRIPT_DIR/resources/indent11chars
  $CLI_SCRIPT $TEST_TEMP/example1-default.js | diff -q $TEST_TEMP/example1-default.js - && {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be different based on HOME settings."
      cleanup 1
  }

  $CLI_SCRIPT -o $TEST_TEMP/example1-indent11chars.js $TEST_TEMP/example1-default.js

  unset HOME
  export USERPROFILE=$SCRIPT_DIR/resources/indent11chars
  # node -p 'process.env["USERPROFILE"] || process.env["HOME"] || "unset"'
  $CLI_SCRIPT $TEST_TEMP/example1-default.js | diff -q $TEST_TEMP/example1-indent11chars.js - || {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be identical for same HOME and USERPROFILE settings."
      cleanup 1
  }

  $CLI_SCRIPT $TEST_TEMP/example1-default.js | diff -q $TEST_TEMP/example1-default.js - && {
      echo "js-beautify output for $TEST_TEMP/example1-default.js was expected to be different based on USERPROFILE settings."
      cleanup 1
  }

  cleanup
}

test_smoke_js_beautify()
{
  echo ----------------------------------------
  echo Testing js-beautify functionality...
  node $SCRIPT_DIR/node-beautify-tests.js || exit 1
  node $SCRIPT_DIR/amd-beautify-tests.js || exit 1
}


test_performance_js_beautify()
{
  echo ----------------------------------------
  echo Testing js-beautify performance...
  node $SCRIPT_DIR/node-beautify-perf-tests.js || exit 1
  echo ----------------------------------------
}

test_performance_html_beautify()
{
  echo ----------------------------------------
  echo Testing html-beautify performance...
  node $SCRIPT_DIR/node-beautify-html-perf-tests.js || exit 1
  echo ----------------------------------------
}

test_cli_common css-beautify
test_cli_common html-beautify
test_cli_common js-beautify

test_cli_js_beautify
test_smoke_js_beautify
test_performance_js_beautify
test_performance_html_beautify

echo ----------------------------------------
echo $0 - PASSED.
echo ----------------------------------------
