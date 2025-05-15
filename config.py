import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///timeless_echoes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)