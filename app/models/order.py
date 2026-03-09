from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processing, shipped, delivered, cancelled
    total_price = db.Column(db.Float, nullable=False)
    shipping_name = db.Column(db.String(150))
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_phone = db.Column(db.String(20))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    STATUS_LABELS = {
        'pending': ('Beklemede', 'warning'),
        'processing': ('Hazırlanıyor', 'info'),
        'shipped': ('Kargoda', 'primary'),
        'delivered': ('Teslim Edildi', 'success'),
        'cancelled': ('İptal Edildi', 'danger'),
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, ('Bilinmiyor', 'secondary'))

    def __repr__(self):
        return f'<Order #{self.id} user={self.user_id} status={self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))  # snapshot at purchase time
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    @property
    def subtotal(self):
        return round(self.unit_price * self.quantity, 2)

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_id}>'
