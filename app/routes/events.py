from flask import render_template, redirect, url_for, flash, request, Blueprint, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Event, RSVP
from app.utils.forms import EventForm, RSVPForm
from app.utils.decorators import admin_required
from app.utils.notifications import create_notification
from app.models.notification import NotificationType

bp = Blueprint('events', __name__)

@bp.route('/')
def event_list():
    page = request.args.get('page', 1, type=int)
    past = request.args.get('past', False, type=bool)
    
    query = Event.query
    
    if past:
        from datetime import datetime
        query = query.filter(Event.event_date < datetime.utcnow())
    else:
        from datetime import datetime
        query = query.filter(Event.event_date >= datetime.utcnow())
    
    events = query.order_by(Event.event_date.asc()).paginate(
        page=page, per_page=current_app.config['EVENTS_PER_PAGE'], error_out=False)
    
    return render_template('events/list.html', title='Events', events=events, past=past)

@bp.route('/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    form = RSVPForm(request.form)
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to RSVP for events', 'warning')
            return redirect(url_for('auth.login'))
        
        rsvp = RSVP.query.filter_by(user_id=current_user.id, event_id=event.id).first()
        if rsvp:
            rsvp.status = form.status.data
            rsvp.notes = form.notes.data if hasattr(form, 'notes') else None
        else:
            rsvp = RSVP(
                user_id=current_user.id,
                event_id=event.id,
                status=form.status.data,
                notes=form.notes.data if hasattr(form, 'notes') else None
            )
            db.session.add(rsvp)
        db.session.commit()
        # Create notification for RSVP
        create_notification(
            user_id=current_user.id,
            message=f"You RSVP'd to {event.title} as {form.status.data}.",
            notif_type=NotificationType.RSVP,
            link=url_for('events.event_detail', event_id=event.id)
        )
        # Notify event organizer if not the same as RSVP-ing user
        if event.created_by != current_user.id:
            from app.models.user import User
            organizer = User.query.get(event.created_by)
            if organizer:
                create_notification(
                    user_id=organizer.id,
                    message=f"{current_user.first_name} {current_user.last_name} RSVP'd to your event: {event.title} as {form.status.data}.",
                    notif_type=NotificationType.EVENT,
                    link=url_for('events.event_detail', event_id=event.id)
                )
        flash('Your RSVP has been updated', 'success')
        return redirect(url_for('events.event_detail', event_id=event.id))
    
    # Pre-fill form if user has already RSVP'd
    if current_user.is_authenticated:
        rsvp = RSVP.query.filter_by(user_id=current_user.id, event_id=event.id).first()
        if rsvp:
            form.status.data = rsvp.status
            form.notes.data = rsvp.notes
    
    # Get RSVP counts
    attending = RSVP.query.filter_by(event_id=event.id, status='attending').count()
    not_attending = RSVP.query.filter_by(event_id=event.id, status='not_attending').count()
    maybe = RSVP.query.filter_by(event_id=event.id, status='maybe').count()
    
    return render_template('events/detail.html', title=event.title, event=event, 
                          form=form, attending=attending, not_attending=not_attending, maybe=maybe)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            venue=form.venue.data,
            max_attendees=form.max_attendees.data,
            created_by=current_user.id
        )
        try:
            db.session.add(event)
            db.session.commit()
            # Notify all users except the creator
            from app.models.user import User
            users = User.query.filter(User.id != current_user.id).all()
            for user in users:
                create_notification(
                    user_id=user.id,
                    message=f"New event created: {event.title}.",
                    notif_type=NotificationType.EVENT,
                    link=url_for('events.event_detail', event_id=event.id)
                )
            flash('Event created successfully!', 'success')
            return redirect(url_for('events.event_detail', event_id=event.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving event: {str(e)}', 'danger')
    else:
        if form.errors:
            flash(f'Form validation errors: {form.errors}', 'danger')
    return render_template('events/create.html', title='Create Event', form=form)

@bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.venue = form.venue.data
        event.max_attendees = form.max_attendees.data
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.event_detail', event_id=event.id))
    return render_template('events/edit.html', title='Edit Event', form=form, event=event)

@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('events.event_list'))