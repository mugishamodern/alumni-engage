from datetime import datetime, timezone
from app import db

class RSVP(db.Model):
    __tablename__ = 'rsvps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'attending', 'not_attending', 'maybe'
    rsvp_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notes = db.Column(db.Text)
    
    # Unique constraint to ensure one RSVP per user per event
    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='unique_user_event'),
    )
    
    def __repr__(self):
        return f'<RSVP {self.user_id} for event {self.event_id}>'