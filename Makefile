
define AVAILABLE_ACTIONS

publish:	publish jsbeautifier to github.com and sync
test:		test both implementations, js and python
testp:		test python implementation
testj:		test javascript implementation

endef
export AVAILABLE_ACTIONS


define SCRIPT_PUBLISH

open spic
cd jsbeautifier.org
mirror -Rv attic
mirror -Rv jquery
mirror -Rv tests
mirror -Rv unpackers
mirror -Rv python
put beautify-css.js beautify-html.js beautify.js index.html license.txt README.md

endef
export SCRIPT_PUBLISH


.SILENT:

all:
	echo "$$AVAILABLE_ACTIONS"

publish:
	git push
	lftp -c "$$SCRIPT_PUBLISH"

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

tests: testj testp

test: testj testp

.PHONY: testp testj all publish edit tests test
