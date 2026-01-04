# Task_Manager\apps\tasks\models.py

from pymongo import MongoClient

# MongoDB connection (Option A)
client = MongoClient("mongodb://localhost:27017/")
db = client["task_manager"]
tasks_collection = db["tasks"]
