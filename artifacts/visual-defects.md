# Visual defects - round0 (1440 render vs reference, per-section aligned)

Method (facts): reference 517x1600 sliced by artifacts/section-inventory.json; render `round0_full_1440.png` sliced by metrics.json section tops, resized to 517 wide (x0.359). Outputs: artifacts/comparisons/round0/{section}_side|overlay|diff.png. All side-by-sides were viewed. No similarity percentages are claimed. Diff images are only a locator (reference photos are AI-generated and differ in content).
Section heights at 1440, scaled, match the reference within 0-5 px except cta-2 (+9) and model (+5). Page 4466 vs ~4457 inferred. 1440 is a sound assumption overall.
Verification status for every item: OPEN (not yet re-rendered).

## P1 - Geometry / layout

D1. Hero image framing and shade.
- Ref: wide shot, Marina Bay Sands at ~x65-93%, domes low-centre, bright blue sky on the right, only the left ~50% darkened.
- Render: image zoomed/cropped (towers at 78-96% and cut), much darker and more orange, dark shade over the top-right.
- Fix `.hero-art{object-position:center bottom}` -> try `left bottom` / `30% 80%` and check hero-bg.jpg is not scaled beyond cover (index.html:21).
- Fix `.hero-shade` -> `linear-gradient(90deg,rgba(0,28,42,.85) 0%,rgba(0,28,42,.45) 35%,rgba(0,28,42,0) 60%)`; reduce the top gradient `rgba(8,23,46,.55)` to `.2`.
- `.hero-loc` (SINGAPORE / INDIA / JAPAC / A STRONGER TOMORROW): nearly invisible in render, pushed to far right. Ref is at container right with a visible vertical rule. Set `color:#fff;font-size:11px;border-left-color:rgba(255,255,255,.6);margin-top:40px`.
- Ref text block starts higher: `.hero-inner{padding-top:60px}` -> `0`. `.play{width:44px;height:44px}`.

D2. Content under-scaled and missing card/circle treatments (systemic; every section has text and icons visibly smaller than ref).
- Focus `.pillars/.pillar`: ref are bordered, softly shadowed cards (~220x190 css px). Render has no boxes, only a top border and left dividers. Fix `.pillar{background:rgba(255,255,255,.55);border:1px solid #e3ddcd;border-radius:4px;box-shadow:0 6px 18px rgba(20,33,58,.06);padding:24px 22px;margin:0 8px}`; remove `.pillar:first-child{padding-left:0;border-left:0}` and `.pillars{border-top}`; `.pillar img{width:48px;height:48px}`; `.pillar p{font-size:13.5px}`; `.pillar h3{font-size:12px}`. `.focus-top{grid-template-columns:1.1fr 1fr}` -> `.9fr 1.2fr` (ref headline wraps to 4 lines with "JAPAC." alone).
- Model `.steps img`: ref are ~70px gold-ringed circles with thin vertical dividers between steps and arrows at icon midline. Fix `.steps img{width:72px;height:72px;padding:18px;border:1px solid rgba(240,180,41,.5);border-radius:50%}`; `.steps li:not(.arrow){border-left:1px solid #e3ddcd}`; `.arrow{margin-top:24px}`; `.steps p{font-size:12.5px}`.
- Nation `.nation-list img` 38px and presence `.locs svg` 30px: ref have ~48px ring icons. Set 48px / 40px; `.nation-list{gap:30px}`; h4 11.5px; p 12.5px.
- Body copy (render vs ref): `.lead` 14 -> 16px; `.focus-text` 14 -> 15; `.nation-copy .muted`, `.presence-copy .muted`, `.model-copy p` 13 -> 15; `.vbody p` 12 -> 13.5; `.ibody h3` 13 -> 15; `.cta p` 13 -> 15; `.stats span` 10.5 -> 12.
- H2s: ref ~1.2-1.25x larger. `.focus-top h2` clamp max 42 -> 48; `.ventures h2` 44 -> 48; `.nation h2` 38 -> 42; `.model h2` 36 -> 40; `.presence h2` 36 -> 40.
- Section top paddings are larger than ref (eyebrow sits ~35px lower at 517 scale in focus/ventures/nation): `.focus{padding:96px 0 90px}` -> `60px 0 56px`; `.ventures{padding:70px 0 74px}` -> `50px 0 56px`; `.nation{padding:80px 0}` -> `56px 0`. Do this together with the enlargements so total heights stay matched.
- See "1440 assumption" note: confirm sizes at 1280 before bulk-editing fonts.

D3. Header. Ref wordmark larger, wide-tracked, sans-like (~30px); nav links brighter and bigger; Home underlined; header bar is tall (ref 38 -> ~106 css px). Render: `.logo-mark{font-size:22px}` thin serif, tag 9px, nav 12.5px, `.nav{height:78px}`. Fix `.logo-mark{font-size:30px;font-family:var(--sans);font-weight:500;letter-spacing:.24em}`, `.logo-tag{font-size:11px}`, `#nav a{font-size:14px}`, `#nav>ul{gap:36px}`, `.nav{height:90px}`.
- Observed fact: in the hero shot "About" is underlined, not "Home". Suspected cause (inference): scroll-spy in assets/js/script.js lines ~35-45 sets `.active` wrongly at scrollY=0 (components/menu.html:3 marks Home active). Home must stay active at top.

D4. Nation map. Ref: night satellite map fills the middle column and bleeds behind the text, bold white labels INDIA/JAPAN/SINGAPORE/ACROSS JAPAC ~12px. Render: small framed 16:9 rectangle with visible edges and tiny labels. Fix `.map-box{aspect-ratio:auto;height:100%;min-height:320px}`, wider/softer mask `radial-gradient(ellipse 85% 90% at 50% 50%,#000 45%,transparent 100%)`, `.map-label{font-size:12px}`, reposition SINGAPORE lower-centre. Presence map: ref is dimmer with few arcs; render is bright and boxed. `.presence .dotmap{opacity:.65}` plus softer mask; `.map-box.wide{aspect-ratio:2.4/1}` -> fill column.

D5. Impact. Ref: left dark navy fade, sun upper-centre (~x55%), hiker small at ~x88%. Render: image zoomed (hiker ~3x larger, sun top-right). Fix `.impact-art{object-position:50% 35%}` and check source aspect (index.html:156); `.impact-shade{background:linear-gradient(90deg,rgba(0,28,42,.9),rgba(0,28,42,.35) 50%,rgba(0,28,42,0) 75%)}`. Stats in ref are larger: `.stats b{font-size:clamp(30px,3.4vw,44px)}`, `.stats{max-width:1000px}`.

## P2 - Images / cards

D6. Ventures cards. Image height: `.vimg{height:150px}` -> `162px`. Card body ref lighter teal-navy `#0a2a40`. Section bg ref `#001c2a`. Carousel chevrons visible at x~8 and x~511 in ref; render has none visible: `.car-btn.prev{left:-17px}` -> `left:8px`, `.next{right:8px}` and check `[hidden]` handling in script.js. Image content: ref card 5 pale grey boulders vs render dark gold ore; card 2 macro leaves vs render hillside. Ref garbled overlay text on cards 2/3 is an AI artefact: do NOT replicate. Swap images only if closer sources exist in ref/ and assets/images/.
D7. Ventures/insights "View all" links. Ref ventures link is white underlined; render is small gold. `.ventures .link-gold{color:#fff;text-decoration:underline;text-underline-offset:4px}`. Ref link sits level with heading's second line; render sits lower.
D8. Insights cards. Ref: larger image (`.iimg{height:130px}` -> `~190px`), category label dark (`.ibody small{color:var(--ink)}` not orange), title 3 lines with narrower padding, soft shadow, taller card (render ~20 scaled-px shorter). `.ibody h3{min-height:54px}` -> `72px`; `.icard{box-shadow:0 8px 24px rgba(20,33,58,.08)}`. Ref photos differ (city/brain/turbines/children in uniform) from render (sunset city/brain/hills/backpack kids); not fixable without new assets.
D9. CTA bands. Ref cta-1 and cta-2 differ in height (87 vs 74 scaled; ~242 vs ~206 css) and use lighter golden-sky/green-hill images; render both 230px with darker orange-misted valley. `.cta-shade{background:rgba(8,23,46,.55)}` -> left gradient `linear-gradient(90deg,rgba(0,28,42,.65),rgba(0,28,42,.15) 60%)`; `.cta h2{font-size:clamp(28px,3.4vw,40px)}` -> `clamp(26px,2.6vw,34px)`; ref button sits ~75-87% from left, render pinned at far right (`.cta-inner` add `padding-right:10%`). Ref cta-1 heading is garbled AI text ("Cingpore what's next"); keep "Let's build what's next." For cta-1 only, ref has no visible "Let's build" duplication risk: confirm in index.html that the two bands are intended (inventory flags cta-1 as garbled).
D10. Footer. Ref: larger wordmark, tagline below, 7 centred nav links, socials far right with Privacy/Terms/Sitemap beneath them, copyright centred beneath, no divider. Render: nav centred but copyright left and legal links on the right with a divider rule. Fix in the footer component and `.foot`/`.site-footer` (`.site-footer{background:#021523}`; wordmark 24px+).

## P3 - Colour tokens (root)
- `--navy:#08172e` -> `#001c2a`; `--navy-2` -> `#01131f`; `--navy-3:#0d2644` -> `#0a2a40`. Render is bluer/purpler than ref teal-navy.
- `--cream:#f8f5ee` -> `#f6f7f2` (ref cooler).
- `--gold:#f0b429` -> `#f3c148` (ref button gold, less orange); `--gold-2` -> `#d9a62e`.
- `.btn{padding:14px 22px;font-size:13px}` -> `16px 28px;14px` (ref buttons larger).

## Sections where the 1440 assumption looks wrong or uncertain
Facts: scaled heights agree within ~1-3% for hero, focus, ventures, nation, impact, insights, presence, footer. Doubtful:
- cta-1 / cta-2: ref heights unequal (87 vs 74 at 517), render equal (230px css).
- model: render 124 vs ref 119 scaled; ref proportions imply bigger text.
- Header: ref bar 38px at 517 (~106 css) vs 78px render.
- Inference only: nearly every section shows text/icons ~10-25% smaller than the ref relative to layout, while section heights match. That could mean the design was ~1280 wide (ref container x28-489 of 517 = ~1284 css px at 1440 scale, vs render 1240px) or simply larger type. Recommend rendering at 1280 and comparing before bulk font edits.

---
# Round1 status (1440 render vs reference, per-section aligned)

Method (facts): same as round0. Reference slices from artifacts/section-inventory.json; render from artifacts/screenshots/round1/round1_1440_{section}.png resized to 517 wide. Images: artifacts/comparisons/round1/{section}_side|overlay|diff.png. All 11 side-by-sides viewed; overlay/diff viewed for hero, nation, presence, impact. No similarity percentages claimed. Metrics: 1440 page 4517 (round0 4466); no broken images, no console errors, no h-overflow at 390/517/820.
Scaled heights, ref -> render: hero 238->237, focus 206->198 (-8), ventures 227->225, nation 173->181 (+8, ~+22 css), model 119->118, impact 101->102, insights 187->190, presence 125->141 (+16, ~+44 css), cta-1 87->83, cta-2 74->83 (+9), footer 63->67.

## Round0 defect status
- D1 hero: PARTIALLY FIXED. Fixed: shade now left-only, sky/right bright blue-orange, text block higher, eyebrow/H1/lead present, Watch Our Story + play present, hero-loc now white with rule. Still open: (a) image framing: towers at ~86-100% x and cut by the right edge vs ref 65-93%; domes are bigger and further right; `.hero-art{object-position:25% bottom}` (stylesheet.css:65) over-crops - source needs a smaller zoom (use `object-position:0% bottom` or reduce scale / `object-fit:cover` on a wider box). (b) `.hero-loc` (css:75) still overlaps the Marina Bay Sands tower top and is illegible (white text over bright sky/tower; ref has it at x~85-95%/y~38-60 over clear sky). Move up/left or add text-shadow, and keep it above the towers (towers must move left/down first). (c) "Watch Our Story" wraps to 2 lines ("Watch Our / Story") - add `white-space:nowrap`. (d) Nav "Nation Building" chevron collides with "Insights" at 1440 (see hero_side): reduce `#nav>ul` gap or font. (e) Eyebrow QUANTLEAP is 1 line at same position, OK.
- D2 content under-scaled/cards: PARTIALLY FIXED. Focus pillars now bordered shadowed cards (fixed); H2 ref wraps 4 lines with "JAPAC." alone, render 3 lines (minor open); pillar icons ~30px vs ref ~32 ok; pillar copy still ~1-2px smaller than ref. Model steps: gold-ringed circles now exist (fixed) but icons inside rings are tiny (render glyph ~12px vs ref ~28px) and step labels sit lower margin (open); ref has vertical dividers - render has them faint. Nation/presence ring icons now present (fixed) but small (~28px vs ref 36-40 rendered). Section heights: focus now 8 scaled px short (~22 css) - open.
- D3 header: PARTIALLY FIXED. Wordmark now sans, tracked, ~30px (fixed); Home underlined/active at top (fixed). Header height now 90 css vs ref ~106 (open): `.nav{height:90px}` -> 106px (css:43). Nav link sizes still smaller than ref (ref cap-height larger); nav crowding with chevron (see D1d).
- D4 nation map: PARTIALLY FIXED. Map is now bigger with soft edge and brighter arcs (improved), but still a framed rectangle with visible edge, left of map is cut at INDIA (labels INDIA missing; "ACROSS JAPAC" label clipped to "ACR" under the list), map does not bleed behind text. Ref map is dimmer/wider. Presence map: wide framed rectangle with visible border, brighter than ref (ref dim, few arcs). `.presence .dotmap{opacity:.65}` applied but edges still show; use stronger mask.
- D5 impact: OPEN (little change). Render still strongly orange, sun top-right at ~x85%, hiker large (~3x) at x~90% cut at bottom vs ref sun x~40%, hiker small on a rock at x~88%, left side dark navy. Heading/eyebrow positions lower than ref (~8 scaled px). Stats larger now (fixed).
- D6 ventures: PARTIALLY FIXED. Image height 162px done; chevrons present in css (`.car-btn.prev{left:8px}`) but not visible in render at 1440 (not seen in ventures_side; verify [hidden]); card body navy ok. Card photos still differ from ref (cards 2, 5) - asset limit, not defect. Heading starts ~13 scaled px lower than ref (section top padding).
- D7 View-all links: PARTIALLY FIXED. Ventures link now white underlined small; sits lower than ref (render y~125 vs ref ~92 at 2x => ~16 scaled px lower) because heading is lower.
- D8 insights: FIXED/mostly. Image height 170, dark category labels, cards with soft shadow, heights near ref (+3). Titles are 2 lines vs ref 3 (narrower padding) - cosmetic. Photos differ (asset).
- D9 CTA: PARTIALLY FIXED. Left gradient and button position improved; button now at ~x75-90% (ok). Still OPEN: both bands are 230px css (83 scaled) vs ref 87/74; cta-1 ref is lighter/darker greener hill photo - render is orange valley; cta-2 in ref has NO button, render shows button in both (ref cta-2 button absent per inventory 'uncertain' - low confidence). Render cta-2 is 9 scaled px too tall.
- D10 footer: PARTIALLY FIXED. Wordmark larger tracked, nav centred, socials right with legal links beneath, copyright centred below, no divider (fixed). Remaining: footer 4 scaled px (~11 css) taller than ref; wordmark/tagline ~10 scaled px lower, copyright lower.
- D11 colour tokens P3: FIXED visually (navy teal-navy, cream cooler, gold button lighter) - confirmed in side-by-sides; no new colour drift seen.

## New / regressed defects (round1)
N1 (REGRESSION, P1) Nation h2 now wraps to 4 lines ("Technology for an / inclusive, resilient / and progressive / JAPAC.") vs ref 3 lines; selector `.nation h2` (css:126, clamp 26px..42px) inside a narrow `.nation-copy` column. Section +8 scaled px (~22 css). Fix: widen copy column (grid-template first col +10%) or `.nation h2{font-size:clamp(26px,2.6vw,38px)}`; ref H2 box ~290/517 = 56% of the width; keep 3 lines.
N2 (REGRESSION, P1) Presence h2 wraps to 3 lines ("Singapore. India. / JAPAC. / And beyond.") vs ref 2 lines; `.presence h2` (css:183, 40px max) in a column limited by `.presence-copy .muted{max-width:320px}`/grid. Presence is +16 scaled px (~44 css) taller than ref; also `.map-box.wide{min-height:200px}` (css:185) and `.presence{padding:30px 0}` plus 4 icon rows ~46px apart. Fix: widen copy column or `font-size:clamp(24px,2.4vw,34px)`, `white-space:nowrap` on the first line; reduce row gap.
N3 (REGRESSION, P2) Hero text collisions: `.hero-loc` over tower top; nav "Nation Building"/"Insights" overlap at 1440; "Watch Our Story" wraps. (See D1.)
N4 (P2) Focus now 8 scaled px short (css .focus padding or pillar padding too tight; ref pillar cards ~66 scaled tall, render ~64; ref H2 4 lines). Fix `.focus-top h2` width/col to wrap "JAPAC." onto 4th line, raising height.
N5 (P2) Nation map label clipping: "ACROSS JAPAC" label rendered as "ACR" cut by `.nation-list` overlay; INDIA label hidden left of map. Selector `.map-label` positions; use right:% anchored positions and z-index below list.
N6 (P3) Impact heading and eyebrow ~8 scaled px lower than ref; stats row ~6 px lower.
N7 (P3) Mobile 390 page height 8147 (no overflow). Not compared to a reference (none exists).

## Priority
1. Presence (+44 css) and nation (+22 css) heights: fix H2 wrapping (N1, N2).
2. Hero: image framing/towers (D1a), hero-loc overlap (D1b), nav collision (D1d), header 106px (D3).
3. Impact image framing/colour (D5).
4. CTA heights 262->~242 (cta-1) / ~206 (cta-2) css, drop cta-2 button if desired.
5. Nation/presence maps edges, labels (D4, N5).
6. Model icons size, ring icons (D2).
7. Focus height/H2 wrap (N4), ventures top padding (D6/D7), footer height (D10).

---
# Round2 status (1440 render vs reference, per-section aligned)

Method (facts): ref slices by artifacts/section-inventory.json; render artifacts/screenshots/round2/round2_1440_{section}.png resized to 517 wide. Images: artifacts/comparisons/round2/{section}_side|overlay|diff.png (side = ref left, render right, 2x). All 11 side-by-sides viewed; overlay + diff viewed for hero, nation, impact, presence (impact/presence diffs not separately opened; overlays were). No similarity percentages claimed. metrics.json: no broken images, no console errors, no h-overflow.
Scaled heights ref -> render (delta): hero 238->237, focus 206->205, ventures 227->225, nation 173->173, model 119->118, impact 101->102, insights 187->190 (+3), presence 125->125, cta-1 87->87, cta-2 74->74, footer 63->62. Header 106 css = ref ~106. All heights are within 3 scaled px (round1 had +8/+16/+9): height defects CLOSED.
Known limits accepted by the caller (not re-raised): impact sun/hiker (one hiker asset), hero towers at 52-89% vs ref 65-93%, hero hamburger absent at desktop, "Watch Our Story" one line, cta-2 button replaced by text link.
Coordinates below are scaled-517 px unless "css" is stated (1 scaled px ~ 2.79 css px). Measurements are from viewing the side images, so +/-2 px.

## Earlier defects - status
- D1 hero: PARTIAL. Fixed: left-only shade, colour close, hero-loc no longer on tower top, eyebrow/H1/lead/CTA/play present, H1 and lead horizontal extents match ref. Open: (a) tower framing (known limit). (b) Text block ~12-17 px (~35-47 css) HIGHER than ref: eyebrow y 48 vs 60, H1 top 67 vs 79, CTA y 172 vs 189. Fix `.hero-inner` (css:67): add `padding-top:40px` or align lower. (c) `.hero-loc` (css:75): ~11 px (~30 css) higher than ref, 4 lines vs ref 5 ("A STRONGER / TOMORROW" wrap), x 81-94% vs ref 86-95%, white on bright cloud = low contrast. Change `top:-40px` -> `-10px`, `max-width:110px`, font 12px, stronger text-shadow. (d) Watch Our Story + play now over the bright domes: small, low contrast; add text-shadow, `.play` 44 -> 50. (e) lead line 3 crosses lit towers (legibility): add text-shadow or widen `.hero-shade` to ~50%.
- D2 content scale: PARTIAL/mostly fixed. Pillars are bordered shadowed cards (fixed) but separate with gaps, narrower/lighter copy than ref. Focus H2 3 lines vs ref 4 (see N4). Model: 76px gold rings (fixed), dividers and arrows present, label rows aligned (y 120 vs 122 at 2x); glyphs inside rings ~60% of ref size; step text smaller/lighter (`.steps p` css:144 12.5px #55617a -> 13px #3d4a63). Nation/presence ring icons ~ref size (fixed). Nation/presence paragraphs 3/2 lines vs ref 4/4: `.nation-copy .muted{max-width:440px}` (css:126) -> 340px; `.presence-copy .muted{max-width:420px}` (css:183) -> 300px.
- D3 header: PARTIAL. Fixed: 106px (css:43), sans tracked wordmark, Home active/underlined. Open: (a) nav spans x 50-95% vs ref 34-86% (ref hamburger at 94%); "About"/"Our Ventures"/"Nation Building" chevron/"Insights" touch or overlap at 1440 (`.nav` space-between css:43; `#nav>ul{gap:28px}` css:47). Fix: shift ul left (`margin-right:60px`) and gap 36px. (b) nav y 36 vs 29 at 2x (~7 css low). (c) wordmark ~10% narrower than ref (165 vs 183 units): `.logo-mark` 30 -> 33px. (d) nav over bright clouds low contrast: text-shadow or top gradient. Hamburger: known limit.
- D4 maps: PARTIAL. Nation: map still a small (~40% of ref width) rectangle with a visible edge, not bleeding behind the text; labels INDIA/JAPAN/SINGAPORE/ACROSS JAPAC now present, unclipped (N5 FIXED) but ~6px vs ref ~12px. Fix `.map-box{aspect-ratio:16/9}` (css:127) -> `aspect-ratio:auto;min-height:300px;margin:0 -8%` plus radial mask; `.map-label{font-size:12px}`. Presence: box edge no longer visible (fixed), dim like ref, but ~60% of ref width, few hotspots; ref has bright hub and long arcs. `.map-box.wide` (css:184) wider (`margin-left:-10%`), dotmap opacity .85. All four presence rows show the same swirl glyph (ref distinct): check index/components markup.
- D5 impact: PARTIAL. Overlay: sun x ~81% and hiker x ~88% match ref (round1 offset fixed). Open: far more saturated orange than ref's muted gold-blue (`.impact-art` css:151: `filter:saturate(.7) brightness(.85)`); shade lighter than ref (`.impact-shade` css:152 .55 -> .75); hiker ~2x ref size (single asset: limit); stat numerals serif old-style vs ref lining sans (`.stats b` css:158 font-family); "$500M+" and "1B+" nearly touch; heading ~4 px lower than ref (was 8).
- D6 ventures: PARTIAL. Image height/body colour fixed. Open: heading/View-all/cards start 3/12/6 px lower than ref (`.ventures` top padding -> ~-16 css); chevrons now visible but INSIDE card 1/5 images (`.car-btn.prev{left:8px}` css:120 is relative to the carousel inside the container); ref in outer gutter (x~8/~511): use `left:-28px`/`right:-28px`; tag line orange in render, grey in ref (`.vbody small`); ref cards span x 21-501 vs render 28-488. Photos 2/5 differ (asset).
- D7 View-all: PARTIAL. White underlined; smaller than ref and ~12 px low (follows D6).
- D8 insights: MOSTLY FIXED. Open cosmetic: `.iimg{height:170px}` (css:167) looks ~11 px taller than ref image; titles 2 lines vs 3 (more `.ibody` padding); card +3 px. Photos differ (asset).
- D9 CTA: PARTIAL. Heights match (243/207 css). cta-1: button x 72-84% vs ref 74-87% ok but ~10 px higher than ref; heading ~6 px lower; image brighter orange vs ref darker green (asset). cta-2: link small, white 13px (`.cta-link` css:195) over bright foliage = low contrast (text-shadow); heading ~7 px higher than ref (`.cta-2 .cta-inner{padding:30px 0}` css:194 -> `44px 0 16px`); sun x ~88% vs ref ~76% (asset/object-position).
- D10 footer: PARTIAL. Structure matches ref. Rows sit lower: nav/socials y 41 vs 34, legal 80 vs 62, copyright 99 vs 85 (2x units; ~4-9 px). `.site-footer` css:200 padding 40/20 -> 30/14; `.foot{padding-bottom:22px}` -> 8px; `.foot-bottom{gap:10px}` -> 6px.
- D11 colour tokens: FIXED, no drift (hero water more orange than ref: asset).

## Round1 new defects - status
- N1 nation H2 4 lines: FIXED (3). N2 presence H2: FIXED (2). N5 label clipping: FIXED. N7 mobile: unchanged, no overflow.
- N3: PARTIAL (overlap fixed; nav collision open, D3a). N4: PARTIAL - height ok, H2 still 3 lines vs 4; eyebrow/H2/cards sit ~9-12 px lower than ref; paragraph column starts ~55 px (~150 css) too far right. Fix `.focus-top{grid-template-columns:.9fr 1.2fr}` (css:85) -> `.8fr 1.3fr`, `.focus-top h2{max-width:440px}`, `.focus{padding:70px 0 66px}` (css:84) -> `50px 0 80px`. N6: PARTIAL (~4 px).

## New defects (round2)
R2-1 (P1, hero) text block 35-47 css too high; `.hero-inner` css:67.
R2-2 (P1, header) nav cluster ~230 css right of ref, crowded/overlapping; css:43,47.
R2-3 (P2, hero) hero-loc ~30 css too high, low contrast; css:75.
R2-4 (P2, nation) eyebrow/H2 ~11 px (~30 css) lower than ref (section top padding too big), paragraph 3 vs 4 lines.
R2-5 (P2, impact) over-saturated, light shade; css:151-152.
R2-6 (P2, ventures) chevrons inside images, tags orange, section 3-12 px low; css:118-120.
R2-7 (P3, cta-2) heading 7 px high, link contrast. R2-8 (P3, footer) rows 4-9 px low. R2-9 (P3, presence) identical row icons, map small. R2-10 (P3, model) inner glyph/step text small.

## Priority of what remains
1. Hero text block offset (R2-1): CSS.
2. Header nav position/collision/contrast (R2-2, D3): CSS.
3. Hero-loc, Watch-story, lead legibility (D1b-e): CSS.
4. Nation map bleed/size + labels + top padding (D4, R2-4): CSS.
5. Impact saturation/shade/stat font (D5): CSS. Hiker size: ASSET-limited. Sun position now fine.
6. Ventures offsets, chevrons to gutter, tag colour (D6): CSS.
7. Focus 4-line H2 and paragraph column (N4): CSS.
8. Presence map size, row icons (D4, R2-9): CSS + markup check.
9. Footer, cta-1/cta-2, insights spacing nits: CSS.
10. ASSET/known limits: hero towers 52-89% vs 65-93%, hamburger, hero water colour, cta photos, ventures cards 2/5 photos, insights photos, impact hiker scale, two-line Watch Our Story, cta-2 button.

---
# Round3 status (1440 render vs reference, per-section aligned)

Method (facts): renders artifacts/screenshots/round3/round3_1440_{section}.png resized to 517 wide, compared to ref slices from section-inventory.json. Images: artifacts/comparisons/round3/{section}_side.png (ref left, render right, 2x) for all 11 sections, plus hero and nation overlay + diff. All viewed. Responsive: resp_517_sheet.png and resp_390_sheet.png (full-page columns) viewed. metrics.json: no broken images, console errors, failed requests or horizontal overflow at 390/517/820/1440. No similarity percentages claimed; offsets are +/-2 scaled px read from images (1 scaled px ~ 2.79 css px).
Heights ref -> render (scaled): hero 238/237, focus 206/206, ventures 227/227, nation 173/173, model 119/118, impact 101/102, insights 187/190, presence 125/125, cta-1 87/87, cta-2 74/74, footer 63/63.
Constraint: user finalised all images and colours; anything needing an image/colour change is "skipped (user constraint)".
Colour tokens (stylesheet.css): --navy #001c2a, --gold #f3c148, --cream #f6f7f2, .site-footer #021523 all present and unchanged. No drift.

## Status of open defects
- R2-1 hero text block too high: FIXED. Eyebrow/H1/CTA now within ~4 scaled px of ref (eyebrow 64 vs 60, CTA y matches).
- R2-2 / D3a header nav position/collision: FIXED. Nav spans ~36-85% vs ref 33-86%, no overlap. D3c wordmark width: FIXED (matches). D3b nav y ~3 px low: open, trivial. D3d nav contrast over bright clouds: PARTIAL (Nation Building/Insights thin white on cloud). Hamburger at desktop: skipped (known limit).
- R2-3 / D1c hero-loc: PARTIAL. Position (86-92%) and 5-line wrap now match ref; still white on bright cloud/tower top, low contrast.
- D1d Watch Our Story: PARTIAL. One line, small, low contrast on domes. D1e lead line 3 over lit domes: PARTIAL, legible. D1a tower framing, hero water colour: skipped (image).
- N4 focus: FIXED. H2 now 4 lines like ref; height matches. Paragraph column wider and ~4 px lower; pillars are separate bordered cards with lighter, smaller copy (cosmetic, open P3).
- D2 model: FIXED/mostly. Ring size, dividers, label rows aligned; glyph differences = asset.
- D2 nation/presence paragraph lengths: FIXED (4/3 lines like ref).
- R2-4 nation top padding/H2: FIXED (3 lines, ~2 px offset). D4 nation map: PARTIAL. Extents now similar to ref, no visible box edge; map dimmer, labels INDIA/JAPAN/ACROSS JAPAC faint (~6 px vs bold white in ref); list sits ~17 scaled px left and ~10 px higher than ref; button ~6 px high. Map imagery differences: skipped (image).
- R2-9 / D4 presence: FIXED for row icons (now distinct); map narrower/dimmer than ref (image-constrained), rows ~15% tighter spacing (open P3).
- R2-5 / D5 impact: PARTIAL. Saturation/shade: skipped (colour/image constraint). Hiker scale: skipped (image). Heading ~4 px low, stats row ~4 px high: open P3. "1B+" label sits on sun glow, low contrast.
- R2-6 / D6 ventures: PARTIAL. Heading offset FIXED; tag line now grey FIXED; card x extents match (40-950 vs 40-960). Open: View all ~6 px low; cards ~18 scaled px shorter than ref (empty strip under cards); body text smaller; chevrons not visible in the 1440 crop (ref has faint gutter arrows). Photos 2/5: skipped (image).
- D7 View all: PARTIAL (follows D6).
- D8 insights: PARTIAL. Image still ~11 scaled px taller than ref (.iimg height); titles 2 lines vs 3; card +3 px. Photos: skipped.
- D9 / R2-7 cta-1: PARTIAL. Heading ~6 px low, button ~11 px high and ~8 px left of ref. Ref heading is garbled text in the ref image; render reads correctly. cta-2: heading offset FIXED (~5 px); "Get in Touch" link tiny, white over bright foliage at far right, low contrast; ref has no button, sun position: skipped (image).
- D10 / R2-8 footer: FIXED. Rows within ~3 px of ref.
- D11 colour tokens: FIXED, no drift.

## Responsive sanity (517 and 390)
Facts: single-column stacking works, no horizontal overflow, no clipped headings or buttons, text readable (body >=13px). Hamburger shows at 517/390. Observations (CSS-fixable): (1) Impact stats at 517/390: "3+" and "$500M+" sit on the bright sun and are low contrast; at 390 the "Capital Deployed / Committed" label wraps. (2) Insights cards have a large empty gap between title and Read more (min-height). (3) Footer nav wraps with orphan "Contact" and a big row gap (517: 6+1; 390: 4+3). (4) Nation map labels JAPAN/ACROSS JAPAC are tiny/faint and "ACROSS JA" clips at the right edge at 390. (5) Focus pillar grid leaves a lone orphan card in the last row (2-col). (6) Ventures carousel peeks the next card with clipped text (intentional carousel). (7) cta-1 and cta-2 stack with identical headings/copy at 517/390 (content duplication; ref has same). Not defects: hero, model, presence stack cleanly.

## Remaining, CSS-fixable only (priority)
1. Hero legibility: hero-loc, nav links, Watch Our Story, "Get in Touch" link on cta-2 -> text-shadow / slight top gradient (low contrast on bright image areas).
2. Ventures cards ~18 px shorter than ref (add card/body padding or min-height) and View all ~6 px high.
3. Insights .iimg height ~137px (from ~170) to match ref image height; more body padding so titles wrap to 3 lines.
4. Nation: map labels brighter/larger (12px, bolder); list shift right ~17 scaled px (~45 css) and down ~10 px; button ~6 px down.
5. Impact: heading ~4 px up-correct, stats row ~4 px down; contrast for stats over sun (text-shadow).
6. cta-1: heading ~6 px up, button ~11 px down and ~8 px right.
7. Presence row spacing ~15% looser; focus paragraph column/pillar copy size nits; nav y ~3 px.
8. Mobile: impact stat contrast, insights card empty gap, footer nav wrap/orphan, 390 nation label clipping.
Skipped (user constraint, image/colour): hero towers framing and water colour, impact saturation/hiker scale, ventures photos 2/5, insights/cta photos, nation/presence map imagery and icon glyphs, hamburger at desktop.
