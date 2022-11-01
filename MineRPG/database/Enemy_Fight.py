from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class Enemy_Fight(Base):
    __tablename__ = "enemy_fight"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    hp = Column(Integer, nullable=False, default=10)
    original_hp = Column(Integer, nullable=False, default=10)
    damage = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=0)
    gold = Column(Integer, nullable=False, default=0)
    user = relationship("User")