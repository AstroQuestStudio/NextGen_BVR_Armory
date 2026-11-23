# Kh-25MPU Passive Anti-Radar (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_AGM_78D](NG_AGM_78D.md) · [NG_KH_28](NG_KH_28.md) →  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_kh58ushke](../renders/ng_kh58ushke.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KH_25MPU` |
| **CLSID Pylône** | `{NEXTGEN_KH_25MPU}` |
| **Nom Court HUD / RWR** | `Kh-25MPU` |
| **Modèle 3D (`.edm`)** | [`ng_kh58ushke.edm`](../../mod/Shapes/ng_kh58ushke.edm) |
| **Calibre / Diamètre** | `0.275 m` (`275 mm`) |
| **Longueur** | `4.19 m` |
| **Masse au Lancement** | `320.0 kg` |
| **Mach Max** | `Mach 2.4` |
| **Portée Max** | `40 km` |
| **Charge Militaire** | `89.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (110.0 kg fuel, Burn: 12.0s, Isp: 242s) |
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
