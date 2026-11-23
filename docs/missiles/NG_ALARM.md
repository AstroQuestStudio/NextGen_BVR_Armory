# MBDA ALARM Loiter-SEAD (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_alarm_sead](../renders/ng_alarm_sead.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ALARM` |
| **CLSID Pylône** | `{NEXTGEN_ALARM}` |
| **Nom Court HUD / RWR** | `ALARM` |
| **Modèle 3D (`.edm`)** | [`ng_alarm_sead.edm`](../../mod/Shapes/ng_alarm_sead.edm) |
| **Calibre / Diamètre** | `0.230 m` (`230 mm`) |
| **Longueur** | `4.24 m` |
| **Masse au Lancement** | `268.0 kg` |
| **Mach Max** | `Mach 2.4` |
| **Portée Max** | `93 km` |
| **Charge Militaire** | `55.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (82.0 kg fuel, Burn: 16.0s, Isp: 240s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques (`polar_profiles.lua`)** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
