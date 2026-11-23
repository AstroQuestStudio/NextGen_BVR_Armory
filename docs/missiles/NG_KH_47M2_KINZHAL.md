# Kh-47M2 Kinzhal Mach 10 (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_KEKA_AAM](NG_KEKA_AAM.md) · [NG_AGM_183A_ARRW](NG_AGM_183A_ARRW.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_kinzhal](../renders/ng_kinzhal.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_47M2_KINZHAL` |
| **CLSID Pylône** | `{NEXTGEN_KH47M2_KINZHAL}` |
| **Nom Court HUD / RWR** | `Kinzhal` |
| **Modèle 3D (`.edm`)** | [`ng_kinzhal.edm`](../../mod/Shapes/ng_kinzhal.edm) |
| **Calibre / Diamètre** | `1.050 m` (`1050 mm`) |
| **Longueur** | `7.40 m` |
| **Masse au Lancement** | `4300.0 kg` |
| **Mach Max** | `Mach 9.5` |
| **Portée Max** | `1500 km` |
| **Charge Militaire** | `480.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (2400.0 kg fuel, Burn: 65.0s, Isp: 290s) |
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
