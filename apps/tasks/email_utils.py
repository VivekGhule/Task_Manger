# Task_Manager/appa/tasks/email_utils.py
# set the message
from django.core.mail import send_mail
from django.conf import settings

def send_task_reminder(user_email, task_title, task_description, due_date, due_time):
    subject = f"⏰ Task Reminder: {task_title}"
    message = f"""
    Hello,
    
    This is a reminder for your task.
    
    📌 Task: {task_title}
    📝 Description: {task_description or 'No description'}
    📅 Due Date: {due_date}
    ⏰ Due Time: {due_time}
    
    Please complete it on time.
    
    – TaskHub
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed for {user_email}: {e}")
