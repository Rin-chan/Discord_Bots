from sqlalchemy import Column, Integer, BIGINT, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, primary_key = True)
    hp = Column(Integer, nullable=False, default=10)
    damage = Column(Integer, nullable=False, default=1)
    level = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=0)
    gold = Column(Integer, nullable=False, default=0)
    weapon = Column(Integer, ForeignKey("weapon.id"), default=1)
    digging = Column(Integer, nullable=False, default=1)
    mining = Column(Integer, nullable=False, default=1)
    farming = Column(Integer, nullable=False, default=1)
    enemy_id = Column(Integer, ForeignKey("enemy_fight.id"))

    weapon_relationship = relationship("Weapon", back_populates="user", foreign_keys=[weapon])
    enemy_relationship = relationship("Enemy_Fight", back_populates="user", foreign_keys=[enemy_id])