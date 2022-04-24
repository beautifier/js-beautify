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
    git clean -xfd || exit 1
    git fetch --all || exit 1

    git checkout -B staging/release origin/staging/release
    git clean -xfd || exit 1 
    cd python
    # python setup.py register -r pypi
    cp setup-js.py setup.py || exit 1
    python setup.py sdist || exit 1
    cp setup-css.py setup.py || exit 1
    python setup.py sdist || exit 1
    rm setup.py || exit 1
    python -m twine upload dist/* || exit 1
}

release_node()
{
    cd $SCRIPT_DIR/..
    git clean -xfd || exit 1
    git fetch --all || exit 1

    git checkout -B staging/release origin/staging/release
    git clean -xfd || exit 1
    unset NPM_TAG
    if [[ $NEW_VERSION =~ .*(rc|beta).* ]]; then
    NPM_TAG='--tag next'
    fi
    $SCRIPT_DIR/npm publish . $NPM_TAG || exit 1
}

release_web()
{
    cd $SCRIPT_DIR/..
    git clean -xfd || exit 1
    git fetch --all || exit 1

    git checkout -B staging/gh-pages site/staging/gh-pages || exit 1
    git reset --hard site/gh-pages || exit 1
    git merge origin/staging/release --no-edit || exit 1
    git push || exit 1

    git checkout -B staging/main site/staging/main || exit 1
    git reset --hard site/main || exit 1
    git merge origin/staging/main --no-edit || exit 1
    git push || exit 1    
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
    cd $SCRIPT_DIR/..
    git clean -xfd || exit 1
    git fetch --all || exit 1

    # trigger remote uses deploy key, push will cause downstream GitHub Actions to fire
    git checkout -B staging/main trigger/staging/main || exit 1
    git merge origin/main --no-edit || exit 1
    git clean -xfd || exit 1

    # Disabled due to build break
     $SCRIPT_DIR/generate-changelog.sh beautify-web/js-beautify $GITHUB_TOKEN || exit 1

    $SCRIPT_DIR/npm version --no-git-tag-version $NEW_VERSION || exit 1

    sedi -E 's@(cdnjs.cloudflare.+beautify/)[^/]+@\1'$NEW_VERSION'@' README.md
    sedi -E 's/\((README\.md:.js-beautify@).+\)/(\1'$NEW_VERSION')/' README.md

    echo "__version__ = \"$NEW_VERSION\"" > python/jsbeautifier/__version__.py
    echo "__version__ = \"$NEW_VERSION\"" > python/cssbeautifier/__version__.py
    git add . || exit 1
    git commit -am "Bump version numbers for $NEW_VERSION" || exit 1
    git push || exit 1
}

update_release_branch()
{
    cd $SCRIPT_DIR/..
    git clean -xfd || exit 1
    git fetch --all || exit 1

    git reset --hard
    # trigger remote uses deploy key, push will cause downstream GitHub Actions to fire
    git checkout -B staging/release trigger/staging/release || exit 1
    git merge origin/release --no-edit || exit 1
    git merge origin/staging/main --no-edit || exit 1

    make js || exit 1
    git add -f js/lib/ || exit 1
    git add -f js/test/generated/
    git add -f python/jsbeautifier/tests/generated/
    git add -f python/cssbeautifier/tests/generated/
    
    git commit -m "Release: $NEW_VERSION"
    git tag "v$NEW_VERSION" || exit 1
    git push || exit 1
    git push --tags
}

main()
{
    cd $SCRIPT_DIR/..

    local NEW_VERSION=$1
    NEW_VERSION=${NEW_VERSION/v/}

    if [[ ! $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9].*$ ]]; then
        echo Version number must start with MAJOR.MINOR.INCREMENTAL numbering.
        exit 1
    fi    

    npm --version > /dev/null || {
        echo ERROR: npm must be installed before attempting release
        exit 1
    }

    twine -h > /dev/null || {
        exit 1
    }

    update_versions
    update_release_branch

    release_python
    release_node
    release_web

    git checkout main
}

(main $*)
