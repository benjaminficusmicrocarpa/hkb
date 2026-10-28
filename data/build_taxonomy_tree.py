#!/usr/bin/env python3
"""Build hkb/data/taxonomy-tree.json from a BLP taxonomic-tree export.

Accepts either the flat export (lex + taxa) or the older export (meta,
reference, taxa with a rank path). A clade that only repeats the subclass
name, or the group name with a plural -s, is not a second node.

Chinese names come from the export. A rank with no name in the file stays
Latin only. Do not invent one. Do not put workbook paths or photo fields
in the output.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HKB = Path(__file__).resolve().parents[1]
OUT = HKB / "data" / "taxonomy-tree.json"
PAGES = HKB / "data" / "page-ids.json"
DEFAULT_SRC = Path("/Users/benjaminlau/Downloads/blp_taxonomy_trees (1).json")

GROUP_ORDER = ["lycophyte", "fern", "gymnosperm", "angiosperm"]
LEX_RANK = {
    "major_group": "group",
    "class": "class",
    "subclass": "subclass",
    "clade": "clade",
    "order": "order",
    "suborder": "suborder",
    "family": "family",
    "genus": "genus",
}
LEAF_RANK = {
    "SPECIES": "species",
    "VARIETY": "variety",
    "SUBSPECIES": "subspecies",
    "FORM": "form",
    "Cultivar": "cultivar",
    "XSPECIES": "xspecies",
    "Section": "section",
}

SYSTEMS = {
    "angiosperm": ["APG V (2026)", "APG V（2026）"],
    "fern": [
        "PPG I (2016); subclass names from PPG II",
        "PPG I（2016）；亞綱名稱依 PPG II",
    ],
    "lycophyte": ["PPG I (2016)", "PPG I（2016）"],
    "gymnosperm": [
        "Yang, Ferguson et al. (2022)",
        "Yang、Ferguson 等（2022）",
    ],
}


class Node:
    def __init__(self, rank: str, name: str) -> None:
        self.rank = rank
        self.name = name
        self.chinese = ""
        self.children: dict[tuple[str, str], Node] = {}
        self.leaves: list[dict] = []
        self.min_blp = 10**9
        self.min_order = 10**9
        self.count = 0


def blp5(value: str) -> str:
    return str(value or "").replace("BLP-", "").zfill(5)


def saved_order_index(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    index: dict[str, int] = {}

    def walk(node: dict) -> None:
        if node.get("r") == "order" and "b" not in node:
            index.setdefault(node["n"], len(index))
        for child in node.get("k") or []:
            if "b" not in child:
                walk(child)

    walk(data.get("root") or {})
    return index


def chinese_of(lex: dict, rank: str, name: str) -> str:
    table = lex.get(LEX_RANK.get(rank, ""))
    if not isinstance(table, dict):
        return ""
    return str(table.get(name) or "").strip()


def steps_from_flat(taxon: dict) -> list[tuple[str, str]]:
    group = taxon["group"]
    steps = [
        ("kingdom", "Plantae"),
        ("phylum", "Tracheophyta"),
        ("major_group", group),
    ]
    if taxon.get("cls"):
        steps.append(("class", taxon["cls"]))
    if taxon.get("subcls"):
        steps.append(("subclass", taxon["subcls"]))
    for clade in taxon.get("clades") or []:
        if taxon.get("subcls") and clade == taxon["subcls"]:
            continue
        if clade == group or clade == group + "s":
            continue
        steps.append(("clade", clade))
    for rank, key in (
        ("order", "order"),
        ("suborder", "suborder"),
        ("family", "family"),
        ("genus", "genus"),
    ):
        if taxon.get(key):
            steps.append((rank, taxon[key]))
    leaf_rank = LEAF_RANK.get(taxon.get("rank") or "", "species")
    steps.append((leaf_rank, taxon["sci"]))
    return steps


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    payload = json.loads(src.read_text(encoding="utf-8"))
    taxa = payload["taxa"]
    new_format = bool(taxa) and "tree" not in taxa[0]
    lex = payload.get("lex") or {}
    if new_format:
        order_index = saved_order_index(OUT)
        counts = dict(Counter(taxon["group"] for taxon in taxa))
        generated = date.today().isoformat()
    else:
        order_index = {
            name: i for i, name in enumerate(payload["reference"]["orders_in_this_dataset"])
        }
        counts = payload["meta"]["counts_by_major_group"]
        generated = payload["meta"].get("generated") or date.today().isoformat()
    page_ids = json.loads(PAGES.read_text(encoding="utf-8")).get("pages") or {}

    root = Node("kingdom", "Plantae")
    skipped = 0
    named_genera = 0
    bare_genera = 0
    for taxon in taxa:
        if new_format:
            steps = steps_from_flat(taxon)
            code = blp5(taxon["id"])
            sci = taxon["sci"]
            chi = taxon.get("chi") or ""
            alt = str(taxon.get("alt") or "").strip()
            order_name = taxon.get("order") or ""
        else:
            steps = [(step["rank"], step["name"]) for step in taxon["tree"]]
            code = blp5(taxon["blp"])
            sci = taxon["scientific_name"]
            chi = taxon.get("chinese_name") or ""
            alt = str(taxon.get("chinese_name_alt") or "").strip()
            order_name = taxon["taxonomy"]["order"]
        if not steps or steps[0] != ("kingdom", "Plantae"):
            raise SystemExit(f"unexpected root on {code}: {steps[:2]}")
        node = root
        previous = None
        for rank, name in steps[1:-1]:
            if not name or "/" in name or ":" in name:
                raise SystemExit(f"bad node name {name!r} on {code}")
            if previous and rank == "clade" and name == previous[1] and previous[0] == "subclass":
                skipped += 1
                continue
            key = (rank, name)
            child = node.children.get(key)
            if child is None:
                child = Node(rank, name)
                child.chinese = chinese_of(lex, rank, name)
                node.children[key] = child
                if rank == "genus":
                    if child.chinese:
                        named_genera += 1
                    else:
                        bare_genera += 1
            node = child
            previous = (rank, name)
        leaf = {
            "r": steps[-1][0],
            "n": sci,
            "b": code,
            "z": chi,
        }
        if not chi:
            leaf.pop("z")
        if alt:
            leaf["a"] = alt
        if code in page_ids:
            leaf["p"] = 1
        node.leaves.append(leaf)
        node.min_blp = min(node.min_blp, int(code))
        node.min_order = min(node.min_order, order_index.get(order_name, 10**6))

    def bubble(node: Node) -> tuple[int, int, int]:
        count = len(node.leaves)
        min_blp = node.min_blp
        min_order = node.min_order
        for child in node.children.values():
            child_count, child_blp, child_order = bubble(child)
            count += child_count
            min_blp = min(min_blp, child_blp)
            min_order = min(min_order, child_order)
        node.count = count
        node.min_blp = min_blp
        node.min_order = min_order
        return count, min_blp, min_order

    bubble(root)

    def sort_key(node: Node) -> tuple:
        if node.rank == "major_group":
            group_at = GROUP_ORDER.index(node.name) if node.name in GROUP_ORDER else 99
            return (group_at, node.min_order, node.min_blp, node.name)
        return (node.min_order, node.min_blp, node.name)

    def pack(node: Node) -> dict:
        children = sorted(node.children.values(), key=sort_key)
        leaves = sorted(node.leaves, key=lambda item: int(item["b"]))
        packed_children = [pack(child) for child in children] + leaves
        item = {"r": node.rank, "n": node.name, "c": node.count}
        if node.chinese:
            item["z"] = node.chinese
        if packed_children:
            item["k"] = packed_children
        return item

    tree = pack(root)
    families = set()
    orders = set()
    genera = set()

    def walk(node: dict) -> None:
        rank = node.get("r")
        if rank == "family":
            families.add(node["n"])
        elif rank == "order":
            orders.add(node["n"])
        elif rank == "genus":
            genera.add(node["n"])
        for child in node.get("k") or []:
            if "b" not in child:
                walk(child)

    walk(tree)
    if tree["c"] != len(taxa):
        raise SystemExit(f"count mismatch tree={tree['c']} taxa={len(taxa)}")

    out = {
        "generated": generated,
        "n_taxa": tree["c"],
        "n_orders": len(orders),
        "n_families": len(families),
        "n_genera": len(genera),
        "counts": counts,
        "systems": SYSTEMS,
        "note": (
            "Family limits follow these systems, not the filing list on Families & Genera. "
            "Chinese names are those supplied with the tree. A name the file does not give is left blank."
        ),
        "root": tree,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT.name} taxa={out['n_taxa']} orders={out['n_orders']} "
        f"families={out['n_families']} genera={out['n_genera']} "
        f"genera_with_chinese={named_genera} genera_without={bare_genera} "
        f"skipped_repeat_clades={skipped} bytes={OUT.stat().st_size}"
    )


if __name__ == "__main__":
    main()
