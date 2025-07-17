from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from app.utils.notifications import get_latest_notifications, get_unseen_notification_count
from app.models import Notification

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('/api/latest')
@login_required
def api_latest():
    limit = int(request.args.get('limit', 5))
    notifs = get_latest_notifications(current_user.id, limit=limit)
    unseen_count = get_unseen_notification_count(current_user.id)
    return jsonify({
        'notifications': [
            {
                'id': n.id,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
                'link': n.link
            } for n in notifs
        ],
        'unseen_count': unseen_count
    })

@bp.route('/')
@login_required
def list_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications/list.html', notifications=notifs)
