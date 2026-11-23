# Zolfaghar 700km Tactical SRBM

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_FATEH_313](NG_FATEH_313.md) · [NG_ROCKS_ALBM](NG_ROCKS_ALBM.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_iskander_atacms](../renders/ng_iskander_atacms.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ZOLFAGHAR` |
| **CLSID Pylône** | `{NEXTGEN_ZOLFAGHAR}` |
| **Nom Court HUD / RWR** | `Zolfaghr` |
| **Modèle 3D (`.edm`)** | [`ng_iskander_atacms.edm`](../../mod/Shapes/ng_iskander_atacms.edm) |
| **Calibre / Diamètre** | `0.680 m` (`680 mm`) |
| **Longueur** | `10.30 m` |
| **Masse au Lancement** | `4600.0 kg` |
| **Mach Max** | `Mach 5.8` |
| **Portée Max** | `700 km` |
| **Charge Militaire** | `580.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (2100.0 kg fuel, Burn: 42.0s, Isp: 260s) |
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
