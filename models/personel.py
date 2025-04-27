from sqlalchemy.orm import relationship

from models.osoba import Osoba
from sqlalchemy import Column, String, Integer, ForeignKey


class Personel(Osoba):
    __tablename__ = 'personel'

    id = Column(Integer, primary_key=True)
    stanowisko = Column(String(50))

    lotnisko_id = Column(Integer, ForeignKey('lotnisko.id'))
    lotnisko = relationship("Lotnisko", back_populates="personele")

    def __init__(self, imie, nazwisko, pesel, plec, email, stanowisko, lotnisko):
        super().__init__(imie, nazwisko, pesel, plec, email)
        self.stanowisko = stanowisko
        self.lotnisko = lotnisko

    def getOsoba(self):
        return f"Personel: {self.imie} {self.nazwisko}, pracuje jako: {self.stanowisko}, na lotnisku {self.lotnisko.nazwa}"