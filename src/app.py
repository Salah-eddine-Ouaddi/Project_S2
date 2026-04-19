import customtkinter as ctk
from tkinter import messagebox
from src.core.logic import ParkingLogic

ctk.set_appearance_mode("dark")      
ctk.set_default_color_theme("blue")


class ParkingApp(ctk.CTk):
    """Fenêtre principale de l'application Parking."""

    def __init__(self, logic: ParkingLogic):
        super().__init__()

        self._logic = logic  

        
        self.title("Gestion du Parking")
        self.geometry("700x600")
        self.resizable(False, False)

        
        self._construire_interface()

        
        self._rafraichir_liste()

    
    def _construire_interface(self):
        """Crée tous les widgets de la fenêtre."""

    
        titre = ctk.CTkLabel(self, text="🚗 Gestion du Parking", font=ctk.CTkFont(size=20, weight="bold"))
        titre.pack(pady=10)

        
        frame_saisie = ctk.CTkFrame(self)
        frame_saisie.pack(padx=20, pady=5, fill="x")

        
        ctk.CTkLabel(frame_saisie, text="Matricule :").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self._champ_matricule = ctk.CTkEntry(frame_saisie, width=150, placeholder_text="ex: 123-A-45")
        self._champ_matricule.grid(row=0, column=1, padx=10, pady=5)


        ctk.CTkLabel(frame_saisie, text="Heure entrée :").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self._champ_entree = ctk.CTkEntry(frame_saisie, width=100, placeholder_text="HH:MM")
        self._champ_entree.grid(row=0, column=3, padx=10, pady=5)

        
        ctk.CTkLabel(frame_saisie, text="Heure sortie :").grid( row=1, column=0, padx=10, pady=5, sticky="w")
        self._champ_sortie = ctk.CTkEntry(frame_saisie, width=150, placeholder_text="HH:MM")
        self._champ_sortie.grid(row=1, column=1, padx=10, pady=5)

        
        frame_boutons = ctk.CTkFrame(self)
        frame_boutons.pack(padx=20, pady=10, fill="x")

        ctk.CTkButton(frame_boutons, text="✅ Enregistrer Entrée", command=self._action_entree).grid( row=0, column=0, padx=10, pady=8)

        ctk.CTkButton(frame_boutons, text="🚪 Enregistrer Sortie", command=self._action_sortie).grid( row=0, column=1, padx=10, pady=8)

        ctk.CTkButton(frame_boutons, text="✏️ Corriger Ticket", fg_color="orange", hover_color="darkorange", command=self._action_corriger).grid( row=0, column=2, padx=10, pady=8)

        ctk.CTkButton(frame_boutons, text="🗑️ Supprimer", fg_color="red", hover_color="darkred", command=self._action_supprimer).grid( row=0, column=3, padx=10, pady=8)

        
        ctk.CTkButton(self, text="📄 Générer Rapport Journalier", command=self._action_rapport).pack(pady=5)

        
        ctk.CTkLabel(self, text="Liste des tickets :", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 2))

        self._liste = ctk.CTkTextbox(self, height=250, width=650)
        self._liste.pack(padx=20, pady=5)
        self._liste.configure(state="disabled")  # lecture seule

    
    #  Fonctions des boutons #
    def _action_entree(self):
        """Bouton Enregistrer Entrée."""
        matricule = self._champ_matricule.get().strip().upper()
        heure     = self._champ_entree.get().strip()

        
        if not matricule or not heure:         # Validation des champs vides
            messagebox.showwarning("Champs manquants", "Veuillez remplir le matricule et l'heure d'entrée.")
            return

        try:
            self._logic.enregistrer_entree(matricule, heure)
            messagebox.showinfo("Succès", f"Entrée enregistrée pour {matricule}.")
            self._vider_champs()
            self._rafraichir_liste()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _action_sortie(self):
        """Bouton Enregistrer Sortie."""
        matricule = self._champ_matricule.get().strip().upper()
        heure     = self._champ_sortie.get().strip()

        if not matricule or not heure:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le matricule et l'heure de sortie.")
            return

        try:
            self._logic.enregistrer_sortie(matricule, heure)

            # Afficher la durée calculée
            ticket = self._logic._trouver_ticket(matricule)
            duree  = self._logic.calculer_duree(ticket)
            messagebox.showinfo("Succès", f"Sortie enregistrée pour {matricule}.\n" f"Durée : {duree} minutes.")
            self._vider_champs()
            self._rafraichir_liste()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _action_corriger(self):
        """Bouton Corriger Ticket."""
        matricule      = self._champ_matricule.get().strip().upper()
        nouvelle_entree = self._champ_entree.get().strip()
        nouvelle_sortie = self._champ_sortie.get().strip()

        if not matricule:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le matricule.")
            return

        try:
            self._logic.corriger_ticket(matricule, nouvelle_entree, nouvelle_sortie)
            messagebox.showinfo("Succès", f"Ticket {matricule} corrigé.")
            self._vider_champs()
            self._rafraichir_liste()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _action_supprimer(self):
        """Bouton Supprimer."""
        matricule = self._champ_matricule.get().strip().upper()

        if not matricule:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le matricule.")
            return

        
        confirmer = messagebox.askyesno("Confirmation",  f"Supprimer le ticket de {matricule} ?")   # Demande de confirmation avant suppression
        if not confirmer:
            return

        try:
            self._logic.supprimer_ticket(matricule)
            messagebox.showinfo("Succès", f"Ticket {matricule} supprimé.")
            self._vider_champs()
            self._rafraichir_liste()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _action_rapport(self):
        """Bouton Générer Rapport."""
        chemin = self._logic.generer_rapport()
        messagebox.showinfo("Rapport généré", f"Rapport exporté dans :\n{chemin}")

    
    #  Dashboard  #

    def _rafraichir_liste(self):
        """Recharge et affiche tous les tickets dans la zone de texte."""
        tickets = self._logic.get_tickets()

        
        self._liste.configure(state="normal")
        self._liste.delete("1.0", "end")

        if not tickets:
            self._liste.insert("end", "Aucun ticket enregistré.")
        else:
            for t in tickets:
                duree = self._logic.calculer_duree(t)
                if duree is not None:
                    ligne = f"  {t.get_matricule():<15} | Entrée: {t.get_heure_entree()} | Sortie: {t.get_heure_sortie()} | {duree} min\n"
                else:
                    ligne = f"  {t.get_matricule():<15} | Entrée: {t.get_heure_entree()} | Sortie: En cours...\n"
                self._liste.insert("end", ligne)

        self._liste.configure(state="disabled")

    def _vider_champs(self):
        """Efface les champs de saisie après une action."""
        self._champ_matricule.delete(0, "end")
        self._champ_entree.delete(0, "end")
        self._champ_sortie.delete(0, "end")