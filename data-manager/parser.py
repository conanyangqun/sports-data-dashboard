from fitparse import FitFile
from datetime import datetime
from config import SPORT_TYPE_MAPPING

class FITParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.fit_file = None
        try:
            self.fit_file = FitFile(file_path)
        except Exception as e:
            raise ValueError(f"Failed to load FIT file: {e}")
    
    def parse(self):
        activity_data = {
            'activity_type': None,
            'start_time': None,
            'duration': None,
            'distance': None,
            'calories': None,
            'max_speed': None,
            'avg_speed': None,
            'max_heart_rate': None,
            'avg_heart_rate': None,
            'max_cadence': None,
            'avg_cadence': None,
            'max_power': None,
            'avg_power': None,
            'normalized_power': None,
            'elevation_gain': None
        }
        
        if not self.fit_file:
            return activity_data
        
        for record in self.fit_file.get_messages('session'):
            for data in record:
                if data.name == 'sport':
                    sport = data.value
                    activity_data['activity_type'] = SPORT_TYPE_MAPPING.get(sport, 'other')
                elif data.name == 'start_time':
                    activity_data['start_time'] = data.value
                elif data.name == 'total_timer_time':
                    activity_data['duration'] = data.value
                elif data.name == 'total_distance':
                    activity_data['distance'] = data.value
                elif data.name == 'total_calories':
                    activity_data['calories'] = data.value
                elif data.name == 'enhanced_max_speed' or data.name == 'max_speed':
                    activity_data['max_speed'] = data.value
                elif data.name == 'enhanced_avg_speed' or data.name == 'avg_speed':
                    activity_data['avg_speed'] = data.value
                elif data.name == 'max_heart_rate':
                    activity_data['max_heart_rate'] = data.value
                elif data.name == 'avg_heart_rate':
                    activity_data['avg_heart_rate'] = data.value
                elif data.name == 'max_cadence':
                    activity_data['max_cadence'] = data.value
                elif data.name == 'avg_cadence':
                    activity_data['avg_cadence'] = data.value
                elif data.name == 'max_power':
                    activity_data['max_power'] = data.value
                elif data.name == 'avg_power':
                    activity_data['avg_power'] = data.value
                elif data.name == 'normalized_power':
                    activity_data['normalized_power'] = data.value
                elif data.name == 'total_ascent':
                    activity_data['elevation_gain'] = data.value
        
        return activity_data
    
    def validate(self):
        if not self.fit_file:
            return False
        try:
            messages = list(self.fit_file.get_messages('session'))
            return len(messages) > 0
        except Exception as e:
            print(f"Invalid FIT file: {e}")
            return False
