# DRDO Rudram-1 NGARM SEAD (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ARMAT](NG_ARMAT.md) · [NG_RUDRAM_2](NG_RUDRAM_2.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_rudram_arm](../renders/ng_rudram_arm.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_RUDRAM_1` |
| **CLSID Pylône** | `{NEXTGEN_RUDRAM_1}` |
| **Nom Court HUD / RWR** | `Rudram-1` |
| **Modèle 3D (`.edm`)** | [`ng_rudram_arm.edm`](../../mod/Shapes/ng_rudram_arm.edm) |
| **Calibre / Diamètre** | `0.360 m` (`360 mm`) |
| **Longueur** | `5.50 m` |
| **Masse au Lancement** | `600.0 kg` |
| **Mach Max** | `Mach 2.5` |
| **Portée Max** | `150 km` |
| **Charge Militaire** | `120.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (210.0 kg fuel, Burn: 22.0s, Isp: 255s) |
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
