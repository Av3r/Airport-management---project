from sqlalchemy import event
from sqlalchemy.orm import Session

from models.miejsce import Miejsce


def check_max_miejsc_samolot(mapper, connection, target):
    session = Session.object_session(target)

    samolot = target.samolot
    if len(samolot.miejsca) > samolot.liczba_miejsc:
        raise ValueError(f'Maximum number of passengers ({samolot.liczba_miejsc}) reached.')

def add_events():
    event.listen(Miejsce, 'before_insert', check_max_miejsc_samolot, propagate=True)