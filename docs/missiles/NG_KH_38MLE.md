# Kh-38MLE Laser Tact-ASM (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_HERMES_A](NG_HERMES_A.md) · [NG_KH_38MTE](NG_KH_38MTE.md) →  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_kh38_grom](../renders/ng_kh38_grom.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_38MLE` |
| **CLSID Pylône** | `{NEXTGEN_KH_38MLE}` |
| **Nom Court HUD / RWR** | `Kh38MLE` |
| **Modèle 3D (`.edm`)** | [`ng_kh38_grom.edm`](../../mod/Shapes/ng_kh38_grom.edm) |
| **Calibre / Diamètre** | `0.310 m` (`310 mm`) |
| **Longueur** | `4.20 m` |
| **Masse au Lancement** | `520.0 kg` |
| **Mach Max** | `Mach 2.2` |
| **Portée Max** | `45 km` |
| **Charge Militaire** | `250.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (145.0 kg fuel, Burn: 12.0s, Isp: 245s) |
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
