# sample_data.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, TaskStatus
from datetime import date, timedelta

db: Session = SessionLocal()

# 🔁 先清除現有資料（可選）
db.query(TaskStatus).delete()
db.query(Task).delete()
db.commit()

# 建立兩天的模擬任務
base_date = date.today()
dl_dates = [base_date, base_date + timedelta(days=1)]

all_tasks = []

for dl_date in dl_dates:
    # 每天兩個大項目
    for section_index in range(2):
        section_name = f"Section {section_index + 1}"

        # 每個 section 四個小項目
        for item_index in range(4):
            task_title = f"{dl_date} - {section_name} - 小任務 {item_index + 1}"
            task = Task(
                title=task_title,
                date=dl_date,
                required=True
            )
            all_tasks.append(task)

db.add_all(all_tasks)
db.commit()

print(f"已建立 {len(all_tasks)} 筆任務資料。")
