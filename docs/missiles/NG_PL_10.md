# PL-10 Domestic IIR HOBS (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_AKDOGAN](NG_AKDOGAN.md) · [NG_PL_16](NG_PL_16.md) →  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_python5](../renders/ng_python5.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_PL_10` |
| **CLSID Pylône** | `{NEXTGEN_PL_10}` |
| **Nom Court HUD / RWR** | `PL-10` |
| **Modèle 3D (`.edm`)** | [`ng_python5.edm`](../../mod/Shapes/ng_python5.edm) |
| **Calibre / Diamètre** | `0.160 m` (`160 mm`) |
| **Longueur** | `3.00 m` |
| **Masse au Lancement** | `105.0 kg` |
| **Mach Max** | `Mach 4.0` |
| **Portée Max** | `38 km` |
| **Charge Militaire** | `11.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `60 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (35.0 kg fuel, Burn: 5.4s, Isp: 246s) |
| **Résistance ECM (`ccm_k0`)** | `0.02` |
| **Temps de Vie Max** | `75 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_WVR` — **High-Alpha HOBS Dogfight Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.420` | `0.500` | `0.960` | `0.750` | `0.580` | `0.480` | `0.420` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
