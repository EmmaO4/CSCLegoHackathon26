from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from .db import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    units = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)  # Easy/Normal/Hard
    target = Column(String, nullable=False)      # Pass/B/A

    logs = relationship("DailyLog", back_populates="course")

class DailyLog(Base):
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    minutes = Column(Integer, nullable=False)
    mood = Column(Integer, nullable=False)  # 1-5
    note = Column(String, default="")
    day = Column(Date, default=date.today)

    course = relationship("Course", back_populates="logs")
