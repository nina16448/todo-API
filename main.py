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
        # 一次把 Task 和它的 status 一併載入
        tasks = (
            db.query(models.Task)
              .options(joinedload(models.Task.status))
              .all()
        )

        now = datetime.now()
        result = []
        for t in tasks:
            status = t.status[0] if t.status else None
            # 保證 required 是布林值
            required_val = t.required if t.required is not None else True

            result.append({
                "id": t.id,
                "title": t.title,
                "due_datetime": t.due_datetime,              # 原生 DateTime 物件，Pydantic 會自動轉 ISO
                "required": required_val,
                "expired": t.due_datetime < now,             # 用 due_datetime 判斷是否過期
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
