from datetime import datetime

def time_ago(value):
    now = datetime.utcnow()
    diff = now - value
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} minutes ago"
    
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hours ago"
    
    days = hours / 24
    if days < 30:
        return f"{int(days)} days ago"
    
    months = days / 30
    if months < 12:
        return f"{int(months)} months ago"
    
    years = days / 365
    return f"{int(years)} years ago"

def init_app(app):
    app.jinja_env.filters['time_ago'] = time_ago