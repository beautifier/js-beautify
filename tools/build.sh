#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"
PROJECT_DIR="`( cd \"$SCRIPT_DIR/..\" && pwd )`"

build_help()
{
  echo "build.sh <action>"
  echo "    full	    - build and test all implementations"
  echo "    all       - build both implementations"
  echo "    static    - serve static version of site locally"
  echo "    js        - build javascript"
  echo "    py        - build python"
  echo "    alltest   - test both implementations, js and python"
  echo "    pytest    - test python implementation"
  echo "    jstest    - test javascript implementation"
}

build_ci()
{
  build_full
  build_git_status
}

build_full()
{
  build_all
  build_alltest
}

build_all()
{
  build_py
  build_js
}

build_static()
{
  npm install || exit 1
  ./node_modules/.bin/static
}

build_py()
{
	echo Building python module...
	/usr/bin/env python -m pip install -e ./python || exit 1
}

build_js()
{
  echo Building javascript...
  npm install || exit 1
  generate_tests

  # generate lib files
  ./node_modules/.bin/webpack

  mkdir -p ./js/lib/unpackers
  cp -r ./js/src/unpackers ./js/lib/
  cp ./js/src/cli.js ./js/lib/

  # Wrap webkit output into an non-breaking form.
  # In an upcoming verion these will be replaced with standard webpack umd
  cat ./tools/template/beautify.begin.js > ./js/lib/beautify.js
  cat ./dist/legacy_beautify_js.js >> ./js/lib/beautify.js
  cat ./tools/template/beautify.end.js >> ./js/lib/beautify.js

  cat ./tools/template/beautify-css.begin.js > ./js/lib/beautify-css.js
  cat ./dist/legacy_beautify_css.js >> ./js/lib/beautify-css.js
  cat ./tools/template/beautify-css.end.js >> ./js/lib/beautify-css.js

  cat ./tools/template/beautify-html.begin.js > ./js/lib/beautify-html.js
  cat ./dist/legacy_beautify_html.js >> ./js/lib/beautify-html.js
  cat ./tools/template/beautify-html.end.js >> ./js/lib/beautify-html.js

  cp ./dist/beautifier.js ./js/lib/
  cp ./dist/beautifier.min.js ./js/lib/

  # jshint
  $PROJECT_DIR/node_modules/.bin/jshint 'js/src' 'test' || exit 1

  # beautify test and data
  for f in $(ls $PROJECT_DIR/js/test/*.js | sort -n); do
      $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $f  || exit 1
  done

  for f in $(find $PROJECT_DIR/test/data -name '*.js' | sort -n); do
      $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $f  || exit 1
  done

  # beautify product code
  for f in $(find $PROJECT_DIR/js/src -name '*.js' | sort -n); do
    $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $f  || exit 1
  done

  for f in $(ls $PROJECT_DIR/web/*.js | sort -n); do
    $PROJECT_DIR/js/bin/js-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $f  || exit 1
  done

  $PROJECT_DIR/js/bin/css-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r $PROJECT_DIR/web/common-style.css || exit 1

  # html not ready yet
  # $PROJECT_DIR/js/bin/html-beautify.js --config $PROJECT_DIR/jsbeautifyrc -r index.html

  # jshint again to make sure things haven't changed
  $PROJECT_DIR/node_modules/.bin/jshint 'js/src' 'test' || exit 1
}

generate_tests()
{
	node test/generate-tests.js || exit 1
}

build_alltest()
{
  build_jstest
  build_pytest
}

build_pytest()
{
	echo Testing python implementation...
	generate_tests
	cd python
	python --version
	./jsbeautifier/tests/shell-smoke-test.sh || exit 1
}

build_jstest()
{
	echo Testing javascript implementation...
	generate_tests
	node --version
	./js/test/shell-smoke-test.sh || exit 1
}

build_git_status()
{
  $SCRIPT_DIR/git-status-clear.sh || exit 1
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
