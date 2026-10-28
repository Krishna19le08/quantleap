# QuantLeap Design Spec

Inputs: artifacts/vision-analysis.md, artifacts/section-inventory.json, reference/quantleap-reference.jpg (517x1600, unmodified).
Labels: **[O]** observed in the reference, **[I]** inferred or chosen. No tests were run to produce this spec and no similarity figures are claimed.

## 1. Scale assumption [I]
Reference is assumed to be a 1440px-wide desktop capture. Factor: 1 ref px = 2.79 css px (0.359). All css px values below are derived from ref measurements by this factor and rounded. Check them against the rendered page at 1440 and adjust where they disagree with the reference.

## 2. Tokens
Colors [O unless noted]
| Token | Value | Use |
|---|---|---|
| --navy | #001c2a | main dark bands, ventures, nation, presence |
| --navy-deep | #01131f | gradient end and deep overlays |
| --footer | #021523 | footer |
| --card-navy | #0a2a40 [I, estimated] | venture/location cards on navy |
| --cream | #f6f7f2 | light bands |
| --gold | #f3c148 | buttons, italic emphasis, icons, stats, tagline |
| --gold-hover | #e2ad2e [I] | button hover |
| --ink | #0b2233 [I] | text on cream |
| --muted-dark | rgba(255,255,255,.68) [I] | body text on navy |
| --muted-light | #4a5b66 [I] | body text on cream |
| --line-dark | rgba(255,255,255,.14) [I] | 1px borders on navy |
| --line-light | rgba(0,28,42,.12) [I] | 1px borders on cream |
The existing stylesheet uses #08172e/#f0b429/#f8f5ee. Replace them with the observed values above.

Other tokens [I]: radius 0 on buttons (square, observed), 3px on cards; card shadow on cream `0 6px 20px rgba(0,28,42,.08)`; transition 200ms ease; z-index scale: header 100, menu 200, modal 300.

## 3. Typography
The reference is too small to identify fonts [O: serif display headings, sans body]. Choices are [I]:
- Display: `'Playfair Display', 'Cormorant Garamond', Georgia, 'Times New Roman', serif`, weight 400-500.
- Body/UI: `'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`.
- Fonts must have fallbacks that do not break layout if the webfont fails (use `font-display: swap`).

Scale at 1440 (clamp for smaller widths):
| Role | Size | Line height | Notes |
|---|---|---|---|
| H1 hero | clamp(40px, 4.6vw, 66px) | 1.08 | 3 lines; last line gold italic |
| H2 | clamp(30px, 3.2vw, 46px) | 1.15 | gold italic tail (em) where the reference shows it |
| H3 card title | 18-20px sans bold | 1.3 | |
| Eyebrow | 12px, uppercase, letter-spacing .2em, gold on navy / ink-gold on cream | | |
| Lead | 17-18px | 1.6 | |
| Body | 15-16px | 1.65 | |
| Small/label | 12-13px uppercase tracking .14em | | pillar and step labels |
| Stat number | clamp(36px, 3.6vw, 52px) serif gold | 1 | |
| Nav | 13-14px, tracking .04em | | |
| Wordmark | 22-26px, tracking .3em, white | | tagline 11px gold below |

## 4. Widths and grid
- Container: left x=28, right x=489 of 517 [O]; content width = 461/517 = 89% of viewport. At 1440 this is about 1280px [I]. Use `width:min(1280px, 100% - 48px)`, centred.
- Side padding at <=900px: 24px; at <=480px: 20px.
- Grid: 12 columns, 24px gutter [I]. Specific layouts below.
- Max page width: content capped at 1280px; photo bands are full-bleed.

## 5. Section vertical rhythm
Heights from the reference at 2.79x [I]; use as targets, not minimums, so content may push them taller.
| Section | Ref h | Target css h (1440) | Padding (top/bottom) |
|---|---|---|---|
| Hero | 238 | ~664 (min-height 640, 100svh capped) | header offset 120 top, 80 bottom |
| Focus | 206 | ~575 | 96 / 96 |
| Ventures | 227 | ~633 | 96 / 96 |
| Nation | 173 | ~483 | 80 / 80 |
| Model | 119 | ~332 | 72 / 72 |
| Impact | 101 | ~282 | 64 / 64 |
| Insights | 187 | ~522 | 88 / 88 |
| Presence | 125 | ~349 | 72 / 72 |
| CTA 1 | 87 | ~243 | 64 / 64 |
| CTA 2 | 74 | ~206 | 56 / 56 |
| Footer | 63 | ~176 | 48 / 32 |
Section padding on <=900px: reduce by about 35%.

## 6. Components
- **Gold button**: bg --gold, text --navy, uppercase 12-13px tracking .1em weight 600, padding 16px 28px, radius 0, trailing arrow "→" with 8px gap. Hover: --gold-hover, arrow shifts 4px right. Focus: 2px outline gold, 3px offset. Min height 48px.
- **Text link with arrow**: gold on navy, ink on cream, 1px gold underline offset 6px, arrow trailing.
- **Watch Our Story**: white text, 44px circle outline (1px white 60%), play triangle centred, hover fills gold.
- **Eyebrow**: see typography.
- **Pillar card** [O: ~85 ref px wide = ~237 css px, y 338-405 = ~187 css px tall]: 1px --line-light border, shadow, padding 20px, gold line icon 32px, uppercase label, ~4 lines body 13px.
- **Venture card** [O: 5 cards, photo ~58 ref = ~160 css px, body lighter navy, 1px border, small radius]: photo 16:9 crop or fixed 160px with object-fit cover; body padding 20px; title bold white 17px; tag muted 12px; description 13px; "Learn more →" gold. Card height equal across row.
- **Carousel**: chevron buttons 40px circle at left/right edges (x~8, x~511 in reference), keyboard operable, scroll-snap. 5 cards visible at 1440; 3 at <=1100; 1.2 at <=640.
- **Ring icon row** (nation, presence): 44px gold ring icon, title bold, subtext muted; rows separated by 1px line.
- **Step** (model): ~56px gold-outline circle with icon, label below uppercase 12px; gold "→" between steps (hidden when wrapped).
- **Stat**: gold serif number, label muted 12px; 1px vertical dividers between, 5 columns.
- **Insight card**: white, photo top (~42 ref = ~117 css px, crop 16:9), padding 20px, category eyebrow gold-dark, bold title, "Read more →".

## 7. Image cropping
Source images in assets/images/ (hero/cta 2172x724 ultrawide; others 1672x941; venture-5 only 624x366, upscaled, may look soft; do not display above 100% of its 360px card width).
- Hero: `background-size: cover; position: 65% center` so the Marina Bay domes sit right of the text; overlay `linear-gradient(90deg, rgba(0,28,42,.92) 0, rgba(0,28,42,.75) 40%, transparent 75%)`.
- Impact: cover, position right center so the hiker ridge stays at right; left overlay as hero.
- CTA 1/2: cover, position center; left overlay.
- Map backgrounds (map-bg.jpg, presence-map.jpg): cover, position center, opacity as needed over --navy; keep labels as real HTML text on top.
- Venture and insight photos: `aspect-ratio:16/9; object-fit:cover`.
- Ventures 2-3 in the reference contain garbled AI text [O]. The project images must not contain text; do not reproduce garbled text.
- Alt text meaningful for content images; decorative backgrounds are CSS, no alt.

## 8. Header and footer
Header [O: transparent overlay on hero, y 0-38 ref = ~106 css px]
- Position absolute/fixed top, transparent over hero; gains solid --navy at 90% opacity with backdrop blur after 40px scroll [I].
- Left: QUANTLEAP wordmark (white, tracked) with gold tagline "Leap beyond the now." below.
- Centre/right: 7 links: Home (gold, 2px gold underline, active), About, Our Ventures, Nation Building (with chevron, dropdown), Insights, Ecosystem, Contact. Hamburger at far right [O] opens components/menu.html overlay.
- At <=1100px, hide the links and show only the hamburger [I].
Footer [O]
- Background --footer. Row 1: logo + gold tagline left; 7 links centred (Home underlined); 4 social icons right (24px, outline, hover gold). Row 2: Privacy Policy, Terms, Sitemap. Row 3 centred: "© 2025 QuantLeap. All rights reserved." Hairline 1px --line-dark between rows.
- Mobile: stack, centre, links wrap in 2 columns.

## 9. Breakpoints
Desktop-first; the reference only shows desktop. All mobile/tablet behaviour is **[I]**.
- >=1281: as spec.
- 1101-1280: container 100% - 48px; venture cards 4 visible.
- <=1100: nav collapses to hamburger; pillars 3+2, ventures 3 visible, insights 2x2, stats 3+2.
- <=900: Focus, Nation, Model, Presence stack in one column; step arrows hidden, steps wrap 3+2; hero padding reduced.
- <=640: one column everywhere; venture carousel 1.2 cards; pillars 1 column; stats 2 columns; buttons full-width; min tap target 44px.
- <=375: H1 minimum 36px; no horizontal scroll.
Test widths: 375, 768, 1024, 1440, 1920.

## 10. Per-section requirements
**Header** - R1 transparent over hero at top; R2 7 links with exact labels; R3 Home gold + underline; R4 Nation Building has chevron and dropdown; R5 hamburger visible at far right and operable by keyboard; R6 wordmark left with gold tagline.

**Hero** - R1 photo of Marina Bay Sands/Gardens by the Bay with left navy gradient to ~58% width; R2 eyebrow "QUANTLEAP"; R3 serif H1 on 3 lines, final line "stronger JAPAC." gold italic; R4 lead copy 3 lines max at 1440; R5 gold button "Explore Our Ventures →" and "Watch Our Story" with outlined play circle; R6 top-right 4-line list SINGAPORE / → INDIA / → JAPAC / → A STRONGER TOMORROW with 1px vertical rule at its left; R7 content left-aligned at container edge.

**Our Focus** - R1 cream bg; R2 eyebrow "OUR FOCUS"; R3 H2 "Technology, capital and human potential for a sustainable JAPAC." with "sustainable JAPAC." gold italic; R4 paragraph in right column after a thin vertical divider; R5 five pillar cards in one row at 1440: Capital, Technology & AI, Markets, Sustainability, Ecosystems; each with gold line icon, uppercase label, ~4-line text, 1px border and soft shadow.

**Our Ventures** - R1 navy bg; R2 eyebrow + H2 "Bold ideas. Real impact." on two lines; R3 "View all ventures →" top right with gold underline; R4 five cards in a row: TransBnk, Kradin Tea, K Now, CloudGrid/UrjaSetu, RareEarths with photos (glass towers, tea leaves, warehouse, wind turbines, rocks); R5 each card title, tag line, description, "Learn more →"; R6 carousel chevrons at both edges; R7 equal card heights.

**Nation Building** - R1 navy with night Asia-Pacific map background; R2 H2 "Technology for an inclusive, resilient and progressive JAPAC." with "progressive JAPAC." gold italic; R3 paragraph and gold button "Our Nation Building Initiatives →"; R4 map labels INDIA, JAPAN, SINGAPORE, ACROSS JAPAC positioned over the map as HTML; R5 right column (about 25% width) with four ring-icon rows: Digital Economy, Green Transition, Skills & Education, Inclusive Growth.

**QuantLeap Model** - R1 cream; R2 left column: eyebrow "THE QUANTLEAP MODEL", H2 "From vision to lasting value.", paragraph, "Our model →"; R3 right: five steps Ideate, Build, Capitalise, Scale, Compound with gold outline circle icons and gold arrows between, even pitch; R4 labels uppercase.

**Our Impact** - R1 sunrise hiker photo, hiker on right; R2 left dark overlay for legibility; R3 eyebrow "OUR IMPACT", H2 "Building a more prosperous JAPAC."; R4 five stats in a row with thin dividers: 10+ Active Ventures, 3+ Countries, 50+ Founders & Teams, $500M+ Capital Deployed / Committed, 1B+ Lives Impacted (est.); R5 numbers gold serif.

**Latest Insights** - R1 cream; R2 H2 "Ideas, analysis and perspectives for what's next."; R3 "View all insights →" right; R4 four white cards in a row with photo top: skyline (NATION BUILDING), AI network (TECH & AI), wind turbines (CLIMATE), schoolchildren (IMPACT); R5 category label, bold title, "Read more →".

**Our Presence** - R1 navy with glowing world map; R2 H2 "Singapore. India. JAPAC. And beyond."; R3 paragraph and gold "Our Ecosystem →"; R4 map in centre with gold nodes; R5 right column four ring-icon rows: Singapore (Regional Headquarters), India (Operations & Partnerships), JAPAC (Investments & Co-Creation), Global (Strategic Alliances).

**CTA 1** - R1 mountain valley sunrise photo with left overlay; R2 serif white heading (reference text garbled; use a sensible heading such as "Singapore. India. JAPAC. Let's talk about what's next." [I], confirm with owner); R3 two-line paragraph; R4 gold "Get in Touch →" at right, vertically centred.

**CTA 2** - R1 misty mountains photo, left overlay; R2 heading "Let's build what's next."; R3 paragraph "Partner with us in building ventures, investing in opportunities and creating lasting impact across JAPAC." in two tones; R4 no button in reference [O: none visible]; a button may be added only if flagged as a deviation.

**Footer** - see section 8.

## 11. Open items
Exact fonts, shadows, radii, hover/carousel behaviour, CTA 1 heading and CTA 2 button cannot be determined from the 517px reference. Mobile and tablet layouts are inferred.
