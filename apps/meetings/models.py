from pymongo import MongoClient
from django.conf import settings
from datetime import datetime
from bson import ObjectId
 


class MeetingManager:
    """Manager class to handle MongoDB operations for meetings"""
    
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db['meetings']
        
        # Create indexes for better query performance
        self.collection.create_index([('user_id', 1), ('meeting_date', -1)])
        self.collection.create_index([('meeting_date', 1), ('meeting_time', 1)])
    
    def create_meeting(self, user_id, data):
        """Create a new meeting"""
        meeting = {
            'user_id': str(user_id),
            'title': data['title'],
            'description': data.get('description', ''),
            'category': data.get('category', 'work'),
            'meeting_link': data.get('meeting_link', ''),
            'meeting_date': data['meeting_date'],
            'meeting_time': data['meeting_time'],
            'duration': data.get('duration', 60),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        
        result = self.collection.insert_one(meeting)
        meeting['_id'] = str(result.inserted_id)
        return meeting
    
    def get_user_meetings(self, user_id):
        """Get all meetings for a user"""
        meetings = list(self.collection.find({'user_id': user_id}).sort('meeting_date', -1))
        for meeting in meetings:
            meeting['_id'] = str(meeting['_id'])
        return meetings
    
    def get_meeting_by_id(self, meeting_id, user_id):
        """Get a specific meeting by ID"""
        try:
            meeting = self.collection.find_one({
                '_id': ObjectId(meeting_id),
                'user_id': str(user_id),
            })
            if meeting:
                meeting['_id'] = str(meeting['_id'])
            return meeting
        except:
            return None
    
    def update_meeting(self, meeting_id, user_id, data):
        """Update a meeting"""
        try:
            update_data = {
                'updated_at': datetime.utcnow()
            }
            
            # Update only provided fields
            if 'title' in data:
                update_data['title'] = data['title']
            if 'description' in data:
                update_data['description'] = data['description']
            if 'category' in data:
                update_data['category'] = data['category']
            if 'meeting_link' in data:
                update_data['meeting_link'] = data['meeting_link']
            if 'meeting_date' in data:
                update_data['meeting_date'] = data['meeting_date']
            if 'meeting_time' in data:
                update_data['meeting_time'] = data['meeting_time']
            if 'duration' in data:
                update_data['duration'] = data['duration']
            
            result = self.collection.update_one(
                {'_id': ObjectId(meeting_id), 'user_id': str(user_id)},
                {'$set': update_data}
            )
            
            return result.modified_count > 0
        except:
            return False
    
    def delete_meeting(self, meeting_id, user_id):
        """Delete a meeting"""
        try:
            # Try ObjectId first
            query = {"user_id": user_id}

            try:
                query["_id"] = ObjectId(meeting_id)
            except Exception:
                # Fallback if _id is stored as string
                query["_id"] = meeting_id

            result = self.collection.delete_one(query)
            return result.deleted_count == 1

        except Exception as e:
            print("DELETE ERROR:", e)
            return False


# Singleton instance
meeting_manager = MeetingManager()