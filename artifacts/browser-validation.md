# Browser validation (functional)

Tooling: playwright-cli was NOT available, so Python Playwright (Chromium, headless) was used.
Script: `artifacts/tools/functional.py` (starts its own `http.server` on port 8791, serves D:\projects\quantleap, no source edited). Raw results: `artifacts/tools/functional-results.json`.
Run: 60 checks, 51 passed, 9 failed. Page: `index.html` with components loaded via fetch.

## Viewports
- Overflow: 320, 390, 517, 820, 1024, 1440.
- Console/network/images: 390, 517, 1440 (page scrolled top to bottom to trigger lazy images).
- Nav, modal, hero CTAs, link audit, focus-visible: 1440. Mobile menu: 390x844. Carousel: 1440 and 390.

## Results

PASS
- All 11 `#nav` links have hrefs resolving to existing ids (#top, #focus, #ventures, #nation, #insights, #presence, #contact). All `#` anchors on the page resolve.
- Clicking each nav link scrolls its target to ~72px below the viewport top (sticky header offset). "Contact" cannot reach the top because it is at the page bottom (target top = 278px at max scroll). Counted as pass.
- Mobile menu (390): starts closed with aria-expanded=false. The burger opens it (aria-expanded=true) and closes it again. A nav link click closes the menu, aria-expanded returns to false, and the page scrolls to the target.
- Modal: hidden initially. "Watch Our Story" opens it without changing the URL hash, and focus moves to the close button. The close button, Escape and a backdrop click all close it. A click inside the box does not close it.
- Hero CTAs: "Explore Our Ventures" -> #ventures, "Watch Our Story" -> #story with a modal handler. Both have real hrefs.
- Tab focus-visible: 44 consecutive Tab stops at 1440, every visible focused element had a non-none computed outline or box-shadow.
- No horizontal overflow at 390, 517, 820, 1024, 1440.
- Console errors/warnings: none at 390, 517, 1440. Failed requests / HTTP >= 400: none. All 29 `<img>` loaded (naturalWidth > 0) at each of the three widths.

FAIL
1. Mobile menu does not close on Escape. `script.js` has no Escape handling for the nav, so the menu stays open and aria-expanded stays "true".
2. Modal focus is not trapped. After opening and pressing Tab twice, focus lands on `A.logo` behind the dialog, although it has `aria-modal="true"`.
3. Modal does not return focus to the trigger on close. After close, `document.activeElement` is BODY, not the `.watch` link.
4. Carousel arrows at 1440 do nothing. The track has scrollWidth = clientWidth = 1280 (the 5 cards fit), so next and prev leave scrollLeft at 0. The arrows are visible but dead on desktop.
5. Carousel arrows are `display:none` at 390 (CSS line 265). The track is scrollable (scrollWidth 1460 vs clientWidth 358) by swipe only, so the arrow buttons could not be tested there.
6. Horizontal overflow at 320px: documentElement/body scrollWidth is 321 vs 320 (1px). No individual offending element was found by the script, which excluded the carousel and `#nav`.
7. Dead links: 7 footer links have `href="#"` (LinkedIn, X, YouTube, Instagram, Privacy Policy, Terms, Sitemap).
8. Self-referencing links: many CTAs point at their own containing section, so clicking does nothing useful. They are "View all ventures" and 5x "Learn more" (-> #ventures), "Our model" (-> #model), "View all insights" and 4x "Read more" (-> #insights), "Our Nation Building Initiatives" (-> #nation) and "Our Ecosystem" (-> #presence). The hero CTAs and the mailto CTAs in #contact are fine.
9. Nested check: the "Digital Economy / Green Transition / Skills & Education / Inclusive Growth" submenu items all link to the same #nation. They resolve, but they are not distinct targets (observation, counted as pass).

## Not tested
- Visual or screenshot comparison with the reference image (a separate capture.py covers screenshots).
- Hover and dropdown behaviour of the "Nation Building" submenu on desktop.
- Submenu visibility on mobile.
- Touch swipe on the carousel, and scroll-snap alignment.
- Browsers other than Chromium, and real devices.
- The modal's contents (the dialog has no video, so playback is untested). Screen-reader behaviour.
- `mailto:` link activation. Focus-visible was checked only at 1440, not on mobile.
- Scroll-spy active-class correctness. The count-up and reveal animations. `prefers-reduced-motion`.
- Overflow detection excluded elements inside `.carousel` and `#nav`.
- Console warnings were captured, but only error/warning types were asserted.
