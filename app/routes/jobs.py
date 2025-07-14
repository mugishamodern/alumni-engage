from flask import Blueprint, render_template

bp = Blueprint('jobs', __name__)

__all__ = ['bp']

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Job
from app import db

@bp.route('/jobs')
@login_required
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs/index.html', jobs=jobs)

@bp.route('/jobs/<int:id>')
@login_required
def detail(id):
    job = Job.query.get_or_404(id)
    return render_template('jobs/detail.html', job=job)

from flask import request, flash
from app.utils.forms import JobForm

@bp.route('/jobs/create', methods=['GET', 'POST'])
@login_required
def create():
    import logging
    logger = logging.getLogger(__name__)
    form = JobForm()
    if form.validate_on_submit():
        try:
            job = Job(
                title=form.title.data,
                company=form.company.data,
                location=form.location.data,
                job_type=form.job_type.data,
                description=form.description.data,
                requirements=form.requirements.data,
                salary_range=form.salary_range.data,
                application_url=form.application_url.data,
                contact_email=form.contact_email.data,
                deadline=form.deadline.data,
                posted_by=current_user.id,
                is_approved=False,
                is_active=True
            )
            db.session.add(job)
            db.session.commit()
            flash('Job posting created successfully.', 'success')
            logger.info(f"Job created: {job.title} by user {current_user.username}")
            return redirect(url_for('jobs.index'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating job: {e}")
            flash('An error occurred while creating the job posting. Please try again.', 'danger')
    return render_template('jobs/create.html', form=form)
