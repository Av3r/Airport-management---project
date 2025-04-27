from datetime import datetime

from sqlalchemy.orm import relationship

from models.osoba import Osoba
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date


class Pilot(Osoba):
    __tablename__ = 'pilot'

    id = Column(Integer, primary_key=True)
    licencja = Column(String(20))
    data_zdania_licencji = Column(Date)
    liczba_godzin_lotu = Column(Float)

    loty = relationship("Lot", back_populates="pilot")

    linia_lotnicza_id = Column(Integer, ForeignKey('linia_lotnicza.id'))
    linia_lotnicza = relationship("LiniaLotnicza", back_populates="piloci")

    def __init__(self, imie, nazwisko, pesel, plec, email, licencja, data_zdania_licencji, liczba_godzin_lotu):
        super().__init__(imie, nazwisko, pesel, plec, email)
        self.licencja = licencja
        self.data_zdania_licencji = datetime.strptime(data_zdania_licencji, '%Y-%m-%d').date()
        self.liczba_godzin_lotu = liczba_godzin_lotu

    # Obliczanie ile lat posiada Pilot Licencje
    def get_lata_posiadanej_licencji(self):
        if self.data_zdania_licencji:
            today = datetime.now().date()
            lata_posiadanej_licendji = today.year - self.data_zdania_licencji.year

            return lata_posiadanej_licendji
        else:
            return None
