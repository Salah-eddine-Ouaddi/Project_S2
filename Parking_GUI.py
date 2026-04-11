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