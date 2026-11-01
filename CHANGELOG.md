# Changelog

A dated log of what changed on [Hong Kong Botanica](https://benjaminficusmicrocarpa.github.io/hkb/) and what was pushed to GitHub. Newest first. Times are Hong Kong time.

This is not an undated Unreleased list. Each entry names the clock time, whether the live site changed, and the commit that was pushed. A push that does not change a page says so.

The site repo is [benjaminficusmicrocarpa/hkb](https://github.com/benjaminficusmicrocarpa/hkb). On the morning of 22 October the same URL was still a folder of [benjaminficusmicrocarpa.github.io](https://github.com/benjaminficusmicrocarpa/benjaminficusmicrocarpa.github.io). Those pushes are marked below.

Photo counts are rows in `species_page_images.json` at that commit.

## 2026-11-01

- 23:52 committed, pushed 23:52. Commit `3694c84`, “Rewrite the taxonomic tree introduction, drop the repeated fern suborders, and add the compare page.” Website changes. The taxonomic tree introduction is the new English and Chinese text. A fern suborder is no longer also listed as a clade. Polypodiales is one order, 185. Lindsaeineae, Pteridineae, Dennstaedtiineae, Aspleniineae and Polypodiineae each appear once, as a suborder. New page at compare/. The header and the mobile drawer on every live page link to it. Two published accounts, lined up by label. Photo count unchanged. Species count stays 100. The local morphology heading rewrite was not in this push.
- 22:09 committed, pushed 22:09. Commit `0ff051b`, “Replace nine frozen plates and add nine organ plates.” Website changes. Nine ids that the 21:11 caption rewrite left on the first upload were deleted and posted again, so the carousel matches the sentence. Those nine were already live before this HTML, because the page already requested the id. Photo count 953 to 962. Species count stays 100. One extra organ plate where the page did not already show that state. Not a match to the longer pages.
- Replaced, same id: `51005d` leaves, `24051c` colony, `25050b` small tree, `25050c` two flowers, `29051e` female spikes, `36424d` leafy pseudostems, `60274e` spine and buds, `68008e` young capsules, `78101c` male flowers.
- Added: `78110g` ripe red fruit, `67167g` ripe and green fruit, `47006g` open flower, `54151g` fringed raceme, `67156g` open capsules, `26138g` leaf base with three veins, `78101g` impressed veins, `29051g` netted veins, `61056g` red young leaves. The new plates appear when Pages serves this commit.
- 21:11 committed, pushed 21:12. Commit `16f4ba3`, “Rewrite today's species captions from the joined frames and drop the hand and label plates.” Website changes. Today's 43 species pages: each caption is a sentence in both languages, written from the vision note of that frame. Keyword dumps and untranslated Chinese are off the page. Chinese morphology, facts, and ecology on the 21 draft pages are translated from the English already there. Photo count 958 to 953. Species count stays 100. The 19:29 line that hands, labels, and tags were left off was wrong. This push removes those plates. The letters are not reused.
- Removed: `20001c`, `24051b`, `29051c`, `45054a`, `45054b`, `47006c`, `47006f`, `53012c`, `54151a`, `54151d`, `61056e`, `67156c`, `67156d`, `67167c`, `67167f`, `67761b`, `68008a`, `75208d`, `78101a`, `78110a`, `78110f`.
- Added 16 plates: `20001d`, `20001e`, `24051d`, `24051e`, `25050e`, `25050f`, `29051f`, `36424e`, `45054g`, `51005e`, `51005f`, `60274f`, `68008f`, `78101d`, `78101e`, `78101f`.
- The banners for 紅花荷, 香港杜鵑, and 兩面針 were replaced on the same Cloudflare id before this push, so those three headers can change before the new HTML is served. The new sentences and plates appear when Pages serves this commit.
- 19:29 committed, pushed. Thirty-two new species pages (batches 2 and 3) with dedicated 12:5 Cloudflare heroes (`hkb-{blp}-hero`), 192 plates, photo count 766 to 958. Species count 68 to 100. The note that hands, labels, and tags were left off was wrong; the 21:11 entry removes them. Heroes on that pass used flower, fruit, autumn colour, or a wide stand, except the three replaced above.
- Batch 2 (11): 鐵冬青 *Ilex rotunda* (`78110`), 浙江潤楠 *Machilus chekiangensis* (`26150`), 山杜英 *Elaeocarpus sylvestris* (`54154`), 圓葉豺皮樟 *Litsea rotundifolia* var. *oblongifolia* (`26133`), 吊鐘花 *Enkianthus quinqueflorus* (`68010`), 艾膠算盤子 *Glochidion lanceolarium* (`56509`), 厚葉山礬 *Symplocos lucida* (`67763`), 細齒葉柃 *Eurya nitida* (`67167`), 樹頭菜 *Crateva unilocularis* (`62152`), 紅花荷 *Rhodoleia championii* (`45054`), 假蘋婆 *Sterculia lanceolata* (`61057`).
- Batch 3 (21): 野漆樹 *Toxicodendron succedaneum* (`60058`), 粗脈桂 *Cinnamomum validinerve* (`26138`), 木薑子 *Litsea cubeba* (`26114`), 刨花潤楠 *Machilus pauhoi* (`26151`), 小葉青岡 *Cyclobalanopsis myrsinifolia* (`51017`), 小果皂莢 *Gleditsia australis* (`47006`), 山烏桕 *Triadica cochinchinensis* (`55913`), 谷木葉冬青 *Ilex memecylifolia* (`78108`), 綠冬青 *Ilex viridis* (`78109`), 香楠 *Aidia canthioides* (`71001`), 青江藤 *Celastrus hindsii* (`53012`), 山礬 *Symplocos sumuntia* (`67761`), 兩廣梭羅 *Reevesia thyrsoidea* (`61056`), 五月茶 *Antidesma bunius* (`56500`), 栓葉安息香 *Styrax suberifolius* (`67853`), 白背鹽膚木 *Rhus hypoleuca* (`60064`), 南酸棗 *Choerospondias axillaris* (`60050`), 五列木 *Pentaphylax euryoides* (`67156`), 顯脈杜英 *Elaeocarpus dubius* (`54152`), 杜英 *Elaeocarpus decipiens* (`54151`), 腺葉桂櫻 *Prunus phaeosticta* (`49004`).
- 18:51 committed, pushed. Eleven new species pages with dedicated 12:5 Cloudflare heroes (`hkb-{blp}-hero`), 48 plates, photo count 718 to 766. The note that hands, labels, and tags were left off was wrong; the 21:11 entry removes the ones from this set too. Heroes use flower, fruit, pitcher, or wide stand, except 香港杜鵑, replaced above. CVH uses the stored SP2000 accepted name when that name is not the page binomial: 香港木蘭 points at *Lirianthe championii*. The same rule was applied to three pages already live: 草海桐 to *Scaevola taccada*, 樟 to *Camphora officinarum*, 銀珠 to *Peltophorum dasyrrhachis* var. *tonkinensis*.
- The eleven: 香港杜鵑 *Rhododendron hongkongense* (`68008`), 豬籠草 *Nepenthes mirabilis* (`64350`), 香港木蘭 *Magnolia championii* (`25050`), 灰冬青 *Ilex cinerea* (`78101`), 中華報春苣苔 *Primulina dryas* (`75208`), 小葉買麻藤 *Gnetum parvifolium* (`20001`), 豔山薑 *Alpinia zerumbet* (`36424`), 兩面針 *Zanthoxylum nitidum* (`60274`), 黃獨 *Dioscorea bulbifera* (`29051`), 黧蒴錐 *Castanopsis fissa* (`51005`), 假蒟 *Piper sarmentosum* (`24051`). 假蒟 has no fruiting months in the account, so the fruit bar is empty. 黧蒴錐 has no English name in the account, so that line stays empty.
- 09:47 committed, pushed 09:48. Commit `00e3317`, “Add the database buttons to the twenty-two newer species pages.”
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
