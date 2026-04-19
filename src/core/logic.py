from pathlib import Path
from src.core.models import Ticket
from src.core.storage import ParkingStorage


class ParkingLogic:
    """Couche logique : manipule les tickets et produit les rapports."""

    def __init__(self, chemin_donnees, chemin_output):
        self._storage = ParkingStorage(chemin_donnees)
        self._tickets = self._storage.charger()  # Charger les tickets existants au démarrage
        self._output  = Path(chemin_output)
        self._output.mkdir(parents=True, exist_ok=True)

    
    #  enregistrer une entrée  #

    def enregistrer_entree(self, matricule, heure_entree):
        """Ajoute un nouveau ticket d'entrée.
        Lève ValueError si le matricule est déjà présent et sans sortie."""

        # Vérifier qu'il n'y a pas déjà un ticket ouvert pour une véhicule
        for t in self._tickets:
            if t.get_matricule() == matricule and t.get_heure_sortie() == "":
                raise ValueError(f"Le véhicule {matricule} est déjà dans le parking.")

        nouveau = Ticket(matricule, heure_entree)
        self._tickets.append(nouveau)
        self._sauvegarder()

    
    #  enregistrer une sortie  #

    def enregistrer_sortie(self, matricule, heure_sortie):
        """Enregistre l'heure de sortie d'un véhicule.
        Lève ValueError si aucune entrée n'existe pour ce matricule."""

        ticket = self._trouver_ticket_ouvert(matricule)

        if ticket is None:
            raise ValueError(f"Aucune entrée trouvée pour {matricule}.")

        # set_heure_sortie valide le format 
        ticket.set_heure_sortie(heure_sortie)
        self._sauvegarder()

    
    #  corriger un ticket  #
    
    def corriger_ticket(self, matricule, nouvelle_entree, nouvelle_sortie):
        """Modifie l'heure d'entrée et/ou de sortie d'un ticket existant."""

        ticket = self._trouver_ticket(matricule)
        if ticket is None:
            raise ValueError(f"Ticket introuvable pour {matricule}.")

        if nouvelle_entree:
            ticket.set_heure_entree(nouvelle_entree)
        if nouvelle_sortie:
            ticket.set_heure_sortie(nouvelle_sortie)

        self._sauvegarder()

    
    #  supprimer un enregistrement   #
    
    def supprimer_ticket(self, matricule):
        """Supprime le ticket correspondant au matricule."""

        ticket = self._trouver_ticket(matricule)
        if ticket is None:
            raise ValueError(f"Ticket introuvable pour {matricule}.")

        self._tickets.remove(ticket)
        self._sauvegarder()

    
    #  récupérer tous les tickets   #
    
    def get_tickets(self):
        """Retourne une copie de la liste des tickets."""
        return list(self._tickets)

    
    #  durée de stationnement   #
    
    def calculer_duree(self, ticket):
        """Calcule la durée en minutes entre l'entrée et la sortie.
        Retourne None si le ticket est encore ouvert."""

        if ticket.get_heure_sortie() == "":
            return None

        # On découpe HH:MM et on convertit en minutes 
        h_e, m_e = ticket.get_heure_entree().split(":")
        h_s, m_s = ticket.get_heure_sortie().split(":")

        entree  = int(h_e) * 60 + int(m_e)
        sortie  = int(h_s) * 60 + int(m_s)

        duree = sortie - entree

        # Cas où la sortie est le lendemain (ex: entrée 23:00, sortie 01:00)
        if duree < 0:
            duree += 24 * 60

        return duree   # en minutes

    
    #  RAPPORT : générer le rapport journalier  #
    
    def generer_rapport(self):
        """Calcule les statistiques et écrit le rapport dans output/."""

        # Séparer tickets terminés et tickets ouverts
        termines = []
        for t in self._tickets:
            if t.get_heure_sortie() != "":
                termines.append(t)

        nb_total   = len(self._tickets)
        nb_termines = len(termines)

        # Calcul de la durée moyenne
        if nb_termines > 0:
            total_minutes = 0
            for t in termines:
                total_minutes += self.calculer_duree(t)
            moyenne = total_minutes / nb_termines
        else:
            moyenne = 0

        # Écriture du rapport dans un fichier texte
        chemin_rapport = self._output / "rapport.txt"
        with open(chemin_rapport, "w", encoding="utf-8") as f:
            print("=== RAPPORT JOURNALIER DU PARKING ===", file=f)
            print(f"Véhicules enregistrés  : {nb_total}", file=f)
            print(f"Véhicules sortis        : {nb_termines}", file=f)
            print(f"Véhicules encore présents : {nb_total - nb_termines}", file=f)
            print(f"Durée moyenne           : {moyenne:.1f} minutes", file=f)
            print("", file=f)
            print("--- Détail ---", file=f)
            for t in self._tickets:
                duree = self.calculer_duree(t)
                if duree is not None:
                    ligne = f"{t.get_matricule()} | {t.get_heure_entree()} → {t.get_heure_sortie()} | {duree} min"
                else:
                    ligne = f"{t.get_matricule()} | {t.get_heure_entree()} → En cours"
                print(ligne, file=f)

        return chemin_rapport   # on retourne le chemin pour l'afficher dans l'interface CustomTkinter

    # ------------------------------------------------------------------ #
    def _trouver_ticket_ouvert(self, matricule):
        """Retourne le ticket sans heure de sortie, ou None."""
        for t in self._tickets:
            if t.get_matricule() == matricule and t.get_heure_sortie() == "":
                return t
        return None

    def _trouver_ticket(self, matricule):
        """Retourne le dernier ticket du matricule (ouvert ou fermé), ou None."""
        resultat = None
        for t in self._tickets:
            if t.get_matricule() == matricule:
                resultat = t
        return resultat

    def _sauvegarder(self):
        """Raccourci interne pour sauvegarder après chaque modification."""
        self._storage.sauvegarder(self._tickets)