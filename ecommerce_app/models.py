from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/store_allowances"
TEST_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test_store_allowances"

engine = create_engine(DATABASE_URL, echo=False)
# Creating a scoped session factory
Session = scoped_session(sessionmaker(bind=engine))


class store(Base):
    __tablename__ = "t_stores"
    a_id = Column(Integer, primary_key=True)
    a_name = Column(String(255))
    a_online = Column(Boolean)


class allowance(Base):
    __tablename__ = "t_allowances"
    a_store_id = Column(Integer, ForeignKey("t_stores.a_id"), primary_key=True)
    a_month = Column(Date, primary_key=True)
    a_allowance_amount = Column(Float)
    a_amount_expenditure = Column(Float)


class Notification(Base):
    __tablename__ = "t_notifications"
    a_store_id = Column(Integer, ForeignKey("t_stores.a_id"), primary_key=True)
    a_month = Column(Date, primary_key=True)
    fifty_percent_notified = Column(Boolean, default=False)
    hundred_percent_notified = Column(Boolean, default=False)
