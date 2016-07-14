#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

test_cli_common()
{
    echo ----------------------------------------
    echo Testing common cli behavior...
    CLI_SCRIPT_NAME=${1:?missing_param}
    CLI_SCRIPT=$SCRIPT_DIR/../../$CLI_SCRIPT_NAME
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
    MISSING_FILE_MESSAGE="No such file or directory"
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

    # EditorConfig related tests
    cd ../js/test/resources/editorconfig
    $CLI_SCRIPT --editorconfig $SCRIPT_DIR/../../../js/bin/js-beautify.js \
    > /dev/null || {
        echo "Invalid editorconfig file will not report error (consistent with the EditorConfig)."
        exit 1
    }
    $CLI_SCRIPT --editorconfig example.js \
    | diff -q example.js - && {
        echo "EditorConfig settings overides indent_size, hence causing diff."
        exit 1
    }
    cd -
    # End EditorConfig
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
    CLI_SCRIPT=$SCRIPT_DIR/../../js-beautify

    $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/js-beautify.js > /dev/null || {
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/js-beautify.js was expected succeed."
        exit 1
    }

    $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/css-beautify.js > /dev/null || {
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/css-beautify.js was expected succeed."
        exit 1
    }

    $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/js-beautify.js | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - || {
        $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/js-beautify.js | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - | cat -t -e
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/js-beautify.js was expected to be unchanged."
        exit 1
    }

    cat $SCRIPT_DIR/../../../js/bin/js-beautify.js | $CLI_SCRIPT | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - || {
        $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/js-beautify.js | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - | cat -t -e
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/js-beautify.js was expected to be unchanged."
        exit 1
    }

    cat $SCRIPT_DIR/../../../js/bin/js-beautify.js | $CLI_SCRIPT - | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - || {
        $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/js-beautify.js | diff $SCRIPT_DIR/../../../js/bin/js-beautify.js - | cat -t -e
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/js-beautify.js was expected to be unchanged."
        exit 1
    }

    setup_temp
    $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $SCRIPT_DIR/../../../js/bin/js-beautify.js && diff $SCRIPT_DIR/../../../js/bin/js-beautify.js $TEST_TEMP/js-beautify.js || {
    $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $SCRIPT_DIR/../../../js/bin/js-beautify.js && diff $SCRIPT_DIR/../../../js/bin/js-beautify.js $TEST_TEMP/js-beautify.js | cat -t -e
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/js-beautify.js should have been created in $TEST_TEMP/js-beautify.js."
        cleanup 1
    }

    # ensure new line settings work
    $CLI_SCRIPT -o $TEST_TEMP/js-beautify-n.js -e '\n' $SCRIPT_DIR/../../../js/bin/js-beautify.js
    $CLI_SCRIPT -o $TEST_TEMP/js-beautify-rn.js -e '\r\n' $TEST_TEMP/js-beautify-n.js

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
    $CLI_SCRIPT -o $TEST_TEMP/js-beautify.js $SCRIPT_DIR/../../../js/bin/js-beautify.js
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

    $CLI_SCRIPT $SCRIPT_DIR/../../../js/bin/css-beautify.js | diff -q $SCRIPT_DIR/../../../js/bin/css-beautify.js - && {
        echo "js-beautify output for $SCRIPT_DIR/../../../js/bin/css-beautify.js was expected to be different."
        cleanup 1
    }

    cleanup
}

test_smoke_js_beautify()
{
    echo ----------------------------------------
    echo Testing beautify functionality...
    $SCRIPT_DIR/../../js-beautify-test.py || exit 1
}

test_perf_js_beautify()
{
    echo ----------------------------------------
    echo Testing beautify performance...
  	# PYTHON=python $SCRIPT_DIR/../../js-beautify-profile || exit 1
  	$SCRIPT_DIR/test-perf-jsbeautifier.py || exit 1
}

main() {
    #test_cli_common css-beautify
    #test_cli_common html-beautify
    test_cli_common js-beautify

    test_cli_js_beautify
    test_smoke_js_beautify
    test_perf_js_beautify

    echo ----------------------------------------
    echo $0 - PASSED.
    echo ----------------------------------------
}

(main $*)
