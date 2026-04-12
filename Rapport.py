from datetime import datetime
import os
from pathlib import Path

class rapport:
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
    
    def nbr_vehicules(self):
        if self._enregistrements:
           nb_vl = [1 for enrg in self._enregistrements if enrg["heure_sortie"]]
           return nb_vl
        else:
            return "pas des donees"
 
    def duree_moyenne(self):
        if self._enregistrements:
            duree=0
            for enrg in self._enregistrements:
                if enrg["heure_sortie"]:
                  h1, m1 = map(int, enrg["heure_entree"].split(':'))
                  h2, m2 = map(int, enrg["heure_sortie"].split(':'))
            
                  minutes_entree = h1 * 60 + m1
                  minutes_sortie = h2 * 60 + m2
            
                  if minutes_sortie < minutes_entree:
                    minutes_sortie += 24 * 60
            
                  duree_minutes = minutes_sortie - minutes_entree
                  heures = duree_minutes / 60
                  duree+=heures
                else:
                    continue
            nb_vl = self.nbr_vehicules()
        return duree/nb_vl
    def __str__(self):
            with open(fichier_raport, 'w', encoding='utf-8') as f:
                    f.write("RAPPORT JOURNALIER DU PARKING\n")
                    f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n")
                    f.write(f"Nombre de véhicules: {self.nbr_vehicules()}\n")
                    f.write(f"Durée moyenne de stationnement: {self.duree_moyenne()} heures\n\n")
    