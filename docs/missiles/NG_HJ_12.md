# Norinco HJ-12 Top-Attack Pod (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_HJ_10](NG_HJ_10.md) · [NG_UMTAS_L](NG_UMTAS_L.md) →  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_javelin_top](../renders/ng_javelin_top.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_HJ_12` |
| **CLSID Pylône** | `{NEXTGEN_HJ_12}` |
| **Nom Court HUD / RWR** | `HJ-12` |
| **Modèle 3D (`.edm`)** | [`ng_javelin_top.edm`](../../mod/Shapes/ng_javelin_top.edm) |
| **Calibre / Diamètre** | `0.135 m` (`135 mm`) |
| **Longueur** | `1.25 m` |
| **Masse au Lancement** | `17.0 kg` |
| **Mach Max** | `Mach 1.1` |
| **Portée Max** | `5 km` |
| **Charge Militaire** | `7.5 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (3.8 kg fuel, Burn: 8.0s, Isp: 220s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
