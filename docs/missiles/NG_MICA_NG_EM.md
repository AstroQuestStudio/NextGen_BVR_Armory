# MICA NG RF Dual-Pulse (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_MICA_IR](NG_MICA_IR.md) · [NG_MICA_NG_IR](NG_MICA_NG_IR.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_mica_ng](../renders/ng_mica_ng.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_MICA_NG_EM` |
| **CLSID Pylône** | `{NEXTGEN_MICA_NG_EM}` |
| **Nom Court HUD / RWR** | `MICA-NGR` |
| **Modèle 3D (`.edm`)** | [`ng_mica_ng.edm`](../../mod/Shapes/ng_mica_ng.edm) |
| **Calibre / Diamètre** | `0.160 m` (`160 mm`) |
| **Longueur** | `3.10 m` |
| **Masse au Lancement** | `115.0 kg` |
| **Mach Max** | `Mach 4.2` |
| **Portée Max** | `105 km` |
| **Charge Militaire** | `12.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `50 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (48.0 kg fuel, Burn: 9.0s, Isp: 258s) |
| **Résistance ECM (`ccm_k0`)** | `0.02` |
| **Temps de Vie Max** | `135 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_WVR` — **High-Alpha HOBS Dogfight Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.420` | `0.500` | `0.960` | `0.750` | `0.580` | `0.480` | `0.420` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
