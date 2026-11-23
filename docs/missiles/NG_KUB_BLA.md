# ZALA KUB-BLA Loitering Delta (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_LANCET_3M](NG_LANCET_3M.md) · [NG_HERO_120](NG_HERO_120.md) →  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_shahed_136](../renders/ng_shahed_136.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KUB_BLA` |
| **CLSID Pylône** | `{NEXTGEN_KUB_BLA}` |
| **Nom Court HUD / RWR** | `KUB-BLA` |
| **Modèle 3D (`.edm`)** | [`ng_shahed_136.edm`](../../mod/Shapes/ng_shahed_136.edm) |
| **Calibre / Diamètre** | `0.140 m` (`140 mm`) |
| **Longueur** | `1.21 m` |
| **Masse au Lancement** | `14.0 kg` |
| **Mach Max** | `Mach 0.25` |
| **Portée Max** | `40 km` |
| **Charge Militaire** | `3.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (2.5 kg fuel, Burn: 600.0s, Isp: 2000s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `900 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.020` | `0.042` | `0.180` | `0.420` | `0.340` | `0.260` |

## Animations & Modèle 3D

- `DrawArg 407` — Rotation continue de l'hélice propulsive
