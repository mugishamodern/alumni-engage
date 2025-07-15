from datetime import datetime, timezone
from app import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    event_image = db.Column(db.String(256))
    max_attendees = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship to RSVPs
    rsvps = db.relationship('RSVP', backref='event', lazy='dynamic')
    
    def __repr__(self):
        return f'<Event {self.title}>'