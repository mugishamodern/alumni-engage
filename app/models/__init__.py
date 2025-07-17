# app/models/__init__.py

# Import all your models here to make them accessible
from .user import User
from .news import News
from .event import Event
from .rsvp import RSVP
from .job import Job
from .testimonial import Testimonial
from .contact import ContactSubmission
from .notification import Notification, NotificationPreference
from .message import Message

# Optional: For convenience in other parts of the app
__all__ = ['User', 'News', 'Event', 'RSVP', 'Job', 'Testimonial', 'ContactSubmission', 'Notification', 'NotificationPreference', 'Message']
