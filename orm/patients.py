# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean
from base import Base

class Patient(Base):
  __tablename__ = 'patients'
  id=Column(Integer, primary_key=True)
  uuid=Column('uuid', String(32))
  room=Column('room', String(32))
  released=Column('released', Boolean)


  def __init__(self, uuid, room, released):
    self.uuid = uuid
    self.room = room
    self.released = released
