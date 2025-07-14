from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    graduation_year = db.Column(db.Integer)
    degree = db.Column(db.String(128))
    current_job_title = db.Column(db.String(128))
    location = db.Column(db.String(128))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    news_posts = db.relationship('News', backref='author', lazy='dynamic')
    events_created = db.relationship('Event', backref='creator', lazy='dynamic')
    rsvps = db.relationship('RSVP', backref='user', lazy='dynamic')
    jobs_posted = db.relationship('Job', backref='poster', lazy='dynamic')
    testimonials = db.relationship('Testimonial', backref='author', lazy='dynamic')
    contact_submissions = db.relationship('ContactSubmission', backref='submitter', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        from app import jwt
        return jwt.dumps({'user_id': self.id}, expires_in=expires_in)
    
    @staticmethod
    def verify_reset_password_token(token):
        from app import jwt
        try:
            user_id = jwt.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))