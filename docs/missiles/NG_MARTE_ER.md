# MBDA Marte ER 100km Turbojet (NG)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_SEA_VENOM](NG_SEA_VENOM.md) · [NG_TESEO_MK2E](NG_TESEO_MK2E.md) →  
> Catégorie : **Anti-Ship Missiles (AShM)** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_kh35u](../renders/ng_kh35u.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_MARTE_ER` |
| **CLSID Pylône** | `{NEXTGEN_MARTE_ER}` |
| **Nom Court HUD / RWR** | `Marte-ER` |
| **Modèle 3D (`.edm`)** | [`ng_kh35u.edm`](../../mod/Shapes/ng_kh35u.edm) |
| **Calibre / Diamètre** | `0.316 m` (`316 mm`) |
| **Longueur** | `3.60 m` |
| **Masse au Lancement** | `340.0 kg` |
| **Mach Max** | `Mach 0.92` |
| **Portée Max** | `110 km` |
| **Charge Militaire** | `75.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (90.0 kg fuel, Burn: 450.0s, Isp: 2800s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `900 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_CRUISE_STEALTH` — **AGM-84H / Kh-101 Subsonic Stealth Cruise Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High L/D folded-wing turbofan cruise curve (`Cx0 = 0.023` subsonic cruise, `Sw = 1.35`, `addDeplSw = 0.80`, `wingsDeplDelay = 1.0s`, `wingsDeplProcTime = 2.5s`).

| Mach | M0.0 | M0.5 | M0.8 | M1.0 | M1.4 | M2.0 |
|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.023` | `0.023` | `0.035` | `0.450` | `0.290` | `0.245` |

## Animations & Modèle 3D

- `DrawArg 25` — Ailes / empennages repliés sur pylône (`0.0`) -> déployés en vol (`1.0`)
