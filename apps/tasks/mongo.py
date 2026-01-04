# Task_Manager\apps\tasks\mongo.py
from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGODB_URI)


db = client[settings.MONGO_DB_NAME]

tasks_collection = db["tasks"]
