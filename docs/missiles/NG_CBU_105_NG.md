# CBU-105 WCMD SFW NG (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **ATGM, Guided Rockets & Tactical ASM** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_durandal_runway](../renders/ng_durandal_runway.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_CBU_105_NG` |
| **CLSID Pylône** | `{NEXTGEN_CBU_105_NG}` |
| **Nom Court HUD / RWR** | `CBU-105N` |
| **Modèle 3D (`.edm`)** | [`ng_durandal_runway.edm`](../../mod/Shapes/ng_durandal_runway.edm) |
| **Calibre / Diamètre** | `0.400 m` (`400 mm`) |
| **Longueur** | `2.34 m` |
| **Masse au Lancement** | `430.0 kg` |
| **Mach Max** | `Mach 1.0` |
| **Portée Max** | `38 km` |
| **Charge Militaire** | `220.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1.0 kg fuel, Burn: 1.0s, Isp: 40s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques (`polar_profiles.lua`)** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

## Animations & Modèle 3D

- `DrawArg 0` — Déploiement du parachute freineur (`1.0`)
