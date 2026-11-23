# AIM-120A AMRAAM (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · [NG_AIM_120C5](NG_AIM_120C5.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_aim120a](../renders/ng_aim120a.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_AIM_120A` |
| **CLSID Pylône** | `{NEXTGEN_AIM_120A}` |
| **Nom Court HUD / RWR** | `AIM-120A` |
| **Modèle 3D (`.edm`)** | [`ng_aim120a.edm`](../../mod/Shapes/ng_aim120a.edm) |
| **Calibre / Diamètre** | `0.178 m` (`178 mm`) |
| **Longueur** | `3.66 m` |
| **Masse au Lancement** | `152.0 kg` |
| **Mach Max** | `Mach 4.0` |
| **Portée Max** | `75 km` |
| **Charge Militaire** | `22.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (45.0 kg fuel, Burn: 7.0s, Isp: 240s) |
| **Résistance ECM (`ccm_k0`)** | `0.12` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
