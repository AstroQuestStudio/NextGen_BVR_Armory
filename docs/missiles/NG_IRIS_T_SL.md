# IRIS-T SL Extended (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_IRIS_T](NG_IRIS_T.md) · [NG_AAM_5B](NG_AAM_5B.md) →  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_sam_irist_slm](../renders/ng_sam_irist_slm.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_IRIS_T_SL` |
| **CLSID Pylône** | `{NEXTGEN_IRIS_T_SL}` |
| **Nom Court HUD / RWR** | `IRIST-SL` |
| **Modèle 3D (`.edm`)** | [`ng_sam_irist_slm.edm`](../../mod/Shapes/ng_sam_irist_slm.edm) |
| **Calibre / Diamètre** | `0.152 m` (`152 mm`) |
| **Longueur** | `4.00 m` |
| **Masse au Lancement** | `118.0 kg` |
| **Mach Max** | `Mach 3.8` |
| **Portée Max** | `45 km` |
| **Charge Militaire** | `11.4 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `50 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (44.0 kg fuel, Burn: 7.5s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.02` |
| **Temps de Vie Max** | `90 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_WVR` — **High-Alpha HOBS Dogfight Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.420` | `0.500` | `0.960` | `0.750` | `0.580` | `0.480` | `0.420` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
