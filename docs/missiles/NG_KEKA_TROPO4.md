# KEKA Troposphere-4 DIY (Troll!)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **KEKA Aerospace Troll Payloads** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_keka_tropo5](../renders/ng_keka_tropo5.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KEKA_TROPO4` |
| **CLSID Pylône** | `{NEXTGEN_KEKA_TROPO4}` |
| **Nom Court HUD / RWR** | `KEKA-T4` |
| **Modèle 3D (`.edm`)** | [`ng_keka_tropo5.edm`](../../mod/Shapes/ng_keka_tropo5.edm) |
| **Calibre / Diamètre** | `0.240 m` (`240 mm`) |
| **Longueur** | `3.20 m` |
| **Masse au Lancement** | `135.0 kg` |
| **Mach Max** | `Mach 2.7` |
| **Portée Max** | `25 km` |
| **Charge Militaire** | `30.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (52.0 kg fuel, Burn: 7.0s, Isp: 215s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_KEKA_TROLL` — **KEKA Aerospace Troposphère Amateur Wobble Polar**
- **Détails physiques (`polar_profiles.lua`)** : High base drag from riveted structural collars (`Cx0 = 0.78..1.48`, `wind_sigma = 12.0`, `wind_time = 8.0`) inducing realistic Savanna amateur flight wobble!

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
