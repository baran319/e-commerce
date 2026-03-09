from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.product import Product, Category
from app.models.order import Order
from app.models.user import User
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_products': db.session.query(Product).count(),
        'total_orders': db.session.query(Order).count(),
        'total_users': db.session.query(User).count(),
        'pending_orders': db.session.query(Order).filter_by(status='pending').count(),
    }
    recent_orders = db.session.execute(
        db.select(Order).order_by(Order.created_at.desc()).limit(10)
    ).scalars().all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    prods = db.paginate(
        db.select(Product).order_by(Product.created_at.desc()),
        page=page,
        per_page=20
    )
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template('admin/products.html', products=prods, categories=categories)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    categories = db.session.execute(db.select(Category)).scalars().all()
# ... rest of the file ...
    if request.method == 'POST':
        f = request.form
        product = Product(
            name=f.get('name'),
            slug=f.get('slug'),
            description=f.get('description'),
            short_description=f.get('short_description'),
            price=float(f.get('price', 0)),
            original_price=float(f.get('original_price')) if f.get('original_price') else None,
            stock=int(f.get('stock', 0)),
            brand=f.get('brand'),
            weight=f.get('weight'),
            flavor=f.get('flavor'),
            image_url=f.get('image_url'),
            badge=f.get('badge'),
            is_featured=f.get('is_featured') == 'on',
            category_id=int(f.get('category_id'))
        )
        db.session.add(product)
        db.session.commit()
        flash('Ürün eklendi!', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=None, categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = db.get_or_404(Product, product_id)
    categories = db.session.execute(db.select(Category)).scalars().all()
    if request.method == 'POST':
        f = request.form
        product.name = f.get('name')
        product.slug = f.get('slug')
        product.description = f.get('description')
        product.short_description = f.get('short_description')
        product.price = float(f.get('price', 0))
        product.original_price = float(f.get('original_price')) if f.get('original_price') else None
        product.stock = int(f.get('stock', 0))
        product.brand = f.get('brand')
        product.weight = f.get('weight')
        product.flavor = f.get('flavor')
        product.image_url = f.get('image_url')
        product.badge = f.get('badge')
        product.is_featured = f.get('is_featured') == 'on'
        product.category_id = int(f.get('category_id'))
        product.is_active = f.get('is_active') == 'on'
        db.session.commit()
        flash('Ürün güncellendi!', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin/product_form.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    product.is_active = False
    db.session.commit()
    flash('Ürün pasif yapıldı.', 'info')
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    stmt = db.select(Order).order_by(Order.created_at.desc())
    if status:
        stmt = stmt.filter_by(status=status)
    all_orders = db.paginate(stmt, page=page, per_page=20)
    return render_template('admin/orders.html', orders=all_orders, selected_status=status)

@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    new_status = request.form.get('status')
    valid = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if new_status in valid:
        order.status = new_status
        db.session.commit()
        flash(f'Sipariş #{order.id} durumu güncellendi.', 'success')
    return redirect(url_for('admin.orders'))
