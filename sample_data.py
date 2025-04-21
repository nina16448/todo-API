from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, TaskStatus
from datetime import date

db: Session = SessionLocal()

# 🔁 清空資料（視情況使用）
db.query(TaskStatus).delete()
db.query(Task).delete()
db.commit()

# 任務日期
task_date = date(2025, 4, 23)

# 模擬任務資料
task_titles = [
    f"{task_date} - OpenCV - 整理好全部每一個資料夾說明",
    f"{task_date} - Vnsg - 跟皓庭說Server跑不動的問題"
]

# 建立任務
tasks = [
    Task(title=title, date=task_date, required=True)
    for title in task_titles
]

db.add_all(tasks)
db.commit()

print(f"✅ 已建立 {len(tasks)} 筆任務資料。")
