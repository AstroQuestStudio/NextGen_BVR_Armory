# Rafael I-Derby ER (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_AAM_4B](NG_AAM_4B.md) · [NG_METEOR](NG_METEOR.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_pl12a](../renders/ng_pl12a.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_I_DERBY_ER` |
| **CLSID Pylône** | `{NEXTGEN_I_DERBY_ER}` |
| **Nom Court HUD / RWR** | `Derby-ER` |
| **Modèle 3D (`.edm`)** | [`ng_pl12a.edm`](../../mod/Shapes/ng_pl12a.edm) |
| **Calibre / Diamètre** | `0.160 m` (`160 mm`) |
| **Longueur** | `3.62 m` |
| **Masse au Lancement** | `118.0 kg` |
| **Mach Max** | `Mach 4.2` |
| **Portée Max** | `100 km` |
| **Charge Militaire** | `23.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `45 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (46.0 kg fuel, Burn: 9.0s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.04` |
| **Temps de Vie Max** | `150 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
