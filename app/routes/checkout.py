from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem

checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/', methods=['GET', 'POST'])
@login_required
def checkout():
    items = db.session.execute(
        db.select(CartItem).filter_by(user_id=current_user.id)
    ).scalars().all()
    if not items:
        flash('Sepetiniz boş.', 'warning')
        return redirect(url_for('cart.view_cart'))

    total = sum(item.subtotal for item in items)
    shipping = 0 if total >= 500 else 29.90
    grand_total = round(total + shipping, 2)
    grand_total = total + shipping

    if request.method == 'POST':
        f = request.form
        order = Order(
            user_id=current_user.id,
            total_price=grand_total,
            shipping_name=f.get('shipping_name'),
            shipping_address=f.get('shipping_address'),
            shipping_city=f.get('shipping_city'),
            shipping_phone=f.get('shipping_phone'),
            note=f.get('note')
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            oi = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            item.product.stock = max(0, item.product.stock - item.quantity)
            db.session.add(oi)
            db.session.delete(item)

        db.session.commit()
        return redirect(url_for('checkout.confirmation', order_id=order.id))

    return render_template('checkout/checkout.html', 
                           items=items, total=total, 
                           shipping=shipping, grand_total=grand_total)

@checkout_bp.route('/confirmation/<int:order_id>')
@login_required
def confirmation(order_id):
    order = db.get_or_404(Order, order_id)
    if order.user_id != current_user.id:
        abort(403)
    return render_template('checkout/confirmation.html', order=order)
