from app import db
from app.models import Notification, NotificationPreference, User
from app.models.notification import NotificationType
from datetime import datetime

def create_notification(user_id, message, notif_type, link=None):
    # Check user preference
    pref = NotificationPreference.query.filter_by(user_id=user_id, type=notif_type.value).first()
    if pref and not pref.enabled:
        return None
    notif = Notification(
        user_id=user_id,
        message=message,
        type=notif_type.value,
        is_read=False,
        created_at=datetime.utcnow(),
        link=link
    )
    db.session.add(notif)
    db.session.commit()
    return notif

def mark_notification_as_read(notification_id, user_id):
    notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notif:
        notif.is_read = True
        db.session.commit()
        return True
    return False

def get_unseen_notification_count(user_id):
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()

def get_latest_notifications(user_id, limit=5):
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(limit).all()

def set_notification_preference(user_id, notif_type, enabled):
    pref = NotificationPreference.query.filter_by(user_id=user_id, type=notif_type.value).first()
    if pref:
        pref.enabled = enabled
    else:
        pref = NotificationPreference(user_id=user_id, type=notif_type.value, enabled=enabled)
        db.session.add(pref)
    db.session.commit()
    return pref

def get_notification_preferences(user_id):
    prefs = NotificationPreference.query.filter_by(user_id=user_id).all()
    # Ensure all types are present
    existing_types = {p.type for p in prefs}
    for notif_type in NotificationType:
        if notif_type.value not in existing_types:
            pref = NotificationPreference(user_id=user_id, type=notif_type.value, enabled=True)
            db.session.add(pref)
            prefs.append(pref)
    db.session.commit()
    return prefs 