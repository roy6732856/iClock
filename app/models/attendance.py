from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    clock_in = Column(DateTime, nullable=True)
    clock_out = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Attendance(user_id={self.user_id}, user_name={self.user_name}, date={self.date})>"