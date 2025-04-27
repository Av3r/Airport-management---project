from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.osoba import Base


class Samolot(Base):
    __tablename__ = 'samolot'

    id = Column(Integer, primary_key=True)
    marka = Column(String(50))
    liczba_miejsc = Column(Integer)

    loty = relationship("Lot", back_populates="samolot")

    miejsca = relationship("Miejsce", back_populates="samolot", cascade="all, delete-orphan")

    linia_lotnicza_id = Column(Integer, ForeignKey('linia_lotnicza.id'))
    linia_lotnicza = relationship("LiniaLotnicza", back_populates="samoloty")

    def __init__(self, marka, liczba_miejsc):
        self.marka = marka
        self.liczba_miejsc = liczba_miejsc
