# AASM-250 Hammer (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **SEAD / Anti-Radar & Powered Precision** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_aasm_hammer](../renders/ng_aasm_hammer.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_AASM_250` |
| **CLSID Pylône** | `{NEXTGEN_AASM_250}` |
| **Nom Court HUD / RWR** | `AASM-250` |
| **Modèle 3D (`.edm`)** | [`ng_aasm_hammer.edm`](../../mod/Shapes/ng_aasm_hammer.edm) |
| **Calibre / Diamètre** | `0.273 m` (`273 mm`) |
| **Longueur** | `3.10 m` |
| **Masse au Lancement** | `340.0 kg` |
| **Mach Max** | `Mach 1.15` |
| **Portée Max** | `75 km` |
| **Charge Militaire** | `120.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (28.0 kg fuel, Burn: 8.0s, Isp: 225s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_GLIDE_BOMB` — **LS-6-500 / JSOW High-L/D Folding Glide Polar**
- **Détails physiques (`polar_profiles.lua`)** : Long-range folding-wing glide polar (`Cx0 = 0.028` subsonic, `Sw = 0.65`, `addDeplSw = 0.85`, `maxAoa = 0.32`).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
