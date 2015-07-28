'use strict'
_ = require 'lodash'
fs = require 'fs'
gulp = require 'gulp'
browserify = require 'browserify'
source = require 'vinyl-source-stream'
bowerResolve = require 'bower-resolve'
stylus = require 'gulp-stylus'
rename = require 'gulp-rename'
del = require 'del'

pkginfo = require './package.json'
bowerinfo = require './bower.json'
bowerPackages = _.keys(bowerinfo.dependencies) or []

production = process.env.NODE_ENV == 'production'


gulp.task 'build:scripts', ['build:scripts:vendor', 'build:scripts:app']
gulp.task 'default', ['build:scripts', 'build:styles']

gulp.task 'build:scripts:vendor', ->
  b = browserify debug: !production
  bowerPackages.forEach (id) -> b.require bowerResolve.fastReadSync(id), expose: id

  b.bundle()
    .pipe source 'vendor.js'
    .pipe gulp.dest pkginfo.dist

gulp.task 'build:scripts:app', ->
  b = browserify pkginfo.js.entries, debug: !production
  bowerPackages.forEach (lib) -> b.external lib

  b.bundle()
    .pipe source 'app.js'
    .pipe gulp.dest pkginfo.dist

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
