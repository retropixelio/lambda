from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET = config('SECRET', cast=str)
PRIVATE_KEY = config('PRIVATE_KEY', cast=str)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', cast=str, default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str, default='')