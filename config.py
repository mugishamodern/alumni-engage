import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost:3306/alumni_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    POSTS_PER_PAGE = 10
    EVENTS_PER_PAGE = 8
    JOBS_PER_PAGE = 6
    
    def __init__(self):
        # Log warnings for missing critical configurations
        if not self.MAIL_USERNAME:
            print("Warning: MAIL_USERNAME is not set")
        if not self.MAIL_PASSWORD:
            print("Warning: MAIL_PASSWORD is not set")
        if not self.MAIL_DEFAULT_SENDER:
            print("Warning: MAIL_DEFAULT_SENDER is not set")