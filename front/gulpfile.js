var gulp = require('gulp');
var cssnano = require('gulp-cssnano');  // css 文件压缩
var sass = require('gulp-sass');// 将scss文件转换为css文件
var rename = require('gulp-rename');    // 文件重命名
var uglify = require('gulp-uglify');    // js文件压缩
var concat = require('gulp-concat');  // 合并多个文件
var cache = require('gulp-cache');     // 图片文件缓存
var imagemin = require('gulp-imagemin');  // 图片压缩
var util = require('gulp-util');        // Js 文件出错打印错误信息，不停止gulp
var sourcemaps = require('gulp-sourcemaps');
var bs = require('browser-sync').create();  // 浏览器自动刷新脚本


var path = {
    'html':'./templates/**/',
    'css':'./src/css/**/',
    'js':'./src/js/**/',
    'images':'./src/images/**/',
    'css_dist':'./dist/css/',
    'js_dist':'./dist/js/',
    'images_dist':'./dist/images/'
};

// css 文件处理任务
gulp.task('css',function () {
    gulp.src(path.css+'*.scss')
        .pipe(sass().on('error',sass.logError))
        .pipe(cssnano())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});

// js 文件处理任务
gulp.task('js',function () {
   gulp.src(path.js+'*.js')
       .pipe(sourcemaps.init())
       .pipe(uglify().on('error',util.log))
       .pipe(rename({'suffix':'.min'}))
       .pipe(sourcemaps.write())
       .pipe(gulp.dest(path.js_dist))
       .pipe(bs.stream())
});

// 图片压缩和缓存的任务
gulp.task('img',function () {
   gulp.src(path.images+'*.*')
       .pipe(cache(imagemin()))
       .pipe(gulp.dest(path.images_dist))
       .pipe(bs.stream())
});

// 监听html文件的修改
gulp.task('html',function () {
    gulp.src(path.html+'*.html')
        .pipe(bs.stream())
});

// 监听事任务watch
gulp.task('watch',function () {
    gulp.watch(path.css+'*.scss',['css']);
    gulp.watch(path.js+'*.js',['js']);
    gulp.watch(path.images+'*.*',['img']);
    gulp.watch(path.html+'*.html',['html'])
});

// server配置
gulp.task('bs',function () {
   bs.init({
       'server':{
           'baseDir':'./'
       }
   })
});

// 执行gulp server 启动服务器,default参数，可以直接使用gulp命令启动服务器
// gulp.task('default',['bs','watch']);
gulp.task('default',['watch']);