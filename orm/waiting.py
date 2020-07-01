# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from base import Base

class Waiting(Base):
  __tablename__ = 'waiting'
  id=Column(Integer, primary_key=True)
  patient=Column('patient', String(32))
  room=Column('room', String(32))
  waiting_for=Column('waiting_for', String(32))

  def __init__(self, patient, room, waiting_for):
    self.patient = patient
    self.room = room
    self.waiting_for = waiting_for