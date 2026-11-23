# Raytheon Peregrine Mini-BVR (NG)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_peregrine](../renders/ng_peregrine.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_PEREGRINE` |
| **CLSID Pylône** | `{NEXTGEN_PEREGRINE}` |
| **Nom Court HUD / RWR** | `Peregrn` |
| **Modèle 3D (`.edm`)** | [`ng_peregrine.edm`](../../mod/Shapes/ng_peregrine.edm) |
| **Calibre / Diamètre** | `0.120 m` (`120 mm`) |
| **Longueur** | `1.80 m` |
| **Masse au Lancement** | `68.0 kg` |
| **Mach Max** | `Mach 4.2` |
| **Portée Max** | `90 km` |
| **Charge Militaire** | `9.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (28.0 kg fuel, Burn: 7.0s, Isp: 252s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `120 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques (`polar_profiles.lua`)** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.

## Emports Multi-Racks Compatibles
- `{NEXTGEN_PEREGRINE_2X}` — **2x Raytheon Peregrine Twin-Rack (NextGen)** (`2x`)
