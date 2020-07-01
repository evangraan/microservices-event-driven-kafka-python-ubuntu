# coding=utf-8

import sys

from base import Session, engine, Base
from room import Room
from cleaners import Cleaner
from porters import Porter
from medical import Medical
from waiting import Waiting
from patients import Patient

Base.metadata.create_all(engine)
session = Session()
roomA1 = Room("A1", False)
roomA2 = Room("A2", False)
roomA3 = Room("A3", False)
roomB1 = Room("B1", False)
roomB2 = Room("B2", False)
roomB3 = Room("B3", False)

session.add(roomA1)
session.add(roomA2)
session.add(roomA3)
session.add(roomB1)
session.add(roomB2)
session.add(roomB3)

sam = Cleaner("Sam", False)
joanne = Cleaner("Joanne", False)

francis = Porter("Francis", False)
michael = Porter("Michael", False)

susan = Medical("Dr. Susan", False)
percy = Medical("Nurse Percy", False)
amelia = Medical("Nurse Amelia", False)

session.add(sam)
session.add(joanne)
session.add(francis)
session.add(michael)
session.add(susan)
session.add(percy)
session.add(amelia)

waiting = Waiting('f432f42fd2342ca', 'A1', 'porter')
session.add(waiting)
session.query(Waiting).delete()

patient = Patient('f432f42fd2342ca', 'A1', False)
session.add(patient)
session.query(Patient).delete()

session.commit()
session.close()