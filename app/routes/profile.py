from flask import Blueprint, render_template

bp = Blueprint('profile', __name__)

__all__ = ['bp']

@bp.route('/profile')
def index():
    return render_template('profile/index.html')
