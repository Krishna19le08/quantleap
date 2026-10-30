import gulp from 'gulp';
import cleanCSS from 'gulp-clean-css';
import terser from 'gulp-terser';
import htmlmin from 'gulp-htmlmin';
import browserSync from 'browser-sync';
import { rm } from 'node:fs/promises';

const { src, dest, series, parallel, watch } = gulp;
const server = browserSync.create();

const clean = () => rm('dist', { recursive: true, force: true });

const css = () => src('assets/css/*.css').pipe(cleanCSS()).pipe(dest('dist/assets/css'));

const js = () =>
  src('assets/js/*.js')
    .pipe(
      terser({
        toplevel: true,
        mangle: { toplevel: true },
        compress: { drop_console: true },
        format: { comments: false },
      }),
    )
    .pipe(dest('dist/assets/js'));

const htmlOpts = { collapseWhitespace: true, removeComments: true, minifyCSS: true, minifyJS: true };
const html = () =>
  src(['index.html', 'components/**/*.html'], { base: '.' })
    .pipe(htmlmin(htmlOpts))
    .pipe(dest('dist'));

// everything that needs no processing is copied as is
const copy = () =>
  src(['assets/fonts/**', 'assets/images/**', 'assets/lib/**'], {
    base: '.',
    encoding: false,
    allowEmpty: true,
  }).pipe(dest('dist'));

// dev server serves the sources directly, no build step needed
const serve = (done) => {
  server.init({ server: '.', open: false, notify: false });
  done();
};
const reload = (done) => {
  server.reload();
  done();
};
const watcher = () => {
  watch(['index.html', 'components/**/*.html', 'assets/js/*.js'], reload);
  watch('assets/css/*.css', () => src('assets/css/*.css').pipe(server.stream()));
};

export const build = series(clean, parallel(css, js, html, copy));
export const dev = series(serve, watcher);
export default dev;
