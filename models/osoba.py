from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Osoba(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    imie = Column(String(50))
    nazwisko = Column(String(100))
    pesel = Column(String(11))
    plec = Column(String(1))
    email = Column(String(50))

    def __init__(self, imie, nazwisko, pesel, plec, email):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.plec = plec
        self.email = email

    def getOsoba(self):
        raise "Implementacja w klasach dziedziczacych"
