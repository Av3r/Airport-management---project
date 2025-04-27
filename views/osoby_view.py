import tkinter as tk
from tkinter import ttk

from models.pasazer import Pasazer
from models.personel import Personel
from models.pilot import Pilot


class OsobyView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lista Osób")

        self.database_manager = master.database_manager

        self.treeview  = ttk.Treeview(self, columns=('ID', 'Imię', 'Nazwisko', 'Pesel', 'Klasa'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Imię', text='Imię')
        self.treeview.heading('Nazwisko', text='Nazwisko')
        self.treeview.heading('Pesel', text='Pesel')
        self.treeview.heading('Klasa', text='Klasa')
        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.get_osoby_treeview()

        cancel_button = tk.Button(self, text="Anuluj", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())


    # Uzupełnianie treeview
    def get_osoby_treeview(self):
        session = self.database_manager.get_session()
        pasazerowie = session.query(Pasazer).all()
        personele = session.query(Personel).all()
        piloci = session.query(Pilot).all()
        osoby = pasazerowie + personele + piloci
        for osoba in osoby:
            self.treeview.insert('', tk.END, values=(osoba.id, osoba.imie, osoba.nazwisko, osoba.pesel, osoba.__tablename__))
