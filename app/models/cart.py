from app.extensions import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def subtotal(self):
        return round(self.product.price * self.quantity, 2)

    def __repr__(self):
        return f'<CartItem user={self.user_id} product={self.product_id} qty={self.quantity}>'
