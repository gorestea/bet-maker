from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bet(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True)
    amount = Column(Float)
    status = Column(String, index=True)
    created_at = Column(DateTime)
