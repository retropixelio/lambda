import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET = os.environ.get('SECRET', 'fake-token')