# Roketsan Tayfun Hypersonic MRBM

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_TRG_300_KAPLAN](NG_TRG_300_KAPLAN.md) · [NG_BORA_KHAN](NG_BORA_KHAN.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_iskander_atacms](../renders/ng_iskander_atacms.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_TAYFUN` |
| **CLSID Pylône** | `{NEXTGEN_TAYFUN}` |
| **Nom Court HUD / RWR** | `Tayfun` |
| **Modèle 3D (`.edm`)** | [`ng_iskander_atacms.edm`](../../mod/Shapes/ng_iskander_atacms.edm) |
| **Calibre / Diamètre** | `0.610 m` (`610 mm`) |
| **Longueur** | `6.50 m` |
| **Masse au Lancement** | `2300.0 kg` |
| **Mach Max** | `Mach 6.5` |
| **Portée Max** | `560 km` |
| **Charge Militaire** | `470.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1100.0 kg fuel, Burn: 38.0s, Isp: 265s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.360` | `0.370` | `0.510` | `0.310` | `0.188` | `0.140` | `0.118` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
