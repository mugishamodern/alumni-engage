from flask import Blueprint, render_template

bp = Blueprint('contacts', __name__)

__all__ = ['bp']

from flask import render_template, request, flash, redirect, url_for
from app.utils.forms import ContactForm
from app.models import ContactSubmission
from app import db
import logging
from app.utils.notifications import create_notification
from app.models.notification import NotificationType

@bp.route('/contacts', methods=['GET', 'POST'])
def index():
    logger = logging.getLogger(__name__)
    form = ContactForm()
    if form.validate_on_submit():
        try:
            contact = ContactSubmission(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
                user_id=None  # Could be set if user is logged in
            )
            db.session.add(contact)
            db.session.commit()
            # Create notification for contact submission (if user is logged in)
            if contact.user_id:
                create_notification(
                    user_id=contact.user_id,
                    message=f"Your inquiry '{contact.subject}' was submitted.",
                    notif_type=NotificationType.CONTACT,
                    link=url_for('contacts.index')
                )
            flash('Your message has been sent successfully.', 'success')
            logger.info(f"New contact submission from {contact.name} ({contact.email})")
            return redirect(url_for('contacts.index'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving contact submission: {e}")
            flash('An error occurred while sending your message. Please try again.', 'danger')
    return render_template('contacts/index.html', form=form)
