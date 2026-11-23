# R-74M2 (K-74M2) WVR (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ASRAAM_BLK6](NG_ASRAAM_BLK6.md) · [NG_PL_10E](NG_PL_10E.md) →  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_r74m2](../renders/ng_r74m2.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_R_74M2` |
| **CLSID Pylône** | `{NEXTGEN_R_74M2}` |
| **Nom Court HUD / RWR** | `R-74M2` |
| **Modèle 3D (`.edm`)** | [`ng_r74m2.edm`](../../mod/Shapes/ng_r74m2.edm) |
| **Calibre / Diamètre** | `0.170 m` (`170 mm`) |
| **Longueur** | `2.90 m` |
| **Masse au Lancement** | `105.0 kg` |
| **Mach Max** | `Mach 3.2` |
| **Portée Max** | `40 km` |
| **Charge Militaire** | `8.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (35.0 kg fuel, Burn: 5.5s, Isp: 242s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `75 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_WVR` — **High-Alpha HOBS Dogfight Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.420` | `0.500` | `0.960` | `0.750` | `0.580` | `0.480` | `0.420` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
