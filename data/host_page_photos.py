#!/usr/bin/env python3
"""Host hkb species-page photos on Cloudflare Images.

Local WebP: ~photos/<blp>/<stem>.webp
Local JPG:  ~original-jpg/<blp>/<stem>.jpg
Committed match: species_page_images.json
pages.json stores image_id only. Do not commit the image folders.
After image_id changes, run build_pages.py so the static HTML picks them up.
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

import requests
from PIL import Image

HKB = Path(__file__).resolve().parents[1]
PAGES = HKB / "data" / "pages.json"
MATCH = HKB / "species_page_images.json"
PHOTOS = HKB / "~photos"
ORIGINALS = HKB / "~original-jpg"
ENV_FILE = HKB / ".env"
LONG_SIDE = 1600
WEBP_QUALITY = 80


def load_dotenv(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def request_with_retry(method: str, url: str, headers: dict, **kwargs) -> requests.Response:
    timeout = kwargs.pop("timeout", 120)
    response = None
    for attempt in range(6):
        response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
        if response.status_code != 429:
            return response
        wait = min(30, 2 ** attempt)
        print(f"  rate limited, waiting {wait}s")
        time.sleep(wait)
    if response is None:
        raise RuntimeError("request was not sent")
    return response


def to_webp(jpg: Path, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(jpg) as img:
        img = img.convert("RGB")
        width, height = img.size
        long_side = max(width, height)
        if long_side > LONG_SIDE:
            scale = LONG_SIDE / long_side
            width = round(width * scale)
            height = round(height * scale)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
        return width, height


def image_exists(base_url: str, headers: dict, image_id: str) -> bool:
    response = request_with_retry("GET", f"{base_url}/{image_id}", headers=headers, timeout=60)
    if response.status_code == 200 and response.json().get("success"):
        return True
    if response.status_code == 404:
        return False
    raise RuntimeError(f"lookup {image_id} failed: {response.status_code}")


def upload_image(base_url: str, token: str, path: Path, image_id: str) -> str:
    with path.open("rb") as handle:
        response = request_with_retry(
            "POST",
            base_url,
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (path.name, handle, "image/webp")},
            data={"requireSignedURLs": "false", "id": image_id},
            timeout=120,
        )
    if response.status_code in (401, 403):
        raise PermissionError("Cloudflare rejected the upload. Token needs Images Edit.")
    data = response.json()
    if response.status_code >= 400 or not data.get("success"):
        raise RuntimeError(f"upload {image_id} failed: {data.get('errors') or response.status_code}")
    return data["result"]["id"]


def public_ok(delivery: str, image_id: str, variant: str) -> bool:
    url = f"https://imagedelivery.net/{delivery}/{image_id}/{variant}"
    response = requests.get(url, timeout=60)
    return response.status_code == 200 and response.headers.get("content-type", "").startswith("image/")


def prepare_local(payload: dict) -> list[dict]:
    jobs = []
    for blp, page in payload["pages"].items():
        hero_src = page.get("hero")
        if not hero_src and not page.get("hero_id"):
            raise SystemExit(f"{blp} has no hero")
        for photo in page["photos"]:
            src = photo.get("src")
            stem = Path(src).stem if src else photo["image_id"].split("-", 2)[-1]
            image_id = photo.get("image_id") or f"hkb-{blp}-{stem}"
            jpg_dest = ORIGINALS / blp / f"{stem}.jpg"
            webp_dest = PHOTOS / blp / f"{stem}.webp"
            jpg = HKB / "species" / src if src else jpg_dest
            if not jpg.exists():
                jpg = jpg_dest
            if not jpg.exists():
                raise SystemExit(f"missing jpg for {image_id}")
            if jpg != jpg_dest and not jpg_dest.exists():
                jpg_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(jpg, jpg_dest)
            width, height = to_webp(jpg_dest if jpg_dest.exists() else jpg, webp_dest)
            print(f"local {image_id} {width}x{height}")
            jobs.append({
                "blp": blp,
                "src": src,
                "hero_src": hero_src,
                "image_id": image_id,
                "filename": f"{blp}/{stem}.webp",
                "jpg": HKB / "species" / src if src else None,
                "jpg_dest": jpg_dest,
                "webp": webp_dest,
            })
    return jobs


def main() -> None:
    payload = json.loads(PAGES.read_text(encoding="utf-8"))
    jobs = prepare_local(payload)
    local = {p.relative_to(PHOTOS).as_posix() for p in PHOTOS.rglob("*.webp")}
    named = {job["filename"] for job in jobs}
    if local != named:
        raise SystemExit(f"webp mismatch extra={sorted(local - named)} missing={sorted(named - local)}")

    load_dotenv(ENV_FILE)
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
    delivery = os.environ.get("CLOUDFLARE_IMAGE_DELIVERY_HASH", "w8B9Irt4MxIF11C23YczhQ").strip()
    full = os.environ.get("CLOUDFLARE_IMAGE_VARIANT_FULL", "public").strip()
    thumb = os.environ.get("CLOUDFLARE_IMAGE_VARIANT_THUMBNAIL", "H300").strip()
    if not account_id or not token:
        raise SystemExit("Cloudflare credentials missing from .env")

    base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"
    headers = {"Authorization": f"Bearer {token}"}
    probe = request_with_retry("GET", f"{base_url}?per_page=1", headers=headers, timeout=30)
    probe_data = probe.json()
    if probe.status_code != 200 or not probe_data.get("success"):
        raise SystemExit(
            f"Cloudflare Images credential check failed ({probe.status_code}). "
            "Local WebP is in hkb/~photos. Replace CLOUDFLARE_API_TOKEN in the repo .env, then rerun."
        )
    print("Cloudflare Images credentials verified.")

    match_rows = []
    hero_by_blp = {}
    for job in jobs:
        image_id = job["image_id"]
        if image_exists(base_url, headers, image_id):
            print(f"{image_id} already on Cloudflare")
        else:
            uploaded = upload_image(base_url, token, job["webp"], image_id)
            if uploaded != image_id:
                raise SystemExit(f"id mismatch {uploaded} != {image_id}")
            print(f"{image_id} uploaded")
            time.sleep(0.4)
        if not public_ok(delivery, image_id, full) or not public_ok(delivery, image_id, thumb):
            raise SystemExit(f"delivery failed for {image_id}")
        if job["jpg"] and job["jpg"].exists() and job["jpg"] != job["jpg_dest"]:
            job["jpg"].unlink()
        if job["src"] and job["src"] == job["hero_src"]:
            hero_by_blp[job["blp"]] = image_id
        match_rows.append({"filename": job["filename"], "image_id": image_id})

    for blp, page in payload["pages"].items():
        hero_id = hero_by_blp.get(blp) or page.get("hero_id")
        if not hero_id:
            raise SystemExit(f"{blp} hero did not match a photo")
        page.pop("hero", None)
        page["hero_id"] = hero_id
        for photo in page["photos"]:
            photo.pop("src", None)
            stem = photo.get("image_id", "").split("-", 2)[-1]
            if "image_id" not in photo:
                src = photo.get("src", "")
                stem = Path(src).stem
                photo["image_id"] = f"hkb-{blp}-{stem}"

    # Re-apply ids from the jobs, which are the authority.
    by_file = {row["filename"]: row["image_id"] for row in match_rows}
    for blp, page in payload["pages"].items():
        for photo in page["photos"]:
            # image_id already set in the loop above only if missing; set from jobs.
            pass
        page["hero_id"] = hero_by_blp[blp]
        for photo, job in zip(page["photos"], [j for j in jobs if j["blp"] == blp]):
            photo.pop("src", None)
            photo["image_id"] = job["image_id"]

    ids = [row["image_id"] for row in match_rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate image_id")
    MATCH.write_text(
        json.dumps({"total_images": len(match_rows), "images": match_rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    PAGES.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    img_root = HKB / "species" / "img"
    if img_root.exists():
        for path in sorted(img_root.rglob("*"), reverse=True):
            if path.is_file() and path.name == ".DS_Store":
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if img_root.exists() and not any(img_root.iterdir()):
            img_root.rmdir()
    print(f"hosted {len(match_rows)} images")
    del by_file


if __name__ == "__main__":
    main()
