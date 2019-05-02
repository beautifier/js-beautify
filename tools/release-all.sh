#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

case "$OSTYPE" in
    darwin*) PLATFORM="OSX" ;;
    linux*)  PLATFORM="LINUX" ;;
    bsd*)    PLATFORM="BSD" ;;
    *)       PLATFORM="UNKNOWN" ;;
esac

release_python()
{
    cd $SCRIPT_DIR/..
    git checkout -B release origin/release
    git clean -xfd || exit 1
    cd python
    # python setup.py register -r pypi
    python setup.py sdist || exit 1
    python -m twine upload dist/* || exit 1
}

release_node()
{
    cd $SCRIPT_DIR/..
    git checkout -B release origin/release
    git clean -xfd || exit 1
    unset NPM_TAG
    if [[ $NEW_VERSION =~ .*(rc|beta).* ]]; then
    NPM_TAG='--tag next'
    fi
    npm publish . $NPM_TAG || exit 1
}

release_web()
{
    echo release is now on beautifier/beautifier.io
    # cd $SCRIPT_DIR/..
    # git clean -xfd || exit 1
    # git fetch || exit 1
    # git checkout -B gh-pages origin/gh-pages || exit 1
    # git merge origin/release --no-edit || exit 1
    # git push || exit 1
    # git checkout master
}

sedi() {
    if [[ "$PLATFORM" == "OSX" || "$PLATFORM" == "BSD" ]]; then
        sed -i "" $@
    elif [ "$PLATFORM" == "LINUX" ]; then
        sed -i $@
    else
        exit 1
    fi
}

update_versions()
{
    git fetch --all || exit 1
    git checkout master || exit 1
    git reset --hard origin/master || exit 1
    git clean -xfd || exit 1
    npm version --no-git-tag-version $NEW_VERSION

    sedi -E 's@(cdn.rawgit.+beautify/v)[^/]+@\1'$NEW_VERSION'@' README.md
    sedi -E 's@(cdnjs.cloudflare.+beautify/)[^/]+@\1'$NEW_VERSION'@' README.md
    sedi -E 's/\((README\.md:.js-beautify@).+\)/(\1'$NEW_VERSION')/' README.md

    echo "__version__ = '$NEW_VERSION'" > python/jsbeautifier/__version__.py
    git add .
    git commit -am "Bump version numbers for $NEW_VERSION"
    git push
}

update_release_branch()
{
    git reset --hard
    git clean -xfd
    git checkout -B release origin/release || exit 1
    git merge origin/master --no-edit || exit 1

    make js || exit 1
    git add -f js/lib/ || exit 1
    git commit -m "Release: $NEW_VERSION"
    git tag "v$NEW_VERSION" || exit 1
    git push || exit 1
    git push --tags
}

main()
{
    cd $SCRIPT_DIR/..

    local NEW_VERSION=$1
    NEW_VERSION=$1

    git checkout master || exit 1

    update_versions
    update_release_branch

    release_python
    release_node
    release_web

    git checkout master
}

(main $*)
