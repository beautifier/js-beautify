var path = require('path');

var legacy = {
  mode: 'none',
  entry: {
    beautify_js: './js/src/javascript/index.js',
    beautify_css: './js/src/css/index.js',
    beautify_html: './js/src/html/index.js'
  },
  resolve: {
    modules: [ path.resolve(__dirname, "js/src") ]
  },
  output: {
    library: 'legacy_[name]',
    filename: 'legacy_[name].js',
    path: path.resolve(__dirname, 'build/legacy')
  }
};

var dist_full = {
  entry: './js/src/index.js',
  mode: 'none',
  resolve: {
    modules: [ path.resolve(__dirname, "js/src") ]
  },
  devtool: 'source-map',
  output: {
    library: 'beautifier',
    libraryTarget: 'umd',
    umdNamedDefine: true,
    filename: 'beautifier.js',
    path: path.resolve(__dirname, 'js/lib'),
    // Workaround for https://github.com/webpack/webpack/issues/6525
    globalObject: "typeof self !== 'undefined' ? self : typeof windows !== 'undefined' ? window : typeof global !== 'undefined' ? global : this"
  }
};

var dist_prod = {
  entry: './js/src/index.js',
  mode: 'production',
  resolve: {
    modules: [ path.resolve(__dirname, "js/src") ]
  },
  devtool: 'source-map',
  output: {
    library: 'beautifier',
    libraryTarget: 'umd',
    umdNamedDefine: true,
    filename: 'beautifier.min.js',
    path: path.resolve(__dirname, 'js/lib'),
    // Workaround for https://github.com/webpack/webpack/issues/6525
    globalObject: "typeof self !== 'undefined' ? self : typeof windows !== 'undefined' ? window : typeof global !== 'undefined' ? global : this"
  }
};


module.exports = [dist_full, dist_prod, legacy];
