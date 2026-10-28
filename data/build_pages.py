#!/usr/bin/env python3
"""Write static species HTML from data/pages.json.

This is the site's SSG step. Run it locally after pages.json changes,
then commit the HTML. GitHub Pages has no build step.

Writes one file per page that already has details:
  hkb/species/{blp}.html
  hkb/data/page-ids.json   (directory cards: presence + hero id only)

Does not write a file per catalogue taxon. taxa.json stays the list.
Does not touch hand-written showcase pages (no generated marker).
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

HKB = Path(__file__).resolve().parents[1]
PAGES = HKB / "data" / "pages.json"
INDEX = HKB / "data" / "page-ids.json"
SPECIES = HKB / "species"
MARKER = "<!-- hkb-generated: source is data/pages.json. Run data/build_pages.py. -->"
SITE = "https://benjaminficusmicrocarpa.github.io/hkb"
PHOTO = "https://imagedelivery.net/w8B9Irt4MxIF11C23YczhQ"
OG = f"{SITE}/og.png"
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
PPG = {
    "Lycopodiales", "Selaginellales", "Equisetales", "Ophioglossales", "Psilotales",
    "Marattiales", "Osmundales", "Hymenophyllales", "Gleicheniales", "Schizaeales",
    "Salviniales", "Cyatheales", "Polypodiales",
}
GYMNOSPERM = {"Cycadales", "Ginkgoales", "Pinales", "Araucariales", "Cupressales", "Gnetales"}


def esc(value) -> str:
    return escape("" if value is None else str(value), quote=True)


def pair(en, zh) -> str:
    return (
        f'<span class="lang-en">{esc(en)}</span>'
        f'<span class="lang-zh hidden">{esc(zh)}</span>'
    )


def photo_url(image_id: str, variant: str = "public") -> str:
    return f"{PHOTO}/{escape(image_id, quote=True)}/{variant}"


def parse_months(value) -> list[int]:
    if not value:
        return []
    text = str(value).strip()
    if "-" in text:
        a_text, b_text = text.split("-", 1)
        a, b = int(a_text), int(b_text)
        if a <= b:
            return list(range(a, b + 1))
        return list(range(a, 13)) + list(range(1, b + 1))
    if "," in text:
        return [int(part) for part in text.split(",") if part.strip()]
    return [int(text)]


def phenology(flower, fruit) -> str:
    def row(months: list[int], on_class: str) -> str:
        cells = []
        for month in range(1, 13):
            on = month in months
            cells.append(
                f'<div class="month {on_class if on else "inactive"}" '
                f'style="height:{"100%" if on else "30%"}" title="{MONTHS[month - 1]}"></div>'
            )
        return f'<div class="phenology-bar" style="height:22px">{"".join(cells)}</div>'

    caption = "".join(f'<div class="month-label">{letter}</div>' for letter in MONTHS)
    return (
        '<div class="space-y-2">'
        '<div>'
        f'<div class="text-[11px] font-semibold tracking-wide text-stone-500 mb-1">{pair("Flowering", "花期")}</div>'
        f'{row(parse_months(flower), "active")}'
        "</div>"
        "<div>"
        f'<div class="text-[11px] font-semibold tracking-wide text-stone-500 mb-1">{pair("Fruiting", "果期")}</div>'
        f'{row(parse_months(fruit), "fruit")}'
        f'<div class="phenology-bar" style="height:auto">{caption}</div>'
        "</div>"
        "</div>"
    )


def class_system(order: str) -> tuple[str, str]:
    if order in PPG:
        return "PPG I", "PPG I"
    if order in GYMNOSPERM:
        return "Christenhusz et al.", "Christenhusz 等"
    return "APG IV", "APG IV"


def card(icon: str, title_html: str, body_html: str) -> str:
    return (
        '<div class="bg-white rounded-xl border border-stone-200 shadow-sm overflow-hidden">'
        '<div class="px-6 py-4 bg-stone-50 border-b border-stone-200">'
        f'<h2 class="font-serif font-bold text-lg text-stone-900 flex items-center gap-2">'
        f'<i class="{icon} text-botanical"></i> {title_html}</h2>'
        "</div>"
        f'<div class="p-6">{body_html}</div>'
        "</div>"
    )


def apa(ref: dict | None) -> str:
    if not ref:
        return ""
    volume = f" (Vol. {esc(ref.get('volume'))})" if ref.get("volume") else ""
    title_zh = f" [{esc(ref.get('title_zh'))}]" if ref.get("title_zh") else ""
    return (
        f"{esc(ref.get('authors'))} ({esc(ref.get('year'))}). "
        f"<em>{esc(ref.get('title'))}</em>{title_zh}{volume}. {esc(ref.get('publisher'))}."
    )


def chips(names) -> str:
    return "".join(
        f'<span class="bg-stone-100 text-stone-700 px-3 py-1 rounded-full text-sm font-medium">{esc(name)}</span>'
        for name in (names or [])
    )


def description(page: dict) -> str:
    eco = ""
    if page.get("ecology"):
        eco = str(page["ecology"][0].get("en") or "")
    bits = [str(page.get("sci") or "")]
    if page.get("chi_line"):
        bits.append(f"({page['chi_line']})")
    text = " ".join(bits)
    if eco:
        text = f"{text}. {eco}"
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 180:
        text = text[:177].rstrip() + "..."
    return text


def json_for_script(value) -> str:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def columns(page: dict) -> str:
    system_en, system_zh = class_system(page.get("order") or "")
    tax_rows = []
    for en, zh, value, italic in (
        ("Order", "目", page.get("order"), False),
        ("Family", "科", page.get("family"), False),
        ("Genus", "屬", page.get("genus"), True),
        ("Species", "種", page.get("sci"), True),
    ):
        style = " italic" if italic else ""
        tax_rows.append(
            '<tr class="border-b border-stone-100 last:border-b-0">'
            f'<td class="py-2.5 pr-4 text-stone-500 font-medium w-32">{pair(en, zh)}</td>'
            f'<td class="py-2.5{style}">{esc(value)}</td>'
            "</tr>"
        )
    morph_blocks = []
    for i, block in enumerate(page.get("morphology") or []):
        items = []
        for item in block.get("items") or []:
            items.append(
                "<div>"
                f'<div class="text-xs text-stone-400 font-semibold uppercase tracking-wider mb-1">{pair(item.get("label_en"), item.get("label_zh"))}</div>'
                f'<p class="lang-en">{esc(item.get("en"))}</p>'
                f'<p class="lang-zh hidden">{esc(item.get("zh"))}</p>'
                "</div>"
            )
        border = "border-t border-stone-100 pt-6" if i else ""
        morph_blocks.append(
            f'<div class="{border}">'
            f'<h3 class="font-serif font-bold text-stone-900 text-base mb-3">{pair(block.get("title_en"), block.get("title_zh"))}</h3>'
            f'<div class="space-y-4">{"".join(items)}</div>'
            "</div>"
        )
    ecology = "".join(
        "<li>"
        f'<span class="lang-en"><strong>{esc(item.get("label_en"))}.</strong> {esc(item.get("en"))}</span>'
        f'<span class="lang-zh hidden"><strong>{esc(item.get("label_zh"))}。</strong> {esc(item.get("zh"))}</span>'
        "</li>"
        for item in (page.get("ecology") or [])
    )
    fruit = page["fruit"] if "fruit" in page else page.get("flower")
    facts = []
    for fact in page.get("facts") or []:
        extra = ""
        if fact.get("phenology"):
            extra = f'<div class="mt-2">{phenology(page.get("flower"), fruit)}</div>'
        icon = fact.get("icon") or "fa-circle"
        facts.append(
            '<div class="flex items-start gap-3">'
            f'<div class="w-9 h-9 rounded-lg bg-stone-100 text-stone-600 flex items-center justify-center flex-shrink-0"><i class="fa-solid {esc(icon)}"></i></div>'
            '<div class="w-full">'
            f'<div class="text-xs text-stone-400 font-semibold uppercase tracking-wider">{pair(fact.get("label_en"), fact.get("label_zh"))}</div>'
            f'<div class="text-stone-800 font-medium text-sm">{pair(fact.get("en"), fact.get("zh"))}</div>'
            f"{extra}"
            "</div></div>"
        )
    synonyms = page.get("synonyms") or []
    synonym_html = ""
    if synonyms:
        names = ", ".join(f'<span class="italic">{esc(name)}</span>' for name in synonyms)
        synonym_html = f'<p class="text-sm text-stone-500 mt-1">{pair("Synonyms", "異名")} {names}</p>'
    photos = page.get("photos") or []
    if photos:
        first = photos[0]
        src = photo_url(first["image_id"]) if first.get("image_id") else esc(first.get("src"))
        photo_body = (
            '<div id="photoMount">'
            f'<img src="{src}" alt="{esc(first.get("en"))}">'
            f'<p class="text-sm text-stone-600 mt-2">{pair(first.get("en"), first.get("zh"))}</p>'
            "</div>"
        )
    else:
        photo_body = (
            f'<div id="photoMount"><p class="text-sm text-stone-400">{pair("No representative photographs yet.", "尚未有代表照片。")}</p></div>'
        )
    left = (
        '<div class="w-full lg:w-[60%] space-y-8">'
        + card("fa-solid fa-sitemap", pair(f"Taxonomic classification ({system_en})", f"分類（{system_zh}）"), f'<table class="w-full text-sm"><tbody>{"".join(tax_rows)}</tbody></table>')
        + card("fa-solid fa-seedling", pair("Plant morphology", "植物形態"), f'<div class="space-y-6 text-stone-700 leading-relaxed text-sm">{"".join(morph_blocks)}</div>')
        + card("fa-solid fa-leaf", pair("Ecology", "生態"), f'<ul class="list-disc list-inside space-y-3 text-stone-700 leading-relaxed">{ecology}</ul>')
        + card("fa-solid fa-camera", pair("Representative photographs", "代表照片"), photo_body)
        + card("fa-solid fa-bookmark", pair("Source", "出處"), f'<p class="text-sm text-stone-600 leading-relaxed">{apa(page.get("reference"))}</p>')
        + "</div>"
    )
    right = (
        '<div class="w-full lg:w-[40%] space-y-6">'
        '<div class="bg-white rounded-xl border border-stone-200 shadow-sm overflow-hidden">'
        '<div class="px-6 py-4 bg-botanical-dark text-white">'
        f'<h2 class="font-serif font-bold text-lg flex items-center gap-2"><i class="fa-solid fa-clipboard-list"></i> {pair("Quick facts", "速覽")}</h2>'
        "</div>"
        f'<div class="p-6 space-y-5">{"".join(facts)}</div>'
        "</div>"
        + card(
            "fa-solid fa-language",
            pair("Names", "名稱"),
            '<div class="space-y-4">'
            "<div>"
            '<div class="text-xs text-stone-400 font-semibold uppercase tracking-wider mb-1">Scientific name</div>'
            f'<div class="text-stone-900 font-serif italic text-lg">{esc(page.get("sci"))} <span class="not-italic text-stone-500 text-sm">{esc(page.get("authority"))}</span></div>'
            f"{synonym_html}"
            "</div>"
            '<div class="border-t border-stone-100 pt-4">'
            f'<div class="text-xs text-stone-400 font-semibold uppercase tracking-wider mb-1.5">{pair("Chinese names", "中文名")}</div>'
            f'<div class="flex flex-wrap gap-2">{chips(page.get("chi_names"))}</div>'
            "</div>"
            '<div class="border-t border-stone-100 pt-4">'
            f'<div class="text-xs text-stone-400 font-semibold uppercase tracking-wider mb-1.5">{pair("English names", "英文名")}</div>'
            f'<div class="flex flex-wrap gap-2">{chips(page.get("en_names"))}</div>'
            "</div>"
            '<div class="border-t border-stone-100 pt-4">'
            f'<span class="blp-badge blp-badge-ink">BLP {esc(page.get("blp"))}</span>'
            "</div></div>",
        )
        + "</div>"
    )
    return left + right


def hero(page: dict) -> tuple[str, str]:
    hero_id = page.get("hero_id") or ""
    if not hero_id:
        raise SystemExit(f"{page.get('blp')} has no hero_id")
    url = photo_url(hero_id)
    style = (
        "background-image: linear-gradient(to top, rgba(28,25,23,0.82), rgba(28,25,23,0.35)), "
        f"url(&quot;{url}&quot;)"
    )
    native = ""
    if page.get("native"):
        native = (
            '<span class="bg-emerald-600/90 backdrop-blur text-white text-xs font-bold px-3 py-1 rounded-full tracking-wide">'
            f'{pair("Native", "原生")}</span>'
        )
    inner = (
        '<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 w-full">'
        '<div class="flex flex-col gap-3">'
        '<div class="flex flex-wrap items-center gap-3">'
        f'<span class="blp-badge" title="BLP">BLP {esc(page.get("blp"))}</span>'
        f"{native}"
        f'<span class="bg-white/20 backdrop-blur text-white text-xs font-medium px-3 py-1 rounded-full">{esc(page.get("family"))}</span>'
        "</div>"
        f'<h1 class="text-4xl md:text-5xl lg:text-6xl font-serif font-bold text-white italic drop-shadow-lg">{esc(page.get("sci"))}</h1>'
        f'<p class="text-xl md:text-2xl text-white/90 font-light">{esc(page.get("chi_line"))}</p>'
        f'<p class="text-lg text-white/70 font-serif">{esc(page.get("authority"))}</p>'
        "</div></div>"
    )
    return style, inner


def render(page: dict) -> str:
    blp = page["blp"]
    title = f"{page.get('sci')} · BLP {blp} | Hong Kong Botanica"
    desc = description(page)
    canonical = f"{SITE}/species/{blp}.html"
    style, inner = hero(page)
    crumb = (
        f'<span class="text-stone-900 font-medium italic">{esc(page.get("sci"))}</span>'
        f'<span class="blp-badge blp-badge-ink">BLP {esc(blp)}</span>'
    )
    photos = [
        {"image_id": photo.get("image_id"), "code": photo.get("code") or "", "en": photo.get("en") or "", "zh": photo.get("zh") or "", "src": photo.get("src") or ""}
        for photo in (page.get("photos") or [])
    ]
    return f"""<!DOCTYPE html>
{MARKER}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="hkb-base" content="..">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Hong Kong Botanica">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{OG}">
    <meta property="og:image:secure_url" content="{OG}">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Hong Kong Botanica">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(desc)}">
    <meta name="twitter:image" content="{OG}">
    <link rel="icon" href="../hkb.svg" type="image/svg+xml">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../css/hkb.css?v=5">
    <script>
        tailwind.config = {{ theme: {{ extend: {{
            fontFamily: {{ sans: ['Roboto', 'Noto Sans TC', 'sans-serif'], serif: ['Playfair Display', 'Noto Serif TC', 'serif'] }},
            colors: {{ botanical: {{ light: '#82c07b', DEFAULT: '#4a8244', dark: '#2d5229', accent: '#d4af37' }} }}
        }}}}}}
    </script>
</head>
<body class="bg-stone-50 text-gray-800 font-sans antialiased">
    <nav class="sticky top-0 z-50 bg-white/95 backdrop-blur shadow-sm border-b border-stone-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <a href="../index.html" class="flex items-center gap-2.5 text-botanical-dark font-serif font-bold text-xl sm:text-2xl tracking-tight">
                        <img src="../hkb.svg" alt="HKB" class="h-9 w-9">
                        <span class="lang-en">Hong Kong Botanica</span>
                        <span class="lang-zh hidden">香港草木誌</span>
                    </a>
                </div>
                <div class="hidden md:flex items-center space-x-6 lg:space-x-8 text-sm lg:text-base">
                    <a href="index.html" class="text-stone-600 hover:text-botanical font-medium transition">
                        <span class="lang-en">Species Directory</span>
                        <span class="lang-zh hidden">物種目錄</span>
                    </a>
                    <a href="../families/index.html" class="text-stone-600 hover:text-botanical font-medium transition">
                        <span class="lang-en">Families & Genera</span>
                        <span class="lang-zh hidden">科屬分類</span>
                    </a>
                    <a href="../taxonomy/index.html" class="text-stone-600 hover:text-botanical font-medium transition">
                        <span class="lang-en">Taxonomic tree</span>
                        <span class="lang-zh hidden">分類樹</span>
                    </a>
                    <a style="display:none" href="../about/index.html" class="text-stone-600 hover:text-botanical font-medium transition">
                        <span class="lang-en">About</span>
                        <span class="lang-zh hidden">關於本庫</span>
                    </a>
                </div>
                <div class="flex items-center space-x-4 text-stone-500">
                    <a href="../search/index.html" class="hover:text-botanical transition"><i class="fa-solid fa-search text-lg"></i></a>
                    <button onclick="toggleLanguage()" class="hover:text-botanical transition font-bold text-sm px-2 py-1 rounded border border-stone-200 hover:border-botanical">
                        <span class="lang-en">中</span>
                        <span class="lang-zh hidden">EN</span>
                    </button>
                    <button onclick="openMobileNav()" class="md:hidden hover:text-botanical transition"><i class="fa-solid fa-bars text-xl"></i></button>
                </div>
            </div>
        </div>
    </nav>

    <div id="mobileOverlay" class="mobile-nav-overlay" onclick="closeMobileNav()"></div>
    <div id="mobileDrawer" class="mobile-nav-drawer">
        <div class="p-5 border-b border-stone-100 flex justify-between items-center">
            <span class="font-serif font-bold text-lg text-botanical-dark">
                <span class="lang-en">Menu</span><span class="lang-zh hidden">選單</span>
            </span>
            <button onclick="closeMobileNav()" class="text-stone-400 hover:text-stone-700"><i class="fa-solid fa-xmark text-xl"></i></button>
        </div>
        <div class="p-5 space-y-1">
            <a href="index.html" class="block px-4 py-3 rounded-lg text-stone-700 hover:bg-botanical/10 hover:text-botanical font-medium transition">
                <i class="fa-solid fa-leaf w-6 text-center mr-2 text-stone-400"></i>
                <span class="lang-en">Species Directory</span><span class="lang-zh hidden">物種目錄</span>
            </a>
            <a href="../families/index.html" class="block px-4 py-3 rounded-lg text-stone-700 hover:bg-botanical/10 hover:text-botanical font-medium transition">
                <i class="fa-solid fa-sitemap w-6 text-center mr-2 text-stone-400"></i>
                <span class="lang-en">Families & Genera</span><span class="lang-zh hidden">科屬分類</span>
            </a>
            <a href="../taxonomy/index.html" class="block px-4 py-3 rounded-lg text-stone-700 hover:bg-botanical/10 hover:text-botanical font-medium transition">
                <i class="fa-solid fa-folder-tree w-6 text-center mr-2 text-stone-400"></i>
                <span class="lang-en">Taxonomic tree</span><span class="lang-zh hidden">分類樹</span>
            </a>
            <a style="display:none" href="../about/index.html" class="block px-4 py-3 rounded-lg text-stone-700 hover:bg-botanical/10 hover:text-botanical font-medium transition">
                <i class="fa-solid fa-circle-info w-6 text-center mr-2 text-stone-400"></i>
                <span class="lang-en">About</span><span class="lang-zh hidden">關於本庫</span>
            </a>
            <a href="../search/index.html" class="block px-4 py-3 rounded-lg text-stone-700 hover:bg-botanical/10 hover:text-botanical font-medium transition">
                <i class="fa-solid fa-search w-6 text-center mr-2 text-stone-400"></i>
                <span class="lang-en">Search</span><span class="lang-zh hidden">搜尋</span>
            </a>
        </div>
        <div class="p-5 border-t border-stone-100">
            <button onclick="toggleLanguage()" class="w-full px-4 py-3 rounded-lg border border-stone-200 text-stone-600 font-medium hover:border-botanical hover:text-botanical transition">
                <span class="lang-en">切換中文</span><span class="lang-zh hidden">Switch to English</span>
            </button>
        </div>
    </div>

    <header id="speciesHero" class="species-hero bg-cover bg-center" style="{style}">{inner}</header>
    <main id="speciesMain" class="animate-in">
        <section class="bg-white border-b border-stone-200 py-4">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <nav class="breadcrumb">
                    <a href="../index.html"><i class="fa-solid fa-house text-xs"></i> <span class="lang-en">Home</span><span class="lang-zh hidden">首頁</span></a>
                    <span class="separator"><i class="fa-solid fa-chevron-right text-[10px]"></i></span>
                    <a href="index.html"><span class="lang-en">Species Directory</span><span class="lang-zh hidden">物種目錄</span></a>
                    <span class="separator"><i class="fa-solid fa-chevron-right text-[10px]"></i></span>
                    <span id="speciesCrumb" class="inline-flex items-center gap-2 flex-wrap">{crumb}</span>
                </nav>
            </div>
        </section>
        <section class="py-10 md:py-14">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div id="speciesColumns" class="flex flex-col lg:flex-row gap-8 lg:gap-12">{columns(page)}</div>
            </div>
        </section>
    </main>
    <footer class="bg-stone-900 text-stone-400 py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-3 text-white">
                <img src="../hkb.svg" alt="" class="h-8 w-8 opacity-80">
                <span class="font-serif font-bold text-xl">
                    <span class="lang-en">Hong Kong Botanica</span><span class="lang-zh hidden">香港草木誌</span>
                </span>
            </div>
            <div class="flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm font-medium">
                <a href="index.html" class="hover:text-white transition"><span class="lang-en">Species List</span><span class="lang-zh hidden">物種名錄</span></a>
                <a href="../families/index.html" class="hover:text-white transition"><span class="lang-en">Taxonomy Guide</span><span class="lang-zh hidden">分類指南</span></a>
                <a style="display:none" href="../about/index.html" class="hover:text-white transition"><span class="lang-en">About</span><span class="lang-zh hidden">關於本庫</span></a>
                <a href="../search/index.html" class="hover:text-white transition"><span class="lang-en">Search</span><span class="lang-zh hidden">搜尋</span></a>
            </div>
            <div class="text-sm text-stone-500 text-center md:text-right">
                <span class="lang-en">&copy; 2026 Hong Kong Botanica. All rights reserved.</span>
                <span class="lang-zh hidden">&copy; 2026 香港草木誌。保留所有權利。</span>
            </div>
        </div>
    </footer>
    <script type="application/json" id="page-photos">{json_for_script(photos)}</script>
    <script src="../js/hkb.js?v=4"></script>
    <script src="../js/species-page.js?v=12"></script>
</body>
</html>
"""


def write_generated(path: Path, text: str) -> None:
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if MARKER not in old:
            raise SystemExit(f"refusing to overwrite non-generated file {path}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    payload = json.loads(PAGES.read_text(encoding="utf-8"))
    pages = payload["pages"]
    if not isinstance(pages, dict) or not pages:
        raise SystemExit("pages.json has no pages")
    index_pages = {}
    written = []
    for key in sorted(pages):
        page = pages[key]
        blp = str(page.get("blp") or "")
        if key != blp or not re.fullmatch(r"\d{5}", blp):
            raise SystemExit(f"bad blp key={key!r} blp={blp!r}")
        if not page.get("sci"):
            raise SystemExit(f"{blp} has no scientific name")
        html = render(page)
        if "fetch(" in html or "Loading…" in html:
            raise SystemExit(f"{blp} still looks like the client-side shell")
        if page["sci"] not in html or f"BLP {blp}" not in html:
            raise SystemExit(f"{blp} missing visible name")
        dest = SPECIES / f"{blp}.html"
        write_generated(dest, html)
        index_pages[blp] = {"hero_id": page["hero_id"]}
        written.append(dest)
    for path in SPECIES.glob("*.html"):
        if not re.fullmatch(r"\d{5}", path.stem):
            continue
        text = path.read_text(encoding="utf-8")
        if MARKER in text and path.stem not in pages:
            path.unlink()
            print(f"removed stale {path.name}")
    index = {
        "note": "Directory index only: which taxa have a generated page, plus the card photo. Full text is in species/{blp}.html.",
        "pages": index_pages,
    }
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(written)} species pages and {INDEX.name}")
    for path in written:
        print(f"  {path.name} {path.stat().st_size}")


if __name__ == "__main__":
    main()
