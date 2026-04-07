import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'public', 'data')
DATABASE_FILE = os.path.join(OUTPUT_DIR, 'data.db')
JSON_FILE = os.path.join(OUTPUT_DIR, 'data.json')

os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPORTED_TYPES = {
    'running': 'running',
    'cycling': 'cycling',
    'swimming': 'swimming',
    'walking': 'walking',
    'hiking': 'hiking',
    'generic': 'other'
}

SPORT_TYPE_MAPPING = {
    'running': 'running',
    'cycling': 'cycling',
    'swimming': 'swimming',
    'walking': 'walking',
    'hiking': 'hiking',
    'generic': 'other',
    'fitness_equipment': 'other',
    'bouldering': 'other',
    'elliptical': 'other',
    'indoor_cycling': 'cycling',
    'recumbent_cycling': 'cycling',
    'mountain_biking': 'cycling',
    'treadmill_running': 'running',
    'track_cycling': 'cycling',
    'road_biking': 'cycling',
    'open_water_swimming': 'swimming',
    'pool_swimming': 'swimming',
    'virtual_run': 'running',
    'indoor_running': 'running'
}
