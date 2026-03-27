import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.discount import DiscountCode

app = create_app()

def add_discount():
    with app.app_context():
        db.create_all()
        code = db.session.execute(db.select(DiscountCode).filter_by(code='SUMMER20')).scalar_one_or_none()
        if not code:
            code = DiscountCode(code='SUMMER20', discount_percent=20)
            db.session.add(code)
            db.session.commit()
            print("Discount code SUMMER20 added successfully!")
        else:
            print("Discount code SUMMER20 already exists.")

if __name__ == '__main__':
    add_discount()
