# GBU-64/B JDAM-ER Winged (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_GBU_62_QS_ER](NG_GBU_62_QS_ER.md) · [NG_BLU_109_NG](NG_BLU_109_NG.md) →  
> Catégorie : **Smart Glide Bombs, PAB & UMPK** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_umpb_d30](../renders/ng_umpb_d30.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_GBU_64_JDAM_ER` |
| **CLSID Pylône** | `{NEXTGEN_GBU_64_JDAMER}` |
| **Nom Court HUD / RWR** | `JDAM-ER` |
| **Modèle 3D (`.edm`)** | [`ng_umpb_d30.edm`](../../mod/Shapes/ng_umpb_d30.edm) |
| **Calibre / Diamètre** | `0.457 m` (`457 mm`) |
| **Longueur** | `3.88 m` |
| **Masse au Lancement** | `950.0 kg` |
| **Mach Max** | `Mach 0.95` |
| **Portée Max** | `75 km` |
| **Charge Militaire** | `430.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (4.0 kg fuel, Burn: 300.0s, Isp: 1800s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_GLIDE_BOMB` — **LS-6-500 / JSOW High-L/D Folding Glide Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Long-range folding-wing glide polar (`Cx0 = 0.028` subsonic, `Sw = 0.65`, `addDeplSw = 0.85`, `maxAoa = 0.32`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.028` | `0.030` | `0.055` | `0.480` | `0.310` | `0.255` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
