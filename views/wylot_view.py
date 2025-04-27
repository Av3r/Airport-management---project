import tkinter as tk
from tkinter import ttk
from models.wylot import Wylot
from views.wylot_add_view import WylotAddView


class WylotView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Wyloty")

        self.database_manager = master.database_manager

        self.header_label = tk.Label(self, text="Wyloty", font=('Arial', 16, 'bold'))
        self.header_label.pack(pady=(10, 20), ipadx=15, ipady=5)

        self.tree = ttk.Treeview(self, columns=('ID', 'Nazwa Lotu', 'Nazwa Lotniska', 'Data Wylotu', 'Data Przylotu', 'Czas Lotu' ), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nazwa Lotu', text='Nazwa Lotu')
        self.tree.heading('Nazwa Lotniska', text='Nazwa Lotniska')
        self.tree.heading('Data Wylotu', text='Data Wylotu')
        self.tree.heading('Data Przylotu', text='Data Przylotu')
        self.tree.heading('Czas Lotu', text='Czas Lotu')
        self.tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.get_wyloty_treeview()

        add_button = tk.Button(self, text="Dodaj Wylot", command=self.open_wylot_add_view, bg='light green')
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        close_button = tk.Button(self, text="Anuluj", command=self.destroy, bg='red')
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

    def get_wyloty_treeview(self):
        self.tree.delete(*self.tree.get_children())
        session = self.database_manager.get_session()
        wyloty = session.query(Wylot).all()
        #print("get_wyloty_treeview ")
        for wylot in wyloty:
            self.tree.insert('', 'end', values=(wylot.id, wylot.lot.nazwa_lotu, wylot.lotnisko.nazwa, wylot.data_wylotu, wylot.data_przylotu, wylot.get_czas_wylotu()))

    def open_wylot_add_view(self):
        WylotAddView(self)

