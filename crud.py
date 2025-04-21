# crud.py
from sqlalchemy.orm import Session
import models, schemas
from datetime import date, datetime

def get_tasks_by_date(db: Session, target_date: date):
    from datetime import date as dt_date

    tasks = db.query(models.Task).filter(models.Task.date == target_date).all()
    task_statuses = {
        s.task_id: s for s in db.query(models.TaskStatus).all()
    }

    result = []
    today = dt_date.today()

    for task in tasks:
        status = task_statuses.get(task.id)
        is_done = status.is_done if status else False

        expired = task.date < today and not is_done

        result.append(schemas.TaskShow(
            id=task.id,
            title=task.title,
            date=task.date,
            required=task.required,
            expired=expired,
        ))

    return result


def complete_task(db: Session, task_id: int, proof: str = ""):
    status = db.query(models.TaskStatus).filter(models.TaskStatus.task_id == task_id).first()
    if not status:
        status = models.TaskStatus(task_id=task_id)
        db.add(status)
    status.is_done = True
    status.proof = proof
    status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(status)
    return status

def submit_unfinished_reason(db: Session, task_id: int, reason: str):
    status = db.query(models.TaskStatus).filter(models.TaskStatus.task_id == task_id).first()
    if not status:
        status = models.TaskStatus(task_id=task_id)
        db.add(status)
    status.unfinished_reason = reason
    status.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(status)
    return status
