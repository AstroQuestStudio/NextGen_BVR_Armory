# TC-2C Sky Sword II BVR (NextGen)

> [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md) · ← [NG_MAGIC_3](NG_MAGIC_3.md) · [NG_KORNET_EM](NG_KORNET_EM.md) →  
> Catégorie : **Air-to-Air BVR & Long-Range** · Fichier source : `mod/Database/weapons_tactical_30.lua`

![Rendu 3D ng_aim120cd](../renders/ng_aim120cd.png)

## Fiche Technique

| Paramètre | Valeur |
|---|---|
| **ID Interne** | `NG_SKY_SWORD_2C` |
| **CLSID Pylône** | `{NEXTGEN_SKY_SWORD_2C}` |
| **Nom Court HUD / RWR** | `TC-2C` |
| **Modèle 3D (`.edm`)** | [`ng_aim120cd.edm`](../../mod/Shapes/ng_aim120cd.edm) |
| **Calibre / Diamètre** | `0.190 m` (`190 mm`) |
| **Longueur** | `3.60 m` |
| **Masse au Lancement** | `184.0 kg` |
| **Mach Max** | `Mach 4.8` |
| **Portée Max** | `110 km` |
| **Charge Militaire** | `22.0 kg` |
| **Facteur de Charge Max (`Nr_max`)** | `40 G` |
| **Guidage / Autodirecteur** | Radar Actif / Multi-Mode / INS+GPS (`Head_Type = 2` / Croisière) |
| **Propulsion** | Single/Sustained (62.0 kg fuel, Burn: 8.5s, Isp: 250s) |
| **Résistance ECM (`ccm_k0`)** | `0.03` |
| **Temps de Vie Max** | `150 s` |

## Polaire Aérodynamique & Modèle de Vol

- **Profil utilisé** : `FM_AAM_BVR` — **AIM-120C / SD-10 Mach 0.0–5.0 Polar**
- **Détails physiques ([`polar_profiles.lua`](../../mod/Database/polar_profiles.lua))** : Supersonic medium/BVR active-missile polar (`Cx0 = 0.468 @ M0 -> 0.880 @ M1.2 -> 0.364 @ M5.0`, `Cya = 0.318..0.518`, `delta_max = 0.349 rad`).

| Mach | M0.0 | M0.8 | M1.2 | M2.0 | M3.0 | M4.0 | M5.0 |
|---|---|---|---|---|---|---|---|
| **Traînée `Cx0`** | `0.468` | `0.479` | `0.880` | `0.720` | `0.555` | `0.444` | `0.364` |

## Animations & Modèle 3D

- Corps monobloc rigide `+X Forward` sans surface mobile repliable.
