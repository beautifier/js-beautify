
define AVAILABLE_ACTIONS

build:		do static checking and build of js
test:		test both implementations, js and python
testp:		test python implementation
testj:		test javascript implementation

endef
export AVAILABLE_ACTIONS


.SILENT:
all: build test

help:
	echo "$$AVAILABLE_ACTIONS"

build:
	echo Building... ;\
	npm install ;\

testp:
	echo Testing python implementation...
	cd python ;\
	python --version ;\
	./jsbeautifier/tests/shell-smoke-test.sh && \
	PYTHON=python ./js-beautify-test

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
	git pull origin gh-pages &&\
	git pull origin master &&\
	git merge master &&\
	git push origin gh-pages

.PHONY: testp testj all edit tests test
