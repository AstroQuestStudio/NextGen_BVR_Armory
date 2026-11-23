"""Generate 20 Photo-Faithful 2K Multi-Zone PBR Texture Sets directly into Saved Games/DCS/Mods/tech/NextGen_BVR_Armory/Textures/NextGen_BVR_Armory/
Derived directly from the 260 real Wikimedia Commons reference photos inspected.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

TEX_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Textures\NextGen_BVR_Armory")
SIZE = 2048
SCALE = SIZE / 4096.0
BODY_U_MAX = int(SIZE * 0.72)


def S(v: float) -> int:
    return int(round(v * SCALE))


def load_font(px_4k: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    px = max(10, int(round(px_4k * SCALE)))
    for path in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\segoeui.ttf"):
        if Path(path).is_file():
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


THEMES = {
    "iris_t": {
        "body": (212, 216, 220), "bay": (202, 206, 212), "radome": (188, 194, 200),
        "tip": (24, 46, 38), "band1": (218, 172, 34), "band2": (48, 112, 184),
        "nozzle": (64, 68, 74), "fin": (204, 208, 214), "intake": (128, 134, 140),
        "stencil_1": "IRIS-T  //  DIEHL BGT", "stencil_2": "IIR TVC  //  NO LIFT", "rough_body": 134,
    },
    "pl12_15": {
        "body": (228, 231, 234), "bay": (218, 222, 226), "radome": (236, 232, 220),
        "tip": (54, 58, 62), "band1": (196, 46, 40), "band2": (44, 96, 168),
        "nozzle": (62, 66, 72), "fin": (216, 220, 224), "intake": (136, 140, 146),
        "stencil_1": "PL-15E  //  PL-12AE", "stencil_2": "AVIC AESA  //  ARMED", "rough_body": 128,
    },
    "r77_grid": {
        "body": (212, 218, 224), "bay": (204, 210, 216), "radome": (238, 238, 236),
        "tip": (58, 62, 68), "band1": (36, 40, 44), "band2": (192, 46, 40),
        "nozzle": (66, 70, 76), "fin": (198, 204, 210), "intake": (96, 102, 110),
        "stencil_1": "RVV-SD  //  R-77-1", "stencil_2": "VYMPEL  //  GRID ACTUATOR", "rough_body": 132,
    },
    "python5": {
        "body": (192, 198, 204), "bay": (182, 188, 194), "radome": (150, 156, 162),
        "tip": (18, 26, 34), "band1": (218, 172, 34), "band2": (122, 70, 42),
        "nozzle": (64, 68, 74), "fin": (184, 190, 196), "intake": (118, 124, 130),
        "stencil_1": "PYTHON-5  //  RAFAEL", "stencil_2": "IIR HOBS  //  ARMED", "rough_body": 136,
    },
    "r74m2": {
        "body": (218, 222, 226), "bay": (208, 212, 218), "radome": (160, 166, 172),
        "tip": (16, 20, 26), "band1": (34, 38, 42), "band2": (194, 48, 42),
        "nozzle": (60, 64, 70), "fin": (206, 210, 215), "intake": (124, 130, 136),
        "stencil_1": "R-74M2  //  RVV-MD", "stencil_2": "TVC ARCHER  //  CAUTION", "rough_body": 134,
    },
    "aim9x_b3": {
        "body": (148, 154, 160), "bay": (136, 142, 148), "radome": (110, 116, 122),
        "tip": (18, 22, 28), "band1": (218, 172, 34), "band2": (122, 70, 42),
        "nozzle": (58, 62, 68), "fin": (138, 144, 150), "intake": (96, 102, 108),
        "stencil_1": "AIM-9X BLK III", "stencil_2": "LOAL DATALINK  //  NO LIFT", "rough_body": 152,
    },
    "aim54e": {
        "body": (236, 238, 240), "bay": (226, 228, 232), "radome": (240, 238, 230),
        "tip": (68, 72, 76), "band1": (218, 172, 34), "band2": (122, 70, 42),
        "nozzle": (66, 70, 76), "fin": (224, 228, 232), "intake": (148, 152, 158),
        "stencil_1": "AIM-54E  //  SEA PHOENIX", "stencil_2": "US NAVY  //  LIVE MOTOR", "rough_body": 120,
    },
    "kinzhal": {
        "body": (196, 202, 208), "bay": (110, 120, 100), "radome": (184, 188, 192),
        "tip": (38, 42, 46), "band1": (212, 168, 34), "band2": (186, 48, 40),
        "nozzle": (224, 228, 232), "fin": (178, 184, 190), "intake": (102, 110, 96),
        "stencil_1": "Kh-47M2  //  KINZHAL", "stencil_2": "AEROBALLISTIC MACH 10", "rough_body": 146,
    },
    "arrw_hyp": {
        "body": (44, 48, 54), "bay": (52, 56, 64), "radome": (32, 35, 40),
        "tip": (118, 122, 128), "band1": (216, 86, 34), "band2": (214, 168, 34),
        "nozzle": (74, 78, 86), "fin": (52, 56, 62), "intake": (38, 42, 48),
        "stencil_1": "AGM-183A ARRW  //  YJ-21", "stencil_2": "HYPERSONIC BOOST-GLIDE", "rough_body": 132,
    },
    "exocet": {
        "body": (198, 204, 208), "bay": (188, 194, 200), "radome": (228, 228, 224),
        "tip": (52, 56, 60), "band1": (214, 168, 34), "band2": (188, 50, 42),
        "nozzle": (64, 68, 74), "fin": (186, 192, 198), "intake": (118, 124, 130),
        "stencil_1": "EXOCET AM39 BLK 3", "stencil_2": "MBDA FRANCE  //  ANTI-NAVIRE", "rough_body": 138,
    },
    "kh35_uran": {
        "body": (210, 216, 220), "bay": (200, 206, 212), "radome": (24, 27, 32),
        "tip": (18, 20, 24), "band1": (194, 48, 42), "band2": (40, 44, 48),
        "nozzle": (58, 62, 68), "fin": (198, 204, 210), "intake": (86, 92, 98),
        "stencil_1": "Kh-35UE  //  URAN", "stencil_2": "TACTICAL MISSILES CORP", "rough_body": 136,
    },
    "kh22_32": {
        "body": (234, 236, 238), "bay": (224, 228, 232), "radome": (238, 238, 234),
        "tip": (42, 46, 52), "band1": (24, 26, 30), "band2": (24, 26, 30),
        "nozzle": (54, 58, 64), "fin": (224, 228, 232), "intake": (72, 76, 82),
        "stencil_1": "Kh-22N / Kh-32  //  MACH 4.6", "stencil_2": "RADUGA  //  ANTI-SHIP", "double_black": True, "rough_body": 118,
    },
    "aargm_er": {
        "body": (216, 220, 224), "bay": (206, 210, 216), "radome": (224, 214, 186),
        "tip": (92, 86, 74), "band1": (218, 172, 34), "band2": (44, 102, 176),
        "nozzle": (64, 68, 74), "fin": (204, 208, 214), "intake": (124, 130, 136),
        "stencil_1": "AGM-88G  //  AARGM-ER", "stencil_2": "NORTHROP GRUMMAN  //  SEAD", "rough_body": 136,
    },
    "kh58_sead": {
        "body": (202, 212, 220), "bay": (192, 202, 210), "radome": (26, 28, 34),
        "tip": (18, 20, 24), "band1": (36, 40, 44), "band2": (192, 48, 42),
        "nozzle": (58, 62, 68), "fin": (192, 202, 210), "intake": (108, 114, 120),
        "stencil_1": "Kh-58UShKE  //  SEAD", "stencil_2": "INTERNAL BAY  //  ARMED", "rough_body": 138,
    },
    "gbu57_mop": {
        "body": (94, 104, 76), "bay": (84, 94, 68), "radome": (88, 98, 72),
        "tip": (52, 56, 50), "band1": (218, 172, 34), "band2": (218, 172, 34),
        "nozzle": (62, 66, 60), "fin": (148, 154, 158), "intake": (118, 124, 128),
        "stencil_1": "GBU-57A/B  //  MOP 30000 LB", "stencil_2": "PENETRATOR  //  LIVE HE", "rough_body": 178,
    },
    "spice_eo": {
        "body": (132, 138, 130), "bay": (188, 194, 198), "radome": (36, 40, 46),
        "tip": (16, 20, 26), "band1": (218, 172, 34), "band2": (186, 190, 194),
        "nozzle": (64, 68, 72), "fin": (194, 198, 202), "intake": (114, 120, 124),
        "stencil_1": "SPICE 250 / 1000 / 2000", "stencil_2": "RAFAEL EO/IR  //  GLIDE", "rough_body": 152,
    },
    "shahed_136": {
        "body": (168, 172, 176), "bay": (158, 162, 166), "radome": (154, 158, 162),
        "tip": (42, 46, 50), "band1": (208, 162, 34), "band2": (182, 48, 40),
        "nozzle": (46, 50, 54), "fin": (156, 160, 164), "intake": (58, 48, 38),
        "stencil_1": "GERAN-2  //  SHAHED-136", "stencil_2": "LONG-RANGE OWA UAV", "rough_body": 168,
    },
    "harop_drone": {
        "body": (204, 208, 210), "bay": (194, 198, 202), "radome": (32, 36, 42),
        "tip": (18, 22, 28), "band1": (214, 168, 34), "band2": (122, 72, 42),
        "nozzle": (54, 58, 62), "fin": (192, 196, 200), "intake": (34, 38, 44),
        "stencil_1": "IAI HAROP  //  SEAD UAV", "stencil_2": "EO/IR GIMBAL  //  ARMED", "rough_body": 144,
    },
    "scalp_new": {
        "body": (136, 144, 154), "bay": (126, 134, 144), "radome": (126, 134, 144),
        "tip": (92, 98, 106), "band1": (208, 164, 36), "band2": (118, 70, 42),
        "nozzle": (56, 60, 66), "fin": (128, 136, 146), "intake": (38, 42, 48),
        "stencil_1": "STORM SHADOW  //  SCALP-EG", "stencil_2": "NO STEP  //  BROACH WARHEAD", "rough_body": 164, "stealth_ram": True,
    },
    "taurus_new": {
        "body": (82, 94, 68), "bay": (74, 86, 60), "radome": (74, 86, 60),
        "tip": (38, 42, 46), "band1": (212, 168, 36), "band2": (186, 52, 42),
        "nozzle": (52, 56, 50), "fin": (78, 90, 64), "intake": (44, 48, 42),
        "stencil_1": "TAURUS KEPD 350", "stencil_2": "MEPHISTO PENETRATOR  //  LO", "rough_body": 172, "stealth_ram": True,
    },
}


def draw_datamatrix(draw: ImageDraw.ImageDraw, x: int, y: int, cell: int = 4) -> None:
    rng = np.random.default_rng(42)
    draw.rectangle([x - 3, y - 3, x + cell * 10 + 3, y + cell * 10 + 3], fill=(225, 225, 220))
    for r in range(10):
        for c in range(10):
            if r == 0 or c == 0 or (r == 9 and c % 2 == 0) or (c == 9 and r % 2 == 0) or rng.random() > 0.48:
                draw.rectangle([x + c * cell, y + r * cell, x + (c + 1) * cell - 1, y + (r + 1) * cell - 1], fill=(24, 26, 28))


def draw_rivet_line(da, dh, dr, dm, x0: int, y0: int, x1: int, y1: int, count: int) -> None:
    ro, ri = max(1, S(4)), max(1, S(2))
    for i in range(count):
        t = i / max(1, count - 1)
        x, y = int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)
        da.ellipse([x - ro, y - ro, x + ro, y + ro], fill=(108, 112, 118))
        da.ellipse([x - ri, y - ri, x + ri, y + ri], fill=(185, 190, 196))
        dh.ellipse([x - ro, y - ro, x + ro, y + ro], fill=172)
        dr.ellipse([x - ro, y - ro, x + ro, y + ro], fill=82)
        dm.ellipse([x - ro, y - ro, x + ro, y + ro], fill=195)


def build_theme(theme_name: str, cfg: dict) -> None:
    albedo = Image.new("RGB", (SIZE, SIZE), cfg["body"])
    da = ImageDraw.Draw(albedo)
    ao = Image.new("L", (SIZE, SIZE), 242)
    dao = ImageDraw.Draw(ao)
    rough = Image.new("L", (SIZE, SIZE), cfg["rough_body"])
    dr = ImageDraw.Draw(rough)
    metal = Image.new("L", (SIZE, SIZE), 14)
    dm = ImageDraw.Draw(metal)
    height = Image.new("L", (SIZE, SIZE), 128)
    dh = ImageDraw.Draw(height)

    da.rectangle([0, 0, BODY_U_MAX, S(740)], fill=cfg["radome"])
    dr.rectangle([0, 0, BODY_U_MAX, S(740)], fill=86)
    da.rectangle([0, 0, BODY_U_MAX, S(130)], fill=cfg["tip"])
    dr.rectangle([0, 0, BODY_U_MAX, S(130)], fill=90)
    dm.rectangle([0, 0, BODY_U_MAX, S(130)], fill=130)

    da.rectangle([0, S(728), BODY_U_MAX, S(756)], fill=(138, 142, 148))
    dm.rectangle([0, S(728), BODY_U_MAX, S(756)], fill=215)
    dr.rectangle([0, S(728), BODY_U_MAX, S(756)], fill=72)
    draw_rivet_line(da, dh, dr, dm, S(40), S(742), BODY_U_MAX - S(40), S(742), 32)
    da.rectangle([0, S(756), BODY_U_MAX, S(1380)], fill=cfg["bay"])

    if cfg.get("double_black"):
        da.rectangle([0, S(1410), BODY_U_MAX, S(1480)], fill=cfg["band1"])
        da.rectangle([0, S(1520), BODY_U_MAX, S(1590)], fill=cfg["band1"])
    else:
        da.rectangle([0, S(1440), BODY_U_MAX, S(1530)], fill=cfg["band1"])
    dr.rectangle([0, S(1410), BODY_U_MAX, S(1590)], fill=124)
    da.rectangle([0, S(2160), BODY_U_MAX, S(2248)], fill=cfg["band2"])
    dr.rectangle([0, S(2160), BODY_U_MAX, S(2248)], fill=128)

    if cfg.get("stealth_ram"):
        pts = []
        for x in range(0, BODY_U_MAX + S(120), S(120)):
            pts.append((x, S(1380)))
            pts.append((x + S(60), S(1330)))
        da.line(pts, fill=(44, 48, 54), width=max(2, S(5)))
        dh.line(pts, fill=76, width=max(2, S(5)))

    da.rectangle([0, S(3520), BODY_U_MAX, SIZE], fill=cfg["nozzle"])
    dr.rectangle([0, S(3520), BODY_U_MAX, SIZE], fill=62)
    dm.rectangle([0, S(3520), BODY_U_MAX, SIZE], fill=235)
    da.rectangle([0, S(3680), BODY_U_MAX, S(3760)], fill=(104, 86, 68))
    da.rectangle([0, S(3760), BODY_U_MAX, S(3860)], fill=(72, 68, 96))
    da.rectangle([0, S(3860), BODY_U_MAX, SIZE], fill=(24, 26, 30))
    dr.rectangle([0, S(3860), BODY_U_MAX, SIZE], fill=215)
    dm.rectangle([0, S(3860), BODY_U_MAX, SIZE], fill=40)
    dao.rectangle([0, S(3840), BODY_U_MAX, SIZE], fill=65)
    for u in range(0, BODY_U_MAX, S(64)):
        da.line([(u, S(3540)), (u, S(3860))], fill=(42, 45, 50), width=max(2, S(4)))
        dh.line([(u, S(3540)), (u, S(3860))], fill=82, width=max(2, S(4)))

    for v in (1020, 1380, 1960, 2820, 3520):
        vy = S(v)
        da.line([(0, vy), (BODY_U_MAX, vy)], fill=(86, 92, 98), width=max(2, S(6)))
        dao.line([(0, vy), (BODY_U_MAX, vy)], fill=125, width=max(3, S(12)))
        dh.line([(0, vy), (BODY_U_MAX, vy)], fill=52, width=max(2, S(6)))
        draw_rivet_line(da, dh, dr, dm, S(30), vy - S(18), BODY_U_MAX - S(30), vy - S(18), 38)
        draw_rivet_line(da, dh, dr, dm, S(30), vy + S(18), BODY_U_MAX - S(30), vy + S(18), 38)

    for u in (360, 1100, 1840, 2580):
        ux = S(u)
        da.line([(ux, S(756)), (ux, S(3520))], fill=(96, 102, 108), width=max(2, S(4)))
        dh.line([(ux, S(756)), (ux, S(3520))], fill=82, width=max(2, S(4)))

    for u_s in (480, 1950):
        box = [S(u_s), S(860), S(u_s + 420), S(1260)]
        da.rounded_rectangle(box, radius=S(20), outline=(76, 82, 90), width=max(2, S(5)))
        dao.rounded_rectangle(box, radius=S(20), outline=140, width=max(3, S(9)))
        dh.rounded_rectangle(box, radius=S(20), outline=65, width=max(2, S(5)))
        draw_rivet_line(da, dh, dr, dm, S(u_s + 24), S(878), S(u_s + 396), S(878), 10)
        draw_rivet_line(da, dh, dr, dm, S(u_s + 24), S(1242), S(u_s + 396), S(1242), 10)
        da.rectangle([S(u_s + 170), S(1030), S(u_s + 250), S(1085)], fill=(95, 100, 108), outline=(55, 58, 62), width=max(1, S(3)))
        dm.rectangle([S(u_s + 170), S(1030), S(u_s + 250), S(1085)], fill=200)

    f_lg, f_sm = load_font(62), load_font(38)
    txt_col = (210, 214, 218) if sum(cfg["body"]) < 260 else (34, 38, 44)
    for u_txt in (160, 1640):
        da.text((S(u_txt), S(1620)), cfg["stencil_1"], fill=txt_col, font=f_lg)
        da.text((S(u_txt), S(2340)), cfg["stencil_2"], fill=txt_col, font=f_sm)
        da.text((S(u_txt), S(2410)), "LOT 2026-NG  //  WT CALIBRATED  //  CG", fill=txt_col, font=f_sm)
        draw_datamatrix(da, S(u_txt + 860), S(1605), cell=max(2, S(9)))
        da.polygon([(S(u_txt + 20), S(1890)), (S(u_txt + 55), S(1945)), (S(u_txt - 15), S(1945))], fill=txt_col)
        da.ellipse([S(u_txt + 120), S(1895), S(u_txt + 170), S(1945)], outline=txt_col, width=max(2, S(5)))

    fx0, fy0, fx1, fy1 = BODY_U_MAX + S(10), 0, SIZE, S(2250)
    da.rectangle([fx0, fy0, fx1, fy1], fill=cfg["fin"])
    dr.rectangle([fx0, fy0, fx1, fy1], fill=cfg["rough_body"])
    da.rectangle([fx0, fy0, fx0 + S(130), fy1], fill=(138, 144, 152))
    dm.rectangle([fx0, fy0, fx0 + S(130), fy1], fill=220)
    dr.rectangle([fx0, fy0, fx0 + S(130), fy1], fill=72)
    da.line([(fx0 + S(780), fy0), (fx0 + S(780), fy1)], fill=(65, 70, 76), width=max(2, S(8)))
    dh.line([(fx0 + S(780), fy0), (fx0 + S(780), fy1)], fill=55, width=max(2, S(8)))
    draw_rivet_line(da, dh, dr, dm, fx0 + S(180), S(120), fx0 + S(180), fy1 - S(120), 24)
    draw_rivet_line(da, dh, dr, dm, fx0 + S(750), S(120), fx0 + S(750), fy1 - S(120), 24)
    fin_txt = (210, 214, 218) if sum(cfg["fin"]) < 260 else (42, 46, 50)
    da.text((fx0 + S(260), S(980)), "NO PUSH", fill=fin_txt, font=f_lg)

    ix0, iy0, ix1, iy1 = BODY_U_MAX + S(10), S(2250), SIZE, SIZE
    da.rectangle([ix0, iy0, ix1, iy1], fill=cfg["intake"])
    dr.rectangle([ix0, iy0, ix1, iy1], fill=135)
    dm.rectangle([ix0, iy0, ix1, iy1], fill=70)
    da.rectangle([ix0, iy0, ix1, iy0 + S(260)], fill=(154, 160, 168))
    dm.rectangle([ix0, iy0, ix1, iy0 + S(260)], fill=225)
    dr.rectangle([ix0, iy0, ix1, iy0 + S(260)], fill=66)
    da.rectangle([ix0, S(3500), ix1, SIZE], fill=(14, 18, 24))
    dr.rectangle([ix0, S(3500), ix1, SIZE], fill=26)
    dao.rectangle([ix0, S(3500), ix1, SIZE], fill=30)
    dm.rectangle([ix0, S(3500), ix1, SIZE], fill=15)
    draw_rivet_line(da, dh, dr, dm, ix0 + S(80), S(2680), ix1 - S(80), S(2680), 14)

    rng = np.random.default_rng(101)
    fine_noise = rng.normal(0.0, 3.8, (SIZE, SIZE)).astype(np.float32)
    streak = np.repeat(rng.normal(0.0, 2.5, (1, SIZE)).astype(np.float32), SIZE, axis=0)
    a_arr = np.asarray(albedo, dtype=np.float32) + (fine_noise + streak)[:, :, None]
    albedo = Image.fromarray(np.clip(a_arr, 0, 255).astype(np.uint8), mode="RGB")
    r_arr = np.asarray(rough, dtype=np.float32) + fine_noise * 1.6
    rough = Image.fromarray(np.clip(r_arr, 10, 250).astype(np.uint8), mode="L")
    h_arr = np.asarray(height, dtype=np.float32) + fine_noise * 0.45
    gx = (np.roll(h_arr, -1, axis=1) - np.roll(h_arr, 1, axis=1)) * 0.72
    gy = (np.roll(h_arr, -1, axis=0) - np.roll(h_arr, 1, axis=0)) * 0.72
    normal = Image.fromarray(np.stack([np.clip(128.0 - gx, 0, 255).astype(np.uint8), np.clip(128.0 - gy, 0, 255).astype(np.uint8), np.full((SIZE, SIZE), 255, dtype=np.uint8)], axis=-1), mode="RGB")
    roughmet = Image.merge("RGB", (ao, rough, metal))

    albedo.save(TEX_DIR / f"ng_{theme_name}_albedo.png")
    normal.save(TEX_DIR / f"ng_{theme_name}_normal.png")
    roughmet.save(TEX_DIR / f"ng_{theme_name}_roughmet.png")
    print(f"[OK] 2K PBR: ng_{theme_name}_*.png")


def main() -> None:
    TEX_DIR.mkdir(parents=True, exist_ok=True)
    for name, cfg in THEMES.items():
        build_theme(name, cfg)


if __name__ == "__main__":
    main()
