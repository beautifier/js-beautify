#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

generate_changelog()
{
    $SCRIPT_DIR/generate-changelog.sh beautify-web/js-beautify || exit 1
    git commit -am "Update Changelog for $NEW_VERSION"
}

release_python()
{
    git clean -xfd || exit 1
    echo "__version__ = '$NEW_VERSION'" > python/jsbeautifier/__version__.py
    git commit -am "Python $NEW_VERSION"
    cd python
    python setup.py register
    python setup.py sdist bdist_wininst upload
    git push
}

release_node()
{
      git clean -xfd || exit 1
      npm version $NEW_VERSION
      npm publish .
      git push
      git push --tags
}

release_web()
{
      local ORIGINAL_BRANCH
      ORIGINAL_BRANCH=$(git branch | grep '[*] .*' | awk '{print $2}')
      git clean -xfd || exit 1
      git fetch || exit 1
      git checkout gh-pages && 	git reset --hard origin/gh-pages || exit 1
      git merge origin/master && git push || exit 1
      git checkout $ORIGINAL_BRANCH
}

main()
{
    cd $SCRIPT_DIR/..

    local NEW_VERSION=$1
    NEW_VERSION=$1

    git checkout master

    generate_changelog
    (release_python)
    release_node
    release_web
}

(main $*)
