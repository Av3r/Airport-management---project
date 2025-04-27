from sqlalchemy import Integer, ForeignKey, Column, Enum
from sqlalchemy.orm import relationship

from models.osoba import Base

from enum import Enum as PythonEnum


class KlasaMiejscaEnum(PythonEnum):
    EKO = "Ekonomiczna"
    BUISS = "Biznesowa"


class Miejsce(Base):
    __tablename__ = 'miejsce'

    id = Column(Integer, primary_key=True)
    numer_miejsca = Column(Integer)
    klasa_miejsca = Column(Enum(KlasaMiejscaEnum))

    samolot = relationship("Samolot", back_populates="miejsca")
    samolot_id = Column(Integer, ForeignKey('samolot.id'))

    bilet = relationship("Bilet", back_populates="miejsca")
    bilet_id = Column(Integer, ForeignKey('bilet.id'))

    def __init__(self, numer_miejsca, klasa_miejsca, samolot):
        self.numer_miejsca = numer_miejsca
        self.klasa_miejsca = klasa_miejsca
        self.samolot = samolot
