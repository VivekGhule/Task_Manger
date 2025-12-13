import json
from datetime import datetime
from typing import Optional
from django.conf import settings
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponse
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from bson.errors import InvalidId

# Create a simple Mongo client singleton
class DB:
    _client = None
    _db = None

    @classmethod
    def client(cls):
        if cls._client is None:
            cls._client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
            # test ping
            cls._client.admin.command("ping")
            cls._db = cls._client[settings.DB_NAME]
        return cls._client

    @classmethod
    def db(cls):
        if cls._db is None:
            cls.client()
        return cls._db

def ok(data=None):
    if data is None:
        data = {}
    response = {"success": True}
    response.update(data)
    return JsonResponse(response, safe=False)

def error(message="Internal error", status=500):
    return JsonResponse({"success": False, "detail": str(message)}, status=status)

def serialize_task(doc):
    if not doc:
        return None
    doc = dict(doc)
    doc["_id"] = str(doc.get("_id"))
    # remove internal field if any
    doc.pop("priority_rank", None)
    # convert datetimes to ISO
    for k in ("created_at", "updated_at"):
        if isinstance(doc.get(k), datetime):
            doc[k] = doc[k].isoformat()
    return doc

# Health check
def health(request: HttpRequest):
    return ok({"message": "API running"})

# GET /api/tasks  (list) and POST /api/tasks (create)
def tasks_collection(request: HttpRequest):
    coll = DB.db()["tasks"]
    if request.method == "GET":
        status_filter = request.GET.get("status_filter")
        priority_filter = request.GET.get("priority_filter")
        query = {}
        if status_filter:
            query["status"] = status_filter.lower()
        if priority_filter:
            query["priority"] = priority_filter.lower()
        try:
            cursor = coll.find(query).sort([("priority_rank", -1), ("created_at", -1)])
            tasks = [serialize_task(t) for t in cursor]
            total = coll.count_documents({})
            completed = coll.count_documents({"status": "completed"})
            pending = coll.count_documents({"status": "pending"})
            stats = {
                "total": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": round((completed / total * 100), 2) if total else 0
            }
            return ok({"tasks": tasks, "stats": stats})
        except PyMongoError as e:
            return error(f"DB read failed: {e}", status=500)

    elif request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponseBadRequest("Invalid JSON")
        title = payload.get("title")
        if not title or not title.strip():
            return JsonResponse({"success": False, "detail": "title is required"}, status=400)
        description = payload.get("description") or ""
        priority = (payload.get("priority") or "medium").lower()
        status_val = (payload.get("status") or "pending").lower()
        due_date = payload.get("due_date")
        # compute priority_rank
        rank = {"low": 1, "medium": 2, "high": 3}.get(priority, 2)
        now = datetime.utcnow()
        doc = {
            "title": title.strip(),
            "description": description,
            "priority": priority,
            "priority_rank": rank,
            "status": status_val,
            "due_date": due_date,
            "created_at": now,
            "updated_at": now
        }
        try:
            res = coll.insert_one(doc)
            return JsonResponse({"success": True, "task_id": str(res.inserted_id), "message": "Task created"}, status=201)
        except PyMongoError as e:
            return error(f"DB insert failed: {e}", status=500)
    else:
        return JsonResponse({"success": False, "detail": "Method not allowed"}, status=405)

# GET, PUT, DELETE /api/tasks/<task_id>
def task_detail(request: HttpRequest, task_id: str):
    coll = DB.db()["tasks"]
    # validate ObjectId
    try:
        oid = ObjectId(task_id)
    except (InvalidId, Exception):
        return JsonResponse({"success": False, "detail": "Invalid task id"}, status=400)

    if request.method == "GET":
        try:
            doc = coll.find_one({"_id": oid})
            if not doc:
                return JsonResponse({"success": False, "detail": "Task not found"}, status=404)
            return ok({"task": serialize_task(doc)})
        except PyMongoError as e:
            return error(f"DB read failed: {e}", status=500)

    elif request.method == "PUT":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponseBadRequest("Invalid JSON")

        update_data = {}
        allowed = {"title", "description", "priority", "status", "due_date"}
        for k in allowed:
            if k in payload:
                val = payload.get(k)
                if k == "title" and val and isinstance(val, str):
                    val = val.strip()
                update_data[k] = val
        if not update_data:
            return JsonResponse({"success": False, "detail": "No data provided"}, status=400)

        # normalize priority and status
        if "priority" in update_data and update_data["priority"] is not None:
            update_data["priority"] = str(update_data["priority"]).lower()
            update_data["priority_rank"] = {"low": 1, "medium": 2, "high": 3}.get(update_data["priority"], 2)
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = str(update_data["status"]).lower()

        update_data["updated_at"] = datetime.utcnow()

        try:
            res = coll.update_one({"_id": oid}, {"$set": update_data})
            if res.matched_count == 0:
                return JsonResponse({"success": False, "detail": "Task not found"}, status=404)
            # return updated doc
            doc = coll.find_one({"_id": oid})
            return ok({"task": serialize_task(doc), "message": "Task updated"})
        except PyMongoError as e:
            return error(f"DB update failed: {e}", status=500)

    elif request.method == "DELETE":
        try:
            res = coll.delete_one({"_id": oid})
            if res.deleted_count == 0:
                return JsonResponse({"success": False, "detail": "Task not found"}, status=404)
            return ok({"message": "Task deleted"})
        except PyMongoError as e:
            return error(f"DB delete failed: {e}", status=500)
    else:
        return JsonResponse({"success": False, "detail": "Method not allowed"}, status=405)

# DELETE /api/tasks/completed/all
def clear_completed(request: HttpRequest):
    if request.method != "DELETE":
        return JsonResponse({"success": False, "detail": "Method not allowed"}, status=405)
    coll = DB.db()["tasks"]
    try:
        res = coll.delete_many({"status": "completed"})
        return ok({"deleted_count": int(res.deleted_count)})
    except PyMongoError as e:
        return error(f"DB delete failed: {e}", status=500)

# GET /api/stats
def get_stats(request: HttpRequest):
    coll = DB.db()["tasks"]
    try:
        total = coll.count_documents({})
        completed = coll.count_documents({"status": "completed"})
        pending = coll.count_documents({"status": "pending"})
        stats = {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round((completed / total * 100), 2) if total else 0
        }
        return ok({"stats": stats})
    except PyMongoError as e:
        return error(f"DB aggregation failed: {e}", status=500)
