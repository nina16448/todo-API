from sqlalchemy.orm import Session
import models, schemas

def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def complete_task(db: Session, task_id: int, proof: str):
    status = db.query(models.TaskStatus).filter_by(task_id=task_id).first()
    if not status:
        status = models.TaskStatus(task_id=task_id)
        db.add(status)
    status.proof = proof
    db.commit()
    return {"message": "任務已完成"}

def submit_unfinished_reason(db: Session, task_id: int, reason: str):
    status = db.query(models.TaskStatus).filter_by(task_id=task_id).first()
    if not status:
        status = models.TaskStatus(task_id=task_id)
        db.add(status)
    status.unfinished_reason = reason
    db.commit()
    return {"message": "已儲存未完成原因"}

def create_task(db: Session, task: schemas.TaskCreate):
    new_task = models.Task(title=task.title, date=task.date, required=True)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
