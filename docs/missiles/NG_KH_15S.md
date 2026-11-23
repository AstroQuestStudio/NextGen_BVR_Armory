# Kh-15S Raduga Mach 5 ASM (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_AIR_LORA](NG_AIR_LORA.md) · [NG_FATH_360](NG_FATH_360.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_rampage_lora](../renders/ng_rampage_lora.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_15S` |
| **CLSID Pylône** | `{NEXTGEN_KH_15S}` |
| **Nom Court HUD / RWR** | `Kh-15S` |
| **Modèle 3D (`.edm`)** | [`ng_rampage_lora.edm`](../../mod/Shapes/ng_rampage_lora.edm) |
| **Calibre / Diamètre** | `0.455 m` (`455 mm`) |
| **Longueur** | `4.78 m` |
| **Masse au Lancement** | `1200.0 kg` |
| **Mach Max** | `Mach 5.0` |
| **Portée Max** | `300 km` |
| **Charge Militaire** | `150.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (580.0 kg fuel, Burn: 32.0s, Isp: 270s) |
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
