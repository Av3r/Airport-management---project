import tkinter as tk
from tkinter import ttk, messagebox

from models.lotnisko import Lotnisko
from models.adres import Adres


class LotniskoAddView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Dodaj Lotnisko i Adres")

        self.database_manager = master.database_manager

        self.label_lotnisko_nazwa = tk.Label(self, text="Nazwa Lotniska:")
        self.entry_lotnisko_nazwa = tk.Entry(self)
        self.label_lotnisko_nazwa.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_lotnisko_nazwa.grid(row=0, column=1, padx=10, pady=5)

        self.label_adres_miasto = tk.Label(self, text="Adres - miasto")
        self.entry_adres_miasto = tk.Entry(self)
        self.label_adres_miasto.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_adres_miasto.grid(row=1, column=1, padx=10, pady=5)

        self.label_adres_ulica = tk.Label(self, text="Adres - ulica:")
        self.entry_adres_ulica = tk.Entry(self)
        self.label_adres_ulica.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_adres_ulica.grid(row=2, column=1, padx=10, pady=5)

        self.label_adres_numer_budynku = tk.Label(self, text="Adres - numer budynku:")
        self.entry_adres_numer_budynku = tk.Entry(self)
        self.label_adres_numer_budynku.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_adres_numer_budynku.grid(row=3, column=1, padx=10, pady=5)

        self.label_adres_kod_pocztowy = tk.Label(self, text="Adres - kod pocztowy:")
        self.entry_adres_kod_pocztowy = tk.Entry(self)
        self.label_adres_kod_pocztowy.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_adres_kod_pocztowy.grid(row=4, column=1, padx=10, pady=5)

        self.button_add = tk.Button(self, text="Dodaj Lotnisko", command=self.add_lotnisko, bg="light green")
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

    def add_lotnisko(self):
        lotnisko_name = self.entry_lotnisko_nazwa.get()
        adres_miasto = self.entry_adres_miasto.get()
        adres_ulica = self.entry_adres_ulica.get()
        adres_numer_budynku = self.entry_adres_numer_budynku.get()
        adres_kod_pocztowy = self.entry_adres_kod_pocztowy.get()

        if lotnisko_name and adres_miasto and adres_ulica and adres_numer_budynku and adres_kod_pocztowy:
            session = self.database_manager.get_session()
            adres_new = Adres(adres_ulica, adres_miasto, adres_numer_budynku, adres_kod_pocztowy)
            lotnisko_new = Lotnisko(lotnisko_name, adres_new)
            try:
                session.add_all([adres_new, lotnisko_new])
                session.commit()
                self.master.get_lotniska_treeview()
                messagebox.showinfo("Dodano", f"Dodano nowe lotnisko : {lotnisko_new.nazwa}.")
                self.destroy()
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas dodawania lotniska: {str(e)}")
        else:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być uzupełnione.")