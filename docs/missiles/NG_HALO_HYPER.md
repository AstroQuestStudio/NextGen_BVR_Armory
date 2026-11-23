# HALO Hypersonic Mach 6+ ASM (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ZIRCON](NG_ZIRCON.md) · [NG_YJ_83K](NG_YJ_83K.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_zircon](../renders/ng_zircon.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_HALO_HYPER` |
| **CLSID Pylône** | `{NEXTGEN_HALO_HYPER}` |
| **Nom Court HUD / RWR** | `HALO-M6` |
| **Modèle 3D (`.edm`)** | [`ng_zircon.edm`](../../mod/Shapes/ng_zircon.edm) |
| **Calibre / Diamètre** | `0.440 m` (`440 mm`) |
| **Longueur** | `6.20 m` |
| **Masse au Lancement** | `1450.0 kg` |
| **Mach Max** | `Mach 6.2` |
| **Portée Max** | `450 km` |
| **Charge Militaire** | `320.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (580.0 kg fuel, Burn: 65.0s, Isp: 320s) |
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
