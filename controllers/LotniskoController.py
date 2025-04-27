from models.lotnisko import Lotnisko
from models.adres import Adres


class LotniskoController:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def get_lotniska(self):
        return self.database_manager.get_session().query(Lotnisko).all()

    def add_lotnisko(self, nazwa, ulica, miasto, numer_budynku, kod_pocztowy):
        session = self.database_manager.get_session()
        adres_new = Adres(ulica, miasto, numer_budynku, kod_pocztowy)
        lotnisko_new = Lotnisko(nazwa, adres_new)
        session.add_all([adres_new, lotnisko_new])
        session.commit()

    def delete_lotnisko(self, lotnisko_id):
        session = self.database_manager.get_session()
        lotnisko = session.query(Lotnisko).get(lotnisko_id)
        if lotnisko:
            session.delete(lotnisko)
            session.commit()
