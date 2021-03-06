# coding=utf-8

from sqlalchemy import Column, Integer, String, Boolean
from base import Base

class Porter(Base):
  __tablename__ = 'porters'
  id=Column(Integer, primary_key=True)
  name=Column('name', String(32))
  occupied=Column('occupied', Boolean)


  def __init__(self, name, occupied):
    self.name = name
    self.occupied = occupied