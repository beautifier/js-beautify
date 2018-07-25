PROJECT_ROOT=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))
BUILD_DIR=$(PROJECT_ROOT)build
SCRIPT_DIR=$(PROJECT_ROOT)tools
SHELL=/bin/bash
PYTHON=$(SCRIPT_DIR)/python
NODE=$(SCRIPT_DIR)/node
NPM=$(SCRIPT_DIR)/npm

all: depends js jstest py pytest beautify

help:
	@echo "make <action>"
	@echo "    all       - build both implementations"
	@echo "    static    - serve static version of site locally"
	@echo "    js        - build javascript"
	@echo "    py        - build python"
	@echo "    alltest   - test both implementations, js and python"
	@echo "    pytest    - test python implementation"
	@echo "    jstest    - test javascript implementation"

ci: all git-status-clear

static: js/lib/*.js
	@./node_modules/.bin/static -H '{"Cache-Control": "no-cache, must-revalidate"}'

js: js/lib/*.js
	@echo Running unit tests...
	./node_modules/.bin/mocha --recursive js/test && \
	./js/test/node-src-index-tests.js

py: python/dist/*

jstest: depends generate-tests js
	@echo Testing javascript implementation...
	@$(NODE) --version && \
		./js/test/shell-smoke-test.sh

pytest: depends generate-tests py
	@echo Testing python implementation...
	@cd python && \
		$(PYTHON) --version && \
		./jsbeautifier/tests/shell-smoke-test.sh

generate-tests: $(BUILD_DIR)/generate

beautify:
	$(SCRIPT_DIR)/build.sh beautify

# Build
#######################################################

# javascript bundle generation
js/lib/*.js: $(BUILD_DIR)/node $(BUILD_DIR)/generate $(wildcard js/src/**/*) js/index.js tools/template/* webpack.config.js
	$(SCRIPT_DIR)/build.sh js
	$(NPM) pack && mv *.tgz build/
	mkdir -p build/node_modules
	rm -rf node_modules/js-beautify
	cd build && \
		$(NPM) install ./*.tgz


# python package generation
python/dist/*: $(BUILD_DIR)/python $(wildcard python/**/*.py) python/jsbeautifier/*
	@echo Building python module...
	rm -f python/dist/*
	@cd python && \
		$(PYTHON) setup.py sdist
	./build/python-rel/bin/pip install -U python/dist/*

# Test generation
$(BUILD_DIR)/generate: $(BUILD_DIR)/node test/generate-tests.js $(wildcard test/data/**/*)
	$(NODE) test/generate-tests.js
	@touch $(BUILD_DIR)/generate


# Handling dependencies
#######################################################
depends: $(BUILD_DIR)/node $(BUILD_DIR)/python
	@$(NODE) --version
	@$(PYTHON) --version

# update dependencies information
update: depends
	npm update

# when we pull dependencies also pull docker image
# without this images can get stale and out of sync from CI system
$(BUILD_DIR)/node: package.json package-lock.json | $(BUILD_DIR)
	@$(NODE) --version
	$(NPM) install
	@touch $(BUILD_DIR)/node

$(BUILD_DIR)/python: python/setup.py | $(BUILD_DIR) $(BUILD_DIR)/virtualenv
	@$(PYTHON) --version
	./build/python-dev/bin/pip install -e ./python
	@touch $(BUILD_DIR)/python

$(BUILD_DIR)/virtualenv: | $(BUILD_DIR)
	virtualenv --version || pip install virtualenv
	virtualenv build/python-dev
	virtualenv build/python-rel
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

.PHONY: all beautify clean depends generate-tests git-status-clear help static update

