# DF-21D ASBM Carrier-Killer (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_kinzhal](../renders/ng_kinzhal.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_DF_21D` |
| **CLSID Pylône** | `{NEXTGEN_DF_21D}` |
| **Nom Court HUD / RWR** | `DF-21D` |
| **Modèle 3D (`.edm`)** | [`ng_kinzhal.edm`](../../mod/Shapes/ng_kinzhal.edm) |
| **Calibre / Diamètre** | `1.000 m` (`1000 mm`) |
| **Longueur** | `8.20 m` |
| **Masse au Lancement** | `4400.0 kg` |
| **Mach Max** | `Mach 9.5` |
| **Portée Max** | `1500 km` |
| **Charge Militaire** | `600.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (2400.0 kg fuel, Burn: 65.0s, Isp: 290s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1400 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques (`polar_profiles.lua`)** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
