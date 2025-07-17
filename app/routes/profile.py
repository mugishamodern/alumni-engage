import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.utils.notifications import get_notification_preferences, set_notification_preference
from app.models.notification import NotificationType
from app.models import User, Job, Event, Testimonial, News, Message, RSVP

bp = Blueprint('profile', __name__)

__all__ = ['bp']


@bp.route('/profile')
def index():
    user = current_user
    jobs = user.jobs_posted.order_by(Job.created_at.desc()).limit(3)
    events = user.events_created.order_by(Event.created_at.desc()).limit(3)
    testimonials = user.testimonials.order_by(Testimonial.created_at.desc()).limit(3)
    news_posts = user.news_posts.order_by(News.created_at.desc()).limit(3)
    sent_messages = sorted(user.sent_messages, key=lambda m: m.sent_at, reverse=True)[:2]
    received_messages = sorted(user.received_messages, key=lambda m: m.sent_at, reverse=True)[:2]
    rsvps = user.rsvps.order_by(RSVP.rsvp_date.desc()).limit(3)
    return render_template(
        'profile/index.html',
        user=user,
        jobs=jobs,
        events=events,
        testimonials=testimonials,
        news_posts=news_posts,
        sent_messages=sent_messages,
        received_messages=received_messages,
        rsvps=rsvps
    )

@bp.route('/profile/<int:user_id>')
def view(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template('profile/view.html', user=user)

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = current_user
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        user.email = request.form.get('email', user.email)
        user.graduation_year = request.form.get('graduation_year', user.graduation_year)
        user.degree = request.form.get('degree', user.degree)
        user.current_job_title = request.form.get('current_job_title', user.current_job_title)
        user.location = request.form.get('location', user.location)
        user.bio = request.form.get('bio', user.bio)
        # Profile image upload handling
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Optionally, prepend user id or username to filename to avoid collisions
                filename = f"user_{user.id}_" + filename
                upload_path = os.path.join(UPLOAD_FOLDER)
                os.makedirs(upload_path, exist_ok=True)
                file.save(os.path.join(upload_path, filename))
                user.profile_image = filename
        from app import db
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.index'))
    return render_template('profile/edit.html', user=user)

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
