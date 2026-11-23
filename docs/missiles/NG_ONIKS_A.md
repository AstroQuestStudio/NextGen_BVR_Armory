# P-800 Oniks Air-Launched (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_brahmos_intake](../renders/ng_brahmos_intake.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ONIKS_A` |
| **CLSID Pylône** | `{NEXTGEN_ONIKS_A}` |
| **Nom Court HUD / RWR** | `Oniks-A` |
| **Modèle 3D (`.edm`)** | [`ng_brahmos_intake.edm`](../../mod/Shapes/ng_brahmos_intake.edm) |
| **Calibre / Diamètre** | `0.670 m` (`670 mm`) |
| **Longueur** | `8.00 m` |
| **Masse au Lancement** | `2500.0 kg` |
| **Mach Max** | `Mach 2.8` |
| **Portée Max** | `400 km` |
| **Charge Militaire** | `300.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (820.0 kg fuel, Burn: 130.0s, Isp: 310s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `900 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_ULTRA` — **Slender Ultra-Long-Range Supersonic / Ramjet Polar**
- **Détails physiques (`polar_profiles.lua`)** : Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
