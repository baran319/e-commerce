from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.order import Order

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def profile():
    return render_template('profile/profile.html')

@profile_bp.route('/orders')
@login_required
def orders():
    stmt = db.select(Order).filter_by(user_id=current_user.id).order_by(Order.created_at.desc())
    user_orders = db.session.execute(stmt).scalars().all()
    return render_template('profile/orders.html', orders=user_orders)

@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    current_user.first_name = request.form.get('first_name', '').strip()
    current_user.last_name = request.form.get('last_name', '').strip()
    current_user.phone = request.form.get('phone', '').strip()
    current_user.address = request.form.get('address', '').strip()
    db.session.commit()
    flash('Profiliniz güncellendi.', 'success')
    return redirect(url_for('profile.profile'))
