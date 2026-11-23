"""Generate 4 labeled high-resolution contact sheets (1920px wide) showing ALL 79 EDM shapes
from docs/renders/*.png so visitors can visually inspect every model directly on the GitHub README.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(r"C:\Users\trufa\NextGen_BVR_Armory")
RENDERS = REPO / "docs" / "renders"
DOCS = REPO / "docs"

SHEETS = [
    (
        "sheet_01_sam_and_cram.png",
        "NEXTGEN ARMORY v5.0 — SURFACE AIR DEFENSES, RADARS & C-RAM (11 UNITS)",
        4,
        [
            ("ng_cram_centurion",  "Centurion C-RAM Phalanx (20mm)"),
            ("ng_iron_dome_ln",    "Iron Dome 5x4 Tamir Launcher"),
            ("ng_iron_dome_radar", "EL/M-2084 MMR AESA Radar"),
            ("ng_irist_slm_ln",    "IRIS-T SLM 8-Cell MAN HX 8x8"),
            ("ng_trml_4d_radar",   "Hensoldt TRML-4D AESA Radar"),
            ("ng_sampt_aster30",   "Eurosam SAMP/T Aster 30"),
            ("ng_pantsir_sm",      "Pantsir-SM 96K6 (KamAZ-6560)"),
            ("ng_patriot_pac3_ln", "Patriot M903 PAC-3 MSE (16-Cell)"),
            ("ng_thaad_ln",        "THAAD M1120 8-Tube Exo-ABM"),
            ("ng_s400_tel",        "S-400 Triumf 5P85SM2 (40N6)"),
            ("ng_keka_launcher",   "KEKA Troposphere Launch Pad"),
        ],
    ),
    (
        "sheet_02_aam_and_sam_missiles.png",
        "AIR-TO-AIR (BVR / WVR / RAMJET) & SAM INTERCEPTOR SHAPES (28 EDM MODELS)",
        5,
        [
            ("ng_aim120a",         "AIM-120A AMRAAM"),
            ("ng_aim120cd",        "AIM-120C-5/7/8 / D-3"),
            ("ng_aim260",          "AIM-260A JATM / Sky Sting"),
            ("ng_aim174b",         "AIM-174B Gunslinger / SM-6"),
            ("ng_aim54e",          "AIM-54C+ / AIM-54E Phoenix"),
            ("ng_meteor",          "MBDA Meteor / Gokhan / Astra-3"),
            ("ng_mica_ng",         "MBDA MICA / MICA NG"),
            ("ng_iris_t",          "IRIS-T / IRIS-T Blk II"),
            ("ng_aim9x_b3",        "AIM-9X Blk II+ / Blk III"),
            ("ng_asraam_sleek",    "ASRAAM Blk 6 / Magic III"),
            ("ng_python5",         "Python-4/5 / PL-10 / PL-10E"),
            ("ng_peregrine",       "Peregrine / Akdogan Mini-AAM"),
            ("ng_aam4b",           "Mitsubishi AAM-4B / R-27EA"),
            ("ng_gokdogan_astra",  "Astra Mk 1/2 & Gokdogan"),
            ("ng_r77_grid",        "R-77-1 Grid-Fin (RVV-SD)"),
            ("ng_r77m",            "R-77M (Izdeliye 180)"),
            ("ng_r74m2",           "R-74M / R-74M2 / RVV-MD2"),
            ("ng_r37m",            "R-37M RVV-BD / KS-172"),
            ("ng_pl12a",           "PL-12A / I-Derby ER / LD-10"),
            ("ng_pl15",            "PL-15 AESA BVR"),
            ("ng_pl15e",           "PL-15E / PL-16 Folded-Fin"),
            ("ng_pl17_long",       "PL-17 AWACS-Killer"),
            ("ng_sam_tamir",       "Tamir / ESSM-B2 / 57E6M / RAM"),
            ("ng_sam_irist_slm",   "IRIS-T SLM / Barak-MX / CAMM-ER"),
            ("ng_sam_aster30",     "Aster 30 B1NT / Aster 15 / 9M96E2"),
            ("ng_sam_pac3_mse",    "PAC-3 MSE / Stunner HTK"),
            ("ng_sam_thaad",       "THAAD KKV / Arrow-3 / HQ-19"),
            ("ng_sam_40n6",        "S-400 40N6 / 48N6DM / SM-3 IIA"),
        ],
    ),
    (
        "sheet_03_cruise_naval_sead_ballistic.png",
        "CRUISE, ANTI-SHIP, SEAD & HYPERSONIC / BALLISTIC ARSENAL (23 EDM MODELS)",
        5,
        [
            ("ng_tomahawk_v",      "BGM-109 Tomahawk Blk IV/V"),
            ("ng_stealth_cruise",  "SCALP-EG / Kh-101 / Kh-50"),
            ("ng_jassm_taurus",    "JASSM-ER/XR / TAURUS / SOM / Kh-69"),
            ("ng_kalibr_3m54",     "3M54 Kalibr / KD-88 / Delilah"),
            ("ng_spear_ew",        "MBDA SPEAR-EW Stand-In Jammer"),
            ("ng_exocet_am39",     "Exocet AM39 / MM40-3c / Sea Venom"),
            ("ng_kh35u",           "Kh-35U/UE / C-802A / Haeseong"),
            ("ng_nsm_jsm",         "NSM / JSM / Gabriel V / Blue Spear"),
            ("ng_brahmos_intake",  "BrahMos-A/NG & P-800 Oniks"),
            ("ng_kh31_ramjet",     "Kh-31PM / YJ-12 / ASM-3"),
            ("ng_kh22_32",         "Kh-22N / Kh-32 Supersonic"),
            ("ng_aargm_er",        "AGM-88G AARGM-ER / AGM-88E"),
            ("ng_kh58ushke",       "Kh-58UShKE / Kh-25MPU / Kh-28"),
            ("ng_alarm_sead",      "ALARM / MAR-1 / ARMAT SEAD"),
            ("ng_rudram_arm",      "DRDO Rudram-1/2 / CM-102"),
            ("ng_kinzhal",         "Kh-47M2 Kinzhal / CM-400AKG"),
            ("ng_arrw",            "AGM-183A ARRW HGV"),
            ("ng_df17_waverider",  "DF-17 Waverider / DF-21D"),
            ("ng_zircon",          "3M22 Zircon / YJ-21 Hypersonic"),
            ("ng_hypersonic",      "HALO Hypersonic Anti-Ship"),
            ("ng_iskander_atacms", "Iskander / ATACMS / Tayfun / KN-23"),
            ("ng_rampage_lora",    "Rampage / Air LORA / ROCKS"),
            ("ng_gmlrs_m31",       "M31A2 / ER-GMLRS / Tornado-S"),
        ],
    ),
    (
        "sheet_04_glide_drones_atgm_keka.png",
        "SMART GLIDE BOMBS, DRONES, ATGMs, ROCKETS & KEKA TROLL COLLECTION (17 EDM MODELS)",
        5,
        [
            ("ng_gbu57_mop",       "GBU-57A/B 30,000lb MOP"),
            ("ng_umpb_d30",        "UMPB D-30SN / 5R / JDAM-ER"),
            ("ng_heavy_umpk",      "FAB-250/500/1500/3000 UMPK"),
            ("ng_spice_glide",     "Rafael SPICE-250/1000/2000"),
            ("ng_glide_sdb",       "GBU-53 / GBU-39 / SPEAR 3 / Tolun"),
            ("ng_aasm_hammer",     "AASM-250/500/1000 Hammer"),
            ("ng_durandal_runway", "BLU-107 Durandal / ODAB-500"),
            ("ng_shahed_136",      "Shahed-136 / 131 / KUB-BLA"),
            ("ng_palianytsia_jet", "Palianytsia / Peklo / Shahed-238"),
            ("ng_harop",           "IAI Harop / Harpy NG / ALTIUS"),
            ("ng_loitering_x",     "Lancet-3/3M / HERO / Kargu / SB600"),
            ("ng_atgm_quad",       "JAGM / Brimstone 2-3 / Spike / Kornet"),
            ("ng_javelin_top",     "Javelin-F / Spike-LR2 / HJ-12 / OMTAS"),
            ("ng_kh38_grom",       "Kh-38MLE/MTE / Grom-E1 / LMUR-305"),
            ("ng_guided_rocket",   "APKWS II / FALCO / CIRIT / S-8KOR"),
            ("ng_keka_tropo5",     "KEKA Troposphere-5 / Baguette-II"),
            ("ng_keka_tropo6",     "KEKA Troposphere-6 / Njiwa-1"),
        ],
    ),
]


def _font(sz: int):
    for p in (r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\arialbd.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def build_sheet(out_name: str, title: str, cols: int, items: list[tuple[str, str]]) -> None:
    cell_w, cell_h = 460, 260
    lbl_h = 52
    pad = 16
    hdr_h = 68
    rows = math.ceil(len(items) / cols)
    W = pad + cols * (cell_w + pad)
    H = hdr_h + pad + rows * (cell_h + lbl_h + pad)

    canvas = Image.new("RGB", (W, H), (14, 17, 22))
    dr = ImageDraw.Draw(canvas)
    f_hdr = _font(32)
    f_lbl = _font(19)
    f_sub = _font(15)

    # Top banner
    dr.rectangle([0, 0, W, hdr_h], fill=(22, 28, 38))
    dr.rectangle([0, hdr_h - 3, W, hdr_h], fill=(58, 130, 220))
    dr.text((22, 16), title, fill=(238, 242, 248), font=f_hdr)

    for idx, (shape, label) in enumerate(items):
        r, c = divmod(idx, cols)
        x0 = pad + c * (cell_w + pad)
        y0 = hdr_h + pad + r * (cell_h + lbl_h + pad)

        img_path = RENDERS / f"{shape}.png"
        if not img_path.exists():
            raise FileNotFoundError(f"Missing render: {img_path}")
        tile = Image.open(img_path).convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        canvas.paste(tile, (x0, y0))

        # Label bar & border
        dr.rectangle([x0, y0 + cell_h, x0 + cell_w, y0 + cell_h + lbl_h], fill=(26, 32, 42))
        dr.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h + lbl_h - 1], outline=(56, 68, 86), width=2)
        dr.text((x0 + 10, y0 + cell_h + 5), label, fill=(242, 246, 250), font=f_lbl)
        dr.text((x0 + 10, y0 + cell_h + 29), shape, fill=(138, 174, 218), font=f_sub)

    out_path = DOCS / out_name
    canvas.save(out_path, optimize=True)
    print(f"[OK] Saved {out_name} ({W}x{H}, {len(items)} items, {out_path.stat().st_size} B)")


def main() -> None:
    covered = set()
    for out_name, title, cols, items in SHEETS:
        build_sheet(out_name, title, cols, items)
        for s, _ in items:
            covered.add(s)
    all_renders = {p.stem for p in RENDERS.glob("*.png")}
    missing = sorted(all_renders - covered)
    print(f"Total unique shapes across 4 sheets: {len(covered)} / {len(all_renders)} renders")
    assert not missing, f"Uncovered renders: {missing}"


if __name__ == "__main__":
    main()
