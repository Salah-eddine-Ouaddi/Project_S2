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
