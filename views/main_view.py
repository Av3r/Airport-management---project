import tkinter as tk

from sqlalchemy import func

from models.bilet import Bilet
from models.pasazer import Pasazer
from views.bilety_view import BiletyView
from views.lot_view import LotView
from views.lotnisko_view import LotniskoView
from views.osoby_view import OsobyView
from views.samolot_view import SamolotView
from views.wylot_view import WylotView


class MainView(tk.Tk):
    def __init__(self, database_manager):
        super().__init__()

        self.title("Aplikacja Lotniska")
        self.database_manager = database_manager

        self.header_label = tk.Label(self, text="Aplikacja Zarządzająca Lotniskiem", font=('Arial', 16, 'bold'))
        self.header_label.grid(pady=(10, 20), ipadx=15, ipady=5, columnspan=1 )#, anchor="center")

        self.views_label = tk.Label(self, text="Dostępne widoki", font=('Arial', 14, 'bold'), anchor="nw")
        self.views_label.grid(row=1, column=0, pady=(0, 10))

        # Numerowanie poszczególnych wierszy w przypadku dodania nowego okna
        num_rows=2

        # Listy z opcjami do poszczególnych okien dla wybranych przypadków
        self.option_label_lotniska = tk.Label(self, text="Lista wszystkich lotnisk z adresami:")
        self.option_label_lotniska.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_lotniska = tk.Button(self, text="Pokaż Lotniska", command=self.open_lotnisko_view, width=25)
        self.option_button_lotniska.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        self.option_label_lot = tk.Label(self, text="Lista wszystkich Lotów:")  # , anchor="w"
        self.option_label_lot.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_lot = tk.Button(self, text="Pokaż Loty", command=self.open_lot_view, width=25)
        self.option_button_lot.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        self.option_label_wylot = tk.Label(self, text="Lista wszystkich Wylotów:")
        self.option_label_wylot.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_wylot = tk.Button(self, text="Pokaż Wyloty", command=self.open_wylot_view, width=25, bg="blue", fg="white")
        self.option_button_wylot.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        self.option_label_osoby = tk.Label(self, text="Lista wszystkich Pasażerów:")
        self.option_label_osoby.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_osoby = tk.Button(self, text="Pokaż Osoby", command=self.open_osoby_view, width=25)
        self.option_button_osoby.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        self.option_label_samolot = tk.Label(self, text="Lista wszystkich Samolotów:")
        self.option_label_samolot.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_samolot = tk.Button(self, text="Pokaż Samoloty", command=self.open_samolot_view, width=25)
        self.option_button_samolot.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        self.option_label_bilety = tk.Label(self, text="Lista wszystkich Biletów:")
        self.option_label_bilety.grid(row=num_rows, column=0, padx=(10, 10), pady=5, sticky="w")

        self.option_button_bilety = tk.Button(self, text="Pokaż Bilety", command=self.open_bilety_view, width=25)
        self.option_button_bilety.grid(row=num_rows, column=1, pady=5, padx=5)

        num_rows += 1

        # Podsumowanie danych umieszczanych w DB - wykorzystanie metod
        self.summary_label = tk.Label(self, text="Podsumowanie", font=('Arial', 14, 'bold'))
        self.summary_label.grid(row=num_rows, column=0, pady=(20, 10))

        num_rows += 1

        self.summary_label_l_pasazerow = tk.Label(self, text="Ile jest Pasażerów w bazie:", anchor="w")
        self.summary_label_l_pasazerow.grid(row=num_rows, column=0, sticky="w", padx=(10, 10), pady=5)

        self.summary_value_l_pasazerow = tk.Label(self, text=str(Pasazer.get_liczba_pasazerow()), anchor="e")
        self.summary_value_l_pasazerow.grid(row=num_rows, column=1, sticky="e", padx=(10, 30), pady=5)

        num_rows += 1

        self.summary_label_ceny_biletow = tk.Label(self, text="Suma zarobionych pieniędzy z biletów:", anchor="w")
        self.summary_label_ceny_biletow.grid(row=num_rows, column=0, sticky="w", padx=(10, 10), pady=5)

        self.summary_value_ceny_biletow = tk.Label(self, text=str(''), anchor="e")
        self.summary_value_ceny_biletow.grid(row=num_rows, column=1, sticky="e", padx=(10, 30), pady=5)
        self.get_cena_biletow()


        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.geometry("+{}+{}".format((self.winfo_screenwidth() - self.winfo_reqwidth()) // 2,
                                      (self.winfo_screenheight() - self.winfo_reqheight()) // 2))

        for row in range(9):
            self.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

    def open_lotnisko_view(self):
        LotniskoView(self)

    def open_lot_view(self):
        LotView(self)

    def open_wylot_view(self):
        WylotView(self)

    def open_add_car_view(self):
        LotView(self)

    def open_samolot_view(self):
        SamolotView(self)

    def open_osoby_view(self):
        OsobyView(self)

    def open_bilety_view(self):
        BiletyView(self)

    # Zwraca Ceny wszystkich biletów w oknie podsumowania
    def get_cena_biletow(self):
        session = self.database_manager.get_session()
        suma_cen = session.query(func.sum(Bilet.cena)).scalar()
        self.summary_value_ceny_biletow.config(text=f'{suma_cen} PLN')
