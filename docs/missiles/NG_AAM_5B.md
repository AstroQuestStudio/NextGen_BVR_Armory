# Mitsubishi AAM-5B IIR (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_IRIS_T_SL](NG_IRIS_T_SL.md) · [NG_PYTHON_4](NG_PYTHON_4.md) →  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_iris_t](../renders/ng_iris_t.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_AAM_5B` |
| **CLSID Pylône** | `{NEXTGEN_AAM_5B}` |
| **Nom Court HUD / RWR** | `AAM-5B` |
| **Modèle 3D (`.edm`)** | [`ng_iris_t.edm`](../../mod/Shapes/ng_iris_t.edm) |
| **Calibre / Diamètre** | `0.130 m` (`130 mm`) |
| **Longueur** | `3.10 m` |
| **Masse au Lancement** | `95.0 kg` |
| **Mach Max** | `Mach 3.5` |
| **Portée Max** | `35 km` |
| **Charge Militaire** | `11.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `55 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (34.0 kg fuel, Burn: 5.2s, Isp: 248s) |
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
