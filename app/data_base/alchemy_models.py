import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, ARRAY, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

engine = create_engine(f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:'
                       f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}'
                       f':{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB_NAME")}', echo=True)

Base = declarative_base()


class AllClients(Base):
    __tablename__ = 'AllClients'

    id = Column(Integer, primary_key=True)
    client_telegram_id = Column(BigInteger, unique=True)


class DataMailing(Base):
    __tablename__ = 'DataMailing'

    id = Column(Integer, primary_key=True)
    photo_id = Column(String)
    text = Column(String)


class Pigments(Base):
    __tablename__ = 'Pigments'

    id = Column(Integer, primary_key=True)
    photo = Column(String)
    direction = Column(String)
    zone_or_color = Column(String)
    company_creator = Column(String, ForeignKey("Creator.creator_name"))
    pigment_name = Column(String)
    description = Column(String)
    volume_and_price = Column(String)
    creator = relationship("Creator", back_populates='pigment')


class Creator(Base):
    __tablename__ = 'Creator'

    direction = Column(String)
    creator_name = Column(String, primary_key=True)
    pigment = relationship("Pigments", back_populates='creator', cascade='all,delete')


class Orders(Base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    client_id = Column(BigInteger)
    items = Column(ARRAY(Integer))
    delivery_data = Column(String)
    how_to_contact = Column(String, default=None)
    more_info = Column(String, default=None)
    order_status = Column(Boolean, default=False)
    create_date = Column(Date)


create_session = sessionmaker(bind=engine)
session = create_session()
