#!/usr/bin/env python3
"""QA/QC for the HKB static site.

Source of truth is the JSON. Generated HTML must match.

Usage:
  python3 data/qaqc.py            # check only
  python3 data/qaqc.py --realign  # rewrite species/*.html from pages.json

Checks:
  - every pages.json entry has a species/{blp}.html with the generated marker
  - page-ids.json matches pages.json (blp + hero_id)
  - stats.json header counts match taxa.json (if both exist)
  - hand-edited species pages that lack the marker are warned
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HKB = Path(__file__).resolve().parents[1]
DATA = HKB / "data"
SPECIES = HKB / "species"
MARKER = "<!-- hkb-generated: source is data/pages.json. Run data/build_pages.py. -->"


def load(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--realign", action="store_true", help="rewrite generated HTML from pages.json")
    args = parser.parse_args()

    pages_file = load(DATA / "pages.json")
    if pages_file is None:
        print("ERROR: data/pages.json missing")
        return 1
    pages = pages_file.get("pages") if isinstance(pages_file, dict) else pages_file
    if isinstance(pages, dict):
        page_list = list(pages.values())
    else:
        page_list = pages

    page_ids_file = load(DATA / "page-ids.json") or {}
    page_ids = page_ids_file.get("pages") if isinstance(page_ids_file, dict) and "pages" in page_ids_file else page_ids_file
    taxa = load(DATA / "taxa.json")
    stats = load(DATA / "stats.json")

    errors = []
    warnings = []

    expected_ids = {}
    for page in page_list:
        blp = str(page.get("blp") or "")
        expected_ids[blp] = {"hero_id": page.get("hero_id")} if page.get("hero_id") else {}
        if page.get("hero_id"):
            expected_ids[blp] = {"hero_id": page["hero_id"]}

    if isinstance(page_ids, dict):
        # Normalize comparison to blp -> {hero_id?}
        got = {}
        for blp, rec in page_ids.items():
            if isinstance(rec, dict):
                got[str(blp)] = {"hero_id": rec["hero_id"]} if rec.get("hero_id") else {}
            else:
                got[str(blp)] = {}
        if set(got) != set(expected_ids):
            missing = sorted(set(expected_ids) - set(got))
            extra = sorted(set(got) - set(expected_ids))
            errors.append(f"page-ids.json keys mismatch missing={missing} extra={extra}")
        else:
            for blp in expected_ids:
                if got.get(blp, {}).get("hero_id") != expected_ids[blp].get("hero_id"):
                    errors.append(f"page-ids.json hero_id mismatch for {blp}")

    for page in page_list:
        blp = str(page["blp"])
        html_path = SPECIES / f"{blp}.html"
        if not html_path.exists():
            errors.append(f"missing species/{blp}.html")
            continue
        text = html_path.read_text(encoding="utf-8")
        if MARKER not in text:
            warnings.append(f"species/{blp}.html lacks generated marker (hand-edited?)")

    if taxa and stats:
        for key in ("n_taxa", "n_species", "n_genera", "n_families", "n_orders"):
            if stats.get(key) != taxa.get(key):
                errors.append(f"stats.json {key}={stats.get(key)} != taxa.json {key}={taxa.get(key)}")

    if args.realign:
        sys.path.insert(0, str(DATA))
        try:
            import build_pages
            build_pages.main()
            print("realigned species HTML from pages.json")
        except Exception as exc:
            errors.append(f"realign failed: {exc}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  ERROR  {e}")
        for w in warnings:
            print(f"  WARN   {w}")
        return 1

    print("OK")
    for w in warnings:
        print(f"  WARN   {w}")
    print(f"  pages={len(page_list)} species_html={len(list(SPECIES.glob('*.html')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
