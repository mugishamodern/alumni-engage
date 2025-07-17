from datetime import datetime
from enum import Enum
from app import db

class NotificationType(Enum):
    RSVP = 'rsvp'
    EVENT = 'event'
    JOB = 'job'
    TESTIMONIAL = 'testimonial'
    CONTACT = 'contact'
    NEWS = 'news'
    MESSAGE = 'message'
    SYSTEM = 'system'

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Store NotificationType.value
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String(255))

    def __repr__(self):
        return f'<Notification {self.type} to user {self.user_id}>'

class NotificationPreference(db.Model):
    __tablename__ = 'notification_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Store NotificationType.value
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<NotificationPreference {self.type} for user {self.user_id}>' 