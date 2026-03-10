from flask import Blueprint, render_template, request, abort
from app.models.product import Product, Category
from app.extensions import db

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def list_products():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category', '')
    brand = request.args.get('brand', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 9999, type=float)
    sort = request.args.get('sort', 'newest')
    search_query = request.args.get('q', '').strip()

    stmt = db.select(Product).filter_by(is_active=True)

    if category_slug:
        cat = db.session.execute(db.select(Category).filter_by(slug=category_slug)).scalar_one_or_none()
        if cat:
            stmt = stmt.filter_by(category_id=cat.id)

    if brand:
        stmt = stmt.filter_by(brand=brand)

    if search_query:
        stmt = stmt.filter(
            Product.name.ilike(f'%{search_query}%') |
            Product.description.ilike(f'%{search_query}%') |
            Product.brand.ilike(f'%{search_query}%')
        )

    stmt = stmt.filter(Product.price >= min_price, Product.price <= max_price)

    if sort == 'price_asc':
        stmt = stmt.order_by(Product.price.asc())
    elif sort == 'price_desc':
        stmt = stmt.order_by(Product.price.desc())
    elif sort == 'name':
        stmt = stmt.order_by(Product.name.asc())
    else:
        stmt = stmt.order_by(Product.created_at.desc())

    pagination = db.paginate(stmt, page=page, per_page=12, error_out=False)
    products = pagination.items
    categories = db.session.execute(db.select(Category)).scalars().all()
    
    unique_brands_stmt = db.select(Product.brand).filter(Product.brand != None, Product.brand != '').distinct()
    brands = db.session.execute(unique_brands_stmt).scalars().all()

    selected_category = db.session.execute(
        db.select(Category).filter_by(slug=category_slug)
    ).scalar_one_or_none() if category_slug else None

    return render_template('products/list.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           brands=brands,
                           selected_category=selected_category,
                           selected_brand=brand,
                           sort=sort,
                           search_query=search_query,
                           min_price=min_price,
                           max_price=max_price)

@products_bp.route('/product/<slug>')
def product_detail(slug):
    product = db.session.execute(
        db.select(Product).filter_by(slug=slug, is_active=True)
    ).scalar_one_or_none()
    if not product:
        abort(404)
        
    related_stmt = db.select(Product).filter_by(
        category_id=product.category_id, 
        is_active=True
    ).filter(Product.id != product.id).limit(4)
    related = db.session.execute(related_stmt).scalars().all()
    
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template('products/detail.html', product=product, related=related, categories=categories)

@products_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    return list_products()
