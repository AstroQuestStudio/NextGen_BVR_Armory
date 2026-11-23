# IAI Green Dragon Tactical Drone

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_HERO_30](NG_HERO_30.md) · [NG_KARGU_3](NG_KARGU_3.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_loitering_x](../renders/ng_loitering_x.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_GREEN_DRAGON` |
| **CLSID Pylône** | `{NEXTGEN_GREEN_DRAGON}` |
| **Nom Court HUD / RWR** | `GrnDrgn` |
| **Modèle 3D (`.edm`)** | [`ng_loitering_x.edm`](../../mod/Shapes/ng_loitering_x.edm) |
| **Calibre / Diamètre** | `0.140 m` (`140 mm`) |
| **Longueur** | `1.60 m` |
| **Masse au Lancement** | `15.0 kg` |
| **Mach Max** | `Mach 0.28` |
| **Portée Max** | `40 km` |
| **Charge Militaire** | `3.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (3.5 kg fuel, Burn: 720.0s, Isp: 2200s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1000 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
- `DrawArg 407` — Rotation continue de l'hélice propulsive
