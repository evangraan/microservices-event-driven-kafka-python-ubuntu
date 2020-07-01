# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://kafka:R!Z::x4Q7XrvTBC~@192.168.1.230:5432/kafka')
Session = sessionmaker(bind=engine)

Base = declarative_base()