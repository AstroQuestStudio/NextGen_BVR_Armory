# BrahMos-NG Light Mach 3.5 (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_BRAHMOS_A](NG_BRAHMOS_A.md) · [NG_ONIKS_A](NG_ONIKS_A.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_brahmos_intake](../renders/ng_brahmos_intake.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_BRAHMOS_NG` |
| **CLSID Pylône** | `{NEXTGEN_BRAHMOS_NG}` |
| **Nom Court HUD / RWR** | `BrahmsNG` |
| **Modèle 3D (`.edm`)** | [`ng_brahmos_intake.edm`](../../mod/Shapes/ng_brahmos_intake.edm) |
| **Calibre / Diamètre** | `0.500 m` (`500 mm`) |
| **Longueur** | `6.00 m` |
| **Masse au Lancement** | `1260.0 kg` |
| **Mach Max** | `Mach 3.5` |
| **Portée Max** | `300 km` |
| **Charge Militaire** | `220.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (460.0 kg fuel, Burn: 95.0s, Isp: 320s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `800 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_ULTRA` — **Slender Ultra-Long-Range Supersonic / Ramjet Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.380` | `0.420` | `0.740` | `0.510` | `0.340` | `0.265` | `0.232` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
