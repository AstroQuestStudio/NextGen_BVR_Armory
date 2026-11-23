# Patriot M903 PAC-3 MSE 16-Cell (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Défense Anti-Aérienne & C-RAM** · Source : `mod/Database/units_air_defense.lua`

![Rendu 3D ng_patriot_pac3_ln](../renders/ng_patriot_pac3_ln.png)

## Fiche Unité Sol-Air

| Paramètre | Valeur |
|---|---|
| **ID Unité** | `NG_Patriot_PAC3_MSE_LN` |
| **Nom Court Carte** | `M903-PAC3` |
| **Modèle 3D (`.edm`)** | [`ng_patriot_pac3_ln.edm`](../../mod/Shapes/ng_patriot_pac3_ln.edm) |
| **Tags DCS** | `Air Defence, SAM` |
| **Portée Détection Radar** | `160 km` |
| **Portée d'Engagement** | `120 km` (min `1 km`) |
| **Plafond d'Interception** | `35 km` |
| **Vitesse Route Max** | `0 km/h` |
| **Capteur Radar (`GT.Sensors`)** | `Patriot str` |
| **Munition Embarquée** | [`NG_SAM_PAC3_MSE`](../missiles/NG_SAM_PAC3_MSE.md) (MIM-104F PAC-3 MSE HTK (NextGen)) |
| **Capacité Chargeur** | `16` coups/missiles |
| **Temps de Réaction** | `1.8 s` |
| **Cadence / Délai Tir** | `0.6 s` · Rechargement `900 s` |
| **Dépendance / Chaînage** | `{ { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }, { { "Patriot str" } }` |

## Animations & Connecteurs EDM

- `DrawArg 0` : Azimut du lanceur 360° (`CENTER_TOWER`) + connecteurs `POINT_MISSILE_01..20`
