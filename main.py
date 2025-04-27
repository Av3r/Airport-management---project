import os

from views.main_view import MainView
from controllers.database import DataBaseManager


def main():

    # Zapisywanie do pliku
    bd_name = "test11.db"
    dataBase_manager = DataBaseManager(bd_name)

    # Jeśli plik nie istnieje to go tworzę i dodaję dane
    if not os.path.exists(bd_name):
        dataBase_manager.create_tables()
        dataBase_manager.add_sample_data()

    # Przypisanie obiektu Bazy danych do Głównego Okna programu
    main_window = MainView(dataBase_manager)
    main_window.mainloop()


if __name__ == "__main__":
    main()
