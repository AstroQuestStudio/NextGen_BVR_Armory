"""Generate 2K multi-zone PBR textures for Ground Air Defenses (C-RAM, Iron Dome, IRIS-T SLM, SAMP/T, Pantsir-SM), KEKA Aerospace & Backlog Missiles."""

from __future__ import annotations

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


TEX_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Textures\NextGen_BVR_Armory")
SIZE = 2048


def _font(sz: int):
    for p in (r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeui.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


THEMES_V2 = {
    "cram_centurion": {
        "base": (212, 198, 168),   # CARC desert tan trailer & cradle
        "nose": (236, 238, 240),   # White Ku-band R2-D2 radome!
        "nozzle": (54, 58, 64),    # Dark gunmetal Vulcan barrels
        "band1": (185, 48, 38),
        "band2": (215, 168, 42),
        "fin": (198, 184, 152),
        "radome_gloss": 28,
        "stencil": "CENTURION C-RAM // PHALANX",
    },
    "iron_dome": {
        "base": (132, 134, 122),   # IDF olive-drab grey
        "nose": (228, 230, 234),   # Tamir white canister / sensor tip
        "nozzle": (48, 52, 56),
        "band1": (212, 162, 42),
        "band2": (60, 72, 84),
        "fin": (150, 152, 140),
        "radome_gloss": 42,
        "stencil": "IRON DOME // TAMIR",
    },
    "elm2084_radar": {
        "base": (134, 136, 124),
        "nose": (194, 198, 192),   # S-band AESA flat face
        "nozzle": (46, 50, 54),
        "band1": (212, 162, 42),
        "band2": (52, 92, 128),
        "fin": (110, 114, 106),
        "radome_gloss": 55,
        "stencil": "EL/M-2084 MMR AESA",
    },
    "sam_nato_olive": {
        "base": (94, 104, 78),     # NATO BRONZE-GREEN (IRIS-T SLM / SAMP-T)
        "nose": (228, 230, 232),   # White canister tubes / Aster nose
        "nozzle": (46, 50, 56),
        "band1": (210, 164, 42),
        "band2": (52, 112, 168),
        "fin": (108, 118, 90),
        "radome_gloss": 40,
        "stencil": "SAM // NATO SHIELD",
    },
    "pantsir_sm": {
        "base": (108, 114, 92),    # Russian olive-khaki
        "nose": (210, 212, 206),   # Radar array / missile caps
        "nozzle": (42, 46, 52),
        "band1": (190, 48, 42),
        "band2": (212, 168, 42),
        "fin": (92, 98, 78),
        "radome_gloss": 48,
        "stencil": "PANTSIR-SM // 57E6M",
    },
    "keka_troll": {
        "base": (232, 224, 210),   # Hand-painted off-white hull
        "nose": (235, 92, 28),     # Safety-orange cone & strap-on boosters!
        "nozzle": (86, 68, 56),    # Scorched welded steel nozzle
        "band1": (22, 24, 28),     # Black/white roll-pattern checkers
        "band2": (235, 92, 28),
        "fin": (218, 165, 38),     # Riveted yellow sheet-metal fins
        "radome_gloss": 80,
        "stencil": "KEKA AEROSPACE // TROPOSPHERE",
    },
    "df17_tps": {
        "base": (52, 56, 62),      # Dark thermal protection carbon-carbon
        "nose": (34, 36, 40),      # Leading-edge UHTC obsidian
        "nozzle": (32, 36, 42),
        "band1": (212, 146, 38),
        "band2": (190, 48, 38),
        "fin": (62, 66, 72),
        "radome_gloss": 105,
        "stencil": "DF-17 HGV // PLA-RF",
    },
    "palianytsia_jet": {
        "base": (118, 126, 134),   # Matte slate/metallic composite
        "nose": (42, 46, 52),
        "nozzle": (38, 42, 48),
        "band1": (44, 108, 186),   # Subtle blue/yellow accent stripe
        "band2": (222, 184, 48),
        "fin": (128, 136, 144),
        "radome_gloss": 65,
        "stencil": "PALIANYTSIA // JET DRONE",
    },
    "iskander_ru": {
        "base": (132, 138, 122),   # Khaki-grey ballistic
        "nose": (48, 52, 56),      # Carbon radome cap
        "nozzle": (40, 44, 48),
        "band1": (195, 46, 40),
        "band2": (214, 166, 42),
        "fin": (118, 124, 110),
        "radome_gloss": 72,
        "stencil": "9M723 // OTK",
    },
    "javelin_dark": {
        "base": (82, 88, 76),      # Olive-grey ATGM
        "nose": (36, 42, 50),      # Sapphire IIR seeker dome
        "nozzle": (40, 44, 48),
        "band1": (218, 170, 38),
        "band2": (146, 98, 44),
        "fin": (96, 102, 90),
        "radome_gloss": 28,
        "stencil": "ATGM // TRI-MODE",
    },
}


def build_theme(name: str, cfg: dict) -> None:
    al = Image.new("RGB", (SIZE, SIZE), cfg["base"])
    nm = Image.new("RGB", (SIZE, SIZE), (128, 128, 255))
    rm = Image.new("RGB", (SIZE, SIZE), (145, 145, 32))

    da = ImageDraw.Draw(al)
    dn = ImageDraw.Draw(nm)
    dr = ImageDraw.Draw(rm)

    u_body_end = int(SIZE * 0.72)

    # Panel shading & subtle grime variation
    for i, y0 in enumerate(range(0, SIZE, 128)):
        delta = 4 if i % 2 == 0 else -4
        c = tuple(max(0, min(255, v + delta)) for v in cfg["base"])
        da.rectangle([0, y0, u_body_end, y0 + 127], fill=c)

    # Top nose / radome zone
    y_nose = int(SIZE * 0.78)
    da.rectangle([0, y_nose, u_body_end, SIZE], fill=cfg["nose"])
    dr.rectangle([0, y_nose, u_body_end, SIZE], fill=(cfg["radome_gloss"], cfg["radome_gloss"], 16))
    da.rectangle([0, y_nose - 10, u_body_end, y_nose], fill=(55, 60, 66))

    # Warhead & motor bands
    y_b1 = int(SIZE * 0.56)
    y_b2 = int(SIZE * 0.40)
    da.rectangle([0, y_b1, u_body_end, y_b1 + 36], fill=cfg["band1"])
    da.rectangle([0, y_b2, u_body_end, y_b2 + 32], fill=cfg["band2"])

    # Boat-tail / nozzle zone
    y_noz = int(SIZE * 0.08)
    da.rectangle([0, 0, u_body_end, y_noz], fill=cfg["nozzle"])
    dr.rectangle([0, 0, u_body_end, y_noz], fill=(75, 75, 225))

    # Panel lines + rivets (recessed grooves in Normal + AO darken)
    for y in [y_noz, int(SIZE * 0.18), y_b2, y_b1, int(SIZE * 0.68), y_nose]:
        da.line([(0, y), (u_body_end, y)], fill=(38, 40, 44), width=3)
        dn.line([(0, y - 2), (u_body_end, y - 2)], fill=(128, 92, 240), width=2)
        dn.line([(0, y + 2), (u_body_end, y + 2)], fill=(128, 168, 240), width=2)
        for rx in range(28, u_body_end, 44):
            da.ellipse([rx - 2, y + 6, rx + 2, y + 10], fill=(70, 74, 80))
            dn.ellipse([rx - 2, y + 6, rx + 2, y + 10], fill=(128, 152, 252))

    # Longitudinal stringer seams
    for x in [u_body_end // 4, u_body_end // 2, (3 * u_body_end) // 4]:
        da.line([(x, y_noz), (x, y_nose)], fill=(54, 58, 62), width=2)
        dn.line([(x - 1, y_noz), (x - 1, y_nose)], fill=(100, 128, 242), width=1)
        dn.line([(x + 1, y_noz), (x + 1, y_nose)], fill=(156, 128, 242), width=1)

    # Extra KEKA checkerboard pattern!
    if name == "keka_troll":
        sq = 32
        for ix in range(0, u_body_end, sq):
            for iy in range(int(SIZE * 0.68), y_nose, sq):
                col = (24, 24, 24) if ((ix // sq + iy // sq) % 2 == 0) else (245, 240, 232)
                da.rectangle([ix, iy, min(u_body_end, ix + sq), min(y_nose, iy + sq)], fill=col)

    # Right sub-zones (fin / metallic / seeker)
    da.rectangle([u_body_end, 0, SIZE, int(SIZE * 0.50)], fill=cfg["fin"])
    dr.rectangle([u_body_end, 0, SIZE, int(SIZE * 0.50)], fill=(125, 125, 42))
    da.rectangle([u_body_end, int(SIZE * 0.50), SIZE, int(SIZE * 0.80)], fill=(68, 72, 78))
    dr.rectangle([u_body_end, int(SIZE * 0.50), SIZE, int(SIZE * 0.80)], fill=(62, 62, 230))
    da.rectangle([u_body_end, int(SIZE * 0.80), SIZE, SIZE], fill=(22, 26, 30))
    dr.rectangle([u_body_end, int(SIZE * 0.80), SIZE, SIZE], fill=(16, 16, 20))

    # Stencil text
    fnt = _font(32)
    da.text((u_body_end // 2 - 220, int(SIZE * 0.48)), cfg["stencil"], fill=(28, 30, 34), font=fnt)

    TEX_DIR.mkdir(parents=True, exist_ok=True)
    al.save(TEX_DIR / f"ng_{name}_albedo.png")
    nm.save(TEX_DIR / f"ng_{name}_normal.png")
    rm.save(TEX_DIR / f"ng_{name}_roughmet.png")
    print(f"[OK] Generated 2K PBR maps for ng_{name}")


def main() -> None:
    for name, cfg in THEMES_V2.items():
        build_theme(name, cfg)


if __name__ == "__main__":
    main()
