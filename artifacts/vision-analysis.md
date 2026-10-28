# QuantLeap Vision Analysis

Source: reference/quantleap-reference.jpg, 517x1600 (unmodified). 3x upscaled slices saved in artifacts/comparisons/ref-slices/; section boundaries found by row-brightness jumps (Pillow/numpy) and checked visually. I read slices s0, s2 and s7 closely and the full image; the rest was judged from the full image plus pixel analysis. No similarity percentages computed; no tests run.

Observed = seen in image. Inferred = assumption.

## Global
- Observed: alternating cream (#f6f7f2) and navy (#001c2a, #01131f, footer #021523) bands plus photographic bands (hero, impact, two CTAs). Gold accent (~#f3c148) on buttons, italic emphasis, icons, stats, tagline.
- Observed: serif display headings with gold italic emphasis ("stronger JAPAC.", "sustainable JAPAC.", "progressive JAPAC."); small uppercase letter-spaced eyebrows; sans body.
- Observed: content container left x=28, right x~489 (ref px). Gold buttons have square corners and trailing arrow.
- Inferred: source viewport 1440 wide, scale 0.359, container ~1280px, page ~4457px tall.

## Sections (reference y-ranges)
| # | Section | y | h |
|---|---|---|---|
| 1 | Header (overlay) | 0-38 | 38 |
| 2 | Hero | 0-238 | 238 |
| 3 | Our Focus (cream) | 238-444 | 206 |
| 4 | Our Ventures (navy) | 444-671 | 227 |
| 5 | Nation Building (navy + map) | 671-844 | 173 |
| 6 | QuantLeap Model (cream) | 844-963 | 119 |
| 7 | Impact (photo) | 963-1064 | 101 |
| 8 | Latest Insights (cream) | 1064-1251 | 187 |
| 9 | Our Presence (navy + map) | 1251-1376 | 125 |
| 10 | CTA 1 (photo) | 1376-1463 | 87 |
| 11 | CTA 2 (photo) | 1463-1537 | 74 |
| 12 | Footer | 1537-1600 | 63 |

## Details
- Header: wordmark wide-tracked white at x28,y~14, gold tagline below; 7 nav links (Home gold underlined, Nation Building with chevron); hamburger at x~488. Transparent over hero.
- Hero: Marina Bay Sands and Gardens domes at golden hour with water reflection; dark navy gradient from left to ~x300. Eyebrow, 3-line serif H1 (last line gold italic), 3-line lead, gold CTA x27-108 y188-206, "Watch Our Story" with outlined play circle, top-right 4-line tagline list with 1px vertical rule at x~445, y45-76.
- Focus: H2 left, paragraph right of a thin divider (x~181-295); five ~85px-wide pillar cards (1px light border, subtle shadow, y~338-405) with gold line icons, uppercase labels and 4-line text.
- Ventures: H2 two lines; "View all ventures ->" right with gold underline; five cards y~514-655, photo ~58px then lighter navy body, small radius, 1px border; photos: glass towers dusk, tea leaves, warehouse, wind turbines sunset, rocks. Title bold white, muted tag line, description, "Learn more ->" y~643. Edge carousel chevrons. Cards 2-3 photos carry garbled AI-rendered text (artifact).
- Nation: night Asia-Pacific map with golden lights; labels INDIA (~203,737), JAPAN (~362,723), SINGAPORE (~290,818), ACROSS JAPAC (~338,790); right column x~410-500 with four ring-icon rows.
- Model: left heading/paragraph/link; steps spread x~175-490 at ~64px pitch with ~20px gold-outline circle icons and gold arrows between.
- Impact: hiker silhouette on right ridge, sunrise haze; left dark overlay; stats row y~1013-1040 with thin dividers, gold numbers.
- Insights: four ~110px white cards y~1127-1237, photo top ~42px, category label, bold title, "Read more ->".
- Presence: glowing world map in centre, four location rows at right with gold ring icons.
- CTAs: full-width mountain photos with left dark overlay; serif white heading; paragraph in two tones; CTA 1 has button right (x~388-451, y~1422-1440), CTA 2 none visible.
- Footer: logo + gold tagline, 7 centred links, 4 social icons right, legal links below, centred copyright.

## Too small / uncertain
- Pillar, step and article body text only partly legible (glyphs ~3px).
- CTA 1 heading garbled; CTA 2 button absent; fonts, shadows, radii, hover and carousel behaviour not determinable.
- The previous inventory pointed to a different reference filename (ref/ff363915...jpg); this version uses reference/quantleap-reference.jpg.
