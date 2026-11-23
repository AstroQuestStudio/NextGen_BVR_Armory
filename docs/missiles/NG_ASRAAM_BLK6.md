# MBDA ASRAAM Block 6 (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Air-to-Air WVR & HOBS** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_asraam_sleek](../renders/ng_asraam_sleek.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ASRAAM_BLK6` |
| **CLSID Pylône** | `{NEXTGEN_ASRAAM_BLK6}` |
| **Nom Court HUD / RWR** | `ASRAAM6` |
| **Modèle 3D (`.edm`)** | [`ng_asraam_sleek.edm`](../../mod/Shapes/ng_asraam_sleek.edm) |
| **Calibre / Diamètre** | `0.166 m` (`166 mm`) |
| **Longueur** | `2.90 m` |
| **Masse au Lancement** | `88.0 kg` |
| **Mach Max** | `Mach 3.8` |
| **Portée Max** | `50 km` |
| **Charge Militaire** | `10.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | IIR / Infra-Rouge Passif (`Head_Type = 1`) |
| **Propulsion** | Single/Sustained (32.0 kg fuel, Burn: 5.5s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `85 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_WVR` — **High-Alpha HOBS Dogfight Polar**
- **Détails physiques (`polar_profiles.lua`)** : High-lift / thrust-vectoring dogfight curve (`Cya = 0.62..0.92`, low pitch/yaw inertia `Iy=68`, high roll rate `Mxd=14`).

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
