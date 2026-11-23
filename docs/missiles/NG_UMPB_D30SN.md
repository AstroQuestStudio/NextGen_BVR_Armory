# UMPB D-30SN Glide (PAB / NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_DELILAH](NG_DELILAH.md) · [NG_UMPB_5R](NG_UMPB_5R.md) →  
> Catégorie : **Smart Glide Bombs, PAB & UMPK** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_umpb_d30](../renders/ng_umpb_d30.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_UMPB_D30SN` |
| **CLSID Pylône** | `{NEXTGEN_UMPB_D30SN}` |
| **Nom Court HUD / RWR** | `UMPB-D30` |
| **Modèle 3D (`.edm`)** | [`ng_umpb_d30.edm`](../../mod/Shapes/ng_umpb_d30.edm) |
| **Calibre / Diamètre** | `0.300 m` (`300 mm`) |
| **Longueur** | `2.85 m` |
| **Masse au Lancement** | `250.0 kg` |
| **Mach Max** | `Mach 0.95` |
| **Portée Max** | `110 km` |
| **Charge Militaire** | `100.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (15.0 kg fuel, Burn: 300.0s, Isp: 2200s) |
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

## Emports Multi-Racks Compatibles
- `{NEXTGEN_UMPB_D30_3X}` — **3x UMPB D-30SN Glide Rack (PAB / NextGen)** (`3x`)
