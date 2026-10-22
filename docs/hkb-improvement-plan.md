# HKB Performance Improvements — Plan and Caveats

**Baseline:** commit `631de1e` (“Remove private working-copy notes from the README.”)  
**Date of plan:** 2026-10-22  
**Goal:** shell (nav + hero text + search + stats) usable in under ~1 s on a weak mobile link. Target critical path ~30–50 KB CSS/JS/HTML + one sized hero image.

## What went wrong on the first attempt

The earlier changes were applied as a series of partial rewrites. Several of them dropped supporting scripts or utility classes that the page still needed. The result was a broken homepage:

- Hero images stopped loading because the slide-building script was removed during a CSS/JS simplification.
- White hero text became unreadable against the solid green fallback.
- “Orders” and “Genera” labels ran together when flex spacing was missing from the purged CSS.
- Large-file API updates truncated `index.html` and `build_pages.py`, leaving incomplete content.

**Lesson:** do one change at a time, keep the page visually identical, and verify before the next step.

## Recommended order (safest first)

### 1. Hero: one image first
**Change:** Load only slide 0 with `loading="eager"` + `fetchpriority="high"`. Build the other 14 slides after `requestIdleCallback` or first interaction, with `loading="lazy"`.  
**Caveat:** Keep the existing `hkbPhotoUrl` call with the `"public"` variant. Flexible Cloudflare variants are not enabled on the account (ERROR 9429). Do not switch to width-limited URLs until that is turned on.  
**Risk:** Low, if the slide script and image IDs stay intact.

### 2. Homepage stats without full taxa.json
**Change:** Bake the six header counts into the HTML or ship a tiny `data/stats.json` (~100–250 B). Stop calling `hkbLoadTaxa()` on the homepage.  
**Caveat:** The counts must stay in sync with `taxa.json`. Add a build step (or the existing `qaqc.py` check) so a catalogue rebuild also refreshes the summary.  
**Risk:** Low. The homepage currently only uses the counts, not the full taxon array.

### 3. Purged Tailwind
**Change:** Build a purged `css/hkb.built.css` with the Tailwind CLI, scanning all HTML. Remove the Play CDN script and inline config. Link the built file with a content hash.  
**Caveat:** The purge must include every utility class actually used (flex gaps, text colours, shadows, responsive prefixes). After switching, open the homepage and the directory pages and confirm nothing is missing. Keep the CDN version available until the built file is verified. A full Tailwind CSS file can be stored in the repo as a temporary fallback if desired.  
**Risk:** Medium. Missing utilities caused the broken layout last time.

### 4. Fonts and icons
**Change:** Drop Google Fonts and Font Awesome. Use a system stack (PingFang TC / Noto Sans TC / Microsoft JhengHei for sans; Songti TC / Noto Serif TC for serif) and replace icons with a small inline SVG sprite.  
**Caveat:** System fonts render differently on Windows and Android. Test on a real device before removing the CDN links. If the stack is inconsistent, self-host a minimal WOFF2 subset instead.  
**Risk:** Low–medium. Visual only.

### 5. Slim search index
**Change:** Emit a slim `data/search.json` (short keys: blp, sci, chi, genus, family, rank) from the build. Use it on the search / species directory path instead of the full 735 KB `taxa.json`.  
**Caveat:** The species directory still needs the order hierarchy for browsing. Keep `taxa.json` for that. Map the short keys back to the names the rendering code expects. The full slim file is ~447 KB; the earlier remote push only stored a one-item sample because of API size limits — push it from the local machine.  
**Risk:** Medium. Larger refactor; easy to break search if the key mapping is incomplete.

### 6. QA/QC realign
**Change:** Treat JSON as the source of truth. `data/qaqc.py` checks that generated species HTML matches `pages.json` and can rewrite it with `--realign`.  
**Caveat:** Hand-edited showcase pages (no generated marker) are left alone. Run the check after every catalogue or page rebuild.  
**Risk:** Low.

## What not to do again

- Do not rewrite `index.html` while removing scripts that populate the hero or the stats.
- Do not assume a purged CSS file contains every class until the live page is checked.
- Do not use width-limited Cloudflare URLs until flexible variants are enabled.
- Do not push large JSON files through an API that truncates; use a local `git push`.

## Verification after each step

1. Hard-refresh the homepage on a throttled mobile connection.
2. Confirm the hero image appears and the text is readable.
3. Confirm the stats strip shows all six counts with correct spacing.
4. Confirm search still redirects and returns results.
5. Run `python3 data/qaqc.py`.

Only then move to the next item.
