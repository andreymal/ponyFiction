'use strict'
_ = require 'lodash'
gulp = require 'gulp'
browserify = require 'browserify'
es = require 'event-stream'
buffer = require 'vinyl-buffer'
source = require 'vinyl-source-stream'
resolve = require 'resolve'
stylus = require 'gulp-stylus'
uglify = require 'gulp-uglify'
rename = require 'gulp-rename'
del = require 'del'
path = require 'path'
glob = require 'glob'

pkginfo = require './package.json'
packages = _.keys(pkginfo.dependencies) or []

debug = process.env.NODE_ENV != 'production'


gulp.task 'build:scripts', ['build:scripts:vendor', 'build:scripts:app']
gulp.task 'default', ['build:scripts', 'build:styles']

gulp.task 'build:scripts:vendor', ->
  b = browserify debug: debug
  packages.forEach (id) -> b.require resolve.sync(id), expose: id

  b.bundle()
    .pipe source 'vendor.js'
    .pipe buffer()
    .pipe if debug then uglify() else gutil.noop()
    .pipe gulp.dest pkginfo.dist


gulp.task 'build:scripts:app', (done) ->
  glob pkginfo.js.entries, (err, files) ->
    if err then done err

    tasks = files.map (file) ->
      b = browserify debug: debug, entries: [file]
      packages.forEach (id) -> b.external resolve.sync(id), expose: id

      b.bundle()
        .pipe source path.basename file
        .pipe rename extname: '.bundle.js'
        .pipe buffer()
        .pipe if debug then uglify() else gutil.noop()
        .pipe gulp.dest pkginfo.dist

    es.merge(tasks).on 'end', done

gulp.task 'build:styles', ->
  gulp.src pkginfo.css.entries
    .pipe stylus
      compress: true,
      'include css': true,
      include: pkginfo.css.includes
    .pipe rename 'bundle.css'
    .pipe gulp.dest pkginfo.dist

gulp.task 'watch', ['build'], ->
  gulp.watch pkginfo.js.watches, ['build:scripts:app']
  gulp.watch pkginfo.css.watches, ['build:stylesheets']

gulp.task 'clean', (cb) ->
  del ['#{pkginfo.dist}/*', '!.gitignore'], cb
