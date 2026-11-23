# 3M22 Tsirkon Scramjet Mach 9 (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_KH_32](NG_KH_32.md) · [NG_HALO_HYPER](NG_HALO_HYPER.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_zircon](../renders/ng_zircon.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ZIRCON` |
| **CLSID Pylône** | `{NEXTGEN_ZIRCON}` |
| **Nom Court HUD / RWR** | `3M22-Zrc` |
| **Modèle 3D (`.edm`)** | [`ng_zircon.edm`](../../mod/Shapes/ng_zircon.edm) |
| **Calibre / Diamètre** | `0.600 m` (`600 mm`) |
| **Longueur** | `8.50 m` |
| **Masse au Lancement** | `2800.0 kg` |
| **Mach Max** | `Mach 8.8` |
| **Portée Max** | `1000 km` |
| **Charge Militaire** | `350.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1350.0 kg fuel, Burn: 180.0s, Isp: 410s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1200 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.360` | `0.370` | `0.510` | `0.310` | `0.188` | `0.140` | `0.118` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
