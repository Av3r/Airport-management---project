import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from models.lot import Lot


class LotAddView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Dodaj Lot")

        self.database_manager = master.database_manager

        self.label_lot_nazwa = ttk.Label(self, text="Nazwa Lotu")
        self.entry_lot_nazwa = ttk.Entry(self)
        self.label_lot_nazwa.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_lot_nazwa.grid(row=0, column=1, padx=10, pady=5)

        self.label_lot_identyfikator = ttk.Label(self, text="Identyfikator lotu")
        self.entry_lot_identyfikator = ttk.Entry(self)
        self.label_lot_identyfikator.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_lot_identyfikator.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Data lotu:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.data_lotu_entry = DateEntry(self, width=12, borderwidth=2, date_pattern="yyyy-mm-dd")
        self.data_lotu_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Godzina lotu:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.godzina_lotu_entry = ttk.Combobox(self, values=[str(i).zfill(2) for i in range(24)], width=3)
        self.godzina_lotu_entry.grid(row=3, column=1, padx=5, pady=5)
        self.godzina_lotu_entry.set("00")

        tk.Label(self, text="Minuta:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.minuty_lotu_entry = ttk.Combobox(self, values=[str(i).zfill(2) for i in range(60)], width=3)
        self.minuty_lotu_entry.grid(row=4, column=1, padx=5, pady=5)
        self.minuty_lotu_entry.set("00")

        self.button_add = tk.Button(self, text="Dodaj Lot", command=self.add_lot, bg="light green")
        self.button_add.grid(row=5, column=0, columnspan=2, pady=10)

        self.button_cancel = tk.Button(self, text="Anuluj", command=self.destroy)
        self.button_cancel.grid(row=6, column=0, columnspan=2)

        # Skalowanie okna
        self.after(0, self.scale_window)

    def scale_window(self):
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # Umieszczenie okna na środku ekranu
        self.geometry("+{}+{}".format((self.winfo_screenwidth() - self.winfo_reqwidth()) // 2,
                                      (self.winfo_screenheight() - self.winfo_reqheight()) // 2))

        for row in range(6):
            self.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

    def add_lot(self):
        lot_name = self.entry_lot_nazwa.get()
        lot_identyfikator = self.entry_lot_identyfikator.get()
        data_lotu = self.data_lotu_entry.get_date()
        godzina_lotu = self.godzina_lotu_entry.get()
        minuta_lotu = self.minuty_lotu_entry.get()

        if lot_name and lot_identyfikator and data_lotu:
            try:
                godzina_lotu = int(godzina_lotu)
                minuta_lotu = int(minuta_lotu)
                if 0 <= godzina_lotu <= 23 and 0 <= minuta_lotu <= 59:
                    data_czas = datetime(data_lotu.year, data_lotu.month, data_lotu.day, godzina_lotu, minuta_lotu)

                    # Formatowanie daty do wstawienia jej do DataTIme
                    data_czas_lotu = data_czas.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'data wylotu str : {data_czas_lotu}')
                else:
                    raise ValueError
            except ValueError:
                print("Błąd dat")

            session = self.database_manager.get_session()
            lot_new = Lot(lot_name, lot_identyfikator, data_czas_lotu)

            try:
                session.add_all([lot_new])
                session.commit()
                self.master.get_loty_treeview()
                messagebox.showinfo("Dodano", f"Dodano nowy lot : {lot_new.nazwa_lotu}.")
                session.close()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas dodawania lotu: {str(e)}")
        else:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być uzupełnione.")
