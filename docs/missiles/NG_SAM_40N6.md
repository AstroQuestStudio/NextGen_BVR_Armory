# S-400 40N6 Ultra-Long ABM (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_SAM_THAAD](NG_SAM_THAAD.md) · [NG_SAM_48N6DM](NG_SAM_48N6DM.md) →  
> Catégorie : **SAM & ABM Interceptors** · Fichier source : `mod/Database/weapons_sam_interceptors.lua`

![Rendu 3D ng_sam_40n6](../renders/ng_sam_40n6.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SAM_40N6` |
| **CLSID Pylône** | `Surface-Launched Only` |
| **Nom Court HUD / RWR** | `40N6` |
| **Modèle 3D (`.edm`)** | [`ng_sam_40n6.edm`](../../mod/Shapes/ng_sam_40n6.edm) |
| **Calibre / Diamètre** | `0.515 m` (`515 mm`) |
| **Longueur** | `7.50 m` |
| **Masse au Lancement** | `1890.0 kg` |
| **Mach Max** | `Mach 6.0` |
| **Portée Max** | `380 km` |
| **Charge Militaire** | `145.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `32 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Dual-stage (`Boost`: 850.0 kg / 6.0s @ Isp 255s · `March`: 420.0 kg / 22.0s @ Isp 248s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `320 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.360` | `0.370` | `0.510` | `0.310` | `0.188` | `0.140` | `0.118` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
