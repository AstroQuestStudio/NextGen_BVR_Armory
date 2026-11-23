"""Generate high-detail 2K multi-zone PBR vehicle, radar, tire, glass, AESA & canister textures for SAMs/C-RAM/Missiles v5.
UV Atlas Layout (2048x2048, pixel y=0 at top in PIL -> Blender v=1.0):
  Zone A (u: 0.00..0.50, v: 0.50..1.00): Primary Hull / Cab / Shelter panels + louvers + panel seams + rivets + stencil
  Zone B (u: 0.50..1.00, v: 0.50..1.00): Radome / Canister End-Caps / AESA Phased-Array Grid + Yellow Hazard Markings
  Zone C (u: 0.00..0.50, v: 0.00..0.50): Rubber Tire Tread (left half) + Steel Wheel Rim & Bolts (right half)
  Zone D (u: 0.50..1.00, v: 0.00..0.50): Sub-zones:
      v 0.25..0.50, u 0.50..0.75 -> Gunmetal / Hydraulic Chrome Pistons / Ammo Belt
      v 0.25..0.50, u 0.75..1.00 -> Dark Armored Tinted Glass / FLIR Optics (low roughness)
      v 0.00..0.25, u 0.50..0.75 -> Grille Louvers / Heat Exchanger Vents
      v 0.00..0.25, u 0.75..1.00 -> Hazard Chevrons / Tail Lights / Red-Amber Beacons
"""

from __future__ import annotations

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TEX_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Textures\NextGen_BVR_Armory")
S = 2048
H = 1024
Q = 512


def _font(sz: int):
    for p in (r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeui.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


SAM_THEMES = {
    "hq_cram": {
        "hull": (212, 196, 162),
        "hull_alt": (198, 182, 148),
        "radome": (238, 240, 244),
        "aesa": (214, 218, 222),
        "accent": (188, 46, 36),
        "metal": (88, 92, 98),
        "label": "CENTURION C-RAM",
    },
    "hq_irondome": {
        "hull": (148, 148, 130),
        "hull_alt": (132, 134, 118),
        "radome": (182, 184, 174),
        "aesa": (204, 206, 196),
        "accent": (216, 166, 42),
        "metal": (84, 88, 94),
        "label": "IRON DOME",
    },
    "hq_nato_sam": {
        "hull": (78, 90, 64),
        "hull_alt": (64, 76, 52),
        "radome": (166, 170, 156),
        "aesa": (190, 194, 180),
        "accent": (212, 164, 38),
        "metal": (82, 86, 92),
        "label": "IRIS-T / PATRIOT",
    },
    "hq_russia_sam": {
        "hull": (74, 88, 60),
        "hull_alt": (60, 72, 48),
        "radome": (192, 172, 128),  # Pantsir bronze-tan tracking radar dome!
        "aesa": (192, 172, 128),
        "accent": (198, 44, 38),     # S-400 red rings!
        "metal": (78, 84, 90),
        "label": "PANTSIR / S-400",
    },
    "hq_thaad_tan": {
        "hull": (206, 188, 150),
        "hull_alt": (188, 170, 134),
        "radome": (218, 206, 178),
        "aesa": (180, 166, 138),
        "accent": (190, 52, 40),
        "metal": (92, 96, 102),
        "label": "THAAD",
    },
    "hq_keka_rig": {
        "hull": (218, 146, 44),
        "hull_alt": (184, 92, 38),
        "radome": (238, 232, 220),
        "aesa": (235, 92, 28),
        "accent": (28, 28, 30),
        "metal": (94, 82, 74),
        "label": "KEKA SPACEPORT",
    },
}


def build_vehicle_atlas(name: str, cfg: dict) -> None:
    al = Image.new("RGB", (S, S), cfg["hull"])
    nm = Image.new("RGB", (S, S), (128, 128, 255))
    rm = Image.new("RGB", (S, S), (178, 168, 18))  # R=AO, G=Roughness, B=Metallic

    da, dn, dr = ImageDraw.Draw(al), ImageDraw.Draw(nm), ImageDraw.Draw(rm)

    # ---- ZONE A (top-left: y 0..1024, x 0..1024 -> Blender u 0..0.5, v 0.5..1.0) ----
    # Clean satin military armor plate with subtle perimeter bevel edge seam, fine rivets & gentle surface modulation (NO internal checkerboard!)
    da.rectangle([0, 0, 1024, 1024], fill=cfg["hull"])
    da.rectangle([28, 28, 996, 996], fill=cfg["hull"], outline=cfg["hull_alt"], width=10)
    da.rectangle([38, 38, 986, 986], outline=(max(0, cfg["hull_alt"][0] - 26), max(0, cfg["hull_alt"][1] - 26), max(0, cfg["hull_alt"][2] - 26)), width=3)
    dn.rectangle([36, 36, 988, 988], outline=(128, 108, 244), width=3)
    for rx in range(72, 960, 88):
        for ry in (54, 970):
            da.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=cfg["hull_alt"])
            dn.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=(128, 165, 250))
    # Subtle NATO/Russian tricolor camo bands (soft wide shapes so each box looks organic, never gridded)
    if name in ("hq_nato_sam", "hq_russia_sam"):
        da.polygon([(110, 140), (540, 110), (620, 420), (220, 460)], fill=(54, 62, 46))
        da.polygon([(460, 560), (910, 490), (940, 860), (510, 890)], fill=(96, 84, 56))
    elif name == "hq_cram":
        da.polygon([(140, 180), (490, 210), (440, 520), (160, 480)], fill=cfg["hull_alt"])

    # ---- ZONE B (top-right: y 0..1024, x 1024..2048 -> Blender u 0.5..1.0, v 0.5..1.0) ----
    # Left half: White/Bronze Radome + seam rings; Right half: AESA Phased Array T/R Honeycomb + Hazard border
    da.rectangle([1024, 0, 1536, 1024], fill=cfg["radome"])
    dr.rectangle([1024, 0, 1536, 1024], fill=(180, 55, 18))
    for ry in range(128, 1024, 256):
        da.line([(1024, ry), (1536, ry)], fill=(120, 124, 128), width=4)
        dn.line([(1024, ry), (1536, ry)], fill=(128, 90, 240), width=3)
    # Red accent stripe ring (S-400 canister / C-RAM / KEKA)
    da.rectangle([1024, 380, 1536, 440], fill=cfg["accent"])

    da.rectangle([1536, 0, 2048, 1024], fill=cfg["aesa"])
    dr.rectangle([1536, 0, 2048, 1024], fill=(165, 90, 75))
    # Micro T/R element dipole grid for AESA arrays & canister cross-caps!
    for gx in range(1552, 2036, 32):
        for gy in range(16, 1008, 32):
            da.rectangle([gx, gy, gx + 24, gy + 24], fill=(max(0, cfg["aesa"][0] - 24), max(0, cfg["aesa"][1] - 24), max(0, cfg["aesa"][2] - 24)))
            dn.rectangle([gx, gy, gx + 24, gy + 24], outline=(105, 105, 240), width=2)
    da.rectangle([1536, 0, 2048, 1024], outline=cfg["accent"], width=12)

    # ---- ZONE C (bottom-left: y 1024..2048, x 0..1024 -> Blender u 0..0.5, v 0..0.5) ----
    # Dark off-road treaded rubber (x 0..512) + armored 8-bolt wheel rim (x 512..1024)
    da.rectangle([0, 1024, 512, 2048], fill=(32, 34, 36))
    dr.rectangle([0, 1024, 512, 2048], fill=(140, 210, 8))
    for ty in range(1040, 2032, 48):
        da.rectangle([18, ty, 230, ty + 24], fill=(22, 24, 26))
        da.rectangle([272, ty + 22, 494, ty + 46], fill=(22, 24, 26))
        dn.rectangle([18, ty, 230, ty + 24], fill=(128, 175, 235))
        dn.rectangle([272, ty + 22, 494, ty + 46], fill=(128, 175, 235))

    # Matte dark rubber tire outer sidewall + recessed bolted alloy/olive rim in center (u 0.25..0.50, v 0.25..0.50 -> PIL x 512..1024, y 1024..1536)
    da.rectangle([512, 1024, 1024, 1536], fill=(34, 36, 38))
    dr.rectangle([512, 1024, 1024, 1536], fill=(150, 200, 12))
    da.ellipse([548, 1060, 988, 1500], fill=cfg["hull"], outline=(42, 44, 46), width=10)
    da.ellipse([588, 1100, 948, 1460], fill=cfg["hull_alt"], outline=(52, 54, 58), width=6)
    dr.ellipse([548, 1060, 988, 1500], fill=(185, 130, 120))
    da.ellipse([668, 1180, 868, 1380], fill=cfg["metal"], outline=(28, 30, 34), width=8)
    for k in range(10):
        import math
        ang = k * math.pi * 0.2
        bx = int(768 + 145 * math.cos(ang))
        by = int(1280 + 145 * math.sin(ang))
        da.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(208, 212, 216))
        dn.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(128, 185, 250))

    # ---- ZONE D (bottom-right: y 1024..2048, x 1024..2048 -> Blender u 0.5..1.0, v 0..0.5) ----
    # Blender v 0.25..0.50 -> PIL y 1024..1536
    # Gunmetal / chrome pistons / brass belt (x 1024..1536)
    da.rectangle([1024, 1024, 1536, 1536], fill=cfg["metal"])
    dr.rectangle([1024, 1024, 1536, 1536], fill=(185, 92, 210))
    # Brass 20mm ammo stripe strip at top edge of metal block
    da.rectangle([1024, 1024, 1536, 1180], fill=(198, 156, 54))
    for ax in range(1036, 1528, 24):
        da.line([(ax, 1024), (ax, 1180)], fill=(86, 66, 22), width=4)
        dn.line([(ax, 1024), (ax, 1180)], fill=(175, 128, 240), width=4)

    # Armored ballistic tinted glass / FLIR lens (x 1536..2048, y 1024..1536 -> Blender u 0.75..1.0, v 0.25..0.50)
    da.rectangle([1536, 1024, 2048, 1536], fill=(18, 28, 34))
    dr.rectangle([1536, 1024, 2048, 1536], fill=(220, 12, 35))  # Gloss specular!

    # Blender v 0.00..0.25 -> PIL y 1536..2048
    # Grille / Radiator cooling louvers (x 1024..1536, y 1536..2048 -> Blender u 0.50..0.75, v 0.00..0.25)
    da.rectangle([1024, 1536, 1536, 2048], fill=(38, 42, 44))
    for ly in range(1556, 2036, 28):
        da.line([(1040, ly), (1520, ly)], fill=(96, 100, 104), width=10)
        dn.line([(1040, ly), (1520, ly)], fill=(128, 190, 230), width=8)

    # Hazard chevrons & lights (x 1536..2048, y 1536..2048 -> Blender u 0.75..1.00, v 0.00..0.25)
    da.rectangle([1536, 1536, 2048, 2048], fill=(224, 168, 28))
    for sx in range(1536, 2148, 96):
        da.polygon([(sx, 1536), (sx + 48, 1536), (sx - 120, 2048), (sx - 168, 2048)], fill=(24, 24, 24))
    da.rectangle([1536, 1536, 1792, 1740], fill=(240, 236, 210))  # White headlight lens
    da.rectangle([1792, 1536, 2048, 1740], fill=(210, 36, 30))   # Red tail light

    TEX_DIR.mkdir(parents=True, exist_ok=True)
    al.save(TEX_DIR / f"ng_{name}_albedo.png")
    nm.save(TEX_DIR / f"ng_{name}_normal.png")
    rm.save(TEX_DIR / f"ng_{name}_roughmet.png")
    print(f"[OK] Built 2K vehicle atlas ng_{name}")


def main() -> None:
    for name, cfg in SAM_THEMES.items():
        build_vehicle_atlas(name, cfg)


if __name__ == "__main__":
    main()
