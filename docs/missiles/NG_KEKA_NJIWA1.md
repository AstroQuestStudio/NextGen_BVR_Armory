# KEKA Njiwa-1 MicroSat Booster!

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **KEKA Aerospace Troll Payloads** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_keka_tropo6](../renders/ng_keka_tropo6.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KEKA_NJIWA1` |
| **CLSID Pylône** | `{NEXTGEN_KEKA_NJIWA1}` |
| **Nom Court HUD / RWR** | `Njiwa-1` |
| **Modèle 3D (`.edm`)** | [`ng_keka_tropo6.edm`](../../mod/Shapes/ng_keka_tropo6.edm) |
| **Calibre / Diamètre** | `0.420 m` (`420 mm`) |
| **Longueur** | `6.20 m` |
| **Masse au Lancement** | `820.0 kg` |
| **Mach Max** | `Mach 5.0` |
| **Portée Max** | `500 km` |
| **Charge Militaire** | `150.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (420.0 kg fuel, Burn: 24.0s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `140 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_KEKA_TROLL` — **KEKA Aerospace Troposphère Amateur Wobble Polar**
- **Détails physiques (`polar_profiles.lua`)** : High base drag from riveted structural collars (`Cx0 = 0.78..1.48`, `wind_sigma = 12.0`, `wind_time = 8.0`) inducing realistic Savanna amateur flight wobble!

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
