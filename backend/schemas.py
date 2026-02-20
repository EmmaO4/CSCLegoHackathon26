from pydantic import BaseModel
from typing import List
from datetime import date

class CourseCreate(BaseModel):
    name: str
    units: int
    difficulty: str
    target: str

class CourseOut(BaseModel):
    id: int
    name: str
    units: int
    difficulty: str
    target: str
    recommended_hours: int

class LogCreate(BaseModel):
    course_id: int
    minutes: int
    mood: int
    note: str = ""

class LogOut(BaseModel):
    id: int
    course_id: int
    course_name: str
    minutes: int
    mood: int
    note: str
    day: date

class SummaryOut(BaseModel):
    weekly_hours: int
    today_minutes: int
    burnout_level: str
    burnout_tip: str

class WellnessOut(BaseModel):
    burnout_level: str
    tip: str
    activities: List[str]
    quote: str


