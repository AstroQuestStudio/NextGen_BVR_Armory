# PL-17 AWACS-Killer (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_pl17_long](../renders/ng_pl17_long.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_PL_17` |
| **CLSID Pylône** | `{NEXTGEN_PL_17}` |
| **Nom Court HUD / RWR** | `PL-17` |
| **Modèle 3D (`.edm`)** | [`ng_pl17_long.edm`](../../mod/Shapes/ng_pl17_long.edm) |
| **Calibre / Diamètre** | `0.260 m` (`260 mm`) |
| **Longueur** | `6.00 m` |
| **Masse au Lancement** | `450.0 kg` |
| **Mach Max** | `Mach 5.5` |
| **Portée Max** | `350 km` |
| **Charge Militaire** | `45.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (210.0 kg fuel, Burn: 16.0s, Isp: 265s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `260 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_ULTRA` — **Slender Ultra-Long-Range Supersonic / Ramjet Polar**
- **Détails physiques (`polar_profiles.lua`)** : Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
