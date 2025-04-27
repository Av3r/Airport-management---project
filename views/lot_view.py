import tkinter as tk
from tkinter import ttk

from models.lot import Lot
from views.lot_add_view import LotAddView
from views.lot_info_view import LotInfoView


class LotView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lista Lotów")

        self.database_manager = master.database_manager

        self.treeview  = ttk.Treeview(self, columns=('ID', 'Nazwa Lotu', 'Marka Samolotu'), show='headings')
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Nazwa Lotu', text='Nazwa Lotu')
        self.treeview.heading('Marka Samolotu', text='Marka Samolotu')
        self.treeview.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.get_loty_treeview()

        add_button = tk.Button(self, text="Dodaj Nowy", command=self.open_lot_add_view)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        get_lotniska_button = tk.Button(self, text="Sprawdź lotniska", command=self.get_info_lot)
        get_lotniska_button.pack(side=tk.LEFT, padx=10, pady=10)

        close_button = tk.Button(self, text="Anuluj", command=self.destroy)
        close_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # Umieszczenie okna na środku ekranu
        self.geometry("+{}+{}".format((self.winfo_screenwidth() - self.winfo_reqwidth()) // 2,
                                      (self.winfo_screenheight() - self.winfo_reqheight()) // 2))

        # Centrowanie danych podczas rozszerzania okna
        for row in range(4):
            self.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

    def open_lot_add_view(self):
        LotAddView(self)

    # Uzupełnianie treeview
    def get_loty_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        with self.database_manager.get_session() as session:
            loty = session.query(Lot).all()
            for lot in loty:
                marka_samolotu = lot.samolot.marka if lot.samolot and lot.samolot.marka else "brak"
                self.treeview.insert('', tk.END, values=(lot.id, lot.nazwa_lotu, marka_samolotu))


    def get_info_lot(self):
        session = self.database_manager.get_session()
        selected_item = self.treeview.selection()
        if selected_item:
            selected_id = self.treeview.set(selected_item, 'ID')
            lot_info = session.query(Lot).filter_by(id=selected_id).first()
            print(f'lotnisko o nazwie: {lot_info}, selected item {selected_item} selected id {selected_id}')

            if hasattr(lot_info, 'wyloty'):
                # Pobieramy wyjazdy z relacji
                wyloty = lot_info.wyloty
                print("wyloty z tego lotu:")
                for wylot in wyloty:
                    print(f'- lotnisko nazwa: {wylot.lotnisko.nazwa}')

            LotInfoView(self, lot_info)
