# TUBITAK Akdogan Mini-AAM (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_GOKHAN](NG_GOKHAN.md) · [NG_PL_10](NG_PL_10.md) →  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_peregrine](../renders/ng_peregrine.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_AKDOGAN` |
| **CLSID Pylône** | `{NEXTGEN_AKDOGAN}` |
| **Nom Court HUD / RWR** | `Akdogan` |
| **Modèle 3D (`.edm`)** | [`ng_peregrine.edm`](../../mod/Shapes/ng_peregrine.edm) |
| **Calibre / Diamètre** | `0.120 m` (`120 mm`) |
| **Longueur** | `1.85 m` |
| **Masse au Lancement** | `62.0 kg` |
| **Mach Max** | `Mach 3.4` |
| **Portée Max** | `35 km` |
| **Charge Militaire** | `9.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `55 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (22.0 kg fuel, Burn: 5.5s, Isp: 245s) |
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
