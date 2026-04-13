import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
class parking:
    def __init__(self,park):
        self._park=park
        self.park.title("parking")
        self.park.geometry("")

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
import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Parking system (Entrée / Sortie)")
app.geometry("1000x600")
title = ctk.CTkLabel(app, text="Parking")
title.pack(pady=20)

# input
plate_entry = ctk.CTkEntry(app, placeholder_text="Entrée le matricule", width=250)
plate_entry.pack(pady=10)

# confirmer l'Entrée
entry_btn = ctk.CTkButton(app, text="confirmer L'Entrée", width=250, fg_color="green")
entry_btn.pack(pady=10)

# confirmer la sortie
exit_btn = ctk.CTkButton(app, text="confirmer La Sortie", width=250, fg_color="red")
exit_btn.pack(pady=10)

# Log label
log_label = ctk.CTkLabel(app, text="Log", font=ctk.CTkFont(size=14, weight="bold"))
log_label.pack(pady=(15, 0))

# Log textbox
log_box = ctk.CTkTextbox(app, width=350, height=150)
log_box.pack(pady=10)



app.mainloop()
