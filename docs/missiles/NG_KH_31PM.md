# Kh-31PM Anti-Radar (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_MAR_1](NG_MAR_1.md) · [NG_GBU_57A_MOP](NG_GBU_57A_MOP.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_kh31_ramjet](../renders/ng_kh31_ramjet.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_31PM` |
| **CLSID Pylône** | `{NEXTGEN_KH_31PM}` |
| **Nom Court HUD / RWR** | `Kh-31PM` |
| **Modèle 3D (`.edm`)** | [`ng_kh31_ramjet.edm`](../../mod/Shapes/ng_kh31_ramjet.edm) |
| **Calibre / Diamètre** | `0.360 m` (`360 mm`) |
| **Longueur** | `4.70 m` |
| **Masse au Lancement** | `610.0 kg` |
| **Mach Max** | `Mach 3.5` |
| **Portée Max** | `250 km` |
| **Charge Militaire** | `90.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (220.0 kg fuel, Burn: 35.0s, Isp: 270s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_ULTRA` — **Slender Ultra-Long-Range Supersonic / Ramjet Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.380` | `0.420` | `0.740` | `0.510` | `0.340` | `0.265` | `0.232` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
