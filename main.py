from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import crud, models, schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=list[schemas.TaskShow])
def get_all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)

@app.post("/tasks/complete")
def mark_done(data: schemas.TaskComplete, db: Session = Depends(get_db)):
    return crud.complete_task(db, data.task_id, data.proof or "")

@app.post("/tasks/unfinished_reason")
def mark_undone(data: schemas.UnfinishedReason, db: Session = Depends(get_db)):
    return crud.submit_unfinished_reason(db, data.task_id, data.reason)

@app.post("/tasks/create")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)
