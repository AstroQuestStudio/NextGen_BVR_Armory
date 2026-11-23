# CM-102 Anti-Radiation (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_RUDRAM_2](NG_RUDRAM_2.md) · [NG_YJ_91](NG_YJ_91.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_rudram_arm](../renders/ng_rudram_arm.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_CM_102` |
| **CLSID Pylône** | `{NEXTGEN_CM_102}` |
| **Nom Court HUD / RWR** | `CM-102` |
| **Modèle 3D (`.edm`)** | [`ng_rudram_arm.edm`](../../mod/Shapes/ng_rudram_arm.edm) |
| **Calibre / Diamètre** | `0.350 m` (`350 mm`) |
| **Longueur** | `4.80 m` |
| **Masse au Lancement** | `520.0 kg` |
| **Mach Max** | `Mach 3.5` |
| **Portée Max** | `100 km` |
| **Charge Militaire** | `80.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (180.0 kg fuel, Burn: 18.0s, Isp: 255s) |
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
