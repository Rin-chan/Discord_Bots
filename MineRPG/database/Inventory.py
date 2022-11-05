from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key = True)
    user_id = Column(BIGINT, ForeignKey("user.id"))
    name = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False, default=1)