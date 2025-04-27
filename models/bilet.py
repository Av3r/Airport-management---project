from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.osoba import Base


class Bilet(Base):
    __tablename__ = 'bilet'

    id = Column(Integer, primary_key=True, unique=True)
    cena = Column(Integer)

    miejsca = relationship("Miejsce", back_populates="bilet")

    pasazer_id = Column(Integer, ForeignKey('pasazer.id'))
    pasazer = relationship("Pasazer", back_populates='bilety')

    liczba_sprzedanych_biletow = 0

    def __init__(self, cena, pasazer):
        self.cena = cena
        self.pasazer = pasazer
        self.miejsca = []

        Bilet.liczba_sprzedanych_biletow += 1

    @classmethod
    def get_liczba_sprzedanych_biletow(cls):
        return Bilet.liczba_sprzedanych_biletow
