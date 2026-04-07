import sqlite3
from config import DATABASE_FILE

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or DATABASE_FILE
        self.conn = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def init_db(self):
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL UNIQUE,
                avatar_url VARCHAR(255),
                bio TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_type VARCHAR(50) NOT NULL,
                start_time TIMESTAMP NOT NULL,
                duration REAL,
                distance REAL,
                calories REAL,
                max_speed REAL,
                avg_speed REAL,
                max_heart_rate INTEGER,
                avg_heart_rate INTEGER,
                max_cadence INTEGER,
                avg_cadence INTEGER,
                max_power INTEGER,
                avg_power INTEGER,
                normalized_power INTEGER,
                elevation_gain REAL
            )
        ''')
        
        self.conn.commit()
        self.close()
    
    def insert_activity(self, activity_data):
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (
                activity_type, start_time, duration, distance, calories,
                max_speed, avg_speed, max_heart_rate, avg_heart_rate,
                max_cadence, avg_cadence, max_power, avg_power,
                normalized_power, elevation_gain
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_data['activity_type'],
            activity_data['start_time'],
            activity_data['duration'],
            activity_data['distance'],
            activity_data['calories'],
            activity_data['max_speed'],
            activity_data['avg_speed'],
            activity_data['max_heart_rate'],
            activity_data['avg_heart_rate'],
            activity_data['max_cadence'],
            activity_data['avg_cadence'],
            activity_data['max_power'],
            activity_data['avg_power'],
            activity_data['normalized_power'],
            activity_data['elevation_gain']
        ))
        
        self.conn.commit()
        activity_id = cursor.lastrowid
        self.close()
        return activity_id
    
    def get_all_activities(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM activities ORDER BY start_time DESC')
        activities = cursor.fetchall()
        self.close()
        return activities
    
    def get_stats(self):
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM activities')
        total_activities = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(distance) FROM activities')
        total_distance = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT SUM(duration) FROM activities')
        total_duration = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT activity_type, COUNT(*) FROM activities GROUP BY activity_type')
        type_stats = cursor.fetchall()
        
        self.close()
        
        return {
            'total_activities': total_activities,
            'total_distance': total_distance,
            'total_duration': total_duration,
            'type_stats': dict(type_stats)
        }
    
    def activity_exists(self, start_time):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM activities WHERE start_time = ?', (start_time,))
        result = cursor.fetchone()
        self.close()
        return result is not None
    
    def insert_user(self, username, avatar_url=None, bio=None):
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (username, avatar_url, bio)
            VALUES (?, ?, ?)
        ''', (username, avatar_url, bio))
        
        self.conn.commit()
        user_id = cursor.lastrowid
        self.close()
        return user_id
    
    def get_user(self, username=None):
        self.connect()
        cursor = self.conn.cursor()
        
        if username:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        else:
            cursor.execute('SELECT * FROM users LIMIT 1')
        
        user = cursor.fetchone()
        self.close()
        return user
    
    def update_user(self, username, avatar_url=None, bio=None):
        self.connect()
        cursor = self.conn.cursor()
        
        if avatar_url and bio:
            cursor.execute('''
                UPDATE users SET avatar_url = ?, bio = ? WHERE username = ?
            ''', (avatar_url, bio, username))
        elif avatar_url:
            cursor.execute('''
                UPDATE users SET avatar_url = ? WHERE username = ?
            ''', (avatar_url, username))
        elif bio:
            cursor.execute('''
                UPDATE users SET bio = ? WHERE username = ?
            ''', (bio, username))
        
        self.conn.commit()
        self.close()
    
    def delete_user(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users')
        self.conn.commit()
        self.close()
    
    def delete_activity(self, activity_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
        self.conn.commit()
        self.close()
    
    def delete_activities_by_date_range(self, start_date, end_date):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM activities 
            WHERE start_time >= ? AND start_time <= ?
        ''', (start_date, end_date))
        deleted_count = cursor.rowcount
        self.conn.commit()
        self.close()
        return deleted_count
    
    def get_activity_by_id(self, activity_id):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
        activity = cursor.fetchone()
        self.close()
        return activity
    
    def get_activities_by_type(self, activity_type):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM activities 
            WHERE activity_type = ? 
            ORDER BY start_time DESC
        ''', (activity_type,))
        activities = cursor.fetchall()
        self.close()
        return activities
    
    def get_activities_by_date_range(self, start_date, end_date):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM activities 
            WHERE start_time >= ? AND start_time <= ?
            ORDER BY start_time DESC
        ''', (start_date, end_date))
        activities = cursor.fetchall()
        self.close()
        return activities
    
    def get_week_stats(self):
        from datetime import datetime, timedelta
        self.connect()
        cursor = self.conn.cursor()
        
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        cursor.execute('''
            SELECT 
                COUNT(*) as count,
                SUM(distance) as total_distance,
                SUM(duration) as total_duration,
                SUM(calories) as total_calories,
                AVG(avg_speed) as avg_speed
            FROM activities
            WHERE start_time >= ?
        ''', (week_ago,))
        
        result = cursor.fetchone()
        self.close()
        
        return {
            'total_activities': result[0] or 0,
            'total_distance': result[1] or 0,
            'total_duration': result[2] or 0,
            'total_calories': result[3] or 0,
            'avg_speed': result[4] or 0
        }
