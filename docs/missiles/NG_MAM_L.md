# Roketsan MAM-L Smart Glide (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_BLUE_SPEAR](NG_BLUE_SPEAR.md) · [NG_MAM_T](NG_MAM_T.md) →  
> Catégorie : **Smart Glide Bombs, PAB & UMPK** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_glide_sdb](../renders/ng_glide_sdb.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_MAM_L` |
| **CLSID Pylône** | `{NEXTGEN_MAM_L}` |
| **Nom Court HUD / RWR** | `MAM-L` |
| **Modèle 3D (`.edm`)** | [`ng_glide_sdb.edm`](../../mod/Shapes/ng_glide_sdb.edm) |
| **Calibre / Diamètre** | `0.160 m` (`160 mm`) |
| **Longueur** | `1.00 m` |
| **Masse au Lancement** | `22.0 kg` |
| **Mach Max** | `Mach 0.85` |
| **Portée Max** | `18 km` |
| **Charge Militaire** | `10.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1.0 kg fuel, Burn: 180.0s, Isp: 1600s) |
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
