# Kh-22N Burya Mach 4.6 ASM (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_HSIUNG_FENG_3](NG_HSIUNG_FENG_3.md) · [NG_KH_32](NG_KH_32.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_kh22_32](../renders/ng_kh22_32.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_22N` |
| **CLSID Pylône** | `{NEXTGEN_KH_22N}` |
| **Nom Court HUD / RWR** | `Kh-22N` |
| **Modèle 3D (`.edm`)** | [`ng_kh22_32.edm`](../../mod/Shapes/ng_kh22_32.edm) |
| **Calibre / Diamètre** | `0.920 m` (`920 mm`) |
| **Longueur** | `11.65 m` |
| **Masse au Lancement** | `5820.0 kg` |
| **Mach Max** | `Mach 4.6` |
| **Portée Max** | `600 km` |
| **Charge Militaire** | `960.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (3000.0 kg fuel, Burn: 120.0s, Isp: 310s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1200 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_HYPERSONIC` — **9M723 Iskander / Kinzhal / DF-17 Hypersonic Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low hypersonic drag curve (`Cx0 = 0.36 @ M0 -> 0.52 @ M1.0 -> 0.118 @ M5.0`, `Iy = 3800`) for quasi-ballistic and ABM trajectories.

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.360` | `0.370` | `0.510` | `0.310` | `0.188` | `0.140` | `0.118` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
