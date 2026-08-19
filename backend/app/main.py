from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

app = FastAPI(title="TaskFlow API Service")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend"}

@app.get("/api/v1/tasks", response_model=List[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.post("/api/v1/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        is_completed=task.is_completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task