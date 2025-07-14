from flask import render_template, Blueprint
from flask_login import current_user
from app.models import News, Event

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    # Get latest news
    news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    
    # Get upcoming events
    from datetime import datetime
    events = Event.query.filter(Event.event_date >= datetime.utcnow()).order_by(Event.event_date.asc()).limit(3).all()
    
    # Placeholder stats, replace with actual queries
    stats = {
        'total_alumni': 500000
    }
    
    return render_template('index.html', title='Home', news=news, events=events, stats=stats)
