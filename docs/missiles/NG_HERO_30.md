# UVision HERO-30 Tube Loiterer

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ALTIUS_700M](NG_ALTIUS_700M.md) · [NG_GREEN_DRAGON](NG_GREEN_DRAGON.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_loitering_x](../renders/ng_loitering_x.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_HERO_30` |
| **CLSID Pylône** | `{NEXTGEN_HERO_30}` |
| **Nom Court HUD / RWR** | `HERO-30` |
| **Modèle 3D (`.edm`)** | [`ng_loitering_x.edm`](../../mod/Shapes/ng_loitering_x.edm) |
| **Calibre / Diamètre** | `0.100 m` (`100 mm`) |
| **Longueur** | `0.95 m` |
| **Masse au Lancement** | `3.5 kg` |
| **Mach Max** | `Mach 0.25` |
| **Portée Max** | `15 km` |
| **Charge Militaire** | `0.8 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (0.8 kg fuel, Burn: 450.0s, Isp: 1900s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `600 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
- `DrawArg 407` — Rotation continue de l'hélice propulsive
