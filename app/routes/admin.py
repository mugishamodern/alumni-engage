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
    # Recent users (last 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    # Upcoming events (next 5)
    from datetime import datetime
    upcoming_events = Event.query.filter(Event.event_date >= datetime.utcnow()).order_by(Event.event_date.asc()).limit(5).all()
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                       user_count=user_count, event_count=event_count,
                       job_count=job_count, testimonial_count=testimonial_count,
                       pending_jobs=pending_jobs, pending_testimonials=pending_testimonials,
                       unread_contacts=unread_contacts, unread_messages=unread_messages,
                       users_for_messaging=users_for_messaging,
                       recent_users=recent_users, upcoming_events=upcoming_events)

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

@bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    from app.utils.forms import EventForm
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin.manage_events'))
    return render_template('events/create.html', title='Edit Event', form=form, event=event)

@bp.route('/events/<int:event_id>/delete')
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted.', 'success')
    return redirect(url_for('admin.manage_events'))

@bp.route('/jobs')
@login_required
@admin_required
def manage_jobs():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=current_app.config['JOBS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_jobs.html', title='Manage Jobs', jobs=jobs)

@bp.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    from app.utils.forms import JobForm
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()
        flash('Job updated successfully.', 'success')
        return redirect(url_for('admin.manage_jobs'))
    return render_template('jobs/create.html', title='Edit Job', form=form, job=job)

@bp.route('/jobs/<int:job_id>/delete')
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job has been deleted.', 'success')
    return redirect(url_for('admin.manage_jobs'))

@bp.route('/testimonials')
@login_required
@admin_required
def manage_testimonials():
    page = request.args.get('page', 1, type=int)
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/manage_testimonials.html', title='Manage Testimonials', testimonials=testimonials)

@bp.route('/contact_submissions')
@login_required
@admin_required
def contact_submissions():
    page = request.args.get('page', 1, type=int)
    contacts = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/contact_submissions.html', title='Contact Submissions', contacts=contacts)

# Similar routes for managing news, jobs, testimonials, and contact submissions
