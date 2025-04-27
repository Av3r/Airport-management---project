from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models.osoba import Osoba


class Pasazer(Osoba):
    __tablename__ = 'pasazer'

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    numer_telefonu = Column(String(15))

    bilety = relationship("Bilet", back_populates="pasazer", cascade="all, delete-orphan")

    bagaze = relationship("Bagaz", back_populates="pasazer", cascade="all, delete-orphan")

    liczba_pasazerow=0

    def __init__(self, imie, nazwisko, pesel, plec, email, login, numer_telefonu=None):
        super().__init__(imie, nazwisko, pesel, plec, email)
        self.login = login
        self.numer_telefonu = numer_telefonu

        Pasazer.liczba_pasazerow += 1

    @classmethod
    def get_liczba_pasazerow(cls):
        return Pasazer.liczba_pasazerow

    def getOsoba(self):
        return f"Pasazer: {self.imie} {self.nazwisko}, numer tel: {self.numer_telefonu}"