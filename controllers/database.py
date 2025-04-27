from sqlalchemy import create_engine, func, event, MetaData
from sqlalchemy.orm import sessionmaker


from controllers.events import add_events
from models.liniaLotnicza import LiniaLotnicza
from models.miejsce import Miejsce, KlasaMiejscaEnum
from models.osoba import Osoba, Base
from models.lotnisko import Lotnisko
from models.wylot import Wylot
from models.adres import Adres
from models.lot import Lot
from models.pasazer import Pasazer
from models.personel import Personel
from models.pilot import Pilot
from models.samolot import Samolot
from models.bilet import Bilet
from models.bagaz import Bagaz



class DataBaseManager:
    def __init__(self, db_file):
        self.database = create_engine(f'sqlite:///{db_file}')
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.database)

        event.listen(Miejsce, 'before_insert', self.check_max_miejsc_samolot, propagate=True)


        # #Tworzenie bazy danych w pamięci - w celach testowych bez tworzenia plików
        # self.database = create_engine('sqlite:///:memory:', echo=True)
        # Base.metadata.bind = self.database
        # self.Session = sessionmaker(bind=self.database)
        #
        # #add_events()
        # event.listen(Miejsce, 'before_insert', self.check_max_miejsc_samolot, propagate=True)


    # Ograniczenie na maksymalną liczbę miejsc w danym samolocie
    def check_max_miejsc_samolot(self, mapper, connection, target):
        session = self.get_session()

        samolot = target.samolot
        if len(samolot.miejsca) > samolot.liczba_miejsc:
            raise ValueError(f'Maksymalna liczba miejsc dla danego samolotu ({samolot.liczba_miejsc}) .')


    def create_tables(self):
        Base.metadata.create_all(self.database)

    def get_session(self):
        return self.Session()

    def add_sample_data(self):
        session = self.get_session()

        #____________________________LOTNISKA + ADRESY_______________
        adres_kr = Adres("Krakowska", "Krakow", "43", "44-444")
        lotnisko_kr = Lotnisko("Lotnisko Krakow", adres_kr)

        adres_oke = Adres("Warszawska", "Warszawa", "423", "22-222")
        lotnisko_oke = Lotnisko("Lotnisko Okiecie", adres_oke)

        adres_ber = Adres("Niemiecka", "Berlin", "19", "19-390")
        lotnisko_ber = Lotnisko("Lotnisko Berlin", adres_ber)

        adres_gda = Adres('Gdanska', 'Gdansk', '111', '66-666')
        lotnisko_gda = Lotnisko('Lotnisko Gdansk', adres_gda)

        adres_rze = Adres('Podkarpacka', 'Rzeszów', '88', '01-345')
        lotnisko_rze =Lotnisko('Lotnisko Rzesszów', adres_rze)

        #___________________________________LOTY___________________________
        lot_kra = Lot('Lot Kraków', 'kr123', '2024-01-30 10:30:00')
        lot_par = Lot('Lot Paryż', 'kr321', '2024-02-20 01:30:00')
        lot_ber = Lot('Lot Berlon', 'oke444', '2024-01-15 11:35:00')
        lot_gda = Lot('Lot Gdansk', 'gda112', '2024-01-16 11:35:00')
        lot_rze = Lot('Lot Rzeszów', 'rze442', '2024-01-25 12:35:00')

        #___________________________________WYLOTY_______________________________

        wylot_kr_waw = Wylot('2024-01-30  10:35:00', '2024-01-30  13:30:00', lotnisko_kr, lot_kra)
        wylot_kr_par = Wylot('2024-03-30  20:35:00', '2024-03-30  23:15:00', lotnisko_kr, lot_par)
        wylot_ber_par = Wylot('2024-02-20  10:35:00', '2024-02-20  11:15:00', lotnisko_ber, lot_par)
        wylot_gda_par = Wylot('2024-12-20  10:35:00', '2024-12-20  13:25:00', lotnisko_gda, lot_par)
        wylot_kr_ber = Wylot('2024-01-30  13:30:00', '2024-01-30  13:35:00', lotnisko_kr, lot_ber)


        session.add_all([wylot_kr_ber, wylot_ber_par, wylot_gda_par])
        session.add_all([lot_kra, wylot_kr_waw, lot_par, lot_ber, adres_ber, lotnisko_ber, lot_gda, lot_rze, wylot_kr_par])
        session.add_all([adres_kr, lotnisko_kr, adres_oke, lotnisko_oke, adres_gda, lotnisko_gda, adres_rze, lotnisko_rze])

        #___________________________________PERSONEL________________________________
        personel_kr = Personel("Jan", "Krakowski", "90909090909", "M", "jan@krak.pl", "ochroniarz", lotnisko_kr)
        personel_kr1 = Personel("Janek", "Kraki", "91234090909", "M", "janek@krak.pl", "kasjer", lotnisko_kr)

        personel_oke = Personel("Dominik", "Dominikanczyk", "44332211994", "M", "dodo@dod.pl", "ochroniarz", lotnisko_oke)

        session.add_all([personel_kr, personel_kr1, personel_oke])

        test_opoznienie = wylot_kr_waw.get_opoznienie()
        print(f"opoznienie wylotu krakow - warszawa {test_opoznienie}")

        #__________________________________PILOCI_________________________________
        pilot1 = Pilot("Eustachy", "Kruk", "10101010101", "M", "e@k.pl", "Pilot001", "2020-01-01", 20)
        pilot2 = Pilot("Sylwester", "Łasik", "90909090905", "M", " ssssyl@o2.pl", "Pilot005", "2021-02-02", 30)

        session.add_all([pilot1, pilot2])

        #---------------------___________--PASAZEROWIE---------------------________
        pasazer1 = Pasazer("Adam", "Podroznik", "1112223334", "M", "adam.p@p.pl", "login_adam")
        pasazer2 = Pasazer("Joanna", "Podrozniczka", "1332223334", "K", "asia.p@a.pl", "login_asiap", "222333444")
        pasazer3 = Pasazer("Marian", "Krab", "23423423423", "M", "krab@o.pl", "krr1","444433333")
        pasazer4 = Pasazer("Ania", "Rak" , "55443344433", "K", "a.rak@k.pl", "araka")

        session.add_all([pasazer1, pasazer2, pasazer3, pasazer4])

        #------------------------_________-Samoloty------------------____________
        #Ograniczenia na tworzeniu większej ilości miejsc niż liczba_miejsc w obiekcie samolot
        samolot1 = Samolot("Boeing", 3)
        samolot2 = Samolot("Airbus", 10)
        samolot3 = Samolot("Embraer", 5)

        lot_par.samolot = samolot2
        lot_kra.samolot = samolot1
        lot_rze.samolot = samolot3

        lot_kra.pilot = pilot1

        #___________________________________MIEJSCA__________________________
        miejsce_samolot1 = Miejsce(1, KlasaMiejscaEnum.EKO, samolot1)
        miejsce_samolot2 = Miejsce(2, KlasaMiejscaEnum.EKO, samolot1)
        miejsce_samolot3 = Miejsce(3, KlasaMiejscaEnum.EKO, samolot1)

        miejsce1_samolot2_1 = Miejsce(1, KlasaMiejscaEnum.EKO, samolot2)
        miejsce1_samolot2_2 = Miejsce(2, KlasaMiejscaEnum.BUISS, samolot2)
        miejsce1_samolot2_3 = Miejsce(3, KlasaMiejscaEnum.EKO, samolot2)

        session.add_all([miejsce_samolot1, miejsce_samolot2, miejsce_samolot3, miejsce1_samolot2_1, miejsce1_samolot2_2, miejsce1_samolot2_3])

        #___TEST BLOKADY
        # miejsce_samolot4 = Miejsce(4, KlasaMiejscaEnum.EKO, samolot1)
        # session.add(miejsce_samolot4)


        #______________________________LINIA LOTNICZA_____________________________
        linia_lotnicza_lot = LiniaLotnicza("Lot")

        pilot1.linia_lotnicza = linia_lotnicza_lot
        samolot1.linia_lotnicza = linia_lotnicza_lot

        linia_lotnicza_ryanair = LiniaLotnicza("Ryanair")
        pilot2.linia_lotnicza = linia_lotnicza_ryanair
        session.add_all([linia_lotnicza_ryanair, linia_lotnicza_lot])

        #_________________________BILETY______________________________
        bilet1_samolot1 = Bilet(120, pasazer1)
        bilet1_samolot1.miejsca.extend([miejsce_samolot1])

        bilet2_samolot1 = Bilet(250, pasazer2)
        bilet2_samolot1.miejsca.extend([miejsce_samolot2, miejsce_samolot3])

        bilet3_samolot2 = Bilet(200, pasazer3)
        bilet3_samolot2.miejsca.extend([miejsce1_samolot2_1])

        bilet4_samolot2 = Bilet(400, pasazer4)
        bilet4_samolot2.miejsca.extend([miejsce1_samolot2_2])

        session.add_all([bilet1_samolot1, bilet2_samolot1, bilet3_samolot2, bilet4_samolot2])


        #__________________________Bagaze______________________________
        bagaz1_lot_kr_pasaze1 = Bagaz(30, pasazer1, lot_kra)

        #Test ograniczenia wagi
        try:
            bagaz2_lot_kr_pasaze1 = Bagaz(30.4, pasazer1, lot_kra)
            session.add_all([bagaz2_lot_kr_pasaze1])
        except ValueError as e:
            print(f"Błąd: {e}")
        print(f"Bilet1 numer biletu: {bagaz1_lot_kr_pasaze1.numer_bagazu}")

        session.add_all([bagaz1_lot_kr_pasaze1])

        #__________________________TESTY METOD I INNYCH FUNC___________

        suma_cen = session.query(func.sum(Bilet.cena)).scalar()
        print(f'Test sumy cen biletów : {suma_cen}')

        print(f"pilot1 linia {pilot1.linia_lotnicza.nazwa_linii}")
        print(f"linia lotnicza {len(linia_lotnicza_lot.piloci)}")

        test_liczbA_lat = pilot1.get_lata_posiadanej_licencji()
        print(f"test ile lat ma eustachy licencje {test_liczbA_lat}")
        print(f"liczba stworzonych pasażerów: {Pasazer.get_liczba_pasazerow()}")
        print(f"liczba sprzedanych biletow: {Bilet.get_liczba_sprzedanych_biletow()}")
        print(f"bilet2 posiada miejsc : {len(bilet2_samolot1.miejsca)}")
        print(f"Ile jest obiektkow klasy Pasazer : {Pasazer.get_liczba_pasazerow()}")


        session.commit()
