# SCALP-EG / Storm Shadow (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_GBU_57A_MOP](NG_GBU_57A_MOP.md) · [NG_TAURUS](NG_TAURUS.md) →  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_stealth_cruise](../renders/ng_stealth_cruise.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SCALP_EG` |
| **CLSID Pylône** | `{NEXTGEN_SCALP_EG}` |
| **Nom Court HUD / RWR** | `SCALP-EG` |
| **Modèle 3D (`.edm`)** | [`ng_stealth_cruise.edm`](../../mod/Shapes/ng_stealth_cruise.edm) |
| **Calibre / Diamètre** | `0.480 m` (`480 mm`) |
| **Longueur** | `5.10 m` |
| **Masse au Lancement** | `1300.0 kg` |
| **Mach Max** | `Mach 0.95` |
| **Portée Max** | `560 km` |
| **Charge Militaire** | `450.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (280.0 kg fuel, Burn: 900.0s, Isp: 3000s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1800 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.023` | `0.023` | `0.035` | `0.450` | `0.290` | `0.245` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
