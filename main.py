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

@app.get("/tasks", response_model=List[schemas.TaskShow])
def get_all_tasks(db: Session = Depends(get_db)) -> List[schemas.TaskShow]:
    try:
        # 一次把 Task 和對應的 TaskStatus 一併載入
        tasks = (
            db.query(models.Task)
              .options(joinedload(models.Task.status))
              .all()
        )

        today = date.today()
        result = []
        for t in tasks:
            status = t.status[0] if t.status else None

            # 如果 t.required 是 None，就用 True 當作預設
            required_val = t.required if t.required is not None else True

            result.append({
                "id": t.id,
                "title": t.title,
                "date": str(t.date),
                "required": required_val,                 # 這裡套用預設
                "expired": t.date < today,
                "completed": status.is_done if status else False,
                "proof": status.proof if status else None,
                "unfinished_reason": status.unfinished_reason if status else None,
            })

        return result

    except Exception as e:
        import traceback; traceback.print_exc()
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
