'use strict';

var assert = require('assert');
var fs = require('fs');
var path = require('path');
var vm = require('vm');

function createElementStub() {
  var state = {
    focused: false,
    selected: false
  };

  var api = {
    val: function(value) {
      if (arguments.length > 0) {
        state.value = value;
        return api;
      }
      return state.value;
    },
    prop: function(name, value) {
      if (arguments.length > 1) {
        state[name] = value;
        return api;
      }
      return state[name];
    },
    text: function(value) {
      if (arguments.length > 0) {
        state.text = value;
        return api;
      }
      return state.text;
    },
    html: function(value) {
      if (arguments.length > 0) {
        state.html = value;
        return api;
      }
      return state.html;
    },
    attr: function(name, value) {
      if (arguments.length > 1) {
        state[name] = value;
        return api;
      }
      return state[name];
    },
    addClass: function(className) {
      state.classes = state.classes || [];
      state.classes.push(className);
      return api;
    },
    removeClass: function(className) {
      state.removedClasses = state.removedClasses || [];
      state.removedClasses.push(className);
      return api;
    },
    children: function() {
      return api;
    },
    bind: function() {
      return api;
    },
    change: function() {
      return api;
    },
    click: function() {
      return api;
    },
    show: function() {
      state.hidden = false;
      return api;
    },
    hide: function() {
      state.hidden = true;
      return api;
    },
    select: function() {
      state.selected = true;
      return api;
    },
    focus: function() {
      state.focused = true;
      return api;
    },
    remove: function() {
      state.removed = true;
      return api;
    },
    append: function() {
      return api;
    },
    valState: state
  };

  return api;
}

function createContext() {
  var elements = {};
  var cookies = {};

  function getElement(selector) {
    if (!elements[selector]) {
      elements[selector] = createElementStub();
    }
    return elements[selector];
  }

  var windowObject = {
    location: {
      href: 'http://localhost/'
    },
    navigator: {
      platform: ''
    },
    screen: {
      orientation: {
        lock: function() {}
      }
    },
    open: function() {
      return {
        focus: function() {}
      };
    },
    matchMedia: function() {
      return {
        matches: false
      };
    }
  };

  var context = {
    console: console,
    window: windowObject,
    document: {
      querySelector: function() {
        return null;
      },
      createElement: function() {
        return {
          style: {},
          click: function() {},
          setAttribute: function() {},
          remove: function() {}
        };
      },
      execCommand: function() {
        return true;
      },
      body: {
        appendChild: function() {}
      }
    },
    Cookies: {
      get: function(name) {
        return cookies[name];
      },
      set: function(name, value) {
        cookies[name] = value;
      }
    },
    requirejs: function(deps, callback) {
      if (typeof deps === 'function') {
        deps();
        return;
      }
      if (typeof callback === 'function') {
        callback({});
      }
    },
    $: function(selector) {
      if (typeof selector === 'function') {
        selector();
        return;
      }
      return getElement(selector);
    },
    _elements: elements,
    _cookies: cookies
  };

  context.requirejs.config = function() {};

  return context;
}

function loadWebCommonFunctions() {
  var context = createContext();
  var source = fs.readFileSync(path.join(__dirname, '../../web/common-function.js'), 'utf8');
  vm.runInNewContext(source, context, {
    filename: 'web/common-function.js'
  });
  return context;
}

describe('web/common-function.js', function() {
  it('hydrates the UI from stored cookie values', function() {
    var context = loadWebCommonFunctions();

    context._cookies.tabsize = '2';
    context._cookies['brace-style'] = 'expand';
    context._cookies['wrap-line-length'] = '80';
    context._cookies['unescape-strings'] = 'on';
    context._cookies.language = 'html';

    context.read_settings_from_cookie();

    assert.strictEqual(context._elements['#tabsize'].val(), '2');
    assert.strictEqual(context._elements['#brace-style'].val(), 'expand');
    assert.strictEqual(context._elements['#wrap-line-length'].val(), '80');
    assert.strictEqual(context._elements['#unescape-strings'].prop('checked'), true);
    assert.strictEqual(context._elements['#language'].val(), 'html');
  });

  it('clears the CodeMirror editor and restores focus', function() {
    var context = loadWebCommonFunctions();
    var calls = [];

    context.the.editor = {
      setValue: function(value) {
        calls.push(['setValue', value]);
      },
      focus: function() {
        calls.push(['focus']);
      }
    };

    context.clearAll();

    assert.deepStrictEqual(calls, [
      ['setValue', ''],
      ['focus']
    ]);
  });

  it('clears the textarea and restores focus when CodeMirror is not active', function() {
    var context = loadWebCommonFunctions();
    var source = context.$('#source');

    context.the.editor = null;

    context.clearAll();

    assert.strictEqual(source.val(), '');
    assert.strictEqual(source.prop('focused'), true);
  });
});
