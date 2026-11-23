# KEKA Baguette-II BVR (Troll AAM!)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_PYTH_STUN](NG_PYTH_STUN.md) · [NG_KH_47M2_KINZHAL](NG_KH_47M2_KINZHAL.md) →  
> Catégorie : **KEKA Aerospace Troll Payloads** · Fichier source : `mod/Database/weapons_nextgen.lua`

![Rendu 3D ng_keka_tropo5](../renders/ng_keka_tropo5.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_KEKA_AAM` |
| **CLSID Pylône** | `{NEXTGEN_KEKA_AAM}` |
| **Nom Court HUD / RWR** | `KEKA-AAM` |
| **Modèle 3D (`.edm`)** | [`ng_keka_tropo5.edm`](../../mod/Shapes/ng_keka_tropo5.edm) |
| **Calibre / Diamètre** | `0.280 m` (`280 mm`) |
| **Longueur** | `3.60 m` |
| **Masse au Lancement** | `190.0 kg` |
| **Mach Max** | `Mach 3.8` |
| **Portée Max** | `95 km` |
| **Charge Militaire** | `45.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `20 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (82.0 kg fuel, Burn: 9.0s, Isp: 245s) |
| **Résistance ECM (`ccm_k0`)** | `0.15` |
| **Temps de Vie Max** | `120 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_KEKA_TROLL` — **KEKA Aerospace Troposphère Amateur Wobble Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : High base drag from riveted structural collars (`Cx0 = 0.78..1.48`, `wind_sigma = 12.0`, `wind_time = 8.0`) inducing realistic Savanna amateur flight wobble!

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.780` | `0.960` | `1.480` | `1.050` | `0.760` | `0.640` | `0.540` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
