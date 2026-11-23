# STM Kargu-3 Precision Loiterer

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_GREEN_DRAGON](NG_GREEN_DRAGON.md) · [NG_RAM_II](NG_RAM_II.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_loitering_x](../renders/ng_loitering_x.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KARGU_3` |
| **CLSID Pylône** | `{NEXTGEN_KARGU_3}` |
| **Nom Court HUD / RWR** | `Kargu-3` |
| **Modèle 3D (`.edm`)** | [`ng_loitering_x.edm`](../../mod/Shapes/ng_loitering_x.edm) |
| **Calibre / Diamètre** | `0.120 m` (`120 mm`) |
| **Longueur** | `0.85 m` |
| **Masse au Lancement** | `7.5 kg` |
| **Mach Max** | `Mach 0.22` |
| **Portée Max** | `15 km` |
| **Charge Militaire** | `1.8 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (1.5 kg fuel, Burn: 500.0s, Isp: 1800s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `700 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
- `DrawArg 407` — Rotation continue de l'hélice propulsive
