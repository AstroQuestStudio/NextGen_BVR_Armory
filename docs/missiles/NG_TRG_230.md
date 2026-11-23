# Roketsan TRG-230 Laser-GPS (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_TORNADO_S_9M544](NG_TORNADO_S_9M544.md) · [NG_TRG_300_KAPLAN](NG_TRG_300_KAPLAN.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_gmlrs_m31](../renders/ng_gmlrs_m31.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_TRG_230` |
| **CLSID Pylône** | `{NEXTGEN_TRG_230}` |
| **Nom Court HUD / RWR** | `TRG-230` |
| **Modèle 3D (`.edm`)** | [`ng_gmlrs_m31.edm`](../../mod/Shapes/ng_gmlrs_m31.edm) |
| **Calibre / Diamètre** | `0.230 m` (`230 mm`) |
| **Longueur** | `3.40 m` |
| **Masse au Lancement** | `215.0 kg` |
| **Mach Max** | `Mach 2.5` |
| **Portée Max** | `70 km` |
| **Charge Militaire** | `42.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (78.0 kg fuel, Burn: 7.5s, Isp: 240s) |
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
