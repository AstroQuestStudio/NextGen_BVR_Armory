# AQ-400 Scythe Long-Range Drone

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_PEKLO](NG_PEKLO.md) · [NG_HAROP_AIR](NG_HAROP_AIR.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_palianytsia_jet](../renders/ng_palianytsia_jet.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_AQ_400_SCYTHE` |
| **CLSID Pylône** | `{NEXTGEN_AQ_400_SCYTHE}` |
| **Nom Court HUD / RWR** | `AQ-400` |
| **Modèle 3D (`.edm`)** | [`ng_palianytsia_jet.edm`](../../mod/Shapes/ng_palianytsia_jet.edm) |
| **Calibre / Diamètre** | `0.300 m` (`300 mm`) |
| **Longueur** | `3.00 m` |
| **Masse au Lancement** | `150.0 kg` |
| **Mach Max** | `Mach 0.28` |
| **Portée Max** | `750 km` |
| **Charge Militaire** | `42.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (42.0 kg fuel, Burn: 2400.0s, Isp: 3200s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `2400 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
