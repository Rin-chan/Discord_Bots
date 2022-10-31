from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class Enemy(Base):
    __tablename__ = "enemy"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    hp = Column(Integer, nullable=False, default=10)
    damage = Column(Integer, nullable=False, default=1)
    user = relationship("User", back_populates="enemy")