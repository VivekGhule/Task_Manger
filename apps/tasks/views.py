# Task_Manager/appa/tasks/views.py

import json
from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .scheduler import schedule_task_email
from .scheduler import cancel_task_email
from .mongo import tasks_collection


@login_required
def dashboard(request):
    return render(request, "tasks/dashboard.html")


@login_required
@csrf_exempt
def tasks_api(request):
    user_id = request.user.id

    # ---------------- GET TASKS ----------------
    if request.method == "GET":
        tasks = list(tasks_collection.find({"user_id": user_id}))
        for t in tasks:
            t["_id"] = str(t["_id"])
        return JsonResponse(tasks, safe=False)

    # ---------------- CREATE TASK ----------------
    if request.method == "POST":
        data = json.loads(request.body)

        task = {
            "title": data.get("title"),
            "description": data.get("description", ""),
            "priority": data.get("priority", "medium"),
            "due_date": data.get("due_date"),
            "due_time": data.get("due_time"),
            "completed": False,
            "user_id": user_id,
        }

        result = tasks_collection.insert_one(task)
        task["_id"] = str(result.inserted_id)

        #  SCHEDULE EMAIL REMINDER (CORRECT PLACE)
        if task.get("due_date") and task.get("due_time"):
            schedule_task_email(
                user_email=request.user.email,
                task_title=task["title"],
                task_description=task.get("description", ""),
                due_date=task["due_date"],
                due_time=task["due_time"],
                task_id=str(task["_id"])
            )


        return JsonResponse(task, status=201)


@login_required
@csrf_exempt
def task_detail_api(request, task_id):
    user_id = request.user.id
    query = {"_id": ObjectId(task_id), "user_id": user_id}

    # ---------------- UPDATE TASK ----------------
    if request.method == "PATCH":
        data = json.loads(request.body)
        tasks_collection.update_one(query, {"$set": data})
        return JsonResponse({"success": True})

    # ---------------- DELETE TASK ----------------
    if request.method == "DELETE":
        cancel_task_email(task_id)
        tasks_collection.delete_one(query)
        return JsonResponse({"success": True})
