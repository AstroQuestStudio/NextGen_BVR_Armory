# Lancet-3M Izdeliye-51M (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Loitering Munitions & One-Way Drones** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_loitering_x](../renders/ng_loitering_x.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_LANCET_3M` |
| **CLSID Pylône** | `{NEXTGEN_LANCET_3M}` |
| **Nom Court HUD / RWR** | `Lancet-3M` |
| **Modèle 3D (`.edm`)** | [`ng_loitering_x.edm`](../../mod/Shapes/ng_loitering_x.edm) |
| **Calibre / Diamètre** | `0.160 m` (`160 mm`) |
| **Longueur** | `1.75 m` |
| **Masse au Lancement** | `22.0 kg` |
| **Mach Max** | `Mach 0.38` |
| **Portée Max** | `80 km` |
| **Charge Militaire** | `8.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (5.5 kg fuel, Burn: 720.0s, Isp: 2400s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `1000 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_LOITER_DRONE` — **Subsonic Loitering Prop / Jet Drone Polar**
- **Détails physiques (`polar_profiles.lua`)** : Ultra-low cruise drag (`Cx0 = 0.020`, `Sw = 1.15`, `dCydA = {0.08, 0.042}`) for long-endurance loitering munitions.

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
- `DrawArg 407` — Rotation continue de l'hélice propulsive
