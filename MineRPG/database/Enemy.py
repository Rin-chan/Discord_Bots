from sqlalchemy import Column, Integer, String

from . import Base

class Enemy(Base):
    __tablename__ = "enemy"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    hp = Column(Integer, nullable=False, default=10)
    damage = Column(Integer, nullable=False, default=1)
    min_level = Column(Integer, nullable=False, default=0)
    max_level = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=0)
    gold = Column(Integer, nullable=False, default=0)