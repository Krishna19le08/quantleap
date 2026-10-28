# Implementation plan / status
Existing static site (index.html + components/*.html loaded by fetch + assets/). Per instructions: no framework swap, no new dependencies. Only CSS/JS tuned.
Round 1: hero location list, presence heading wrap, nation section height, carousel arrows hidden when inert.
Round 2 (mobile): hero shade, 44px touch targets, social icon hit area.

Round 1 (visual-defects round0 D1-D10, P3): 1440 vs 1280 test: at 1280 sections scale 8-15% taller than ref (hero 267 vs 238, focus 231 vs 206, presence 141 vs 125); at 1440 within 0-3%. Ref container is 461/517 (89%) = 1280px container at 1440, so container widened 1240 -> 1280 and 1440 kept as design basis. Hero h1 was actually larger than ref (198 vs 168 at 517 scale) so reduced to clamp(..,3.8vw,54px). Changed: stylesheet.css tokens (navy/gold/cream), header, hero (position 25% bottom, shade, loc), pillar cards, steps rings, nation/presence maps, impact, insights, cta, footer grid, responsive rules; script.js scroll-spy rewritten (scroll-position based, Home active at top; old IntersectionObserver never observed hero so a stale "About" stayed active after scroll-to-top).

## Round 2 changelog (Implementation Agent)
Files: assets/css/stylesheet.css, index.html, assets/js/script.js.
- Header: `.nav` height 90->106; `#nav>ul` gap 36->28 and `#nav a{white-space:nowrap}` (no Nation Building/Insights collision at 1440).
- Hero: `.hero-art` object-position 25%->70% bottom (towers now ~52-89% width); `.hero-loc` absolutely positioned top-right (top:-40px, clear sky above the roof) in clear sky with text-shadow; `.watch{white-space:nowrap}` and removed `<br>` so "Watch Our Story" is one line.
- Nation: grid columns 1.4/1.3/.75, h2 clamp max 40px (3 lines), copy max-width 440, `.map-box` aspect-ratio 16/9 (no more crop of INDIA/ACROSS JAPAC labels baked into map-bg.jpg), softer radial mask, padding 44->73 (section 482 = ref); list icons 52px. Removed unused `.map-label`.
- Presence: grid 1.5/1.5/.8, h2 clamp max 34px (2 lines), map mask/opacity .55, icons 44px, padding 38 (section 348 = ref).
- Model: step icon box 76px with 12px padding (larger glyph).
- Impact: image now right-anchored 64% wide, object-position 50% 55%, left-fade mask over dark navy section background; hiker small at ~88% x; heading/stats moved up (inner padding 14/58). LIMITATION: in the only available asset the sun is ~12% of image width left of the hiker, so sun lands ~81% not ~40% as in ref; no lawful asset in ref/ has the sun-left/hiker-right composition (ref/Lone Hiker... is the same image).
- CTA: cta-1 min-height 242, `.cta-2` 206 (new class on 2nd section); cta-2 button replaced by minimal underlined text link `.cta-link` (kept for functionality; ref has no button).
- Carousel: removed hiding of chevrons in script.js (they were hidden because all 5 cards fit); `.car-btn` top:81px (centred on image, not over text); removed dead `[hidden]` rule.
- Focus padding 70/66 (+20); ventures padding 36/70 (heading up ~14px); impact heading up; footer padding 40/20.
Metrics @1440 (css px, render vs ref*scale): hero 660/663, focus 570/574, ventures 625/632, nation 482/482, model 328/331, impact 284/281, insights 529/521, presence 348/348, cta-1 242/242, cta-2 206/206, footer 173/175; page 4448. No h-overflow at 390/517/820/1440, no console errors or broken images.

## Round 3 changelog
Constraint received mid-round: no image edits/swaps, no new colours, keep object-position/crop rules. Edits are HTML/CSS/JS only.
Visual (assets/css/stylesheet.css): header nav margin-left:auto + margin-right clamp(0,8vw,120px), ul gap clamp(18,3.1vw,44), logo 33px, nav text-shadow (nav now spans ~36-86% at 1440); hero: .hero-inner padding-top 90px, .hero-loc top 30px/max-width 130/12px/stronger shadow, hero-shade stronger navy alpha (same navy token), lead/watch text-shadow, .play 50px; focus: grid minmax(0,400px) 1fr, h2 40px, `sustainable<br>JAPAC.` (JAPAC. on its own 4th line), padding 50/64; ventures: padding 20/93, tag colour var(--muted), chevrons in outer gutter at >=1400px (wrap margin -20px, arrows -58px); nation: padding 43/79, map-box min-height 380 with negative margins bleeding behind copy, soft elliptical mask, copy z-index, paragraph max 340; impact: stat numerals sans lining 28-40px, li padding 18px; presence: map margins wider, paragraph 300px, 4 distinct inline SVG row icons; cta-2 padding 44/16 + link shadow; footer padding 30/44, .foot padding-bottom 10; modal max-height + sitemap list. Section heights at 1440: header 106, hero 660, focus 574, ventures 632, nation 482, model 328, impact 284, insights 529, presence 349, cta-1 242, cta-2 206, footer 175.
Reverted after the constraint: impact-art filter, impact-shade alpha, presence dotmap opacity, new tag/nav/lead colours, header top gradient, presence row icons via <img> (now distinct inline SVG instead).
Functional (script.js + components): Escape closes mobile menu, aria-expanded false, focus to burger; generic [data-modal] dialogs with Tab focus trap and focus return to opener; carousel arrows hidden when track does not overflow (desktop: 5 cards fit, so no dead buttons), shown at 390 and page by one card; 320px overflow fixed (.pillars minmax(0,1fr) + overflow-wrap); footer legal links open in-page modals (Privacy, Terms, Sitemap, placeholder text); social links point to network root URLs marked PLACEHOLDER in footer.html; self-pointing CTAs retargeted (venture Learn more / View all ventures / insight Read more / View all insights -> mailto with subject; Nation Initiatives -> #model; Our model -> #impact; Our Ecosystem -> #contact).
Deviation: reference shows carousel chevrons at desktop; hidden here because the 5 cards fit and arrows would be dead.

## Round 4 changelog (CSS only, assets/css/stylesheet.css; no images, colours or tokens touched)
- Ventures: .vbody min-height 226 (cards ~+50px), .ventures bottom padding 93->43, View-all margin-bottom 17px + navy text-shadow.
- Insights: .iimg 170->139 (ref image height), .ibody padding 20/28/24, h3 min-height 63 (3-line titles); section stays 521. Mobile: h3 min-height 0 (no gap above Read more).
- Nation (>1100px): .nation-list left 45/top 28, button top 17. Reset on <=1100 to avoid overflow.
- Impact: min-height 281, h2 top -11, stats top +11, navy alpha text-shadow on heading/numbers/labels, labels #fff. Mobile: stat li padding 10, label 11px (no wrap at 390).
- cta-1: h2 top -17, button top 31 / left 22 (desktop only).
- Presence: .locs gap 20->32, padding 37.5. Model padding 37.5 (331). Hero height cap 660->663.
- Contrast: nav link and .cta-link text-shadow strengthened (navy alpha).
- Mobile: footer nav 4-col grid (4+3, no lone Contact, no big row gap); last focus pillar spans both columns.
- Unfixed: nation map labels (INDIA/JAPAN/ACROSS JAPAC) and "ACROSS JA" clip at 390 are baked into map-bg.jpg / its cover crop (image-constrained); carousel arrows at 1440 (documented deviation).
