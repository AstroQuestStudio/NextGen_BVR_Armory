# NextGen BVR & Strategic Armory (DCS World 2.9+)

A modular, non-destructive DCS World `Saved Games` weapon expansion featuring **118 weapons**, **125 loadouts (including multi-ejector racks)**, **50 custom `.edm` 3D shapes**, and **111 2K PBR texture maps (`albedo`, `normal`, `roughmet`)** built from real photographic & orthographic reference checks.

## Visual Showcase & Orthographic Verification

| Showcase | Orthographic / Animation Audit |
|---|---|
| `docs/preview_mega_aam_v3.png` | `docs/ortho_aam_top_side.png` |
| `docs/preview_ballistic_naval_sead_v3.png` | `docs/ortho_arsenal_top_side.png` |
| `docs/preview_cruise_drones_bombs_v3.png` | `docs/ortho_folded_vs_deployed.png` |

## Arsenal Overview

- **BVR & WVR Air-to-Air (`mod/Database/weapons_nextgen.lua` — 26 weapons / 26 loadouts)**:
  - US / NATO / Allied: `AIM-120A`, `AIM-120C-5`, `AIM-120C-7`, `AIM-120C-8`, `AIM-120D-3`, `AIM-260A JATM`, `AIM-174B Gunslinger`, `AIM-54C+ Sea Phoenix`, `AAM-4B`, `I-Derby ER`, `MBDA Meteor` (chin ramjets).
  - European / WVR: `MICA RF / IR`, `MICA NG RF / IR`, `IRIS-T`, `IRIS-T SL`, `AAM-5B`, `Python-4`.
  - East / Russia / China: `PL-12A / SD-10A`, `PL-15`, `PL-15E` (folding-fin internal bay), `R-77-1 / RVV-SD` (3D lattice grid fins), `R-77M (Izdeliye 180)`, `R-37M`, `KS-172`.
- **Ballistic, Anti-Ship, SEAD, Bunker-Busters, Stealth Cruise & Drones (`mod/Database/weapons_arsenal_ag.lua` — 50 weapons / 55 loadouts)**:
  - Ballistic / Hypersonic: `Kh-47M2 Kinzhal`, `AGM-183A ARRW`, `YJ-21`, `IAI Rampage`, `IAI Air LORA`, `Kh-15S`.
  - Anti-Ship / Naval: `Exocet AM39 Block 2/3`, `Kh-35U / Kh-35UE` (ventral intake + folding wings), `NSM / JSM`, `Kh-22N / Kh-32` (folding ventral fin), `3M22 Tsirkon`, `HALO Hypersonic`, `AGM-84N Harpoon II+`, `YJ-83K`, `YJ-18A`.
  - SEAD: `AGM-88G AARGM-ER` (conformal strakes), `AGM-88E AARGM`, `Kh-58UShKE` (folding internal-bay fins), `MBDA ALARM / ALARM-NG`, `SPEAR-EW`, `LD-10`, `MAR-1`, `Kh-31PM`.
  - Strategic Penetrators & Stealth Cruise: `GBU-57A/B MOP` (3D folding lattice grid fins), `SCALP-EG / Storm Shadow` (blunt chisel nose), `TAURUS KEPD 350`, `AGM-158B JASSM-ER`, `AGM-158C LRASM`, `Kh-69`, `Kh-101`, `GBU-53/B`, `JSOW-ER`, `SPEAR 3`, `MALD-J`, `AASM-250 / 500 / 1000`.
  - One-Way Attack / Loitering Drones: `Shahed-136 / Geran-2`, `IAI Harop`, `Lancet-3`, `Lancet-3M`, `Switchblade 600` (with `DrawArg 407` pusher prop spin + `DrawArg 25` wing fold).
  - Special AAMs & Multi-Racks: `PL-17`, `Python-5`, `AIM-9X Block III`, `Peregrine` + `4x GBU-53`, `3x SPEAR 3`, `3x SPEAR-EW`, `3x Lancet-3`, `2x Peregrine`.
- **Tactical Rockets, ATGMs, UMPK / UMPB / SPICE / JDAM-ER & Sub-Variants (`mod/Database/weapons_tactical_30.lua` — 42 weapons / 44 loadouts)**:
  - `APKWS II HE/AP`, `Zuni Laser`, `S-8KOR`, `S-13DF`, `CRV7-PG`, `AGM-179 JAGM`, `Brimstone 2`, `Spike NLOS`, `Akeron LP`, `Vikhr-M`, `Hermes-A`.
  - `UMPB D-30SN (PAB)`, `UMPB-5R`, `PBK-500U Drel`, `FAB-250 / 500 / 1500 / 3000 UMPK`, `SPICE-250 / 1000 / 2000`, `GBU-38/62/64 JDAM-ER`, `BLU-109 Wing`, `GBU-39B/B`, `Durandal NG`, `ODAB-500`, `CBU-105`.
  - Heavy ASM / Cruise & Special AAMs: `BrahMos-A`, `Oniks-A`, `ASM-3`, `YJ-12`, `Kh-59MK2`, `RBS-15F Mk4`, `AIM-54E`, `ASRAAM Block 6`, `R-74M2`, `PL-10E`, `Magic III`, `Sky Sword II-C` + `3x UMPB D-30SN` & `4x SPICE-250` racks.

## Installation

Copy `mod/` directly into your DCS `Saved Games` folder (never modifies your core DCS install):

```powershell
.\sync_to_saved_games.ps1
```

Target path: `%USERPROFILE%\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\`

## Moving / Syncing Back to `D:\DCS MODDING`

When `D:` is reconnected, simply move this repository to `D:\DCS MODDING\NextGen_BVR_Armory` or pull from GitHub, then run `python tools/verify_mod.py` and `.\sync_to_saved_games.ps1`.
