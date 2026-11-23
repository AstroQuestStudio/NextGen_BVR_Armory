# NextGen BVR, Strategic & Air Defense Armory v3.0 (DCS World 2.9+)

A modular, non-destructive DCS World `Saved Games` weapon & SAM expansion featuring:
- **176+ unique weapons** across Air-to-Air, Ballistic, Anti-Ship, SEAD, Cruise, Glide Bombs, Drones, SAM Interceptors, and **KEKA Aerospace** troll payloads
- **8 animated Surface Air Defense Systems** (`Centurion C-RAM Phalanx CIWS`, `Iron Dome 20-Cell MFR + Tamir`, `EL/M-2084 MMR Radar`, `IRIS-T SLM 8-Cell VLS`, `SAMP/T Aster 30 B1NT`, `Pantsir-SM 96K6`, `Patriot M903 PAC-3 MSE`, and `KEKA Aerospace Troposphère Pad`)
- **Calibrated Mach-Indexed DCS Aerodynamic Polars** (`mod/Database/polar_profiles.lua`) built from real DCS World polar families (`AIM-120C`, `SD-10`, `9M723`, `AGM-84H`, `X-101`, `LS-6`, `AGM-88`, `RIM-7M`, `AGR-20A`)
- **72 custom `+X Forward` `.edm` 3D shapes** & **141 2K PBR texture maps**

## Visual Showcase & Orthographic Audit

| Showcase | Orthographic / Animation Audit |
|---|---|
| `docs/preview_mega_aam_v3.png` | `docs/ortho_aam_top_side.png` |
| `docs/preview_ballistic_naval_sead_v3.png` | `docs/ortho_arsenal_top_side.png` |
| `docs/preview_cruise_drones_bombs_v3.png` | `docs/ortho_folded_vs_deployed.png` |
| `docs/preview_sam_cram_v4.png` | `docs/preview_backlog_keka_v4.png` |

## Highlights Added in v3.0

- **C-RAM & Integrated Air Defenses (`mod/Database/units_air_defense.lua` + `weapons_sam_interceptors.lua`)**:
  - `Centurion C-RAM`: 4,500 rpm 20mm Vulcan (`M246_20_HE_gr`), 0.25s reaction time, `reflection_limit = 0.008`, spinning barrel `DrawArg 23`, azimuth `DrawArg 0`, elevation `DrawArg 1`, domed Ku-band radome.
  - `Iron Dome Battery`: 20-cell Tamir launcher (`NG_IronDome_Launcher`) + S-band AESA `EL/M-2084 MMR` search radar (`DrawArg 11`) configured with low-RCS target tracking (`reflection_limit = 0.006`) for rockets, cruise missiles, drones & aircraft.
  - `IRIS-T SLM`, `SAMP/T Aster 30 B1NT`, `Pantsir-SM` (12x `57E6M` + dual 30mm `2A38M`), and `Patriot M903 PAC-3 MSE` (16-cell quad-pack).
- **KEKA Aerospace Troll Collection**:
  - `Troposphère 4`, `Troposphère 5 (Viral Cat Edition)`, `Troposphère 6 Strap-On Heavy`, `2x Twin Pod`, plus `KEKA Troposphere Launch Pad` mobile ground launcher!
- **400-Item Backlog P1 Wave (`dcs_missiles_backlog_2026.md`)**:
  - AAMs: `Astra Mk 1/2/3`, `Bozdoğan`, `Gökdoğan`, `A-Darter`, `R-Darter`, `RVV-MD2`, `TC-1`.
  - Strike / Ballistic / Hypersonic / SEAD: `DF-17 Waverider HGV`, `DF-21D`, `9M723 Iskander-M`, `ATACMS Block IVA`, `PrSM Inc 1`, `Fath-360`, `Kheibar Shekan`, `Rudram-1/2`, `CM-102`, `YJ-91`, `AGM-122 Sidearm`, `ARMAT`.
  - Cruise / ASM / Tactical / Jet Drones: `JASSM-XR`, `SLAM-ER`, `SOM-J/B2`, `Çakır`, `Atmaca`, `Gabriel V`, `Ice Breaker`, `Hsiung Feng III`, `3M54 Kalibr`, `Kh-50`, `Kh-38MLE/MTE`, `Grom-E1`, `LMUR-305`, `Delilah`, `FGM-148F Javelin`, `Spike-LR2`, `AKERON MP`, `Brimstone 3`, `AGR-20 FALCO`, `CIRIT`, `GLSDB`, `Palianytsia`, `Peklo`, `Shahed-131/238`, `AQ-400 Scythe`, `HERO-120/400EC`, `ALTIUS-600M`, `Harpy NG`, `KUB-BLA`, `Warmate`.

## Installation & Sync to `D:\DCS MODDING`

```powershell
.\sync_to_saved_games.ps1
python tools\verify_mod.py
```
