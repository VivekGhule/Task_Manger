# Task_Manager\apps\meetings\views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # Added
from django.shortcuts import get_object_or_404      # Added
from datetime import datetime, timedelta, timezone   # Updated for timezone safety
import json
from .models import meeting_manager  # Assuming this handles MongoDB logic

@login_required
@require_http_methods(["GET", "POST"])
def meeting_list_create(request):
    # """List all meetings or create a new meeting"""
    
    # Consistent ID handling (String for MongoDB)
    user_id_str = str(request.user.id)

    if request.method == "GET":
        try:
            meetings = meeting_manager.get_user_meetings(user_id_str)
            
            # Use timezone-aware UTC now
            now = datetime.now(timezone.utc)
            
            for meeting in meetings:
                try:
                    m_date = meeting.get('meeting_date')
                    m_time = meeting.get('meeting_time')
                    
                    if m_date and m_time:
                        # Parse and make timezone aware for safe comparison
                        dt_str = f"{m_date} {m_time}"
                        meeting_datetime = datetime.strptime(dt_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
                        
                        meeting['is_past'] = meeting_datetime < now
                        meeting['is_upcoming'] = now < meeting_datetime < now + timedelta(days=1)
                    else:
                        meeting['is_past'] = False
                        meeting['is_upcoming'] = False
                except (ValueError, TypeError):
                    meeting['is_past'] = False
                    meeting['is_upcoming'] = False
            
            return JsonResponse({'meetings': meetings})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # 1. Validation
            required_fields = ['title', 'meeting_date', 'meeting_time']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required'}, status=400)
            
            # 2. Date/Time format validation
            try:
                meeting_date_obj = datetime.strptime(data['meeting_date'], '%Y-%m-%d')
                meeting_time_obj = datetime.strptime(data['meeting_time'], '%H:%M')
            except ValueError:
                return JsonResponse({'error': 'Invalid format. Use YYYY-MM-DD and HH:MM'}, status=400)
            
            # 3. Past meeting check
            meeting_datetime = datetime.combine(meeting_date_obj.date(), meeting_time_obj.time()).replace(tzinfo=timezone.utc)
            if meeting_datetime < datetime.now(timezone.utc):
                return JsonResponse({'error': 'Cannot create meeting in the past'}, status=400)
            
            # 4. Create
            meeting = meeting_manager.create_meeting(user_id_str, data)
            return JsonResponse({
                'message': 'Meeting created successfully',
                'meeting': meeting
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to create: {str(e)}'}, status=500)

@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def meeting_detail(request, meeting_id):
    # """Get, update, or delete a specific meeting"""
    user_id_str = str(request.user.id)
    
    if request.method == "GET":
        try:
            meeting = meeting_manager.get_meeting_by_id(meeting_id, user_id_str)
            if not meeting:
                return JsonResponse({'error': 'Meeting not found'}, status=404)
            return JsonResponse({'meeting': meeting})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            # Add partial date validation if necessary (as in your original code)
            success = meeting_manager.update_meeting(meeting_id, user_id_str, data)
            if not success:
                return JsonResponse({'error': 'Update failed'}, status=404)
            
            updated_meeting = meeting_manager.get_meeting_by_id(meeting_id, user_id_str)
            return JsonResponse({'message': 'Updated', 'meeting': updated_meeting})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "DELETE":
        try:
            success = meeting_manager.delete_meeting(meeting_id, user_id_str)
            if not success:
                return JsonResponse({'error': 'Delete failed'}, status=404)
            return JsonResponse({'message': 'Meeting deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)