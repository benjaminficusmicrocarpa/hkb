# Changelog

All notable changes to [Hong Kong Botanica](https://benjaminficusmicrocarpa.github.io/hkb/) are recorded here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- The 22 new species pages now show the IPNI publication under the scientific name, from the local WCVP row for that page binomial.
- Eleven further species pages: 橄欖, 銀珠, 桂花, 毛葉桉, 桂木, 藍花楹, 阿江欖仁, 香椿, 土蜜樹, 杉氏爵床, 斷腸草. Plate count follows the Best frames that are not the same state. 毛葉桉 and 藍花楹 use a cropped banner because the flower frame is vertical. The taxonomic tree marks every species that has a page.
- The first new species pages follow the Best-frame rule, not a quota of 14. 蒲桃 is 20 plates. 白蠟樹 stays at 5. The Project Overview photograph is a Kadoorie Farm overlook, not a stock image.
- Eleven species pages from the local Flora of Hong Kong extract: *Uvaria calamistrata* (25206), *Dichanthium annulatum* (38299), *Peltophorum pterocarpum* (47056), *Mallotus apelta* (55908), *Flueggea virosa* (56523), *Syzygium jambos* (58370), *Myrsine seguinii* (67400), *Ehretia acuminata* (73001), *Fraxinus chinensis* (75031), *Clerodendrum cyrtophyllum* (76623), *Callicarpa kochiana* (76626). New plates are short side 720. The hero is a landscape flower or spikelet frame.
- Taxonomic tree page: collapsible outline and column browser, from the catalogue placed on APG V, PPG, and Yang, Ferguson et al. (2022). Chinese names sit beside the Latin names where the export gives one. The detail panel lists every lower rank under the selection. Family limits on that page are not the Families & Genera filing list.
- Ten species pages: *Liquidambar formosana* (45002), *Delonix regia* (47029), *Rhaphiolepis indica* (49028), *Ficus pumila* (49591), *Bruguiera gymnorhiza* (55050), *Vernicia montana* (55919), *Bombax ceiba* (61065), *Thespesia populnea* (61083), *Camellia hongkongensis* (67603), *Mussaenda pubescens* (71031).
- Species-page photo index grows from 80 to 310 images, then sixteen reviewed plates are removed (294 remain). Remaining codes are not renumbered.
- The first twenty species pages gain 170 plates (80 to 250) so the set covers bark, venation, stipules, glands, stamens, seeds, and other parts the four-plate set left out. The page list was 464 images. Codes already on a page are not renumbered.
- Five species pages: *Podocarpus macrophyllus* (18050), *Phoenix loureiroi* (34000), *Miscanthus floridulus* (38240), *Drosera spatulata* (64302), *Arundina graminifolia* (32014). The page list is 508 images. Code 38240c was removed before publish and is not reused.

### Changed

- Species-page heroes use a flower, fruit, autumn colour, or a wide stand, not a trunk. A portrait source is cropped to a 12:5 banner before resize (`hkb-{blp}-hero`); landscape plates stay the hero id. Codes 67415i and 49591b are removed and not reused.
- Species photographs are filed as `{blp}{letter}` (a–z, then aa, ab, …). The carousel shows that code in both the contracted and enlarged views. The plate note is `description` in `species_page_images.json`.
- Shell pages (`index`, `search`, `species` directory, `families`, `about`) load Google fonts: Roboto and Noto Sans TC for sans, Playfair Display and Noto Serif TC for serif.
- `data/build_pages.py` emits the Tailwind Play CDN, those Google fonts, and Font Awesome for newly generated species pages. Existing species pages still use `hkb.built.css` until they are rebuilt.

## [2026-10-22] — Performance pass

Baseline restored to `631de1e`, then the six improvements from [`docs/hkb-improvement-plan.md`](docs/hkb-improvement-plan.md) were applied in one checked commit (`c17c5b5`).

### Added

- `css/hkb.built.css` — purged Tailwind build (~27 KB) for the main shells
- `data/stats.json` — tiny header counts for the homepage and search page
- `data/search.json` — slim search index (short keys; full catalogue, ~557 KB)
- `data/qaqc.py` — JSON/HTML alignment check (`python3 data/qaqc.py`; `--realign` rewrites generated species HTML)
- `js/taxa.js` — `hkbLoadSearch()` maps slim rows back to the names the UI expects
- `docs/hkb-improvement-plan.md` — plan, caveats, and safe order

### Changed

- **Hero:** first slide loads eager with `fetchpriority="high"`; remaining slides use `data-src` and load on `requestIdleCallback` or first interaction. Image URLs keep the Cloudflare `"public"` variant (flexible width variants are not enabled on the account).
- **Homepage / search counts:** read `data/stats.json` instead of downloading full `data/taxa.json`.
- **CSS:** main shells (`index`, `search`, `species` directory, `families`, `about`) link the purged file and drop the Tailwind Play CDN.
- **Fonts:** system stack (PingFang TC / Noto Sans TC / Microsoft JhengHei; Songti TC / Noto Serif TC for serif) instead of Google Fonts.
- **Icons:** Font Awesome CDN removed on those shells; inline SVG sprite instead.
- **`data/build_taxa.py`:** also writes `stats.json` and `search.json` when the catalogue is rebuilt.
- **`data/build_pages.py`:** generated species pages point at `hkb.built.css` instead of the Tailwind CDN.

### Fixed / restored

- `main` was force-reset to `631de1e` (“Remove private working-copy notes from the README.”) to undo the earlier broken performance attempt (truncated HTML, missing hero script, purged-CSS gaps, API-truncated `search.json`).
- The improvement plan was re-added on top of that baseline as `d3e724f`, then the careful one-pass implementation landed as `c17c5b5`.

### Notes

- The species directory still loads `data/taxa.json` for order / family hierarchy. Slim `search.json` is available for search-shaped loads via `hkbLoadSearch()`.
- Do not switch hero images to width-limited Cloudflare URLs until flexible variants are enabled.
- After changing the catalogue workbook, run `python3 data/build_taxa.py` so `taxa.json`, `stats.json`, and `search.json` stay in sync, then `python3 data/qaqc.py`.

### Verification checklist

1. Hard-refresh the homepage on a throttled mobile connection.
2. Confirm the hero image appears and the text is readable.
3. Confirm the stats strip shows all six counts with correct spacing.
4. Confirm search still redirects and returns results.
5. Run `python3 data/qaqc.py`.

[Unreleased]: https://github.com/benjaminficusmicrocarpa/hkb/compare/c17c5b5...HEAD
[2026-10-22]: https://github.com/benjaminficusmicrocarpa/hkb/commit/c17c5b5
