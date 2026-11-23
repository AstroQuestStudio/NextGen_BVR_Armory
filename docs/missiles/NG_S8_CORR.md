# S-8KOR 80mm Laser Rocket (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ZUNI_LASER](NG_ZUNI_LASER.md) · [NG_S13_DF](NG_S13_DF.md) →  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_guided_rocket](../renders/ng_guided_rocket.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_S8_CORR` |
| **CLSID Pylône** | `{NEXTGEN_S8_CORR}` |
| **Nom Court HUD / RWR** | `S-8KOR` |
| **Modèle 3D (`.edm`)** | [`ng_guided_rocket.edm`](../../mod/Shapes/ng_guided_rocket.edm) |
| **Calibre / Diamètre** | `0.080 m` (`80 mm`) |
| **Longueur** | `1.65 m` |
| **Masse au Lancement** | `15.5 kg` |
| **Mach Max** | `Mach 2.1` |
| **Portée Max** | `10 km` |
| **Charge Militaire** | `4.2 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (3.8 kg fuel, Burn: 1.8s, Isp: 220s) |
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
