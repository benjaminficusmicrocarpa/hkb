# Changelog

A dated log of what changed on [Hong Kong Botanica](https://benjaminficusmicrocarpa.github.io/hkb/) and what was pushed to GitHub. Newest first. Times are Hong Kong time.

This is not an undated Unreleased list. Each entry names the clock time, whether the live site changed, and the commit that was pushed. A push that does not change a page says so.

The site repo is [benjaminficusmicrocarpa/hkb](https://github.com/benjaminficusmicrocarpa/hkb). On the morning of 22 October the same URL was still a folder of [benjaminficusmicrocarpa.github.io](https://github.com/benjaminficusmicrocarpa/benjaminficusmicrocarpa.github.io). Those pushes are marked below.

Photo counts are rows in `species_page_images.json` at that commit.

## 2026-11-01

- 09:47 committed, pushed 09:48. Commit `00e3317`, “Add the database buttons to the twenty-two newer species pages.” Remote `main` is this commit.
- Website: the 22 species pages added on 31 October gained the same database buttons as the earlier pages: HKCWW, Hong Kong Herbarium, GBIF, POWO, WFO, WFO List, and CVH. 毛葉桉 (`58392`) CVH uses the stored SP2000 name *Eucalyptus torelliana*. 阿江欖仁 (`58005`) has no CVH button. Photo count stayed 718.
- Checked live: https://benjaminficusmicrocarpa.github.io/hkb/species/58392.html shows the HKCWW button and that CVH link.

## 2026-10-31

- 14:33 committed, pushed 14:34. Commit `b25ad9a`, “Add twenty-two species pages, flowering heroes, and the IPNI name citations.”
- Website: 22 new species pages. Photo count 508 to 718. Each page shows the IPNI publication under the scientific name. The taxonomic tree marks every species that has a page.
- The 22 pages: 刺果紫玉盤 *Uvaria calamistrata* (`25206`), 雙花草 *Dichanthium annulatum* (`38299`), 雙翼豆 *Peltophorum pterocarpum* (`47056`), 銀珠 *Peltophorum tonkinense* (`47144`), 桂木 *Artocarpus parvus* (`49575`), 白背葉 *Mallotus apelta* (`55908`), 土蜜樹 *Bridelia tomentosa* (`56507`), 白飯樹 *Flueggea virosa* (`56523`), 阿江欖仁 *Terminalia arjuna* (`58005`), 蒲桃 *Syzygium jambos* (`58370`), 毛葉桉 *Corymbia torelliana* (`58392`), 橄欖 *Canarium album* (`60000`), 香椿 *Toona sinensis* (`60503`), 密花樹 *Myrsine seguinii* (`67400`), 斷腸草 *Gelsemium elegans* (`71750`), 厚殼樹 *Ehretia acuminata* (`73001`), 桂花 *Osmanthus fragrans* (`75013`), 白蠟樹 *Fraxinus chinensis* (`75031`), 杉氏爵床 *Justicia championii* (`75839`), 藍花楹 *Jacaranda mimosifolia* (`76204`), 大青 *Clerodendrum cyrtophyllum* (`76623`), 枇杷葉紫珠 *Callicarpa kochiana* (`76626`).
- Homepage: the Project Overview photograph left the stock image and now uses the Kadoorie Farm overlook (`hkb-about-kfbg-overlook`). The first hero slide left the 細葉榕 trunk and now uses the canopy figs.
- Species heroes on this pass use a flower, fruit, autumn colour, or a wide stand, not a trunk. A portrait source is cropped to a 12:5 banner before resize. 毛葉桉 and 藍花楹 use that cropped banner. Codes `67415i` (桐花樹) and `49591b` (薜荔) were removed and are not reused.

## 2026-10-29

- 00:10 committed and pushed the same minute. Commit `77a90b4`, “Add a taxonomic tree with Chinese names beside the Latin names.” GitHub push record: 28 October 16:10 UTC, `f3a9039` to `77a90b4`.
- Website: new page at `taxonomy/`. Collapsible outline and column browser. Chinese names sit beside the Latin names. The detail panel lists every lower rank under the selection. Family limits on that page are not the Families & Genera filing list. Shell nav points at the tree. Photo count stayed 508. No new species page.

## 2026-10-27

- 08:28 committed and pushed the same minute. Commit `f3a9039`, “Add five species pages for a conifer, a palm, a grass, a sundew, and an orchid.” GitHub push record: 00:28 UTC, `18e964c` to `f3a9039`.
- Website: 羅漢松 *Podocarpus macrophyllus* (`18050`), 竹葉蘭 *Arundina graminifolia* (`32014`), 刺葵 *Phoenix loureiroi* (`34000`), 五節芒 *Miscanthus floridulus* (`38240`), 寬苞茅膏菜 *Drosera spatulata* (`64302`). Photo count 464 to 508. Code `38240c` is not on the published 五節芒 page and is not reused.

## 2026-10-25

- 21:27 committed and pushed the same minute. Commit `18e964c`, “Add 170 plates to the first twenty species pages.” GitHub push record: 13:27 UTC, `08b31d8` to `18e964c`.
- Website: the first twenty species pages gained 170 plates (photo count 294 to 464), covering bark, venation, stipules, glands, stamens, seeds, and other parts the short set left out. No new species page. Codes already on a page were not renumbered.

## 2026-10-24

- 00:17 two commits, pushed 00:19. GitHub push record: 23 October 16:19 UTC, `a15194a` to `08b31d8`.
- Commit `b4b93d0`, “Name each species photograph by its BLP code and remove sixteen reviewed plates.” Website: each plate is filed as the BLP number plus a letter (`a`–`z`, then `aa`, `ab`, …). The carousel shows that code in the contracted and enlarged views. Sixteen reviewed plates were removed (photo count 310 to 294), from 石斑木, 薜荔, 木油樹, 木棉, 恆春黃槿, and 玉葉金花. Remaining codes were not renumbered.
- Commit `08b31d8`, “Ignore the local preview script.” No website change. The ignore rule only keeps the local script out of the repo.

## 2026-10-22

The URL did not move. The files did: morning pushes were the parent site; from 08:20 the project repo serves that URL.

- 00:05 parent repo, pushed 00:05. Commit `1e3bc07`, “Publish Hong Kong Botanica species pages and serve the photographs from Cloudflare Images.” GitHub push record on `benjaminficusmicrocarpa.github.io`: 21 October 16:05 UTC. Website: the species pages went live under `/hkb/`, photographs from Cloudflare Images.
- 00:12 parent repo, pushed 00:12. Commit `672fc63`, “Add the Hong Kong Botanica logo as the link preview image.” The share card is `og.png`.
- 00:26 parent repo, commit `b60addb`, “Name the classification system on each species page.” Website: each species page names the classification system. This commit was already the parent remote tip when the folder was removed at 08:21. The public push feed does not give a separate clock time for this push.
- 08:19 this repo, first commit `39cc33f`, “Publish Hong Kong Botanica as its own site.” GitHub created the repo at 08:20. Website, once this repo was the one served: twenty species pages (馬尾松, 樟, 露兜樹, 白花油麻藤, 細葉榕, 水筆仔, 黃牛木, 海漆, 白楸, 秋楓, 桃金娘, 毛稔, 銀葉樹, 土沉香, 桐花樹, 木荷, 梔子, 絡石, 草海桐, 鴨腳木), the directory, families, search, and about. Three older hand-written pages stay beside the numbered pages: `bauhinia-blakeana.html`, `rhododendron-simsii.html`, and `mucuna-birdwoodiana.html`. Photo count 80.
- 08:21 parent repo, pushed 08:21. Commit `26e1e9a`, “Move Hong Kong Botanica to its own repository.” The `hkb/` folder left the parent site. The URL is the project site from here on.
- 08:23 pushed `3d75d85`, “Add a README for the Hong Kong Botanica site.” No page change.
- 08:27 pushed `631de1e`, “Remove private working-copy notes from the README.” No page change. The public README no longer names local folders.
- 13:59–15:53 a run of performance commits was pushed to `main` (hero lazy-load, `stats.json`, purged CSS, system fonts, a slim search index, `data/qaqc.py`, and two doc files, `docs/hkb-update-log.md` and `docs/hkb-outstanding.md`). The homepage broke on that run: the hero script was dropped, stats labels collided, and the remote search file was a one-item sample. Those commits are not on `main` now.
- 19:06 force-pushed `main` back to `631de1e` (remote tip had been `1042684`). That undid the broken run, including the update log. Then pushed `d3e724f`, “docs: performance improvement plan with caveats.” The plan is `docs/hkb-improvement-plan.md`. No page change.
- 19:11 pushed `c17c5b5`, “perf: apply homepage improvements in one carefully checked pass.” Website: the first hero slide loads immediately and the rest wait; homepage and search counts read `data/stats.json` instead of the full catalogue; the shells (`index`, `search`, species directory, `families`, `about`) use the purged CSS, a system font stack, and inline icons, and drop the Tailwind Play CDN and Font Awesome. The species directory still loads `data/taxa.json` for the order and family tree.
- 19:13 pushed `30b9420`, “docs: add CHANGELOG for the 2026-10-22 performance pass.” No page change. That file is the one this log replaces: it dated only the performance pass and left every later change in Unreleased.
- 22:27 pushed `0151e30`, “Bake EXIF orientation into species-page photos before Cloudflare upload.” No page change. The upload script now applies the camera orientation before resize. The five corrected photos had already been replaced on Cloudflare.
- 23:44 committed and pushed the same minute. Commit `a15194a`, “Publish ten species pages and switch shells to Roboto and Playfair Display.” The public push feed does not list this push; the 24 October push records `a15194a` as the previous remote tip, and the push was confirmed against `origin/main` at 23:44.
- Website: ten new pages — 楓香 *Liquidambar formosana* (`45002`), 鳳凰木 *Delonix regia* (`47029`), 石斑木 *Rhaphiolepis indica* (`49028`), 薜荔 *Ficus pumila* (`49591`), 木欖 *Bruguiera gymnorhiza* (`55050`), 木油樹 *Vernicia montana* (`55919`), 木棉 *Bombax ceiba* (`61065`), 恆春黃槿 *Thespesia populnea* (`61083`), 香港茶 *Camellia hongkongensis* (`67603`), 玉葉金花 *Mussaenda pubescens* (`71031`). Photo count 80 to 310.
- This push reversed the 19:11 font change. The shells load Google fonts again: Roboto and Noto Sans TC for sans, Playfair Display and Noto Serif TC for serif. Newly generated species pages use the Tailwind Play CDN, those fonts, and Font Awesome. The system-font stack from the performance pass is not what the site serves.
