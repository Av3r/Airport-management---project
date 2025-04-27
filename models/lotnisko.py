from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from models.osoba import Base


class Lotnisko(Base):
    __tablename__ = 'lotnisko'

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    adres_id = Column(Integer, ForeignKey('adres.id'), unique=True)
    adres = relationship('Adres', uselist=False, cascade="all, delete")

    personele = relationship("Personel", back_populates="lotnisko")

    wyloty = relationship('Wylot', back_populates='lotnisko')

    def __init__(self, nazwa, adres):
        self.nazwa = nazwa
        self.adres = adres


    @validates('adres')
    def validate_adres(self, key, value):
        if value is None:
            raise ValueError("Lotnisko musi posiadać adres")
        return value
