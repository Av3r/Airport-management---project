from sqlalchemy import Column, Integer, String
from models.osoba import Base


class Adres(Base):
    __tablename__ = 'adres'

    id = Column(Integer, primary_key=True)
    ulica = Column(String(50), nullable=False)
    miasto = Column(String(50), nullable=False)
    numer_budynku = Column(String(50), nullable=False)
    kod_pocztowy = Column(String(50), nullable=False)

    def __init__(self, ulica, miasto, numer_budynku, kod_pocztowy):
        self.ulica = ulica
        self.miasto = miasto
        self.numer_budynku = numer_budynku
        self.kod_pocztowy = kod_pocztowy
