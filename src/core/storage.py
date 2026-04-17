import os
from pathlib import Path

fichier="input.txt"

class storage:
  def __init__(self,fichier):
        self._fichier_donnees=fichier
        self._enregistrements = self.charger_donnees()
  def charger_donnees(self):
        enregistrements = []
        if os.path.exists(self._fichier_donnees):
            try:
                with open(self.fichier_donnees, 'r', encoding='utf-8') as f:
                    for ligne in f:
                        ligne = ligne.strip()
                        if ligne:
                            try:
                                matricule, heure_entree, heure_sortie = ligne.split(',')
                                enregistrements.append({
                                    "matricule": matricule,
                                    "heure_entree": heure_entree,
                                    #si heure de sortie n est existe pas 
                                    "heure_sortie": heure_sortie if heure_sortie != "None" else None 
                                })
                            except ValueError:
                                continue
            except Exception as e:
                    print(f"Erreur du chargement: {e}")
                    raise
        return enregistrements