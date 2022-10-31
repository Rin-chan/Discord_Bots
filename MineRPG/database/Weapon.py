from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base

class Weapon(Base):
    __tablename__ = "weapon"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    damage = Column(Integer, nullable=False, default=1)
    cost = Column(Integer, nullable=False, default=0)
    user = relationship("User")