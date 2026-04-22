

class Ticket:
    """Représente un enregistrement de stationnement pour un véhicule."""

    def __init__(self, matricule, heure_entree, heure_sortie=""):
        if not Ticket._valider_matricule(matricule):
            raise ValueError(
                f"Format de matricule invalide : '{matricule}'. "
                f"Attendu : NNN-L-NN (ex: 123-A-45)"
            )
        if not Ticket._valider_heure(heure_entree):
            raise ValueError(f"Format d'heure invalide : '{heure_entree}'. Attendu HH:MM")
    
        self._matricule    = matricule
        self._heure_entree = heure_entree
        self._heure_sortie = heure_sortie

    #  Getters   #

    def get_matricule(self):
        return self._matricule

    def get_heure_entree(self):
        return self._heure_entree

    def get_heure_sortie(self):
        return self._heure_sortie

    
    #  Setters avec validation    #
    
    def set_heure_sortie(self, heure):
        if not Ticket._valider_heure(heure):
            raise ValueError(f"Format d'heure invalide : '{heure}'. Attendu HH:MM")
        self._heure_sortie = heure

    def set_heure_entree(self, heure):
        if not Ticket._valider_heure(heure):
            raise ValueError(f"Format d'heure invalide : '{heure}'. Attendu HH:MM")
        self._heure_entree = heure

    
    #  Fonctions de validation   #
    


    def _valider_matricule(matricule):
        """Retourne True si le matricule est au format NNN-L-NN.
        Exemple valide : 123-A-45"""
        parties = matricule.split("-")

        # Avoir exactement 3 parties : ['123', 'A', '45']
        if len(parties) != 3:
            return False

        chiffres_debut, lettre, chiffres_fin = parties

        if not chiffres_debut.isdigit() or len(chiffres_debut) != 3:
            return False

        if not lettre.isalpha() or len(lettre) != 1:
            return False

        if not chiffres_fin.isdigit() or len(chiffres_fin) != 2:
            return False

        return True

    def _valider_heure(heure):
        """Retourne True si l'heure est au format HH:MM, False sinon."""
        parties = heure.split(":")
        if len(parties) != 2:
            return False
        h, m = parties
        if not h.isdigit() or not m.isdigit():
            return False
        if not (0 <= int(h) <= 23) or not (0 <= int(m) <= 59):
            return False
        return True

    
    #  Affichage  #
    
    def __str__(self):
        sortie = self._heure_sortie if self._heure_sortie else "En cours"
        return f"Ticket({self._matricule} | Entrée: {self._heure_entree} | Sortie: {sortie})"

    
    #  JSON   #
    
    def to_dict(self):
        return {
            "matricule"    : self._matricule,
            "heure_entree" : self._heure_entree,
            "heure_sortie" : self._heure_sortie
        }


    def from_dict(d):
        return Ticket(
            d["matricule"],
            d["heure_entree"],
            d.get("heure_sortie", "")
        )
