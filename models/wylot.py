from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.osoba import Base


class Wylot(Base):
    __tablename__ = 'wylot'

    id = Column(Integer, primary_key=True)
    data_wylotu = Column(DateTime)
    data_przylotu = Column(DateTime)

    lotnisko_id = Column(Integer, ForeignKey('lotnisko.id'))
    lot_id = Column(Integer, ForeignKey('lot.id'))

    lotnisko = relationship("Lotnisko", back_populates="wyloty")
    lot = relationship("Lot", back_populates="wyloty")

    def __init__(self, data_wylotu, data_przylotu, lotnisko, lot):
        self.data_wylotu = datetime.strptime(data_wylotu, '%Y-%m-%d %H:%M:%S')
        self.data_przylotu = datetime.strptime(data_przylotu, '%Y-%m-%d %H:%M:%S')
        self.lotnisko = lotnisko
        self.lot = lot

    #@property
    # Zwraca opóźnienie wylotu - sprawdzając Planowany wylot od realnego wylotu
    def get_opoznienie(self):
        if self.lot:
            planowany_wylot = datetime.strptime(str(self.lot.data_lotu), '%Y-%m-%d %H:%M:%S')
            rzeczywisty_wylot = datetime.strptime(str(self.data_wylotu), '%Y-%m-%d %H:%M:%S')
            opoznienie = rzeczywisty_wylot - planowany_wylot
            return opoznienie.total_seconds() // 60
        else:
            return None

    # #@property
    # Oblicza ile będzie trwał caly lot
    def get_czas_wylotu(self):
        if self.lot:
            data_wylot = datetime.strptime(str(self.data_wylotu), '%Y-%m-%d %H:%M:%S')
            data_przylot = datetime.strptime(str(self.data_przylotu), '%Y-%m-%d %H:%M:%S')
            czas_lotu = data_przylot - data_wylot
            return czas_lotu
        else:
            return None