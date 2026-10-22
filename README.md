# Hong Kong Botanica

香港草木誌. A personal record of the vascular flora of Hong Kong: native, naturalised, and exotic taxa.

The site is at https://benjaminficusmicrocarpa.github.io/hkb/

GitHub Pages serves the files on `main`. There is no build step on GitHub, and no site framework. HTML is written on this machine and committed.

## Catalogue

The species directory and the family list are driven by `data/taxa.json`. That file is a taxon list only: name, rank, genus, family, order. It does not hold photographs.

`data/build_taxa.py` rebuilds it from the BLP catalogue workbook. Run that script when the workbook changes, then commit `data/taxa.json`.

The directory does not become one HTML file per taxon. A taxon with no written page stays a row in the list.

## Species pages

Written pages live in `data/pages.json`. The page address is the five-digit BLP number, for example `species/49562.html`.

Do not edit those HTML files by hand. After changing `data/pages.json`, run:

```
python3 data/build_pages.py
```

Commit the HTML files it writes, and `data/page-ids.json`. The directory uses that small index to know which rows have a page. Add a page to `pages.json` only when a dedicated page was asked for.

Three older pages are hand-written and are not generated: `species/bauhinia-blakeana.html`, `species/rhododendron-simsii.html`, and `species/mucuna-birdwoodiana.html`. Leave them alone. The generator will not overwrite a file it did not write.

`species/detail.html` and the short slug files only redirect to the numbered page.

## Photographs

Species photographs are hosted on Cloudflare Images. The HTML stores an image id, not a file in this repository.

Do not commit `~photos/` or `~original-jpg/`. They are local working copies. `data/host_page_photos.py` uploads them. Credentials stay in `.env` in this folder, which is not committed. After an image id changes, run `build_pages.py` again so the static page picks it up.

The share card for the site is `og.png`.

## What is not published

`.env`, `~photos/`, `~original-jpg/`, and `_parked/` stay on this machine.
