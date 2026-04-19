# 🚗 Gestion du Parking 🅿️

**Module** : Programmation Python 2  
**Filière** : IA-2 — Faculté des Sciences d'Agadir (Université Ibn Zohr)  
**Année universitaire** : 2025–2026  

**Membres du groupe** :
- [Kounkour Omar] — Team Leader
- [Ouaddi Salah eddine]
- [Alhyane Mohamed]

---

## Description

Application de gestion d'un parking permettant d'enregistrer les entrées et sorties de véhicules, de calculer la durée de stationnement et de générer un rapport journalier.

---

## Installation

### Prérequis
- Python 3.9+ installé sur votre machine
- Le module customTkinter

### Installer les dépendances

```bash
pip install customtkinter
```
---

## Lancement

```bash
# Depuis la racine du projet
python main.py
```

> Le fichier `data/parking.json` est créé automatiquement au premier lancement s'il est absent.

---

## Format des données
Les données sont stockées dans `data/parking.json`.  
Chaque enregistrement suit ce format :

```json
[
    {
        "matricule"    : "123-A-45",
        "heure_entree" : "08:30",
        "heure_sortie" : "10:15"
    },
    {
        "matricule"    : "456-B-78",
        "heure_entree" : "09:00",
        "heure_sortie" : ""
    }
]
```

### Règles de format
| Champ          | Format attendu|    Exemple      |
|----------------|---------------|-----------------|
| `matricule`    |   NNN-L-NN    |    `123-A-45`   |
| `heure_entree` |    HH:MM      |     `08:30`     |
| `heure_sortie` | HH:MM ou vide | `10:15` ou `""` |

---

## Fonctionnalités

- ✅ **Enregistrer une entrée** : ajoute un nouveau véhicule
- ✅ **Enregistrer une sortie** : ferme le ticket et calcule la durée
- ✅ **Corriger un ticket** : modifie l'heure d'entrée ou de sortie
- ✅ **Supprimer un enregistrement** : supprime un ticket avec confirmation
- ✅ **Rapport journalier** : exporté automatiquement dans `output/rapport.txt`
- ✅ **Persistance** : les données sont conservées après fermeture

---

## Gestion des erreurs

|           Erreur                  |           Comportement                 |
|-----------------------------------|----------------------------------------|
| Matricule invalide (`ABCDEFG`)    | Message d'erreur, saisie refusée       |
| Format d'heure invalide (`99:99`) | Message d'erreur, saisie refusée       |
| Sortie sans entrée                | Message d'erreur explicite             |
| Véhicule déjà présent             | Message d'erreur explicite             |
| Fichier JSON absent               | Démarrage à vide, création automatique |
| Fichier JSON corrompu             | Message clair, démarrage à vide        |

---

## Structure du projet
mon_projet/
├── main.py          ← point d'entrée
├── src/
│   ├── app.py       ← interface customTkinter
│   └── core/
│       ├── models.py   ← classe Ticket
│       ├── storage.py  ← lecture/écriture JSON
│       └── logic.py    ← calculs (durée, rapport)
├── data/
│   └── parking.json
├── output/
│   └── rapport.txt
└── README.md

---


## Rapport généré

Le rapport est exporté dans `output/rapport.txt` et contient :
- Nombre total de véhicules enregistrés
- Nombre de véhicules sortis
- Nombre de véhicules encore présents
- Durée moyenne de stationnement
- Détail ligne par ligne de tous les tickets