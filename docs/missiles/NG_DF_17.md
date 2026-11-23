# DF-17 Air-Drop Waverider HGV (NG)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_df17_waverider](../renders/ng_df17_waverider.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_DF_17` |
| **CLSID Pylône** | `{NEXTGEN_DF_17}` |
| **Nom Court HUD / RWR** | `DF-17` |
| **Modèle 3D (`.edm`)** | [`ng_df17_waverider.edm`](../../mod/Shapes/ng_df17_waverider.edm) |
| **Calibre / Diamètre** | `0.850 m` (`850 mm`) |
| **Longueur** | `7.80 m` |
| **Masse au Lancement** | `3400.0 kg` |
| **Mach Max** | `Mach 9.2` |
| **Portée Max** | `1800 km` |
| **Charge Militaire** | `380.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1950.0 kg fuel, Burn: 60.0s, Isp: 295s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1400 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques (`polar_profiles.lua`)** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
