# SAMP/T Aster 30 B1NT 8-Cell VLS (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Défense Anti-Aérienne & C-RAM** · Source : `mod/Database/units_air_defense.lua`

![Rendu 3D ng_sampt_aster30](../renders/ng_sampt_aster30.png)

## Fiche Unité Sol-Air

| Paramètre | Valeur |
|---|---|
| **ID Unité** | `NG_SAMPT_Aster30_Launcher` |
| **Nom Court Carte** | `SAMP/T` |
| **Modèle 3D (`.edm`)** | [`ng_sampt_aster30.edm`](../../mod/Shapes/ng_sampt_aster30.edm) |
| **Tags DCS** | `Air Defence, SAM` |
| **Portée Détection Radar** | `180 km` |
| **Portée d'Engagement** | `150 km` (min `1 km`) |
| **Plafond d'Interception** | `30 km` |
| **Vitesse Route Max** | `70 km/h` |
| **Capteur Radar (`GT.Sensors`)** | `Patriot str` |
| **Munition Embarquée** | [`NG_SAM_ASTER30`](../missiles/NG_SAM_ASTER30.md) (MBDA Aster 30 B1NT ABM (NextGen)) |
| **Capacité Chargeur** | `8` coups/missiles |
| **Temps de Réaction** | `1.5 s` |
| **Cadence / Délai Tir** | `0.7 s` · Rechargement `600 s` |
| **Dépendance / Chaînage** | `{ { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }` |

## Animations & Connecteurs EDM

- Connecteurs verticaux / inclinés `CENTER_TOWER`, `POINT_SIGHT_01` et `POINT_MISSILE_01..08`
