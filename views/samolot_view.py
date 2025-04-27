import tkinter as tk
from tkinter import ttk

from models.samolot import Samolot


class SamolotView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lista Samolotów")

        self.database_manager = master.database_manager

        self.treeview = ttk.Treeview(self, columns=('ID', 'Marka', 'Liczba Miejsc', 'Linia Lotnicza'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Marka', text='Marka')
        self.treeview.heading('Liczba Miejsc', text='Liczba Miejsc')
        self.treeview.heading('Linia Lotnicza', text='Linia Lotnicza')
        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.get_samoloty_treeview()

        cancel_button = tk.Button(self, text="Anuluj", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def get_samoloty_treeview(self):
        with self.database_manager.get_session() as session:
            samoloty = session.query(Samolot).all()
            for samolot in samoloty:
                linia_lotnicza = samolot.linia_lotnicza.nazwa_linii if samolot.linia_lotnicza else ""
                self.treeview.insert('', tk.END, values=(samolot.id, samolot.marka, samolot.liczba_miejsc, linia_lotnicza))
