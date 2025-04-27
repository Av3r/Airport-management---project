import tkinter as tk
from tkinter import ttk

from models.bilet import Bilet


class BiletyView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lista Biletów")

        self.database_manager = master.database_manager

        self.treeview = ttk.Treeview(self, columns=('ID', 'Cena', 'Liczba Miejsc', 'Pasazer'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Cena', text='Cena')
        self.treeview.heading('Liczba Miejsc', text='Liczba Miejsc')
        self.treeview.heading('Pasazer', text='Pasazer')
        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.get_bilety_treeview()

        cancel_button = tk.Button(self, text="Anuluj", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    # Uzupełnia treeview
    def get_bilety_treeview(self):
        with self.database_manager.get_session() as session:
            bilety = session.query(Bilet).all()
            for bilet in bilety:
                self.treeview.insert('', tk.END, values=(bilet.id, bilet.cena, len(bilet.miejsca), bilet.pasazer.pesel))
