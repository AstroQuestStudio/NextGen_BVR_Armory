# Mitsubishi ASM-3 Ramjet (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_ONIKS_A](NG_ONIKS_A.md) · [NG_YJ_12](NG_YJ_12.md) →  
> Catégorie : **Ballistic, MRBM, ALBM & Precision Artillery** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_kh31_ramjet](../renders/ng_kh31_ramjet.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_ASM_3` |
| **CLSID Pylône** | `{NEXTGEN_ASM_3}` |
| **Nom Court HUD / RWR** | `ASM-3` |
| **Modèle 3D (`.edm`)** | [`ng_kh31_ramjet.edm`](../../mod/Shapes/ng_kh31_ramjet.edm) |
| **Calibre / Diamètre** | `0.350 m` (`350 mm`) |
| **Longueur** | `6.00 m` |
| **Masse au Lancement** | `900.0 kg` |
| **Mach Max** | `Mach 3.2` |
| **Portée Max** | `220 km` |
| **Charge Militaire** | `200.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (300.0 kg fuel, Burn: 80.0s, Isp: 300s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `600 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_ULTRA` — **Slender Ultra-Long-Range Supersonic / Ramjet Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Low wave-drag supersonic/ramjet envelope (`Cx0 = 0.38 @ M0 -> 0.74 @ M1.2 -> 0.232 @ M5.0`, sustained low drag above Mach 3).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.380` | `0.420` | `0.740` | `0.510` | `0.340` | `0.265` | `0.232` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
