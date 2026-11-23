"""Fetch up to 20 real reference images per weapon family from Wikimedia Commons using curl.exe
and assemble 4x5 visual inspection contact sheets so the 3D pipeline sees 15-20 real photos per missile.
"""

from __future__ import annotations

import json
import subprocess
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4\scratch\ref_bank")

FAMILIES = {
    "IRIS-T": ["IRIS-T missile", "IRIS-T SL"],
    "Meteor_MICA": ["MBDA Meteor missile", "MBDA MICA missile"],
    "PL12_PL15_PL17": ["PL-12 missile", "PL-15 missile", "SD-10 missile"],
    "R77_R77M_R74": ["R-77 missile", "Vympel R-73", "R-37 missile"],
    "Python5_AIM9X_AIM54": ["Python-5 missile", "AIM-9X Sidewinder", "AIM-54 Phoenix"],
    "Kinzhal_ARRW_Ballistic": ["Kh-47M2 Kinzhal", "Iskander missile", "AGM-183 ARRW", "Air LORA missile"],
    "AntiShip_Exocet_Kh35_NSM": ["Exocet missile", "Kh-35 missile", "Naval Strike Missile", "Harpoon missile"],
    "AntiShip_Heavy_Kh22_BrahMos": ["BrahMos missile", "P-800 Oniks", "Kh-22 missile", "3M22 Zircon"],
    "SEAD_AARGM_Kh58_ALARM": ["AGM-88 HARM", "AARGM missile", "MBDA ALARM", "Kh-58 missile", "Kh-31 missile"],
    "Bombs_UMPK_SDB_MOP_SPICE": ["UMPK glide bomb", "FAB-1500", "GBU-39 SDB", "GBU-53 StormBreaker", "GBU-57 MOP", "SPICE bomb"],
    "Cruise_SCALP_TAURUS_JASSM": ["Storm Shadow missile", "SCALP-EG", "Taurus KEPD 350", "AGM-158 JASSM", "Kh-101"],
    "Drones_Lancet_Shahed_Harop": ["ZALA Lancet", "Shahed 136", "IAI Harop", "Switchblade drone"],
}


def curl_get(url: str) -> bytes:
    r = subprocess.run(
        ["curl.exe", "-sL", "--max-time", "12", "-A", "DCSModdingRefBot/1.0 (https://commons.wikimedia.org)", url],
        capture_output=True,
    )
    return r.stdout if r.returncode == 0 else b""


def search_commons(query: str, limit: int = 12) -> list[dict]:
    q = urllib.parse.quote(query)
    api = (
        "https://commons.wikimedia.org/w/api.php?"
        f"action=query&generator=search&gsrsearch={q}&gsrnamespace=6&gsrlimit={limit}"
        "&prop=imageinfo&iiprop=url|mime|size&iiurlwidth=640&format=json"
    )
    raw = curl_get(api)
    if not raw:
        return []
    try:
        data = json.loads(raw.decode("utf-8", errors="ignore"))
    except Exception:
        return []
    pages = (data.get("query") or {}).get("pages") or {}
    results = []
    for p in pages.values():
        infos = p.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = info.get("mime", "")
        if mime not in ("image/jpeg", "image/png", "image/webp"):
            continue
        thumb = info.get("thumburl") or info.get("url")
        if thumb:
            results.append({"title": p.get("title", ""), "url": thumb})
    return results


def fetch_family(fam_name: str, queries: list[str]) -> tuple[str, int, str]:
    fam_dir = OUT_DIR / fam_name
    fam_dir.mkdir(parents=True, exist_ok=True)

    seen_urls: set[str] = set()
    candidates: list[dict] = []
    for q in queries:
        for item in search_commons(q, limit=12):
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                candidates.append(item)
            if len(candidates) >= 20:
                break
        if len(candidates) >= 20:
            break

    saved_paths: list[Path] = []
    for idx, item in enumerate(candidates[:20]):
        ext = ".png" if ".png" in item["url"].lower() else ".jpg"
        dst = fam_dir / f"ref_{idx:02d}{ext}"
        if not dst.is_file() or dst.stat().st_size < 2000:
            blob = curl_get(item["url"])
            if len(blob) > 2000:
                dst.write_bytes(blob)
        if dst.is_file() and dst.stat().st_size > 2000:
            saved_paths.append(dst)

    # Build 4x5 contact sheet (2000 x 1400 px)
    cols, rows = 5, 4
    tw, th = 400, 350
    sheet = Image.new("RGB", (cols * tw, rows * th), (18, 20, 26))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 16)
    except Exception:
        font = ImageFont.load_default()

    for idx, p in enumerate(saved_paths[:20]):
        r_idx, c_idx = divmod(idx, cols)
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((tw - 10, th - 32))
            x0 = c_idx * tw + (tw - im.width) // 2
            y0 = r_idx * th + 24 + (th - 28 - im.height) // 2
            sheet.paste(im, (x0, y0))
            draw.text((c_idx * tw + 8, r_idx * th + 4), f"#{idx:02d} {p.stem}", fill=(200, 220, 240), font=font)
        except Exception:
            pass

    sheet_path = OUT_DIR / f"sheet_{fam_name}.jpg"
    sheet.save(sheet_path, quality=88)
    return fam_name, len(saved_paths), str(sheet_path)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        for fam_name, count, sheet in ex.map(lambda kv: fetch_family(*kv), FAMILIES.items()):
            print(f"[OK] {fam_name}: {count} images -> {sheet}")


if __name__ == "__main__":
    main()
