#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

build_help()
{
    echo "build.sh <action>"
    echo "    full	    - build and test of all implementations"
    echo "    all       - build of both implementations"
    echo "    js        - build of javascript"
    echo "    py        - build of python"
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

build_py()
{
  	echo Building python module...
  	pip install -e ./python || exit 1
}

build_js()
{
    echo Building javascript...
    npm install || exit 1
}

build_alltest()
{
    build_jstest
    build_pytest
}

build_pytest()
{
  	echo Testing python implementation...
  	node test/generate-tests.js || exit 1
  	cd python
  	python --version
  	./jsbeautifier/tests/shell-smoke-test.sh || exit 1
}

build_jstest()
{
  	echo Testing javascript implementation...
  	node test/generate-tests.js || exit 1
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
  cd $SCRIPT_DIR/..
  local ACTION
  ACTION=build_${1:-full}
  if [ -n "$(type -t $ACTION)" ] && [ "$(type -t $ACTION)" = "function" ]; then
      $ACTION
  else
      build_help
  fi

}

(main $*)
