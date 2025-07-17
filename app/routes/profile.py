from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.notifications import get_notification_preferences, set_notification_preference
from app.models.notification import NotificationType
from app.models import User

bp = Blueprint('profile', __name__)

__all__ = ['bp']


@bp.route('/profile')
def index():
    return render_template('profile/index.html')

@bp.route('/profile/<int:user_id>')
def view(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template('profile/view.html', user=user)

@bp.route('/preferences/notifications', methods=['GET', 'POST'])
@login_required
def notification_preferences():
    if request.method == 'POST':
        for notif_type in NotificationType:
            enabled = request.form.get(f'enabled_{notif_type.value}') == '1'
            set_notification_preference(current_user.id, notif_type, enabled)
        flash('Notification preferences updated.', 'success')
        return redirect(url_for('profile.notification_preferences'))
    preferences = get_notification_preferences(current_user.id)
    return render_template('profile/preferences.html', preferences=preferences)
