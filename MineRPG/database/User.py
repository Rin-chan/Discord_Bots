from sqlalchemy import Column, Integer, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, primary_key = True)
    hp = Column(Integer, nullable=False, default=10)
    damage = Column(Integer, nullable=False, default=1)
    level = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=1)
    exploring = Column(Integer, nullable=False, default=1)
    digging = Column(Integer, nullable=False, default=1)
    mining = Column(Integer, nullable=False, default=1)
    farming = Column(Integer, nullable=False, default=1)
    fighting = Column(Integer, nullable=False, default=1)
    enemy_id = Column(Integer, ForeignKey("enemy.id"))
    enemy = relationship("Enemy", back_populates="user", foreign_keys=[enemy_id])