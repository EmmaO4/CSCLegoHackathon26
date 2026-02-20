from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
from db import SessionLocal, engine, Base
from models import Course, DailyLog
from schemas import CourseCreate, CourseOut, LogCreate, LogOut, SummaryOut, WellnessOut
from logic import recommended_hours, burnout_assessment, wellness_pack

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lego Study Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    out = []
    for c in courses:
        out.append({
            "id": c.id,
            "name": c.name,
            "units": c.units,
            "difficulty": c.difficulty,
            "target": c.target,
            "recommended_hours": recommended_hours(c.units, c.difficulty, c.target)
        })
    return out

@app.post("/courses", response_model=CourseOut)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    c = Course(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return {
        "id": c.id,
        "name": c.name,
        "units": c.units,
        "difficulty": c.difficulty,
        "target": c.target,
        "recommended_hours": recommended_hours(c.units, c.difficulty, c.target)
    }

@app.post("/logs", response_model=LogOut)
def add_log(payload: LogCreate, db: Session = Depends(get_db)):
    log = DailyLog(
        course_id=payload.course_id,
        minutes=payload.minutes,
        mood=payload.mood,
        note=payload.note,
        day=date.today()
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    course = db.query(Course).filter(Course.id == log.course_id).first()
    return {
        "id": log.id,
        "course_id": log.course_id,
        "course_name": course.name if course else "Course",
        "minutes": log.minutes,
        "mood": log.mood,
        "note": log.note,
        "day": log.day
    }

@app.get("/logs/today", response_model=list[LogOut])
def today_logs(db: Session = Depends(get_db)):
    logs = db.query(DailyLog).filter(DailyLog.day == date.today()).all()
    out = []
    for l in logs:
        out.append({
            "id": l.id,
            "course_id": l.course_id,
            "course_name": l.course.name,
            "minutes": l.minutes,
            "mood": l.mood,
            "note": l.note,
            "day": l.day
        })
    return out

@app.get("/summary", response_model=SummaryOut)
def summary(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    weekly = sum(recommended_hours(c.units, c.difficulty, c.target) for c in courses)

    logs = db.query(DailyLog).filter(DailyLog.day == date.today()).all()
    today_minutes = sum(l.minutes for l in logs)
    avg_mood = (sum(l.mood for l in logs) / len(logs)) if logs else 3.5

    level, tip = burnout_assessment(weekly, today_minutes, avg_mood)
    return {"weekly_hours": weekly, "today_minutes": today_minutes, "burnout_level": level, "burnout_tip": tip}

@app.get("/wellness", response_model=WellnessOut)
def wellness(db: Session = Depends(get_db)):
    s = summary(db)
    activities, quote = wellness_pack(s["burnout_level"])
    return {
        "burnout_level": s["burnout_level"],
        "tip": s["burnout_tip"],
        "activities": activities,
        "quote": quote
    }
