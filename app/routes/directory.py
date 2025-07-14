from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from app.models import User
from app import db

bp = Blueprint('directory', __name__)

@bp.route('/')
@login_required
def list_alumni():
    # Get query parameters
    search_query = request.args.get('q', '')
    graduation_year = request.args.get('year', type=int)
    program = None
    page = request.args.get('page', 1, type=int)
    
    # Start building query
    query = User.query.filter(User.is_active == True)
    
    # Apply filters
    if search_query:
        query = query.filter(
            (User.first_name.ilike(f'%{search_query}%')) |
            (User.last_name.ilike(f'%{search_query}%'))
        )
    
    if graduation_year:
        query = query.filter(User.graduation_year == graduation_year)
    
    if program:
        query = query.filter(User.degree.ilike(f'%{program}%'))
    
    # Order and paginate results
    alumni = query.order_by(User.last_name.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get unique graduation years for filter dropdown
    graduation_years = db.session.query(
        User.graduation_year
    ).distinct().filter(
        User.graduation_year != None
    ).order_by(
        User.graduation_year.desc()
    ).all()
    
    # Get unique programs for filter dropdown
    programs = db.session.query(
        User.degree
    ).distinct().filter(
        User.degree != None
    ).order_by(
        User.degree.asc()
    ).all()
    
    return render_template('directory/list.html', 
                          alumni=alumni,
                          graduation_years=graduation_years,
                          programs=programs,
                          search_query=search_query,
                          graduation_year=graduation_year,
                          program=program)