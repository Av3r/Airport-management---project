from sqlalchemy.orm import relationship

from models.osoba import Base
from sqlalchemy import Column, String, Integer


class LiniaLotnicza(Base):
    __tablename__ = 'linia_lotnicza'

    id = Column(Integer, primary_key=True)
    nazwa_linii = Column(String(50))

    piloci = relationship("Pilot", back_populates="linia_lotnicza")
    samoloty = relationship("Samolot", back_populates="linia_lotnicza")

    def __init__(self, nazwa_linii):
        self.nazwa_linii = nazwa_linii