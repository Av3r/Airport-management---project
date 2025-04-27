from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.osoba import Base


class Lot(Base):
    __tablename__ = 'lot'

    id = Column(Integer, primary_key=True)
    nazwa_lotu = Column(String(40))
    identyfikator_lotu = Column(String(10))
    data_lotu = Column(DateTime)

    pilot_id = Column(Integer, ForeignKey('pilot.id'))
    pilot = relationship("Pilot", back_populates='loty')

    wyloty = relationship('Wylot', back_populates='lot')

    samolot_id = Column(Integer, ForeignKey('samolot.id'))
    samolot = relationship("Samolot", back_populates='loty')

    bagaze = relationship("Bagaz", back_populates="lot", cascade="all, delete-orphan")

    def __init__(self, nazwa_loty, identyfikator_lotu, data_lotu, samolot=None):
        self.nazwa_lotu = nazwa_loty
        self.identyfikator_lotu = identyfikator_lotu
        self.data_lotu = datetime.strptime(data_lotu, '%Y-%m-%d %H:%M:%S')
        self.samolot = samolot
