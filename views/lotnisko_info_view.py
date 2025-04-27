import tkinter as tk
from tkinter import ttk


class LotniskoInfoView(tk.Toplevel):
    def __init__(self, master, lotnisko_info):
        super().__init__(master)

        self.lotnisko_info = lotnisko_info

        self.title("Lista Lotów dla danego Lotniska")

        self.treeview = ttk.Treeview(self, columns=('ID', 'Nazwa Lotu', 'Identyfikator Lotu'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Nazwa Lotu', text='Nazwa Lotu')
        self.treeview.heading('Identyfikator Lotu', text='Identyfikator Lotu')
        self.get_treeview_lotniska()

        close_button = tk.Button(self, text="Zamknij", command=self.destroy)
        close_button.pack(pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def get_treeview_lotniska(self):
        wyloty = self.lotnisko_info.wyloty

        for wylot in wyloty:
            self.treeview.insert('', 'end', values=(wylot.lot.id, wylot.lot.nazwa_lotu, wylot.lot.identyfikator_lotu))

        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
