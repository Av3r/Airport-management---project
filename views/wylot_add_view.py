import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from models.wylot import Wylot
from models.lot import Lot
from models.lotnisko import Lotnisko


class WylotAddView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.database_manager = master.database_manager

        self.title("Dodaj Wyjazd")

        self.lot_frame = tk.Frame(self)
        self.lot_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.lotnisko_frame = tk.Frame(self)
        self.lotnisko_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.data_wylotu_frame = tk.Frame(self)
        self.data_wylotu_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.data_przylotu_frame = tk.Frame(self)
        self.data_przylotu_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(self.lot_frame, text="Lot:").grid(row=0, column=0, padx=5, pady=5)
        self.lot_var = tk.StringVar()
        self.lot_listbox = ttk.Combobox(self.lot_frame, textvariable=self.lot_var)
        self.lot_listbox.grid(row=0, column=1, padx=5, pady=5)
        self.get_loty_db()

        tk.Label(self.lotnisko_frame, text="Lotnisko:").grid(row=0, column=0, padx=5, pady=5)
        self.lotnisko_var = tk.StringVar()
        self.lotnisko_listbox = ttk.Combobox(self.lotnisko_frame, textvariable=self.lotnisko_var)
        self.lotnisko_listbox.grid(row=0, column=1, padx=5, pady=5)
        self.get_lotnitka()

        #_______Data wylotu
        tk.Label(self.data_wylotu_frame, text="Data wylotu:").grid(row=0, column=0, padx=5, pady=5)
        self.data_wylotu_entry = DateEntry(self.data_wylotu_frame, width=12, borderwidth=2,
                                           date_pattern="yyyy-mm-dd")
        self.data_wylotu_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.data_wylotu_frame, text="Godzina wylotu:").grid(row=1, column=0, padx=5, pady=5)
        self.godzina_wylotu_entry = ttk.Combobox(self.data_wylotu_frame, values=[str(i).zfill(2) for i in range(24)], width=3)
        self.godzina_wylotu_entry.grid(row=1, column=1, padx=5, pady=5)
        self.godzina_wylotu_entry.set("00")

        tk.Label(self.data_wylotu_frame, text="Minuta:").grid(row=2, column=0, padx=5, pady=5)
        self.minuty_wylotu_entry = ttk.Combobox(self.data_wylotu_frame, values=[str(i).zfill(2) for i in range(60)], width=3)
        self.minuty_wylotu_entry.grid(row=2, column=1, padx=5, pady=5)
        self.minuty_wylotu_entry.set("00")

        #_______Data przylotu
        tk.Label(self.data_przylotu_frame, text="Data przylotu:").grid(row=0, column=0, padx=5, pady=5)
        self.data_przylotu_entry = DateEntry(self.data_przylotu_frame, width=12, borderwidth=2,date_pattern="yyyy-mm-dd")
        self.data_przylotu_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.data_przylotu_frame, text="Godzina przylotu:").grid(row=1, column=0, padx=5, pady=5)
        self.godzina_przylotu_entry = ttk.Combobox(self.data_przylotu_frame, values=[str(i).zfill(2) for i in range(24)], width=3)
        self.godzina_przylotu_entry.grid(row=1, column=1, padx=5, pady=5)
        self.godzina_przylotu_entry.set("00")

        tk.Label(self.data_przylotu_frame, text="Minuta:").grid(row=2, column=0, padx=5, pady=5)
        self.minuty_przylotu_entry = ttk.Combobox(self.data_przylotu_frame, values=[str(i).zfill(2) for i in range(60)], width=3)
        self.minuty_przylotu_entry.grid(row=2, column=1, padx=5, pady=5)
        self.minuty_przylotu_entry.set("00")

        add_button = tk.Button(self.button_frame, text="Dodaj", command=self.add_wylot, bg='light green')
        add_button.pack(side="left", padx=5, pady=5)

        close_button = tk.Button(self.button_frame, text="Anuluj", command=self.destroy, bg='red')
        close_button.pack(side="right", padx=5, pady=5)


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

    def get_loty_db(self):
        session = self.database_manager.get_session()
        loty = session.query(Lot).all()

        self.lot_listbox['values'] = [f"{lot.id} - {lot.nazwa_lotu}" for lot in loty]
        session.close()

    def get_lotnitka(self):
        session = self.database_manager.get_session()
        lotniska = session.query(Lotnisko).all()

        self.lotnisko_listbox['values'] = [f"{lotnisko.id} - {lotnisko.nazwa}" for lotnisko in lotniska]
        session.close()

    def add_wylot(self):
        session = self.database_manager.get_session()

        selected_lot = self.lot_listbox.get()
        selected_lotnisko = self.lotnisko_listbox.get()

        data_wylotu = self.data_wylotu_entry.get_date()
        godzina_wylotu = self.godzina_wylotu_entry.get()
        minuta_wylotu = self.minuty_wylotu_entry.get()

        data_przylotu = self.data_przylotu_entry.get_date()
        godzina_przylotu = self.godzina_przylotu_entry.get()
        minuta_przylotu = self.minuty_przylotu_entry.get()

        if selected_lot and selected_lotnisko and data_przylotu and data_wylotu:
            try:
                godzina_wylotu = int(godzina_wylotu)
                minuta_wylotu = int(minuta_wylotu)
                if 0 <= godzina_wylotu <= 23 and 0 <= minuta_wylotu <= 59:
                    data_czas = datetime(data_wylotu.year, data_wylotu.month, data_wylotu.day, godzina_wylotu,
                                         minuta_wylotu)

                    # Formatowanie daty do wstawienia jej do DataTIme
                    data_czas_wylotu = data_czas.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'data wylotu str : {data_czas_wylotu}')
                else:
                    raise ValueError

                godzina_przylotu = int(godzina_przylotu)
                minuta_przylotu = int(minuta_przylotu)

                if 0 <= godzina_przylotu <= 23 and 0 <= minuta_przylotu <= 59:
                    data_czas = datetime(data_przylotu.year, data_przylotu.month, data_przylotu.day, godzina_przylotu,
                                         minuta_przylotu)
                    # Formatowanie daty do wstawienia jej do DataTIme
                    data_czas_przylotu = data_czas.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Błąd dat")

            if data_czas_przylotu > data_czas_wylotu:
                lot_id, lot_name = selected_lot.split(' - ', 1)
                lot = session.query(Lot).filter_by(id=lot_id).first()

                lotnisko_id, lotnisko_name = selected_lotnisko.split(' - ', 1)
                lotnisko = session.query(Lotnisko).filter_by(id=lotnisko_id).first()

                wylot_new = Wylot(data_czas_wylotu, data_czas_przylotu, lotnisko, lot)

                session.add(wylot_new)
                session.commit()
                self.master.get_wyloty_treeview()
                messagebox.showinfo("Dodano",
                                    f"Dodano nowy Wylot : {wylot_new.lotnisko.nazwa} lot nazwa: {wylot_new.lot.nazwa_lotu}.")

                print(f"Nowy wyjazd : {wylot_new}")
                session.close()
                self.destroy()
            else:
                messagebox.showerror("Błąd", "Data przylotu nie może być wcześniejsza niz data wylotu")

        else:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być uzupełnione.")