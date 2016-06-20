var gulp = require('gulp');
var gutil = require('gulp-util');
var csslint = require('gulp-csslint');
var cleanCss = require('gulp-clean-css');
var less = require('gulp-less');
var prefix = require('gulp-autoprefixer');
var path = require('path');

var DEBUG = process.env.NODE_ENV != "production";


gulp.task('images:copy', function () {
    gulp.src('assets/images/**')
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

gulp.task('scripts:compile', function () {
    // Simple copy by now
    gulp.src('assets/scripts/**')
        .pipe(gulp.dest('static/scripts'));
});


gulp.task('assets:dev', ['images:copy', 'fonts:copy', 'styles:compile', 'scripts:compile']);

gulp.task('assets', ['images:copy', 'fonts:copy', 'styles:compile', 'scripts:compile']);

gulp.task('watch', function () {
    gulp.watch(
        [
            'assets/styles/**/*.css',  // Until conversion of all legacy CSS files
            'assets/scripts/*.js',  // Until conversion of all legacy JSS files
            'assets/styles/**/*.less',
            'assets/fonts/*',
            'assets/images/**/*'
        ],
        ['assets:dev']
    );
});

