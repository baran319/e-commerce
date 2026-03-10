from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()
with app.app_context():
    broken_1 = "https://images.unsplash.com/photo-1544991936-9464fa57a54a?w=600&q=80"
    broken_2 = "https://images.unsplash.com/photo-1550572017-edd951aa8ca6?w=600&q=80"
    
    fix_1 = "https://images.unsplash.com/photo-1594882645126-14020914d58d?w=600&q=80"
    fix_2 = "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80"

    products = db.session.execute(db.select(Product)).scalars().all()
    count = 0
    for p in products:
        if p.image_url == broken_1:
            p.image_url = fix_1
            count += 1
        elif p.image_url == broken_2:
            p.image_url = fix_2
            count += 1
    
    db.session.commit()
    print(f"Fixed {count} broken images.")
