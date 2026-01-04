# Task_Manager/appa/tasks/schedular.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from apscheduler.jobstores.base import JobLookupError
from .email_utils import send_task_reminder

# ------------------------------
# Start scheduler only once
# ------------------------------
scheduler = BackgroundScheduler()
scheduler.start()


# ------------------------------
# Schedule task reminder email
# ------------------------------
def schedule_task_email(
    user_email,
    task_title,
    task_description,
    due_date,
    due_time,
    task_id
):
    """
    Schedules an email reminder for a task
    """

    # Convert date & time to datetime
    run_at = datetime.strptime(
        f"{due_date} {due_time}",
        "%Y-%m-%d %H:%M"
    )

    # Do not schedule if time already passed
    if run_at <= datetime.now():
        return

    job_id = f"task-reminder-{task_id}"

    try:
        scheduler.add_job(
            send_task_reminder,
            trigger="date",
            run_date=run_at,
            args=[
                user_email,
                task_title,
                task_description,
                due_date,
                due_time
            ],
            id=job_id,
            replace_existing=True,
            misfire_grace_time=60  # 1 minute grace
        )
    except Exception as e:
        print("Scheduler error:", e)


# ------------------------------
# Cancel scheduled reminder
# ------------------------------
def cancel_task_email(task_id):
    job_id = f"task-reminder-{task_id}"

    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        pass
