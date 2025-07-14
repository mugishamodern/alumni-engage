from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import User, News, Event, Job, Testimonial, ContactSubmission
from app.utils.decorators import admin_required

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
    
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                           user_count=user_count, event_count=event_count,
                           job_count=job_count, testimonial_count=testimonial_count,
                           pending_jobs=pending_jobs, pending_testimonials=pending_testimonials,
                           unread_contacts=unread_contacts)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_users.html', title='Manage Users', users=users)

@bp.route('/events')
@login_required
@admin_required
def manage_events():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date.desc()).paginate(
        page=page, per_page=current_app.config['EVENTS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_events.html', title='Manage Events', events=events)

# Similar routes for managing news, jobs, testimonials, and contact submissions