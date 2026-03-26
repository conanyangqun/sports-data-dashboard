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
    'generic': 'other'
}
