# S-13DF 122mm Thermobaric (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_S8_CORR](NG_S8_CORR.md) · [NG_CRV7_PG](NG_CRV7_PG.md) →  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_guided_rocket](../renders/ng_guided_rocket.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_S13_DF` |
| **CLSID Pylône** | `{NEXTGEN_S13_DF}` |
| **Nom Court HUD / RWR** | `S-13DF` |
| **Modèle 3D (`.edm`)** | [`ng_guided_rocket.edm`](../../mod/Shapes/ng_guided_rocket.edm) |
| **Calibre / Diamètre** | `0.122 m` (`122 mm`) |
| **Longueur** | `2.90 m` |
| **Masse au Lancement** | `68.0 kg` |
| **Mach Max** | `Mach 2.3` |
| **Portée Max** | `14 km` |
| **Charge Militaire** | `32.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (16.0 kg fuel, Burn: 2.5s, Isp: 230s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
