from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, joinedload
from fastapi.responses import JSONResponse
import crud, models, schemas
from database import SessionLocal, engine, Base
from sqlalchemy import text  # 加上這行！
from datetime import date
from typing import List


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/debug-db")
def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM tasks")).fetchone()
        return {"total": result[0]}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)) -> List[schemas.TaskShow]:
    try:
        tasks = db.query(models.Task).options(joinedload(models.Task.status)).all()

        for t in tasks:
            print(f"[任務] ID: {t.id} / 標題: {t.title} / 日期: {t.date}")

        result = [
            {
                "id": task.id,
                "title": task.title,
                "date": str(task.date),
                "required": task.required,
                "expired": task.date < date.today(),
                "completed": (task.status and task.status[0].is_done) or False,
                "proof": task.status[0].proof if task.status else None,
                "unfinished_reason": task.status[0].unfinished_reason if task.status else None,
            }
            for task in tasks
        ]

        print("✅ 資料處理完成")
        return result

    except Exception as e:
        
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.post("/tasks/complete")
def mark_done(data: schemas.TaskComplete, db: Session = Depends(get_db)):
    return crud.complete_task(db, data.task_id, data.proof or "")

@app.post("/tasks/unfinished_reason")
def mark_undone(data: schemas.UnfinishedReason, db: Session = Depends(get_db)):
    return crud.submit_unfinished_reason(db, data.task_id, data.reason)

@app.post("/tasks/create")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)
