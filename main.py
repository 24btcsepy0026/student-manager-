from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
def read_index():
    return FileResponse(BASE_DIR / "index.html")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.create_student(db, student)
    return db_student

@app.get("/students/", response_model=List[schemas.StudentResponse])
def read_all(db: Session = Depends(get_db)):
    students = crud.get_students(db)
    return students

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated

@app.delete("/students/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

