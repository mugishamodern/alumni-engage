from flask import Blueprint, render_template

bp = Blueprint('contacts', __name__)

__all__ = ['bp']

@bp.route('/contacts')
def index():
    return render_template('contacts/index.html')
