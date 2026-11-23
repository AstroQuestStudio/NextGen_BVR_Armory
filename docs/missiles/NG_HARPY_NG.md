# IAI Harpy NG Anti-Radar Drone

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_HAROP_AIR](NG_HAROP_AIR.md) · [NG_ALTIUS_600M](NG_ALTIUS_600M.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_harop](../renders/ng_harop.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_HARPY_NG` |
| **CLSID Pylône** | `{NEXTGEN_HARPY_NG}` |
| **Nom Court HUD / RWR** | `Harpy-NG` |
| **Modèle 3D (`.edm`)** | [`ng_harop.edm`](../../mod/Shapes/ng_harop.edm) |
| **Calibre / Diamètre** | `0.280 m` (`280 mm`) |
| **Longueur** | `2.70 m` |
| **Masse au Lancement** | `160.0 kg` |
| **Mach Max** | `Mach 0.42` |
| **Portée Max** | `500 km` |
| **Charge Militaire** | `32.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (48.0 kg fuel, Burn: 1600.0s, Isp: 2800s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `2000 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- `DrawArg 407` — Rotation continue de l'hélice propulsive
