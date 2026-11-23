# Rafael Spike-LR2 Air-Pod (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_SPIKE_NLOS](NG_SPIKE_NLOS.md) · [NG_FGM_148F_JAV](NG_FGM_148F_JAV.md) →  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_javelin_top](../renders/ng_javelin_top.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SPIKE_LR2` |
| **CLSID Pylône** | `{NEXTGEN_SPIKE_LR2}` |
| **Nom Court HUD / RWR** | `SpikeLR2` |
| **Modèle 3D (`.edm`)** | [`ng_javelin_top.edm`](../../mod/Shapes/ng_javelin_top.edm) |
| **Calibre / Diamètre** | `0.130 m` (`130 mm`) |
| **Longueur** | `1.20 m` |
| **Masse au Lancement** | `13.0 kg` |
| **Mach Max** | `Mach 1.1` |
| **Portée Max** | `10 km` |
| **Charge Militaire** | `4.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (3.2 kg fuel, Burn: 12.0s, Isp: 225s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
