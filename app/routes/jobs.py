from flask import Blueprint, render_template

bp = Blueprint('jobs', __name__)

__all__ = ['bp']

@bp.route('/jobs')
def index():
    return render_template('jobs/index.html')
