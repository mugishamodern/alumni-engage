from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    
    login.login_view = 'auth.login'
    login.login_message_category = 'info'
    
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')
    
    from app.routes.news import bp as news_bp
    app.register_blueprint(news_bp, url_prefix='/news')
    
    from app.routes.events import bp as events_bp
    app.register_blueprint(events_bp, url_prefix='/events')
    
    from app.routes.directory import bp as directory_bp
    app.register_blueprint(directory_bp, url_prefix='/directory')
    
    from app.routes.jobs import bp as jobs_bp
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.routes.contacts import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')
    
    return app

from app import models
