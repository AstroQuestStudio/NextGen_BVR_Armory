# THAAD M1120 8-Tube Exo-ABM TEL (NextGen)

> Retour : [Catalogue Général](../CATALOG.md) · [Accueil Mod](../../README.md)  
> Catégorie : **Défense Anti-Aérienne & C-RAM** · Source : `mod/Database/units_air_defense.lua`

![Rendu 3D ng_thaad_ln](../renders/ng_thaad_ln.png)

## Fiche Unité Sol-Air

| Paramètre | Valeur |
|---|---|
| **ID Unité** | `NG_THAAD_Launcher` |
| **Nom Court Carte** | `THAAD` |
| **Modèle 3D (`.edm`)** | [`ng_thaad_ln.edm`](../../mod/Shapes/ng_thaad_ln.edm) |
| **Tags DCS** | `Air Defence, SAM` |
| **Portée Détection Radar** | `240 km` |
| **Portée d'Engagement** | `200 km` (min `5 km`) |
| **Plafond d'Interception** | `150 km` |
| **Vitesse Route Max** | `65 km/h` |
| **Capteur Radar (`GT.Sensors`)** | `Patriot str` |
| **Munition Embarquée** | [`NG_SAM_THAAD`](../missiles/NG_SAM_THAAD.md) (THAAD Exo-Atmospheric KKV (NG)) |
| **Capacité Chargeur** | `8` coups/missiles |
| **Temps de Réaction** | `2.0 s` |
| **Cadence / Délai Tir** | `1.0 s` · Rechargement `1200 s` |
| **Dépendance / Chaînage** | `{ { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }, { { "Patriot str" } }` |

## Animations & Connecteurs EDM

- Connecteurs verticaux / inclinés `CENTER_TOWER`, `POINT_SIGHT_01` et `POINT_MISSILE_01..08`
