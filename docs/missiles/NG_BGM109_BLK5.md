# BGM-109 Tomahawk Block V MST (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_PEREGRINE](NG_PEREGRINE.md) · [NG_BGM109_BLK4](NG_BGM109_BLK4.md) →  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_tomahawk_v](../renders/ng_tomahawk_v.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_BGM109_BLK5` |
| **CLSID Pylône** | `{NEXTGEN_BGM109_BLK5}` |
| **Nom Court HUD / RWR** | `BGM109-V` |
| **Modèle 3D (`.edm`)** | [`ng_tomahawk_v.edm`](../../mod/Shapes/ng_tomahawk_v.edm) |
| **Calibre / Diamètre** | `0.520 m` (`520 mm`) |
| **Longueur** | `6.25 m` |
| **Masse au Lancement** | `1510.0 kg` |
| **Mach Max** | `Mach 0.9` |
| **Portée Max** | `1600 km` |
| **Charge Militaire** | `450.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (450.0 kg fuel, Burn: 1800.0s, Isp: 3200s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `3200 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.023` | `0.023` | `0.035` | `0.450` | `0.290` | `0.245` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)

## Emports Multi-Racks Compatibles
- `{NEXTGEN_TOMAHAWK_2X}` — **2x BGM-109 Tomahawk Block V Heavy Rack (NG)** (`2x`)
