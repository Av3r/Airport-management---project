import tkinter as tk
from tkinter import ttk

from models.lotnisko import Lotnisko
from views.lotnisko_add_view import LotniskoAddView

from controllers.LotniskoController import LotniskoController
from views.lotnisko_info_view import LotniskoInfoView


class LotniskoView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Lista Lotnisk")

        self.database_manager = master.database_manager

        self.controller = LotniskoController(self.database_manager)

        self.treeview = tk.ttk.Treeview(self, columns=('ID', 'Nazwa', 'Ad Miasto', 'Ad Ulica', 'Ad Numer budynku', 'Ad Kod pocztowy'), show='headings')
        self.treeview.heading('ID', text='ID', anchor=tk.W)
        self.treeview.heading('Nazwa', text='Nazwa', anchor=tk.W)
        self.treeview.heading('Ad Miasto', text='Ad Miasto', anchor=tk.W)
        self.treeview.heading('Ad Ulica', text='Ad Ulica', anchor=tk.W)
        self.treeview.heading('Ad Numer budynku', text='Ad Numer budynku', anchor=tk.W)
        self.treeview.heading('Ad Kod pocztowy', text='Ad Kod pocztowy', anchor=tk.W)
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.get_lotniska_treeview()

        add_button = tk.Button(self, text="Dodaj Lotnisko", command=self.open_lotnisko_add_view, bg="light green")
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = tk.Button(self, text='Usuń Lotnisko', command=self.delete_lotnisko)
        delete_button.pack(side=tk.LEFT, pady=10)

        get_lotniska_button = tk.Button(self, text="Sprawdź Loty", command=self.get_info_lotnisko)
        get_lotniska_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = tk.Button(self, text="Anuluj", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # Umieszczenie okna na środku ekranu
        self.geometry("+{}+{}".format((self.winfo_screenwidth() - self.winfo_reqwidth()) // 2,
                                      (self.winfo_screenheight() - self.winfo_reqheight()) // 2))

        # Centrowanie danych podczas rozszerzania okna
        for row in range(7):
            self.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

    def get_lotniska_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        lotniska = self.controller.get_lotniska()
        for lotnisko in lotniska:
            adres_miasto = lotnisko.adres.miasto if lotnisko.adres else ""
            adres_ulica = lotnisko.adres.ulica if lotnisko.adres else ""
            adres_numer_budynku = lotnisko.adres.numer_budynku if lotnisko.adres else ""
            adres_kod_pocztowy = lotnisko.adres.kod_pocztowy if lotnisko.adres else ""
            self.treeview.insert('', 'end', values=(
            lotnisko.id, lotnisko.nazwa, adres_miasto + ' ' + adres_ulica, adres_ulica, adres_numer_budynku,
            adres_kod_pocztowy))

    def open_lotnisko_add_view(self):
        LotniskoAddView(self)

    def delete_lotnisko(self):
        selected_item = self.treeview.selection()
        if selected_item:
            lotnisko_id = self.treeview.item(selected_item, 'values')[0]
            print(f"lotnisko_id : {lotnisko_id} , selected_item {selected_item}")
            session = self.database_manager.get_session()
            lotnisko = session.query(Lotnisko).get(lotnisko_id)
            if lotnisko:
                session.delete(lotnisko)
                session.commit()
                self.get_lotniska_treeview()
                session.close()

    def get_info_lotnisko(self):
        session = self.database_manager.get_session()
        selected_item = self.treeview.selection()
        if selected_item:
            selected_id = self.treeview.set(selected_item, 'ID')
            lotnisko_info = session.query(Lotnisko).filter_by(id=selected_id).first()

            LotniskoInfoView(self, lotnisko_info)
