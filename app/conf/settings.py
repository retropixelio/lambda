from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET = config('SECRET')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default="")
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default="")