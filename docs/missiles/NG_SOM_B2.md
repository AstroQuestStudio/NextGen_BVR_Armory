# TUBITAK SOM-B2 Deep-Pen Cruise (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_KH_59MK2](NG_KH_59MK2.md) · [NG_RBS_15_MK4](NG_RBS_15_MK4.md) →  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_jassm_taurus](../renders/ng_jassm_taurus.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SOM_B2` |
| **CLSID Pylône** | `{NEXTGEN_SOM_B2}` |
| **Nom Court HUD / RWR** | `SOM-B2` |
| **Modèle 3D (`.edm`)** | [`ng_jassm_taurus.edm`](../../mod/Shapes/ng_jassm_taurus.edm) |
| **Calibre / Diamètre** | `0.420 m` (`420 mm`) |
| **Longueur** | `5.00 m` |
| **Masse au Lancement** | `620.0 kg` |
| **Mach Max** | `Mach 0.92` |
| **Portée Max** | `250 km` |
| **Charge Militaire** | `230.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (165.0 kg fuel, Burn: 580.0s, Isp: 2850s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1200 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.023` | `0.023` | `0.035` | `0.450` | `0.290` | `0.245` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
