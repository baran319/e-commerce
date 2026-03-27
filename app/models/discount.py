from app.extensions import db
from datetime import datetime

class DiscountCode(db.Model):
    __tablename__ = 'discount_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DiscountCode {self.code} ({self.discount_percent}%)>'
