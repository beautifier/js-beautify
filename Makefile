
define AVAILABLE_ACTIONS

test:		test both implementations, js and python
testp:		test python implementation
testj:		test javascript implementation

endef
export AVAILABLE_ACTIONS


.SILENT:

all:
	echo "$$AVAILABLE_ACTIONS"

testp:
	cd python ;\
	echo Testing python3 ;\
	PYTHON=python3 ./js-beautify-test ;\
	echo Testing python2 ;\
	PYTHON=python2 ./js-beautify-test
	echo

testj:
	echo Testing javascript implementation...
	./tests/run-tests
	echo

edit:
	vim \
		beautify.js python/jsbeautifier/__init__.py \
		tests/beautify-tests.js python/jsbeautifier/tests/testjsbeautifier.py

gedit:
	gvim \
		beautify.js \
		tests/beautify-tests.js \
		python/jsbeautifier/__init__.py \
		python/jsbeautifier/tests/testjsbeautifier.py &

tests: testj testp

test: testj testp

gh:
	git push origin master &&\
	cd gh-pages &&\
	git pull origin master &&\
	git merge master &&\
	git push origin gh-pages

.PHONY: testp testj all edit tests test
