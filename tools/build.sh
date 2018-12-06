#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"
PROJECT_DIR="`( cd \"$SCRIPT_DIR/..\" && pwd )`"

build_js()
{
  echo Building javascript...
  cd $PROJECT_DIR

  # jshint
  $PROJECT_DIR/node_modules/.bin/jshint . || exit 1

  # generate lib files
  $PROJECT_DIR/node_modules/.bin/webpack || exit 1

  mkdir -p ./js/lib/unpackers
  cp -r ./js/src/unpackers ./js/lib/
  cp ./js/src/cli.js ./js/lib/

  # Wrap webkit output into an non-breaking form.
  # In an upcoming verion these will be replaced with standard webpack umd
  sed '/GENERATED_BUILD_OUTPUT/ r ./build/legacy/legacy_beautify_js.js' <./tools/template/beautify.wrapper.js >./js/lib/beautify.js || exit 1
  sed '/GENERATED_BUILD_OUTPUT/ r ./build/legacy/legacy_beautify_css.js' <./tools/template/beautify-css.wrapper.js >./js/lib/beautify-css.js || exit 1
  sed '/GENERATED_BUILD_OUTPUT/ r ./build/legacy/legacy_beautify_html.js' <./tools/template/beautify-html.wrapper.js >./js/lib/beautify-html.js || exit 1
}

build_beautify()
{
  cd $PROJECT_DIR
    # beautify test and data
  $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/js/test/*.js || exit 1
  $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/js/test/core/*.js || exit 1
  $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/test/data/**/*.js || exit 1

  # beautify product code
  $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/js/src/**/*.js || exit 1
  $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/web/*.js || exit 1

  $PROJECT_DIR/js/bin/css-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/web/common-style.css || exit 1

  $PROJECT_DIR/js/bin/html-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r index.html

  build_js
}

build_update-codemirror()
{
  rm -rf node_modules/codemirror
  npm install codemirror
  rm -rf ./web/third-party/codemirror/*
  cp ./node_modules/codemirror/LICENSE ./web/third-party/codemirror/
  cp ./node_modules/codemirror/README.md ./web/third-party/codemirror/
  cp -r ./node_modules/codemirror/lib ./web/third-party/codemirror/
  mkdir -p ./web/third-party/codemirror/mode
  cp -r ./node_modules/codemirror/mode/javascript ./web/third-party/codemirror/mode/
  git add -Av ./web/third-party/codemirror
}

main() {
  cd $PROJECT_DIR
  local ACTION
  ACTION=build_${1:-full}
  if [ -n "$(type -t $ACTION)" ] && [ "$(type -t $ACTION)" = "function" ]; then
      $ACTION
  else
      build_help
  fi

}

(main $*)
