"""Generate complete 1-by-1 Markdown fiches for all 262 weapons & 11 ground air defense units,
plus master docs/CATALOG.md and README.md links with rendered 3D screenshots.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

REPO = Path(r"C:\Users\trufa\NextGen_BVR_Armory")
MOD = REPO / "mod"
DB = MOD / "Database"
DOCS = REPO / "docs"
MISSILES_DIR = DOCS / "missiles"
AD_DIR = DOCS / "air-defense"
RENDERS_DIR = DOCS / "renders"

# Clean literal Lua-table key=val extractor
KV_RE = re.compile(r'(\w+)\s*=\s*("[^"]*"|true|false|-?\d+(?:\.\d+)?)')

POLAR_SUMMARIES = {
    "FM_AAM_BVR": ("AIM-120C / SD-10 Mach 0.0–5.0 Polar", "Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`)."),
    "FM_AAM_WVR": ("High-Alpha HOBS Dogfight Polar", "High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`)."),
    "FM_AAM_ULTRA": ("Slender Ultra-Long-Range Supersonic / Ramjet Polar", "Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3)."),
    "FM_HYPERSONIC": ("9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar", "Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories."),
    "FM_KEKA_TROLL": ("KEKA Aerospace Troposphère Amateur Wobble Polar", "High base drag from riveted structural collars (`Cx0 = 0.78..1.48`, `wind_sigma = 12.0`, `wind_time = 8.0`) inducing realistic Savanna amateur flight wobble!"),
    "FM_CRUISE_STEALTH": ("AGM-84H / Kh-101 Subsonic Stealth Cruise Polar", "High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`)."),
    "FM_GLIDE_BOMB": ("LS-6-500 / JSOW High-L/D Folding Glide Polar", "Long-range folding-wing glide polar (`Cx0 = 0.028` subsonic, `Sw = 0.65`, `addDeplSw = 0.85`, `maxAoa = 0.32`)."),
    "FM_LOITER_DRONE": ("Subsonic Loitering Prop / Jet Drone Polar", "Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions."),
}

FOLDING_SHAPES = {
    "ng_pl15e", "ng_stealth_cruise", "ng_jassm_taurus", "ng_glide_sdb", "ng_loitering_x",
    "ng_umpb_d30", "ng_heavy_umpk", "ng_kh35u", "ng_nsm_jsm", "ng_kh22_32", "ng_kh58ushke",
    "ng_spear_ew", "ng_gbu57_mop", "ng_spice_glide", "ng_kalibr_3m54", "ng_javelin_top",
    "ng_tomahawk_v", "ng_atgm_quad",
}
PROP_SHAPES = {"ng_loitering_x", "ng_shahed_136", "ng_harop"}


def parse_spec_line(line: str) -> dict[str, object]:
    out: dict[str, object] = {}
    for k, raw in KV_RE.findall(line):
        if raw.startswith('"') and raw.endswith('"'):
            out[k] = raw[1:-1]
        elif raw == "true":
            out[k] = True
        elif raw == "false":
            out[k] = False
        elif "." in raw:
            out[k] = float(raw)
        else:
            out[k] = int(raw)
    return out


def infer_category(src: str, sp: dict) -> str:
    if src == "weapons_sam_interceptors.lua":
        return "SAM & ABM Interceptors"
    if sp.get("troll") or "KEKA" in str(sp.get("id", "")) or "KEKA" in str(sp.get("display_name", "")):
        return "KEKA Aerospace Troll Payloads"
    role = str(sp.get("role", ""))
    faction = str(sp.get("faction", ""))
    head = sp.get("head_type")
    if src == "weapons_nextgen.lua" or role == "aam":
        if head == 1 or faction == "nato_wvr" or "IRIS-T" in str(sp.get("id")) or "AIM_9" in str(sp.get("id")) or "PYTHON" in str(sp.get("id")) or "R_74" in str(sp.get("id")) or "PL_10" in str(sp.get("id")) or "ASRAAM" in str(sp.get("id")) or "MAGIC" in str(sp.get("id")) or "FALCO" in str(sp.get("id")):
            return "Air-to-Air WVR & HOBS"
        return "Air-to-Air BVR & Long-Range"
    if role == "sead" or "ARM" in str(sp.get("id")) or "KH_58" in str(sp.get("id")) or "KH_31" in str(sp.get("id")) or "KH_25" in str(sp.get("id")) or "KH_28" in str(sp.get("id")) or "RUDRAM" in str(sp.get("id")) or "LD_10" in str(sp.get("id")) or "MAR_1" in str(sp.get("id")) or "YJ_91" in str(sp.get("id")) or "CM_102" in str(sp.get("id")) or "AASM" in str(sp.get("id")):
        return "SEAD / Anti-Radar & Powered Precision"
    if role == "ballistic":
        return "Ballistic, MRBM, ALBM & Precision Artillery"
    if role == "glide":
        return "Smart Glide Bombs, PAB & UMPK"
    if role == "loiter":
        return "Loitering Munitions & One-Way Drones"
    if role == "cruise" or "EXOCET" in str(sp.get("id")) or "HARPOON" in str(sp.get("id")) or "NSM" in str(sp.get("id")) or "MARTE" in str(sp.get("id")) or "TESEO" in str(sp.get("id")) or "PENGUIN" in str(sp.get("id")) or "BLUE_SPEAR" in str(sp.get("id")) or "HAESEONG" in str(sp.get("id")) or "YJ_" in str(sp.get("id")) or "C_802" in str(sp.get("id")) or "HSIUNG" in str(sp.get("id")) or "GABRIEL" in str(sp.get("id")) or "ATMACA" in str(sp.get("id")) or "CAKIR" in str(sp.get("id")) or "ICE_BREAKER" in str(sp.get("id")) or "SEA_VENOM" in str(sp.get("id")):
        nm = str(sp.get("display_name", "")) + " " + str(sp.get("id", ""))
        if any(k in nm.upper() for k in ("EXOCET", "HARPOON", "NSM", "ATMACA", "GABRIEL", "ASHM", "SEA ", "MARTE", "TESEO", "PENGUIN", "BLUE_SPEAR", "HAESEONG", "YJ_62", "YJ_83", "YJ_18", "C_802", "HSIUNG", "MM40", "KH_35")):
            return "Anti-Ship Missiles (AShM)"
        return "Stealth Cruise & Stand-Off"
    if sp.get("polar") == "FM_HYPERSONIC" or "ZIRCON" in str(sp.get("id")) or "KINZHAL" in str(sp.get("id")) or "ARRW" in str(sp.get("id")) or "KH_22" in str(sp.get("id")) or "KH_32" in str(sp.get("id")) or "BRAHMOS" in str(sp.get("id")) or "ONIKS" in str(sp.get("id")) or "ASM_3" in str(sp.get("id")) or "HALO" in str(sp.get("id")):
        return "Ballistic, MRBM, ALBM & Precision Artillery"
    return "ATGM, Guided Rockets & Tactical ASM"


def infer_polar(src: str, sp: dict) -> str:
    if "polar" in sp:
        return str(sp["polar"])
    if sp.get("troll"):
        return "FM_KEKA_TROLL"
    role = str(sp.get("role", ""))
    shape = str(sp.get("shape", ""))
    is_folding = role != "aam" and shape in FOLDING_SHAPES
    if src == "weapons_tactical_30.lua":
        if is_folding and role != "ag":
            return "FM_CRUISE_STEALTH" if role == "cruise" else "FM_GLIDE_BOMB"
        return "FM_AAM_WVR" if (role == "aam" and sp.get("head_type") == 1) else "FM_AAM_BVR"
    if is_folding or role in ("cruise", "glide", "loiter"):
        if role == "loiter":
            return "FM_LOITER_DRONE"
        if role == "glide":
            return "FM_GLIDE_BOMB"
        return "FM_CRUISE_STEALTH"
    return "FM_HYPERSONIC" if role == "ballistic" else "FM_AAM_BVR"


def load_all_weapons():
    weapons = []
    racks = {}
    for fname in ("weapons_nextgen.lua", "weapons_arsenal_ag.lua", "weapons_tactical_30.lua", "weapons_sam_interceptors.lua"):
        txt = (DB / fname).read_text(encoding="utf-8")
        for ln in txt.splitlines():
            s = ln.strip()
            if s.startswith("{ id ="):
                sp = parse_spec_line(s)
                if "id" in sp and "shape" in sp:
                    sp["_source"] = fname
                    sp["_category"] = infer_category(fname, sp)
                    sp["_polar"] = infer_polar(fname, sp)
                    weapons.append(sp)
        # Scan multi_racks blocks or attr_id bindings
        for m in re.finditer(r'CLSID\s*=\s*"([^"]+)".*?displayName\s*=\s*_\("([^"]+)"\)', txt, re.S):
            pass
    # Clean rack extraction per file
    for fname in ("weapons_arsenal_ag.lua", "weapons_tactical_30.lua"):
        txt = (DB / fname).read_text(encoding="utf-8")
        for m in re.finditer(r'clsid\s*=\s*"(\{NEXTGEN_[^"]+\})".*?attr_id\s*=\s*"([^"]+)".*?display_name\s*=\s*"([^"]+)".*?offsets\s*=\s*\{([^\n]+)\}', txt, re.S):
            racks.setdefault(m.group(2), []).append((m.group(1), m.group(3), m.group(4).count("{")))
        for m in re.finditer(r'CLSID\s*=\s*"(\{NEXTGEN_[^"]+\})".*?displayName\s*=\s*_\("([^"]+)"\).*?Count\s*=\s*(\d+).*?attribute\s*=\s*tac_attrs\["([^"]+)"\]', txt, re.S):
            racks.setdefault(m.group(4), []).append((m.group(1), m.group(2), int(m.group(3))))
    return weapons, racks


def load_air_defense_units(sam_weapons_by_id: dict):
    txt = (DB / "units_air_defense.lua").read_text(encoding="utf-8")
    # Split cleanly around section headers or base_vehicle_skeleton calls
    units = []
    # Match each top-level block containing id = "NG_..."
    blocks = re.split(r'\n\s*--\s*=====================================================================\n', txt)
    for blk in blocks:
        idm = re.search(r'id\s*=\s*"([^"]+)"', blk)
        if not idm:
            continue
        uid = idm.group(1)
        dnm = re.search(r'display_name\s*=\s*"([^"]+)"', blk)
        snm = re.search(r'short_name\s*=\s*"([^"]+)"', blk)
        shm = re.search(r'shape\s*=\s*"([^"]+)"', blk)
        detm = re.search(r'det_range\s*=\s*(\d+)', blk)
        thrm = re.search(r'threat_range\s*=\s*(\d+)', blk)
        minm = re.search(r'threat_min\s*=\s*(\d+)', blk)
        altm = re.search(r'max_alt\s*=\s*(\d+)', blk)
        spdm = re.search(r'max_speed\s*=\s*([0-9.]+)', blk)
        radm = re.search(r'sensors\s*=\s*\{\s*RADAR\s*=\s*"([^"]+)"', blk)
        ammom = re.search(r'sam_weapons\["([^"]+)"\]', blk)
        shellm = re.search(r'shell_display_name\s*=\s*"([^"]+)"', blk)
        capm = re.search(r'ammo_capacity\s*=\s*(\d+)', blk)
        rctm = re.search(r'reactionTime\s*=\s*([0-9.]+)', blk)
        relm = re.search(r'reload_time\s*=\s*(\d+)', blk)
        shotm = re.search(r'shot_delay\s*=\s*([0-9.]+)', blk)
        depm = re.search(r'depends_on_unit\s*=\s*\{([^\n]+)\}', blk)
        tags_m = re.search(r'tags\s*=\s*\{([^}]+)\}', blk)
        title_m = re.search(r'^\s*--\s*\d+\.\s*([^\n]+)', blk)

        ammo_id = ammom.group(1) if ammom else None
        units.append({
            "id": uid,
            "title": title_m.group(1).strip() if title_m else (dnm.group(1) if dnm else uid),
            "display_name": dnm.group(1) if dnm else uid,
            "short_name": snm.group(1) if snm else uid,
            "shape": shm.group(1) if shm else "",
            "det_range_m": int(detm.group(1)) if detm else 0,
            "threat_range_m": int(thrm.group(1)) if thrm else 0,
            "threat_min_m": int(minm.group(1)) if minm else 0,
            "max_alt_m": int(altm.group(1)) if altm else 25000,
            "max_speed_kmh": float(spdm.group(1)) if spdm else 0.0,
            "radar_sensor": radm.group(1) if radm else "Built-in",
            "ammo_id": ammo_id,
            "ammo_name": sam_weapons_by_id[ammo_id]["display_name"] if ammo_id and ammo_id in sam_weapons_by_id else (shellm.group(1) if shellm else "N/A"),
            "ammo_capacity": int(capm.group(1)) if capm else 0,
            "reaction_s": float(rctm.group(1)) if rctm else 1.0,
            "reload_s": int(relm.group(1)) if relm else 0,
            "shot_delay_s": float(shotm.group(1)) if shotm else 0.0,
            "depends": depm.group(1).strip() if depm else "Autonomous",
            "tags": tags_m.group(1).strip().replace('"', '') if tags_m else "Air Defence",
        })
    return units


def load_polar_cx0() -> dict[str, tuple[float, list[float]]]:
    """Parse exact Cx0 arrays and table_scale from mod/Database/polar_profiles.lua."""
    txt = (DB / "polar_profiles.lua").read_text(encoding="utf-8")
    cx_map: dict[str, tuple[float, list[float]]] = {}
    base_cx0 = [float(x) for x in re.search(r"M\.FM_AAM_BVR\s*=.*?Cx0\s*=\s*\{([^}]+)\}", txt, re.S).group(1).split(",")]
    cx_map["FM_AAM_BVR"] = (0.2, base_cx0)
    # Direct table_scale = 0.1 profiles
    for pname in ("FM_CRUISE_STEALTH", "FM_GLIDE_BOMB", "FM_LOITER_DRONE"):
        blk = re.search(rf"M\.{pname}\s*=\s*\{{(.*?)\n\}}", txt, re.S).group(1)
        arr = [float(x) for x in re.search(r"Cx0\s*=\s*\{([^}]+)\}", blk).group(1).split(",")]
        cx_map[pname] = (0.1, arr)
    # Derived deep_copy profiles (scale 0.2)
    for pname in ("FM_AAM_WVR", "FM_AAM_ULTRA", "FM_HYPERSONIC", "FM_KEKA_TROLL"):
        m = re.search(rf"M\.{pname}\.Cx0\s*=\s*\{{([^}}]+)\}}", txt)
        cx_map[pname] = (0.2, [float(x) for x in m.group(1).split(",")] if m else base_cx0)
    return cx_map


def fmt_km(m: object) -> str:
    val = float(m)
    if val >= 1000:
        return f"{val / 1000.0:.0f} km"
    return f"{val:.0f} m"


def write_weapon_fiche(sp: dict, racks_map: dict, polar_cx: dict, prev_w: dict | None, next_w: dict | None) -> None:
    wid = str(sp["id"])
    shape = str(sp["shape"])
    pname = str(sp["_polar"])
    p_title, p_desc = POLAR_SUMMARIES.get(pname, (pname, ""))

    # Build sampled Mach -> Cx0 drag curve row
    scale, arr = polar_cx.get(pname, (0.2, []))
    polar_tbl = ""
    if arr:
        sample_machs = [0.0, 0.5, 0.8, 1.0, 1.4, 2.0] if scale == 0.1 else [0.0, 0.8, 1.2, 2.0, 3.0, 4.0, 5.0]
        hdr = " | ".join(f"M{m:.1f}" for m in sample_machs)
        sep = "|".join("---" for _ in sample_machs)
        vals = " | ".join(f"`{arr[min(len(arr) - 1, int(round(m / scale)))]:.3f}`" for m in sample_machs)
        polar_tbl = f"\n| Mach | {hdr} |\n|---|{sep}|\n| **Traînée `Cx0`** | {vals} |\n"

    render_file = RENDERS_DIR / f"{shape}.png"
    has_render = render_file.exists()

    # Determine propulsion display cleanly
    if "boost_fuel" in sp:
        prop_txt = f"Dual-stage (`Boost`: {sp['boost_fuel']} kg / {sp['boost_time']}s @ Isp {sp.get('boost_isp', 255)}s · `March`: {sp['march_fuel']} kg / {sp['march_time']}s @ Isp {sp.get('march_isp', 248)}s)"
    else:
        fm = sp.get("fuel_mass", 0)
        isp = sp.get("impulse", 250)
        bt = sp.get("burn_time", 0)
        frac = sp.get("boost_frac")
        if frac:
            prop_txt = f"Dual-stage (`Boost` {float(frac)*100:.0f}% + `Sustainer` {(1-float(frac))*100:.0f}%, Total fuel: {fm} kg, Burn: {bt}s, Isp: {isp}s)"
        else:
            prop_txt = f"Single/Sustained ({fm} kg fuel, Burn: {bt}s, Isp: {isp}s)"

    # Animations & DrawArgs
    anims = []
    if shape in FOLDING_SHAPES:
        anims.append("`DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)")
    if shape in PROP_SHAPES:
        anims.append("`DrawArg 407` — Rotation continue de l'hélice propulsive")
    if shape == "ng_durandal_runway":
        anims.append("`DrawArg 0` — Déploiement du parachute freineur (`1.0`)")
    anim_md = "\n".join(f"- {a}" for a in anims) if anims else "- Corps monobloc rigide `+X Forward` sans surface mobile repliable."

    # Multi-racks
    rk = racks_map.get(wid, [])
    rack_md = ""
    if rk:
        lines = [f"- `{clsid}` — **{dname}** (`{cnt}x`)" for clsid, dname, cnt in rk]
        rack_md = "\n## Emports Multi-Racks Compatibles\n" + "\n".join(lines) + "\n"

    seeker_txt = (
        "IIR / Infra-Rouge Passif (`Head_Type = 1`)"
        if sp.get("head_type") == 1
        else "Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière)"
    )

    nav_parts = ["[Catalogue Général](../CATALOG.md)", "[Accueil Mod](../../README.md)"]
    if prev_w:
        nav_parts.append(f"← [{prev_w['id']}]({prev_w['id']}.md)")
    if next_w:
        nav_parts.append(f"[{next_w['id']}]({next_w['id']}.md) →")

    md = f"""# {sp.get('display_name', wid)}

> {' · '.join(nav_parts)}  
> Catégorie : **{sp['_category']}** · Fichier source : `mod/Database/{sp['_source']}`

{f'![Rendu 3D {shape}](../renders/{shape}.png)' if has_render else '_Rendu individuel non généré_'}

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `{wid}` |
| **CLSID Pylône** | `{sp.get('clsid', 'Surface-Launched Only')}` |
| **Nom Court HUD / RWR** | `{sp.get('short_name', wid)}` |
| **Modèle 3D (`.edm`)** | [`{shape}.edm`](../../mod/Shapes/{shape}.edm) |
| **Calibre / Diamètre** | `{sp.get('caliber', 0):.3f} m` (`{int(round(float(sp.get('caliber', 0))*1000))} mm`) |
| **Longueur** | `{sp.get('length', 0):.2f} m` |
| **Masse au Lancement** | `{sp.get('mass', 0):.1f} kg` |
| **Mach Max** | `Mach {sp.get('mach_max', 0)}` |
| **Portée Max** | `{fmt_km(sp.get('range_max', 0))}` |
| **Charge Militaire** | `{sp.get('warhead_mass', sp.get('warhead', 0))} kg` |
| **Facteur de Charge Max (`Nr_max`)** | `{sp.get('g_limit', 40)} G` |
| **Guidage / Autodirecteur** | {seeker_txt} |
| **Propulsion** | {prop_txt} |
| **Résistance ECM (`ccm_k0`)** | `{sp.get('ccm', 0.03)}` |
| **Temps de Vie Max** | `{sp.get('life_time', 140)} s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `{pname}` — **{p_title}**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : {p_desc}
{polar_tbl}
## Animations & Modèle 3D

{anim_md}
{rack_md}"""
    (MISSILES_DIR / f"{wid}.md").write_text(md, encoding="utf-8")


def write_ad_fiche(u: dict) -> None:
    uid = u["id"]
    shape = u["shape"]
    render_file = RENDERS_DIR / f"{shape}.png"
    ammo_link = f"[`{u['ammo_id']}`](../missiles/{u['ammo_id']}.md) ({u['ammo_name']})" if u["ammo_id"] else f"`{u['ammo_name']}`"

    if u["id"] == "NG_CRAM_Centurion":
        anims = "- `DrawArg 0` : Azimut tourelle 360° (`CENTER_TOWER`)\n- `DrawArg 1` : Élévation berceau `-15° / +85°`\n- `DrawArg 23` : Rotation continue du canon rotatif M61A1 6 tubes 20mm (`POINT_GUN_01`)"
    elif "Radar" in uid or "ELM" in uid:
        anims = "- `DrawArg 11` : Rotation continue à 360° de l'antenne radar AESA"
    elif "Pantsir" in uid:
        anims = "- `DrawArg 0` : Azimut tourelle 360° (`CENTER_TOWER`)\n- `DrawArg 1` : Élévation 12x tubes 57E6M + bi-tubes 30mm 2A38M\n- `DrawArg 11` : Radar de veille Janus rotatif"
    elif "Patriot" in uid or "IronDome" in uid or "KEKA" in uid:
        anims = "- `DrawArg 0` : Azimut du lanceur 360° (`CENTER_TOWER`) + connecteurs `POINT_MISSILE_01..20`"
    else:
        anims = "- Connecteurs verticaux / inclinés `CENTER_TOWER`, `POINT_SIGHT_01` et `POINT_MISSILE_01..08`"

    md = f"""# {u['display_name']}

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Défense Anti-Aérienne & C-RAM** · Source : `mod/Database/units_air_defense.lua`

{f'![Rendu 3D {shape}](../renders/{shape}.png)' if render_file.exists() else ''}

## Fiche Unité Sol-Air

| Paramètre | Valeur |
|---|---|
| **ID Unité** | `{uid}` |
| **Nom Court Carte** | `{u['short_name']}` |
| **Modèle 3D (`.edm`)** | [`{shape}.edm`](../../mod/Shapes/{shape}.edm) |
| **Tags DCS** | `{u['tags']}` |
| **Portée Détection Radar** | `{fmt_km(u['det_range_m'])}` |
| **Portée d'Engagement** | `{fmt_km(u['threat_range_m'])}` (min `{fmt_km(u['threat_min_m'])}`) |
| **Plafond d'Interception** | `{fmt_km(u['max_alt_m'])}` |
| **Vitesse Route Max** | `{u['max_speed_kmh']:.0f} km/h` |
| **Capteur Radar (`GT.Sensors`)** | `{u['radar_sensor']}` |
| **Munition Embarquée** | {ammo_link} |
| **Capacité Chargeur** | `{u['ammo_capacity']}` coups/missiles |
| **Temps de Réaction** | `{u['reaction_s']} s` |
| **Cadence / Délai Tir** | `{u['shot_delay_s']} s` · Rechargement `{u['reload_s']} s` |
| **Dépendance / Chaînage** | `{u['depends']}` |

## Animations & Connecteurs EDM

{anims}
"""
    (AD_DIR / f"{uid}.md").write_text(md, encoding="utf-8")


def main() -> None:
    MISSILES_DIR.mkdir(parents=True, exist_ok=True)
    AD_DIR.mkdir(parents=True, exist_ok=True)
    for old in list(MISSILES_DIR.glob("*.md")) + list(AD_DIR.glob("*.md")):
        old.unlink()

    weapons, racks_map = load_all_weapons()
    polar_cx = load_polar_cx0()
    by_id = {str(w["id"]): w for w in weapons}
    ad_units = load_air_defense_units(by_id)

    for idx_w, w in enumerate(weapons):
        prev_w = weapons[idx_w - 1] if idx_w > 0 else None
        next_w = weapons[idx_w + 1] if idx_w + 1 < len(weapons) else None
        write_weapon_fiche(w, racks_map, polar_cx, prev_w, next_w)
    for u in ad_units:
        write_ad_fiche(u)

    # Build grouped Master Catalog (docs/CATALOG.md)
    cat_order = [
        "Air-to-Air BVR & Long-Range",
        "Air-to-Air WVR & HOBS",
        "Ballistic, MRBM, ALBM & Precision Artillery",
        "Stealth Cruise & Stand-Off",
        "Anti-Ship Missiles (AShM)",
        "SEAD / Anti-Radar & Powered Precision",
        "Smart Glide Bombs, PAB & UMPK",
        "ATGM, Guided Rockets & Tactical ASM",
        "Loitering Munitions & One-Way Drones",
        "SAM & ABM Interceptors",
        "KEKA Aerospace Troll Payloads",
    ]
    grouped: dict[str, list[dict]] = {c: [] for c in cat_order}
    for w in weapons:
        grouped.setdefault(str(w["_category"]), []).append(w)

    lines = [
        "# Catalogue Complet NextGen_BVR_Armory v5.0\n",
        f"> **Total vérifié** : **{len(weapons)} armes individuelles** + **{len(ad_units)} systèmes sol-air / C-RAM** + **79 modèles 3D `.edm`** + **79 rendus studio**.\n",
        "> Retour à la présentation : [README.md](../README.md)\n",
        "\n## Sommaire Rapide\n",
        f"- [Systèmes Sol-Air, Radars & C-RAM ({len(ad_units)})](#systèmes-sol-air-radars--c-ram-{len(ad_units)})",
    ]
    for c in cat_order:
        items = grouped.get(c, [])
        slug = re.sub(r"[^a-z0-9 -]", "", c.lower()).replace(" ", "-")
        lines.append(f"- [{c} ({len(items)})](#{slug}-{len(items)})")

    # Section: Air Defense Units
    lines.append(f"\n## Systèmes Sol-Air, Radars & C-RAM ({len(ad_units)})\n")
    lines.append("| Aperçu | Fiche | Rôle / Radar | Portée | Plafond | Munition |")
    lines.append("|---|---|---|---|---|---|")
    for u in ad_units:
        thumb = f"![{u['short_name']}](renders/{u['shape']}.png)" if (RENDERS_DIR / f"{u['shape']}.png").exists() else f"`{u['shape']}`"
        ammo_col = f"[{u['ammo_id']}](missiles/{u['ammo_id']}.md) x{u['ammo_capacity']}" if u["ammo_id"] else f"{u['ammo_name']} ({u['ammo_capacity']})"
        lines.append(
            f"| {thumb} | **[{u['display_name']}](air-defense/{u['id']}.md)** (`{u['id']}`) | `{u['radar_sensor']}` | {fmt_km(u['threat_range_m'])} | {fmt_km(u['max_alt_m'])} | {ammo_col} |"
        )

    # Sections: Weapons
    for c in cat_order:
        items = grouped.get(c, [])
        lines.append(f"\n## {c} ({len(items)})\n")
        lines.append("| Fiche Arme | ID / CLSID | Forme 3D | Mach | Portée | Masse / Charge | Polaire |")
        lines.append("|---|---|---|---|---|---|---|")
        for w in items:
            wid = str(w["id"])
            sh = str(w["shape"])
            clsid = w.get("clsid", "Sol-Air")
            wh = w.get("warhead_mass", w.get("warhead", 0))
            lines.append(
                f"| **[{w.get('display_name', wid)}](missiles/{wid}.md)** | `{wid}`<br>`{clsid}` | [`{sh}`](renders/{sh}.png) | M{w.get('mach_max', 0)} | {fmt_km(w.get('range_max', 0))} | {w.get('mass', 0):.0f} kg / {wh} kg | `{w['_polar']}` |"
            )

    (DOCS / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Collect unique multi-racks for showcase
    all_racks: list[tuple[str, str, int, str]] = []
    seen_racks = set()
    for wid_k, rlist in racks_map.items():
        for clsid, dname, cnt in rlist:
            if clsid not in seen_racks:
                seen_racks.add(clsid)
                all_racks.append((clsid, dname, cnt, wid_k))

    # Build rich, ultra-visual GitHub front page (README.md) so visitors see EVERYTHING immediately!
    readme = [
        '<div align="center">\n',
        "# NextGen BVR, Strategic & Air Defense Armory v5.0\n",
        "![DCS World 2.9+](https://img.shields.io/badge/DCS%20World-2.9%2B-1f6feb?style=for-the-badge) "
        "![262 Weapons](https://img.shields.io/badge/Weapons-262-238636?style=for-the-badge) "
        "![11 Air Defenses](https://img.shields.io/badge/Air%20Defenses-11-d29922?style=for-the-badge) "
        "![79 EDM Models](https://img.shields.io/badge/3D%20Models%20(.edm)-79-8957e5?style=for-the-badge) "
        "![159 PBR Maps](https://img.shields.io/badge/2K%20PBR%20Textures-159-da3633?style=for-the-badge)\n",
        "\n**[Catalogue Complet (`docs/CATALOG.md`)](docs/CATALOG.md) · "
        "[262 Fiches Missiles](docs/missiles/) · "
        "[11 Fiches Sol-Air / C-RAM](docs/air-defense/) · "
        "[79 Rendus 3D](docs/renders/)**\n",
        "\n![NextGen Armory v5.0 HQ Air Defense Showcase](docs/preview_hq_sam_v5.png)\n",
        "</div>\n",
        "---\n",
        "\n## Vue d'Ensemble Visuelle — Tous les 79 Modèles 3D (`.edm`)\n",
        "\n### 1. Défenses Sol-Air, Radars AESA & C-RAM (11 Systèmes)\n",
        "![Sheet 01 SAM & C-RAM](docs/sheet_01_sam_and_cram.png)\n",
        "\n| Aperçu | Système Sol-Air (Fiche 1-par-1) | Radar / Rôle | Portée / Plafond | Armement / Cadence |",
        "|---|---|---|---|---|",
    ]
    for u in ad_units:
        ammo_txt = (
            f"[{u['ammo_id']}](docs/missiles/{u['ammo_id']}.md) ×{u['ammo_capacity']}"
            if u["ammo_id"]
            else f"{u['ammo_name']} ({u['ammo_capacity']})"
        )
        readme.append(
            f"| [<img src=\"docs/renders/{u['shape']}.png\" width=\"160\"/>](docs/air-defense/{u['id']}.md) | "
            f"**[{u['display_name']}](docs/air-defense/{u['id']}.md)**<br>`{u['id']}` · `{u['shape']}.edm` | "
            f"`{u['radar_sensor']}`<br>Détect `{fmt_km(u['det_range_m'])}` · Réaction `{u['reaction_s']}s` | "
            f"`{fmt_km(u['threat_range_m'])}` / `{fmt_km(u['max_alt_m'])}` | {ammo_txt} |"
        )

    readme += [
        "\n### 2. Missiles Air-Air (BVR / WVR / Ramjet) & Intercepteurs SAM (28 Modèles)\n",
        "![Sheet 02 AAM & SAM](docs/sheet_02_aam_and_sam_missiles.png)\n",
        "\n### 3. Missiles de Croisière, Anti-Navires, SEAD, Balistiques & Hypersoniques (23 Modèles)\n",
        "![Sheet 03 Cruise Naval SEAD Ballistic](docs/sheet_03_cruise_naval_sead_ballistic.png)\n",
        "\n### 4. Bombes Planantes, Drones, ATGMs, Roquettes & Collection Troll KEKA (17 Modèles)\n",
        "![Sheet 04 Glide Drones ATGM KEKA](docs/sheet_04_glide_drones_atgm_keka.png)\n",
        "\n---\n",
        "\n## Catalogue Intégral des 262 Armes (Déplier Chaque Catégorie)\n",
        "\n> Cliquez sur n'importe quelle catégorie ci-dessous pour afficher **toutes les armes directement ici** avec accès 1-clic à leur **fiche détaillée** (`docs/missiles/<ID>.md`) et leur **rendu 3D** (`docs/renders/<shape>.png`). Vous pouvez aussi tout consulter d'un bloc dans [`docs/CATALOG.md`](docs/CATALOG.md).\n",
    ]

    for idx_cat, c in enumerate(cat_order):
        items = grouped.get(c, [])
        open_attr = " open" if idx_cat in (0, 9, 10) else ""
        readme.append(f"\n<details{open_attr}>")
        readme.append(f"<summary><strong>{c} — {len(items)} armes</strong> (cliquer pour déplier)</summary>\n")
        readme.append("\n| Arme (Fiche 1-par-1) | ID / CLSID | Modèle 3D | Mach | Portée | Masse / Charge | Polaire |")
        readme.append("|---|---|---|---|---|---|---|")
        for w in items:
            wid = str(w["id"])
            sh = str(w["shape"])
            clsid = w.get("clsid", "Sol-Air")
            wh = w.get("warhead_mass", w.get("warhead", 0))
            readme.append(
                f"| **[{w.get('display_name', wid)}](docs/missiles/{wid}.md)** | `{wid}`<br>`{clsid}` | "
                f"[`{sh}`](docs/renders/{sh}.png) | M{w.get('mach_max', 0)} | {fmt_km(w.get('range_max', 0))} | "
                f"{w.get('mass', 0):.0f} kg / {wh} kg | `{w['_polar']}` |"
            )
        readme.append("\n</details>\n")

    readme += [
        "\n## Emports Multi-Racks (12 Racks)\n",
        "| CLSID | Désignation | Quantité | Munition / Fiche |",
        "|---|---|---|---|",
    ]
    for clsid, dname, cnt, wid_k in sorted(all_racks):
        readme.append(f"| `{clsid}` | **{dname}** | `{cnt}x` | [{wid_k}](docs/missiles/{wid_k}.md) |")

    readme += [
        "\n## Audits Orthographiques & Planches Studio\n",
        "| Gros Plan C-RAM / Iron Dome | Missiles v5 (Tomahawk V, THAAD, 40N6, GMLRS) |",
        "|---|---|",
        "| ![Close-up C-RAM Iron Dome](docs/preview_hq_cram_irondome_closeup.png) | ![Missiles v5 Ortho](docs/preview_missiles_v5_ortho.png) |",
        "| ![AAM Ortho Top/Side](docs/ortho_aam_top_side.png) | ![Arsenal Ortho Top/Side](docs/ortho_arsenal_top_side.png) |",
        "| ![Folded vs Deployed Wings](docs/ortho_folded_vs_deployed.png) | ![Backlog & KEKA](docs/preview_backlog_keka_v4.png) |",
        "\n## Installation & Vérification\n",
        "```powershell\n"
        ".\\sync_to_saved_games.ps1\n"
        "python tools\\verify_mod.py\n"
        "```\n",
        "- Copier vers `%USERPROFILE%\\Saved Games\\DCS\\Mods\\tech\\NextGen_BVR_Armory` (mod non destructif : les fichiers d'origine de DCS World ne sont jamais modifiés).\n"
        "- Polaires aérodynamiques calibrées par Mach dans [`mod/Database/polar_profiles.lua`](mod/Database/polar_profiles.lua).\n",
    ]

    (REPO / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"[OK] Generated {len(weapons)} weapon fiches, {len(ad_units)} air-defense fiches, docs/CATALOG.md, and full visual README.md ({len('\n'.join(readme))} bytes)")


if __name__ == "__main__":
    main()
