# IMI Delilah Stand-Off Loiter (NG)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_kalibr_3m54](../renders/ng_kalibr_3m54.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_DELILAH` |
| **CLSID Pylône** | `{NEXTGEN_DELILAH}` |
| **Nom Court HUD / RWR** | `Delilah` |
| **Modèle 3D (`.edm`)** | [`ng_kalibr_3m54.edm`](../../mod/Shapes/ng_kalibr_3m54.edm) |
| **Calibre / Diamètre** | `0.330 m` (`330 mm`) |
| **Longueur** | `2.71 m` |
| **Masse au Lancement** | `187.0 kg` |
| **Mach Max** | `Mach 0.85` |
| **Portée Max** | `250 km` |
| **Charge Militaire** | `30.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (62.0 kg fuel, Burn: 700.0s, Isp: 2800s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1400 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques (`polar_profiles.lua`)** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
