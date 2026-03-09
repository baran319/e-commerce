from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='🏋️')
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)  # For showing discount
    stock = db.Column(db.Integer, default=0)
    brand = db.Column(db.String(100))
    weight = db.Column(db.String(50))   # e.g. "1kg", "2kg"
    flavor = db.Column(db.String(100))  # e.g. "Chocolate, Vanilla, Strawberry"
    image_url = db.Column(db.String(500))
    image_url_2 = db.Column(db.String(500))
    badge = db.Column(db.String(50))    # e.g. "NEW", "BESTSELLER", "SALE"
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    reviews = db.relationship('Review', backref='product', lazy='dynamic')

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    def __repr__(self):
        return f'<Product {self.name}>'
