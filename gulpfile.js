var gulp = require('gulp');
var gutil = require('gulp-util');
var csslint = require('gulp-csslint');
var cleanCss = require('gulp-clean-css');
var imagemin = require('gulp-imagemin');
var pngcrush = require('imagemin-pngcrush');
var less = require('gulp-less');
var prefix = require('gulp-autoprefixer');
var path = require('path');

var DEBUG = process.env.NODE_ENV != "production";


gulp.task('images:copy', function () {
    gulp.src('assets/images/**')
        .pipe(gulp.dest('static/images'));
});

gulp.task('images:optimize', function () {
    gulp.src('assets/images/**')
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{
                removeViewBox: false
            }],
            use: [pngcrush()]
        }))
        .pipe(gulp.dest('static/images'));
});

gulp.task('fonts:copy', function () {
    gulp.src('assets/fonts/**')
        .pipe(gulp.dest('static/fonts'));
});

gulp.task('styles:lint', function () {
    gulp.src(['static/styles/*.css'])
        .pipe(prefix('last 3 version', '> 1%', {cascade: true}))
        .pipe(csslint('.csslintrc'))
        .pipe(csslint.reporter());
});

gulp.task('styles:compile', function () {
    gulp.src('assets/styles/*.less')
        .pipe(less({
            paths: [
                './assets/styles',
                '/usr/lib/node_modules',
                process.env.NODE_PATH
            ]
        }))
        .pipe(DEBUG ? gutil.noop() : cleanCss())
        .pipe(gulp.dest('static/styles/'));
});

gulp.task('assets:dev', ['images:copy', 'fonts:copy', 'styles:compile']);

gulp.task('assets:production', ['images:optimize', 'fonts:copy', 'styles:compile']);

gulp.task('watch', function () {
    gulp.watch(['assets/styles/**/*.less', 'assets/fonts/*', 'assets/images/**/*'], ['assets:dev']);
});

