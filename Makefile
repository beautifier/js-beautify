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

static: $(BUILD_DIR)/node
	./node_modules/.bin/static

js: js/lib/*.js

py: python/dist/*

generate-tests: $(BUILD_DIR)/tests

jstest: depends generate-tests js
	@echo Testing javascript implementation...
	@$(NODE) --version && \
		./node_modules/.bin/mocha --recursive js/test && \
		./js/test/shell-smoke-test.sh


pytest: depends generate-tests py
	@echo Testing python implementation...
	@cd python && \
		$(PYTHON) --version && \
		./jsbeautifier/tests/shell-smoke-test.sh

beautify:
	$(SCRIPT_DIR)/build.sh beautify

# Build
#######################################################

# javascript bundle generation
js/lib/*.js: $(BUILD_DIR)/node $(wildcard js/src/**/*) tools/template/* webpack.config.js
	$(SCRIPT_DIR)/build.sh js


# python package generation
python/dist/*: $(BUILD_DIR)/python $(wildcard python/**/*.py) python/jsbeautifier/*
	@echo Building python module...
	@cd python && \
		$(PYTHON) setup.py sdist


# Test generation
$(BUILD_DIR)/tests: $(BUILD_DIR)/node test/generate-tests.js $(wildcard test/data/**/*)
	$(NODE) test/generate-tests.js
	@touch $(BUILD_DIR)/tests


# Handling dependencies
#######################################################
depends: $(BUILD_DIR)/node $(BUILD_DIR)/python

# update dependencies information
update: depends
	npm update

# when we pull dependencies also pull docker image
# without this images can get stale and out of sync from CI system
$(BUILD_DIR)/node: package.json package-lock.json | $(BUILD_DIR)
	$(NPM) install
	@touch $(BUILD_DIR)/node

$(BUILD_DIR)/python: python/setup.py
	$(PYTHON) -m pip install -e ./python
	@touch $(BUILD_DIR)/python



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

