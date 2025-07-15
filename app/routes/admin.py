from flask import render_template, redirect, url_for, flash, request, Blueprint, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, News, Event, Job, Testimonial, ContactSubmission
from app.utils.decorators import admin_required
from app.models.message import Message

bp = Blueprint('admin', __name__)

@bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    user_count = User.query.count()
    event_count = Event.query.count()
    job_count = Job.query.filter_by(is_approved=True).count()
    testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
    
    # Get pending items
    pending_jobs = Job.query.filter_by(is_approved=False).count()
    pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
    unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
    # Unread messages for current user
    unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
    # List of users for admin to message (exclude self)
    users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                           user_count=user_count, event_count=event_count,
                           job_count=job_count, testimonial_count=testimonial_count,
                           pending_jobs=pending_jobs, pending_testimonials=pending_testimonials,
                           unread_contacts=unread_contacts, unread_messages=unread_messages,
                           users_for_messaging=users_for_messaging)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_users.html', title='Manage Users', users=users)

@bp.route('/users/<int:user_id>/deactivate')
@login_required
@admin_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_active:
        user.is_active = False
        db.session.commit()
        flash(f'User {user.first_name} {user.last_name} has been deactivated.', 'success')
    else:
        flash(f'User {user.first_name} {user.last_name} is already deactivated.', 'info')
    return redirect(url_for('admin.manage_users'))

@bp.route('/users/<int:user_id>/activate')
@login_required
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user.is_active:
        user.is_active = True
        db.session.commit()
        flash(f'User {user.first_name} {user.last_name} has been activated.', 'success')
    else:
        flash(f'User {user.first_name} {user.last_name} is already active.', 'info')
    return redirect(url_for('admin.manage_users'))

@bp.route('/users/<int:user_id>/delete')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.first_name} {user.last_name} has been deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

@bp.route('/events')
@login_required
@admin_required
def manage_events():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date.desc()).paginate(
        page=page, per_page=current_app.config['EVENTS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_events.html', title='Manage Events', events=events)

# Similar routes for managing news, jobs, testimonials, and contact submissions
