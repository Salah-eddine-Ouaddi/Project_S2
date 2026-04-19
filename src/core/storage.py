

import json
from pathlib import Path
from src.core.models import Ticket

class ParkingStorage:
    """Gère la persistance des tickets dans un fichier JSON."""

    def __init__(self, chemin_fichier):
        #un chemin robuste
        self._chemin = Path(chemin_fichier)

        self._chemin.parent.mkdir(parents=True, exist_ok=True)

    
    #  Chargement           #
    def charger(self):
        """Lit le fichier JSON et retourne une liste de Ticket.
        Retourne une liste vide si le fichier est absent ou corrompu."""

        # si le fichier n'existe pas → démarre à vide
        if not self._chemin.exists():
            return []

        try:
            with open(self._chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)

            # On reconstruit chaque Ticket depuis son dictionnaire
            tickets = []
            for d in donnees:
                tickets.append(Ticket.from_dict(d))
            return tickets

        except json.JSONDecodeError:
            # si le fichier est corrompu → message d'erreur
            print("[ERREUR] Fichier JSON corrompu. Démarrage à vide.")
            return []

    
    #  Sauvegarde   #
    
    def sauvegarder(self, tickets):
        """Écrit la liste de Ticket dans le fichier JSON."""

        # convertir chaque Ticket en dictionnaire
        donnees = []
        for ticket in tickets:
            donnees.append(ticket.to_dict())

        with open(self._chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=4)