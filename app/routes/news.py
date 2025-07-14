from flask import Blueprint, render_template

bp = Blueprint('news', __name__)

__all__ = ['bp']

@bp.route('/news')
def index():
    return render_template('news/index.html')
