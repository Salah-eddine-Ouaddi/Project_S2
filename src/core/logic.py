from .storage import storage
from datetime import datetime
import os

fichier_raport="rapport.txt"
class logique:
    def claculer_duree(self,heure_entree,heure_sortie):
        if not heure_sortie:
            return "en cours"
        try:
            h1, m1 = map(int, heure_entree.split(':'))
            h2, m2 = map(int, heure_sortie.split(':'))
            
            minutes_entree = h1 * 60 + m1
            minutes_sortie = h2 * 60 + m2
            
            if minutes_sortie < minutes_entree:
                minutes_sortie += 24 * 60
            
            duree_minutes = minutes_sortie - minutes_entree
            heures = duree_minutes / 60
            return f"{heures:.2f}"
        except:
            return "Erreur!!"
    
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
    
    def est_valide(self,matricul):
        if self._enregistrements:
            for enrg in self._enregistrements:
                if matricul==enrg["matricule"] and not enrg["heure_sortie"]:
                    raise (f"erreur cette matricule {matricul} est deja existe")
    def __str__(self):
            with open(fichier_raport, 'w', encoding='utf-8') as f:
                    f.write("RAPPORT JOURNALIER DU PARKING\n")
                    f.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}\n")
                    f.write(f"Nombre de véhicules: {self.nbr_vehicules()}\n")
                    f.write(f"Durée moyenne de stationnement: {self.duree_moyenne()} heures\n\n")