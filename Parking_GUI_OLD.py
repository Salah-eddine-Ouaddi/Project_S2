from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

class parking:
    def __init__(self, park):
        self.park = park
        self.park.title("Parking system (Entrée / Sortie)")
        self.park.geometry("1000x600")
        self.park.configure(bg='black')
        self.vehicules_presents = {}

    
        self.title = tk.Label(self.park, text="Parking", font=("Arial", 24, "bold"), fg="white", bg="black")
        self.title.pack(pady=20)

        self.plate_entry = tk.Entry(self.park, font=("Arial", 14), width=30, justify="center")
        self.plate_entry.insert(0, "Entrée le matricule")
        self.plate_entry.bind('<FocusIn>', self.on_entry_click)
        self.plate_entry.pack(pady=10)

        btn_frame = tk.Frame(self.park, bg="black")
        btn_frame.pack(pady=10)

        self.entry_btn = tk.Button(btn_frame, text="confirmer L'Entrée", bg="#10B981", fg="white", 
                                   font=("Arial", 12, "bold"), width=20, height=2, command=self.enregistrer_entree)
        self.entry_btn.pack(side=tk.LEFT, padx=20)

        self.exit_btn = tk.Button(btn_frame, text="confirmer La Sortie", bg="#EF4444", fg="white", 
                                  font=("Arial", 12, "bold"), width=20, height=2, command=self.enregistrer_sortie)
        self.exit_btn.pack(side=tk.LEFT, padx=20)

        self.log_label = tk.Label(self.park, text="Log", font=("Arial", 16, "bold"), fg="white", bg="black")
        self.log_label.pack(pady=(20, 5))

        self.log_box = scrolledtext.ScrolledText(self.park, width=60, height=12, font=("Consolas", 11),
                                                bg="#1f1f1f", fg="white", insertbackground="white")
        self.log_box.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)

    def on_entry_click(self, event):
        self.plate_entry.delete(0, tk.END)
        self.plate_entry.config(fg="black")

    def calculer_duree(self, heure_entree, heure_sortie):
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

    def enregistrer_entree(self):
        matricule = self.plate_entry.get().upper().strip()
        if matricule and matricule != "ENTRÉE LE MATRICULE":
            heure_actuelle = datetime.now().strftime("%H:%M")
            self.vehicules_presents[matricule] = heure_actuelle
            self.log_box.insert(tk.END, f"📥 Entrée: {matricule} à {heure_actuelle}\n")
            self.plate_entry.delete(0, tk.END)
        else:
            self.log_box.insert(tk.END, "⚠️ Erreur: Entrez un matricule valide !\n")
        self.log_box.see(tk.END)

    def enregistrer_sortie(self):
        matricule = self.plate_entry.get().upper().strip()
        if matricule and matricule != "ENTRÉE LE MATRICULE":
            if matricule in self.vehicules_presents:
                heure_entree = self.vehicules_presents[matricule]
                heure_sortie = datetime.now().strftime("%H:%M")
                duree = self.calculer_duree(heure_entree, heure_sortie)
                self.log_box.insert(tk.END, f"📤 Sortie: {matricule} | Durée: {duree}h\n")
                del self.vehicules_presents[matricule]
                self.plate_entry.delete(0, tk.END)
            else:
                self.log_box.insert(tk.END, f"❓ {matricule} n'est pas dans le parking.\n")
        else:
            self.log_box.insert(tk.END, "⚠️ Erreur: Entrez un matricule valide !\n")
        self.log_box.see(tk.END)

if __name__ == "__main__":
    app = tk.Tk()
    parking_app = parking(app)
    app.mainloop()

