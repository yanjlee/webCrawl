# coding=utf8
from sqlalchemy import Column, Integer, Sequence, String

from sqlEngine import Base
'''作为存放models'''

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'),
            primary_key=True, autoincrement=True)
    name = Column(String(50))
