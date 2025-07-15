from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.event import Event
from app.models.job import Job
from app.models.testimonial import Testimonial
from app.models.contact import ContactSubmission
from app.models.message import Message
from sqlalchemy import or_, and_, desc

bp = Blueprint('messages', __name__, url_prefix='/messages')

@bp.route('/inbox')
@login_required
def inbox():
    # Get all users who have sent or received messages with current user
    user_ids = set()
    messages = Message.query.filter(or_(Message.sender_id==current_user.id, Message.recipient_id==current_user.id)).all()
    for m in messages:
        if m.sender_id != current_user.id:
            user_ids.add(m.sender_id)
        if m.recipient_id != current_user.id:
            user_ids.add(m.recipient_id)
    # For each user, get the latest message in the conversation
    conversations = []
    for uid in user_ids:
        latest = Message.query.filter(
            or_(
                and_(Message.sender_id==current_user.id, Message.recipient_id==uid),
                and_(Message.sender_id==uid, Message.recipient_id==current_user.id)
            )
        ).order_by(desc(Message.sent_at)).first()
        if latest:
            conversations.append(latest)
    # Sort conversations by latest message
    conversations.sort(key=lambda m: m.sent_at, reverse=True)
    if getattr(current_user, 'is_admin', False):
        user_count = User.query.count()
        event_count = Event.query.count()
        job_count = Job.query.filter_by(is_approved=True).count()
        testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
        pending_jobs = Job.query.filter_by(is_approved=False).count()
        pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
        unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
        unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
        users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            user_count=user_count,
            event_count=event_count,
            job_count=job_count,
            testimonial_count=testimonial_count,
            pending_jobs=pending_jobs,
            pending_testimonials=pending_testimonials,
            unread_contacts=unread_contacts,
            unread_messages=unread_messages,
            users_for_messaging=users_for_messaging,
            conversations=conversations,
            show_inbox_in_content=True
        )
    else:
        return render_template('messages/inbox.html', conversations=conversations)

@bp.route('/sent')
@login_required
def sent():
    messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.sent_at.desc()).all()
    if getattr(current_user, 'is_admin', False):
        user_count = User.query.count()
        event_count = Event.query.count()
        job_count = Job.query.filter_by(is_approved=True).count()
        testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
        pending_jobs = Job.query.filter_by(is_approved=False).count()
        pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
        unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
        unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
        users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            user_count=user_count,
            event_count=event_count,
            job_count=job_count,
            testimonial_count=testimonial_count,
            pending_jobs=pending_jobs,
            pending_testimonials=pending_testimonials,
            unread_contacts=unread_contacts,
            unread_messages=unread_messages,
            users_for_messaging=users_for_messaging,
            sent_messages=messages,
            show_sent_in_content=True
        )
    else:
        return render_template('messages/sent.html', messages=messages)

@bp.route('/compose/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def compose(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        if not subject or not content:
            flash('Subject and content are required.', 'danger')
        else:
            message = Message(
                sender_id=current_user.id,
                recipient_id=recipient.id,
                subject=subject,
                content=content
            )
            db.session.add(message)
            db.session.commit()
            flash('Message sent!', 'success')
            return redirect(url_for('messages.sent'))
    if getattr(current_user, 'is_admin', False):
        user_count = User.query.count()
        event_count = Event.query.count()
        job_count = Job.query.filter_by(is_approved=True).count()
        testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
        pending_jobs = Job.query.filter_by(is_approved=False).count()
        pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
        unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
        unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
        users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            user_count=user_count,
            event_count=event_count,
            job_count=job_count,
            testimonial_count=testimonial_count,
            pending_jobs=pending_jobs,
            pending_testimonials=pending_testimonials,
            unread_contacts=unread_contacts,
            unread_messages=unread_messages,
            users_for_messaging=users_for_messaging,
            compose_recipient=recipient,
            show_compose_in_content=True
        )
    else:
        return render_template('messages/compose.html', recipient=recipient)

@bp.route('/conversation/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    thread_messages = Message.query.filter(
        or_(
            and_(Message.sender_id==current_user.id, Message.recipient_id==user_id),
            and_(Message.sender_id==user_id, Message.recipient_id==current_user.id)
        )
    ).order_by(Message.sent_at.asc()).all()
    for msg in thread_messages:
        if msg.recipient_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')
        if not subject or not content:
            flash('Subject and content are required.', 'danger')
        else:
            message = Message(
                sender_id=current_user.id,
                recipient_id=other_user.id,
                subject=subject,
                content=content
            )
            db.session.add(message)
            db.session.commit()
            flash('Reply sent!', 'success')
            return redirect(url_for('messages.conversation', user_id=other_user.id))
    if getattr(current_user, 'is_admin', False):
        user_count = User.query.count()
        event_count = Event.query.count()
        job_count = Job.query.filter_by(is_approved=True).count()
        testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
        pending_jobs = Job.query.filter_by(is_approved=False).count()
        pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
        unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
        unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
        users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            user_count=user_count,
            event_count=event_count,
            job_count=job_count,
            testimonial_count=testimonial_count,
            pending_jobs=pending_jobs,
            pending_testimonials=pending_testimonials,
            unread_contacts=unread_contacts,
            unread_messages=unread_messages,
            users_for_messaging=users_for_messaging,
            conversation_user=other_user,
            thread_messages=thread_messages,
            show_conversation_in_content=True
        )
    else:
        return render_template('messages/conversation.html', other_user=other_user, messages=thread_messages)

@bp.route('/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.recipient_id != current_user.id and message.sender_id != current_user.id:
        flash('You do not have permission to view this message.', 'danger')
        return redirect(url_for('messages.inbox'))
    if message.recipient_id == current_user.id and not message.is_read:
        message.is_read = True
        db.session.commit()
    if getattr(current_user, 'is_admin', False):
        user_count = User.query.count()
        event_count = Event.query.count()
        job_count = Job.query.filter_by(is_approved=True).count()
        testimonial_count = Testimonial.query.filter_by(is_approved=True).count()
        pending_jobs = Job.query.filter_by(is_approved=False).count()
        pending_testimonials = Testimonial.query.filter_by(is_approved=False).count()
        unread_contacts = ContactSubmission.query.filter_by(is_read=False).count()
        unread_messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
        users_for_messaging = User.query.filter(User.id != current_user.id).order_by(User.first_name.asc()).all()
        return render_template(
            'admin/dashboard.html',
            title='Admin Dashboard',
            user_count=user_count,
            event_count=event_count,
            job_count=job_count,
            testimonial_count=testimonial_count,
            pending_jobs=pending_jobs,
            pending_testimonials=pending_testimonials,
            unread_contacts=unread_contacts,
            unread_messages=unread_messages,
            users_for_messaging=users_for_messaging,
            view_message=message,
            show_view_in_content=True
        )
    else:
        return render_template('messages/view.html', message=message)

@bp.route('/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('You do not have permission to delete this message.', 'danger')
        return redirect(url_for('messages.inbox'))
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('messages.inbox')) 