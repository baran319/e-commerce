from flask import Blueprint, render_template
from app.models.product import Product, Category
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured = db.session.execute(
        db.select(Product).filter_by(is_featured=True, is_active=True).limit(8)
    ).scalars().all()
    categories = db.session.execute(db.select(Category)).scalars().all()
    bestsellers = db.session.execute(
        db.select(Product).filter_by(is_active=True, badge='BESTSELLER').limit(4)
    ).scalars().all()
    new_arrivals = db.session.execute(
        db.select(Product).filter_by(is_active=True, badge='NEW').limit(4)
    ).scalars().all()
    return render_template('index.html',
                           featured_products=featured,
                           categories=categories,
                           bestsellers=bestsellers,
                           new_arrivals=new_arrivals)

@main_bp.route('/about')
def about():
    return render_template('about.html')
