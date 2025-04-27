from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
import uuid

from models.osoba import Base


class Bagaz(Base):
    __tablename__ = 'bagaz'

    id = Column(Integer, primary_key=True)
    waga = Column(Float)
    numer_bagazu = Column(String(10), default=str(uuid.uuid4()), unique=True)

    pasazer = relationship("Pasazer", back_populates="bagaze")
    pasazer_id = Column(Integer, ForeignKey('pasazer.id'))

    lot = relationship("Lot", back_populates="bagaze")
    lot_id = Column(Integer, ForeignKey('lot.id'))

    def __init__(self, waga, pasazer, lot):
        if waga > 30:
            raise ValueError("Waga powyzej 30 kg")
        self.waga = waga
        self.numer_bagazu = str(uuid.uuid4())
        self.pasazer = pasazer
        self.lot = lot
