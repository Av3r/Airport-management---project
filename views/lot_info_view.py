import tkinter as tk
from tkinter import ttk


class LotInfoView(tk.Toplevel):
    def __init__(self, master, lot_info):
        super().__init__(master)

        self.lot_info = lot_info

        self.title("Lista Lotnisk dla danego Lotu")

        self.treeview = ttk.Treeview(self, columns=('ID', 'Nazwa', 'Adres Miasto'),  show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Nazwa', text='Nazwa')
        self.treeview.heading('Adres Miasto', text='Adres Miasto')
        self.get_treeview_lotniska()

        close_button = tk.Button(self, text="Zamknij", command=self.destroy)
        close_button.pack(pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    # Uzupełnienie treeview
    def get_treeview_lotniska(self):
        wyloty = self.lot_info.wyloty
        for wylot in wyloty:
            self.treeview.insert('', 'end', values=(wylot.lotnisko.id, wylot.lotnisko.nazwa, wylot.lotnisko.adres.miasto))

        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)