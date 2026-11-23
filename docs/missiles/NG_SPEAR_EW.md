# MBDA SPEAR-EW Stand-In Jammer (NG)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Stealth Cruise & Stand-Off** · Fichier source : `mod/Database/weapons_arsenal_ag.lua`

![Rendu 3D ng_spear_ew](../renders/ng_spear_ew.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SPEAR_EW` |
| **CLSID Pylône** | `{NEXTGEN_SPEAR_EW}` |
| **Nom Court HUD / RWR** | `SPEAR-EW` |
| **Modèle 3D (`.edm`)** | [`ng_spear_ew.edm`](../../mod/Shapes/ng_spear_ew.edm) |
| **Calibre / Diamètre** | `0.180 m` (`180 mm`) |
| **Longueur** | `1.80 m` |
| **Masse au Lancement** | `92.0 kg` |
| **Mach Max** | `Mach 0.95` |
| **Portée Max** | `140 km` |
| **Charge Militaire** | `15.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (26.0 kg fuel, Burn: 420.0s, Isp: 2500s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `900 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques (`polar_profiles.lua`)** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)

## Emports Multi-Racks Compatibles
- `{NEXTGEN_SPEAR_EW_3X}` — **3x MBDA SPEAR-EW Jammer Rack (NextGen)** (`3x`)
