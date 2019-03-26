import datetime
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, ForeignKey, Integer, String,
                        Float, Sequence, Table, DateTime)
import constants

Base = declarative_base()
TaskMapping = Table('TaskMapping', Base.metadata,
                    Column('user_id', Integer, ForeignKey('user_details.user_id')),
                    Column('task_id', Integer, ForeignKey('task_details.task_id', ondelete='CASCADE')))


class User(Base):
    __tablename__ = 'user_details'
    user_id = Column(Integer, Sequence('user_id_seq', start=1001, increment=1), primary_key=True)
    user_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    tasks = relationship('Tasks', backref='user', lazy='dynamic',
                         secondary=TaskMapping)


class Tasks(Base):
    __tablename__ = 'task_details'
    task_id = Column(Integer, Sequence('task_id_seq', start=1001, increment=1), primary_key=True)
    description = Column(String(250))
    hrs = Column(Float)
    percent_complete = Column(Float, default=0.0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine(constants.DB_URL)
Base.metadata.create_all(engine)
