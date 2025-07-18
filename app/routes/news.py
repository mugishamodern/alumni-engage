from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import News
from app.utils.notifications import create_notification
from app.models.notification import NotificationType

bp = Blueprint('news', __name__)

@bp.route('/news')
def index():
    news_list = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).all()
    return render_template('news/index.html', news_list=news_list)

@bp.route('/news/<int:id>')
def detail(id):
    news_item = News.query.get_or_404(id)
    return render_template('news/detail.html', news=news_item)

@bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        summary = request.form.get('summary')
        image_url = request.form.get('image_url')
        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('news.add'))
        news_item = News(
            title=title,
            content=content,
            summary=summary,
            image_url=image_url,
            author_id=current_user.id,
            is_published=True
        )
        db.session.add(news_item)
        db.session.commit()
        # Create notification for news post
        create_notification(
            user_id=current_user.id,
            message=f"You published a news article: {news_item.title}.",
            notif_type=NotificationType.NEWS,
            link=url_for('news.detail', id=news_item.id)
        )
        flash('News article added successfully.', 'success')
        return redirect(url_for('news.index'))
    return render_template('news/add.html')
