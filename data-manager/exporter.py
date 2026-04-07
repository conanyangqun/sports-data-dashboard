import json
from database import Database
from config import DATABASE_FILE, JSON_FILE

class DataExporter:
    def __init__(self, db_path=None, json_path=None):
        self.db_path = db_path or DATABASE_FILE
        self.json_path = json_path or JSON_FILE
        self.db = Database(self.db_path)
    
    def export_to_json(self, pretty=True):
        self.db.connect()
        cursor = self.db.conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        user_data = None
        if users:
            user = users[0]
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'display_name': user['display_name'],
                'avatar_url': user['avatar_url'],
                'bio': user['bio']
            }
        
        cursor.execute('SELECT * FROM activities ORDER BY start_time DESC')
        activities = cursor.fetchall()
        activities_data = []
        
        for activity in activities:
            activity_dict = {
                'id': activity['id'],
                'activity_type': activity['activity_type'],
                'start_time': activity['start_time'],
                'duration': activity['duration'],
                'distance': activity['distance'],
                'calories': activity['calories'],
                'max_speed': activity['max_speed'],
                'avg_speed': activity['avg_speed'],
                'max_heart_rate': activity['max_heart_rate'],
                'avg_heart_rate': activity['avg_heart_rate'],
                'max_cadence': activity['max_cadence'],
                'avg_cadence': activity['avg_cadence'],
                'max_power': activity['max_power'],
                'avg_power': activity['avg_power'],
                'normalized_power': activity['normalized_power'],
                'elevation_gain': activity['elevation_gain']
            }
            activities_data.append(activity_dict)
        
        self.db.close()
        
        export_data = {
            'user': user_data,
            'activities': activities_data
        }
        
        indent = 2 if pretty else None
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=indent, default=str)
        
        return export_data
    
    def validate_data(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM activities')
        activity_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        self.db.close()
        
        issues = []
        
        if user_count == 0:
            issues.append('No user data found')
        elif user_count > 1:
            issues.append(f'Multiple users found ({user_count}), expected 1')
        
        if activity_count == 0:
            issues.append('No activities found')
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'activity_count': activity_count,
            'user_count': user_count
        }
    
    def get_data_summary(self):
        self.db.connect()
        cursor = self.db.conn.cursor()
        
        cursor.execute('SELECT MIN(start_time), MAX(start_time) FROM activities')
        date_range = cursor.fetchone()
        
        cursor.execute('SELECT DISTINCT activity_type FROM activities')
        types = [row[0] for row in cursor.fetchall()]
        
        self.db.close()
        
        return {
            'total_activities': len(self.export_to_json(pretty=False)['activities']),
            'date_range': {
                'earliest': date_range[0],
                'latest': date_range[1]
            },
            'activity_types': types
        }
