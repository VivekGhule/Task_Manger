# Task_Manager/config/mongo_utils.py
from pymongo import MongoClient, errors
from django.conf import settings

_client = None

def get_mongo_client():
    """
    Get MongoDB client (singleton pattern)
    Safe for MongoDB 8.x
    """
    global _client

    if _client is None:
        try:
            _client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=3000,  # 3 seconds timeout
            )
            # Force connection check
            _client.admin.command('ping')
        except errors.ServerSelectionTimeoutError as e:
            raise Exception(
                "❌ MongoDB is not running or connection failed. "
                "Make sure MongoDB is started on localhost:27017"
            ) from e

    return _client


def get_database():
    """Return MongoDB database"""
    return get_mongo_client()[settings.MONGO_DB_NAME]


def get_tasks_collection():
    """Return tasks collection"""
    return get_database()['tasks']
