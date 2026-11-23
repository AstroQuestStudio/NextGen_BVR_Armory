# DRDO Astra Mk 2 Dual-Pulse (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ASTRA_MK1](NG_ASTRA_MK1.md) · [NG_ASTRA_MK3](NG_ASTRA_MK3.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_gokdogan_astra](../renders/ng_gokdogan_astra.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ASTRA_MK2` |
| **CLSID Pylône** | `{NEXTGEN_ASTRA_MK2}` |
| **Nom Court HUD / RWR** | `Astra-2` |
| **Modèle 3D (`.edm`)** | [`ng_gokdogan_astra.edm`](../../mod/Shapes/ng_gokdogan_astra.edm) |
| **Calibre / Diamètre** | `0.178 m` (`178 mm`) |
| **Longueur** | `3.80 m` |
| **Masse au Lancement** | `165.0 kg` |
| **Mach Max** | `Mach 4.6` |
| **Portée Max** | `160 km` |
| **Charge Militaire** | `15.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `42 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (66.0 kg fuel, Burn: 12.0s, Isp: 256s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `185 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
