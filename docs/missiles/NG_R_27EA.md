# R-27EA Active Alamo (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_R_74M](NG_R_74M.md) · [NG_PYTH_STUN](NG_PYTH_STUN.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_aam4b](../renders/ng_aam4b.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_R_27EA` |
| **CLSID Pylône** | `{NEXTGEN_R_27EA}` |
| **Nom Court HUD / RWR** | `R-27EA` |
| **Modèle 3D (`.edm`)** | [`ng_aam4b.edm`](../../mod/Shapes/ng_aam4b.edm) |
| **Calibre / Diamètre** | `0.260 m` (`260 mm`) |
| **Longueur** | `4.78 m` |
| **Masse au Lancement** | `350.0 kg` |
| **Mach Max** | `Mach 4.5` |
| **Portée Max** | `130 km` |
| **Charge Militaire** | `39.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `26 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (135.0 kg fuel, Burn: 11.0s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.04` |
| **Temps de Vie Max** | `160 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
