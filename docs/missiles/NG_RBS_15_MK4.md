# RBS-15F Mk4 Gungnir (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_SOM_B2](NG_SOM_B2.md) · [NG_AIM_54E](NG_AIM_54E.md) →  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_nsm_jsm](../renders/ng_nsm_jsm.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_RBS_15_MK4` |
| **CLSID Pylône** | `{NEXTGEN_RBS_15_MK4}` |
| **Nom Court HUD / RWR** | `RBS15-4` |
| **Modèle 3D (`.edm`)** | [`ng_nsm_jsm.edm`](../../mod/Shapes/ng_nsm_jsm.edm) |
| **Calibre / Diamètre** | `0.500 m` (`500 mm`) |
| **Longueur** | `4.35 m` |
| **Masse au Lancement** | `650.0 kg` |
| **Mach Max** | `Mach 0.95` |
| **Portée Max** | `300 km` |
| **Charge Militaire** | `200.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (180.0 kg fuel, Burn: 650.0s, Isp: 2800s) |
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
