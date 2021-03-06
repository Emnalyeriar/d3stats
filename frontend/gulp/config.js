'use strict';

export default {

  browserPort: 3000,
  UIPort: 3001,

  sourceDir: './app/',
  buildDir: '../static/d3stats/',
  templatesDir: '../templates/',

  styles: {
    src: 'app/styles/**/*.scss',
    dest: '../static/d3stats/css',
    prodSourcemap: false,
    sassIncludePaths: []
  },

  scripts: {
    src: 'app/js/**/*.js',
    dest: '../static/d3stats/js'
  },

  images: {
    src: 'app/images/**/*',
    dest: '../static/d3stats/images'
  },

  fonts: {
    src: ['app/fonts/**/*'],
    dest: '../static/d3stats/fonts'
  },

  views: {
    index: 'app/index.html',
    src: 'app/views/**/*.html',
    dest: 'app/js'
  },

  gzip: {
    src: '../static/d3stats/**/*.{html,xml,json,css,js,js.map,css.map}',
    dest: '../static/d3stats/',
    options: {}
  },

  browserify: {
    bundleName: 'main.js',
    prodSourcemap: false
  },

  test: {
    karma: 'test/karma.conf.js',
    protractor: 'test/protractor.conf.js'
  },

  init: function() {
    this.views.watch = [
      this.views.index,
      this.views.src
    ];

    return this;
  }

}.init();
