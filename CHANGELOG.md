# Changelog

All notable changes to [Hong Kong Botanica](https://benjaminficusmicrocarpa.github.io/hkb/) are recorded here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Ten species pages: *Liquidambar formosana* (45002), *Delonix regia* (47029), *Rhaphiolepis indica* (49028), *Ficus pumila* (49591), *Bruguiera gymnorhiza* (55050), *Vernicia montana* (55919), *Bombax ceiba* (61065), *Thespesia populnea* (61083), *Camellia hongkongensis* (67603), *Mussaenda pubescens* (71031).
- Species-page photo index grows from 80 to 310 images, then sixteen reviewed plates are removed (294 remain). Remaining codes are not renumbered.

### Changed

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
