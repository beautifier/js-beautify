
define AVAILABLE_ACTIONS

build:		do static checking and build of js
buildp:		do static checking and build of python
buildj:		do static checking and build of javascript
test:		test both implementations, js and python
testp:		test python implementation
testj:		test javascript implementation

endef
export AVAILABLE_ACTIONS


.SILENT:
all: build test

help:
	echo "$$AVAILABLE_ACTIONS"

build: buildj buildp

buildj:
	echo Building javascript... ;\
	npm install ;\

buildp:
	echo Building python... ;\
	pip install -e ./python 
	
testp:
	echo Testing python implementation...
	cd python ;\
	python --version ;\
	./jsbeautifier/tests/shell-smoke-test.sh

testj:
	echo Testing javascript implementation...
	node --version; \
	npm test


edit:
	vim \
		js/lib/beautify.js python/jsbeautifier/__init__.py \
		js/test/beautify-tests.js python/jsbeautifier/tests/testjsbeautifier.py

gedit:
	gvim \
		js/lib/beautify.js \
		js/test/beautify-tests.js \
		python/jsbeautifier/__init__.py \
		python/jsbeautifier/tests/testjsbeautifier.py &

tests: testj testp

test: testj testp

gh:
	git push origin master &&\
	cd gh-pages &&\
	git fetch &&\
	git checkout gh-pages &&\
	git reset --hard origin/gh-pages &&\
	git merge origin/master &&\
	git push origin gh-pages

.PHONY: testp testj all edit tests test
