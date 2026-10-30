import gulp from 'gulp';
import cleanCSS from 'gulp-clean-css';
import terser from 'gulp-terser';
import htmlmin from 'gulp-htmlmin';
import concat from 'gulp-concat';
import replace from 'gulp-replace';
import obfuscator from 'gulp-javascript-obfuscator';
import browserSync from 'browser-sync';
import { rm } from 'node:fs/promises';

const { src, dest, series, parallel, watch } = gulp;
const server = browserSync.create();

// the production build obfuscates the JS (conservative settings) on top of minifying it; OBFUSCATE=0 npm run build skips that
const obfuscate = process.env.OBFUSCATE !== '0';

const clean = async () => {
  await rm('dist', { recursive: true, force: true });
  // only the generated bundles, so anything else you keep in assets/dist survives
  await rm('assets/dist/css', { recursive: true, force: true });
  await rm('assets/dist/js', { recursive: true, force: true });
};

// fonts.css first, then stylesheet.css; its @import is dropped because fonts.css is already in the bundle
const css = () =>
  src(['assets/css/fonts.css', 'assets/css/stylesheet.css'])
    .pipe(replace(/url\((['"]?)\.\.\/(fonts|images)\//g, 'url($1../../$2/')) // bundle lives one level deeper (assets/dist/css)
    .pipe(replace(/@import\s+url\(["']?fonts\.css["']?\);?/g, ''))
    .pipe(concat('styles.min.css'))
    .pipe(cleanCSS())
    .pipe(dest('assets/dist/css'));

const js = () => {
  let stream = src('assets/js/script.js').pipe(
    terser({ toplevel: true, mangle: { toplevel: true }, format: { comments: false } }),
  );
  if (obfuscate) {
    stream = stream.pipe(
      obfuscator({
        compact: true,
        stringArray: true,
        stringArrayThreshold: 0.5,
        controlFlowFlattening: false,
        deadCodeInjection: false,
        selfDefending: false,
        debugProtection: false,
      }),
    );
  }
  return stream.pipe(concat('script.min.js')).pipe(dest('assets/dist/js'));
};

// production HTML points at the minified bundles, never at the originals
const stamp = Date.now().toString(36); // new cache-busting version on every build
const html = () =>
  src(['index.html', 'components/**/*.html'], { base: '.' })
    .pipe(replace(/<link rel="stylesheet" href="assets\/css\/fonts\.css[^"]*">\s*/g, ''))
    .pipe(replace(/assets\/css\/stylesheet\.css\?v=[\d.]+/g, 'assets/dist/css/styles.min.css?v=' + stamp))
    .pipe(replace(/assets\/js\/script\.js\?v=[\d.]+/g, 'assets/dist/js/script.min.js?v=' + stamp))
    .pipe(htmlmin({ collapseWhitespace: true, removeComments: true, minifyCSS: true, minifyJS: true }))
    .pipe(dest('dist'));

// the minified bundles are built into assets/dist and copied into the deployable dist/
const bundles = () => src('assets/dist/**', { base: '.' }).pipe(dest('dist'));

// images and fonts are copied untouched so the design cannot change
const images = () => src('assets/images/**', { base: '.', encoding: false }).pipe(dest('dist'));
const fonts = () => src('assets/fonts/**', { base: '.', encoding: false }).pipe(dest('dist'));
const lib = () => src('assets/lib/**', { base: '.', encoding: false, allowEmpty: true }).pipe(dest('dist'));

// development: serves the readable sources directly with live reload
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

export { clean, css, js, html, images, fonts };
export const build = series(clean, parallel(css, js), parallel(bundles, html, images, fonts, lib));
export const dev = series(serve, watcher);
export default dev;
