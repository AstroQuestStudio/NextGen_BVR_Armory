# Kh-50 Compact ALCM (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_KH_69](NG_KH_69.md) · [NG_KH_101](NG_KH_101.md) →  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_stealth_cruise](../renders/ng_stealth_cruise.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_50` |
| **CLSID Pylône** | `{NEXTGEN_KH_50}` |
| **Nom Court HUD / RWR** | `Kh-50` |
| **Modèle 3D (`.edm`)** | [`ng_stealth_cruise.edm`](../../mod/Shapes/ng_stealth_cruise.edm) |
| **Calibre / Diamètre** | `0.560 m` (`560 mm`) |
| **Longueur** | `6.00 m` |
| **Masse au Lancement** | `1600.0 kg` |
| **Mach Max** | `Mach 0.94` |
| **Portée Max** | `1500 km` |
| **Charge Militaire** | `450.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (620.0 kg fuel, Burn: 1800.0s, Isp: 3300s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `2800 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.023` | `0.023` | `0.035` | `0.450` | `0.290` | `0.245` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
