from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5433/example_tele_bot", echo=True)


Base = declarative_base()


class AllClients(Base):
    __tablename__ = 'AllClients'

    id = Column(Integer, primary_key=True)
    client_telegram_id = Column(BigInteger, unique=True)


class AllManagers(Base):
    __tablename__ = 'AllManagers'

    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    manager_telegram_id = Column(BigInteger, unique=True)


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
    company_creator = Column(String)
    pigment_name = Column(String)
    description = Column(String)
    volume_and_price = Column(String)




create_session = sessionmaker(bind=engine)
session = create_session()
