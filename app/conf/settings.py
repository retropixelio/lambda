from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET = config('SECRET', cast=str)
FIREBASE_CERTS = config('GOOGLE_CERTS', cast=str, default='https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')
FIREBASE_ID = config('FIREBASE_ID', cast=str, default='retropixel-62580')
PRIVATE_KEY = config('PRIVATE_KEY', cast=str)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', cast=str, default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str, default='')