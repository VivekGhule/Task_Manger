# Task_Manager\apps\tasks\presenters.py
from bson import ObjectId
from datetime import datetime
from .models import tasks_collection
from datetime import datetime, timedelta, timezone   # Updated for timezone safety

class TaskPresenter:

    @staticmethod
    def create_task(data, user_id):
        tasks_collection.insert_one({
            "title": data.get("title"),
            "description": data.get("description"),
            "priority": data.get("priority"),
            "due_date": data.get("due_date"),
            "due_time": data.get("due_time"),
            "is_completed": False,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc)
        })

    @staticmethod
    def get_tasks(user_id):
        return list(tasks_collection.find({"user_id": user_id}))

    @staticmethod
    def toggle_task(task_id, user_id):
        tasks_collection.update_one(
            {"_id": ObjectId(task_id), "user_id": user_id},
            {"$set": {"is_completed": True}}
        )

    @staticmethod
    def delete_completed(user_id):
        tasks_collection.delete_many(
            {"user_id": user_id, "is_completed": True}
        )
