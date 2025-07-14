from flask import Blueprint, render_template

bp = Blueprint('profile', __name__)

__all__ = ['bp']

from flask import render_template, abort
from app.models import User

@bp.route('/profile')
def index():
    return render_template('profile/index.html')

@bp.route('/profile/<int:user_id>')
def view(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template('profile/view.html', user=user)
