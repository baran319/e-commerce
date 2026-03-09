from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.cart import CartItem
from app.models.product import Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
@login_required
def view_cart():
    items = db.session.execute(
        db.select(CartItem).filter_by(user_id=current_user.id)
    ).scalars().all()
    total = sum(item.subtotal for item in items)
    return render_template('cart/cart.html', items=items, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = db.get_or_404(Product, product_id)
    quantity = int(request.form.get('quantity', 1))
    
    item = db.session.execute(
        db.select(CartItem).filter_by(user_id=current_user.id, product_id=product.id)
    ).scalar_one_or_none()
    
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(item)
    
    db.session.commit()
    flash(f'{product.name} sepete eklendi.', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update', methods=['POST'])
@login_required
def update_cart():
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    item = db.get_or_404(CartItem, item_id)
    if item.user_id != current_user.id:
        abort(403)
        
    if quantity > 0:
        item.quantity = quantity
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        stmt = db.select(CartItem).filter_by(user_id=current_user.id)
        items = db.session.execute(stmt).scalars().all()
        cart_total = sum(i.subtotal for i in items)
        cart_count = sum(i.quantity for i in items)
        return jsonify({
            'success': True,
            'item_subtotal': item.subtotal,
            'cart_total': cart_total,
            'cart_count': cart_count
        })
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = db.get_or_404(CartItem, item_id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Ürün sepetten kaldırıldı.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    db.session.execute(db.delete(CartItem).filter_by(user_id=current_user.id))
    db.session.commit()
    return redirect(url_for('cart.view_cart'))
