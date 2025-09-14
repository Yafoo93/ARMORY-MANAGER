from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    armorer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    ended_at = Column(DateTime)
    active = Column(Boolean, nullable=False, default=True)

    armorer = relationship("User", backref="shifts")
