# Contributing


## Report Issues and Request Changes
If you find a bug, please report it, including environment and examples of current behavior and what you believe to be the correct behavior.  The clearer your description and information, the more likely it is someone will be able to make progress on it.  The default issue template will help guide you through this.

## How to Make Changes (Implement Fixes and New Features)
Fixes and enhancements are totally welcome.  We prefer you to file an issue before filing a PR, as this gives us chance to discuss design details, but feel free to dive right in.

### 1. Build and Test Locally
This repository holds two mostly identical implementations of the beautifiers: a JavaScript implementation and a Python implementation.
While developing, you may locally build and test the JavaScript or Python (or both). The HTML beautifier is only implemented in JavaScript.

* Familiarize yourself with the folder structure and code style before you dive in.
* Make changes to the implementation of your choice.
* If working in the JavaScript implementation:
  * Run `./build js`
  * Run `./build static` to see changes served locally
* If working in the Python implementation:
  * Run `./build py`
  * Run `./build static` to see changes served locally
* Add tests to `/test/data/*/test.js`.
* Run `./build jstest` or `./build pytest` to run style checks, and to generate and run tests.
* Include all changed files in your commit - The generated test files are checked in along with changes to the test data files.

### 2. Ensure Feature Parity
Any changes made to one implementation must be also made to the other implementation.  **This is required**.  Every time we make an exception to this requirement the project becomes harder to maintain.  This will become painfully clear, should you find yourself unable to port changes from one implementation to the other due to implementations being out of sync. We made this a requirement several years ago and there are **still** open issues for changes that people promised to port "in the next week or two".  The entire HTML beautifier is an example of this. :(

The implementations are already very similar and neither Python nor JavaScript are that hard to understand.  Take the plunge, it is easier than you think.  If you get stuck, go ahead and file a Pull Request and we can discuss how to move forward.

* Run `./build` (with no parameters) to run style checks, and to generate and run tests on both implementations.
* Include all changed files in your commit - The generated test files are checked in along with changes to the test data files.

### 3. Update Documentation and Tools
Update documentation as needed.  This includes files such as the README.md, internal command-line help, and file comments.
Also, check if your change needs any tooling updates.  For example, the CDN URLs required additional scripting to update automatically for new releases.

### 4. Submit a Pull Request

* Run `./build full` locally after commit but before creation of Pull Request.  You may start a Pull Request even if this reports errors, but the PR will not be merged until all errors are fixed.
* Include description of changes. Include examples of input and expected output if possible.
* Pull requests must pass build checks on all platforms before being merged. We use Travis CI and AppVeyor to run tests on Linux and Windows across multiple versions of Node.js and Python.


# Folders

## Root
Some files related to specific implementations or platforms are found in the root folder, but most are cross-project tools and configuration.

## `js`
Files related to the JavaScript implementations of the beautifiers.

## `python`
Files related to the Python implementations of the beautifiers.

## `web`
Files related to http://jsbeautifier.org/.

## `test`
Test data files and support files used to generate implementation-specific test files.


# Branches
We use the `master` branch as the primary development branch.

## Releases
Each platform has a branch that tracks to the latest release of that platform.

* `python-stable`
* `node-stable`
* `gh-pages`

## Functional Parity
Keeping the platforms in some semblance of functional parity is one of the key features of this project.  As such, there branches for the last time synchronization occurred and when it stabilized.

* `sync`
* `sync-stable`

## Attic
This project has been around for a while.  While some parts have improved significantly over time, others fell
into disrepair and were mothballed.

### PHP
There is an out-of-date version of the beautifier available on branch `attic-php`.  If you're interested
in using it feel free. If you plan to enhance it, please consider joining this project, and updating this
version to match current functionality.

### Other Languages
Versions of the beautifier adapted to other languages are at least two years out-of-date and are
available on branch `attic-other`.  Take a look and feel free to resurrect them, but know it's pretty
dusty back there.

### Generic Eval Unpacker
The `attic-genericeval` branch includes an unpacker that calls `eval` on whatever source is passed to it.
This file may be useful when working with source that unpacks itself when `eval` is called on it, but is also very unsafe.  
We have isolated it on this separate branch to keep it from hurting the other children.

# Publishing a Release
Each platform has its own release process.

NOTE: Before you do any of the following make sure the latest changes have passed the Travis CI build!

## Web
Merge changes from `master` to `gh-pages` branch.  This is very low cost and can be done whenever is convenient.

## Python
NOTE: For now, we'd like to keep Python and Node version numbers synchronized,
so if you publish a Python release, you should publish a Node release as well.

To perform these steps you will need:
1. A PyPI user account from https://pypi.python.org/pypi?%3Aaction=register_form.
2. Permissions to the jsbeautifier package.  File an issue here on GitHub and the appropriate person will help you.

We basically follow the simplest release path found at http://docs.python.org/2/distutils/packageindex.html:
```bash
git clean -xfd
# replace 0.0.1 with the actual version number you want to use
NEW_VERSION=0.0.1
echo "__version__ = '$NEW_VERSION'" > python/jsbeautifier/__version__.py
git commit -am "Python $NEW_VERSION"
cd python
python setup.py register
python setup.py sdist bdist_wininst upload
git push
```

## Node
NOTE: For now, we'd like to keep Python and Node version numbers synchronized,
so if you plan to publish a Node release, you should publish a Python release *first*,
then perform the steps below.

To perform these steps you will need:
1. An npmjs.org user account from https://npmjs.org/signup.
2. Permissions to the js-beautify module on npmjs.org.  File an issue here on GitHub and the appropriate person will help you.

NPM makes this process even simpler than Python's and also creates a tag for the release.

```bash
git clean -xfd
# replace 0.0.1 with the actual version number you want to use
NEW_VERSION=0.0.1
npm version $NEW_VERSION
npm publish .
git push --tags
```
