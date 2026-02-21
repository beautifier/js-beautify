#!/usr/bin/env node

'use strict';

// jshint expects legacy minimatch CJS shape (callable export). Newer minimatch
// versions export an object with `minimatch`, so normalize it just for jshint.
const Module = require('module');
const originalLoad = Module._load;

Module._load = function patchedLoad(request, parent, isMain) {
  if (request === 'minimatch') {
    const loaded = originalLoad.call(this, request, parent, isMain);

    if (typeof loaded === 'function') {
      return loaded;
    }

    if (loaded && typeof loaded.minimatch === 'function') {
      const compat = loaded.minimatch;
      Object.assign(compat, loaded);
      return compat;
    }

    return loaded;
  }

  return originalLoad.call(this, request, parent, isMain);
};

require('jshint/src/cli.js').interpret(process.argv);
