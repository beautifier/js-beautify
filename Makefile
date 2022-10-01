PROJECT_ROOT=$(subst \,/,$(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
BUILD_DIR=$(PROJECT_ROOT)build
SCRIPT_DIR=$(PROJECT_ROOT)tools
SHELL=/bin/bash
PYTHON=$(SCRIPT_DIR)/python
NODE=$(SCRIPT_DIR)/node
NPM=$(SCRIPT_DIR)/npm

all: depends generate-tests js beautify py package jstest pytest perf

help:
	@echo "make <action>"
	@echo "    all       - build both implementations"
	@echo "    serve    - serve site locally from localhost:8080"
	@echo "    js        - build javascript"
	@echo "    py        - build python"
	@echo "    alltest   - test both implementations, js and python"
	@echo "    pytest    - test python implementation"
	@echo "    jstest    - test javascript implementation"

ci: all git-status-clear

serve: js/lib/*.js
	@./node_modules/.bin/serve

js: generate-tests js/lib/*.js
	@echo Testing node beautify functionality...
	./node_modules/.bin/mocha --recursive js/test && \
		./js/test/node-src-index-tests.js

py: generate-tests $(BUILD_DIR)/python
	@echo Testing python beautify functionality...
	$(SCRIPT_DIR)/python-dev3 black --config=python/pyproject.toml python
	$(SCRIPT_DIR)/python-dev python python/js-beautify-test.py || exit 1

jstest: depends js build/*.tgz
	@echo Testing javascript implementation...
	@$(NODE) js/test/node-beautify-tests.js || exit 1
	@$(NODE) js/test/amd-beautify-tests.js || exit 1
	@$(NODE) --version && \
		./js/test/shell-test.sh

pytest: depends py python/dist/*
	@echo Testing python implementation...
	@cd python && \
		$(PYTHON) --version && \
		./jsbeautifier/tests/shell-test.sh

alltest: jstest pytest

package: js py build/*.tgz python/dist/*


perf:
	@echo ----------------------------------------
	@echo Testing node js beautify performance...
	$(NODE) js/test/node-beautify-perf-tests.js || exit 1
	@echo Testing node css beautify performance...
	$(NODE) js/test/node-beautify-css-perf-tests.js || exit 1
	@echo Testing html-beautify performance...
	$(NODE) js/test/node-beautify-html-perf-tests.js || exit 1
	@echo Testing python js beautify performance...
	$(SCRIPT_DIR)/python-dev python python/test-perf-jsbeautifier.py || exit 1
	@echo Testing python css beautify performance...
	$(SCRIPT_DIR)/python-dev python python/test-perf-cssbeautifier.py || exit 1
	@echo ----------------------------------------

generate-tests: $(BUILD_DIR)/generate

beautify:
	$(SCRIPT_DIR)/build.sh beautify

# Build
#######################################################

# javascript bundle generation
js/lib/*.js: $(BUILD_DIR)/node $(BUILD_DIR)/generate $(wildcard js/src/*) $(wildcard js/src/**/*) $(wildcard web/*.js) js/index.js tools/template/* webpack.config.js
	$(SCRIPT_DIR)/build.sh js


# python package generation
python/dist/*: $(BUILD_DIR)/python $(BUILD_DIR)/generate $(wildcard python/**/*.py) python/jsbeautifier/* python/cssbeautifier/*
	@echo Building python package...
	@rm -f python/dist/*
	@cd python && \
		cp setup-css.py setup.py && \
		$(PYTHON) setup.py sdist && \
		rm setup.py
	@cd python && \
		cp setup-js.py setup.py && \
		$(PYTHON) setup.py sdist && \
		rm setup.py
	# Order matters here! Install css then js to make sure the local dist version of js is used
	$(SCRIPT_DIR)/python-rel pip install -U python/dist/cssbeautifier*
	$(SCRIPT_DIR)/python-rel pip install -U python/dist/jsbeautifier*

# python package generation
build/*.tgz: js/lib/*.js
	@echo Building node package...
	mkdir -p build/node_modules
	rm -f build/*.tgz
	rm -rf node_modules/js-beautify
	$(NPM) pack && mv *.tgz build/
	cd build && \
		$(NPM) install ./*.tgz

# Test generation
$(BUILD_DIR)/generate: $(BUILD_DIR)/node test/generate-tests.js $(wildcard test/data/**/*)
	@echo Generating tests...
	$(NODE) test/generate-tests.js
	@touch $(BUILD_DIR)/generate


# Handling dependencies
#######################################################
depends: $(BUILD_DIR)/node $(BUILD_DIR)/python
	@$(NODE) --version
	@$(PYTHON) --version

# update dependencies information
update: depends
	@rm package-lock.json
	$(NPM) update --save

# when we pull dependencies also pull docker image
# without this images can get stale and out of sync from CI system
$(BUILD_DIR)/node: package.json package-lock.json | $(BUILD_DIR)
	@$(NODE) --version
	$(NPM) --version
	$(NPM) install 
	@touch $(BUILD_DIR)/node

$(BUILD_DIR)/python: $(BUILD_DIR)/generate python/setup-js.py python/setup-css.py | $(BUILD_DIR) $(BUILD_DIR)/virtualenv
	@$(PYTHON) --version
	# Order matters here! Install css then js to make sure the local dist version of js is used
	@cp ./python/setup-css.py ./python/setup.py
	$(SCRIPT_DIR)/python-dev pip install -e ./python
	@cp ./python/setup-js.py ./python/setup.py
	$(SCRIPT_DIR)/python-dev pip install -e ./python
	@rm ./python/setup.py
	@touch $(BUILD_DIR)/python

$(BUILD_DIR)/virtualenv: | $(BUILD_DIR)
	virtualenv --version || pip install virtualenv
	virtualenv build/python-dev
	virtualenv build/python-rel
	$(SCRIPT_DIR)/python-dev python -m pip install --upgrade pip || exit 0
	$(SCRIPT_DIR)/python-rel python -m pip install --upgrade pip || exit 0
	$(SCRIPT_DIR)/python-dev3 pip install black
	@touch $(BUILD_DIR)/virtualenv



# Miscellaneous tasks
#######################################################
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

git-status-clear:
	$(SCRIPT_DIR)/git-status-clear.sh

clean:
	git clean -xfd
#######################################################

.PHONY: all beautify clean depends generate-tests git-status-clear help serve update

