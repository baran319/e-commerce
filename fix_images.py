import os
import sys

# Ensure this is running from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.product import Product

app = create_app()

def fix_images():
    with app.app_context():
        products = db.session.execute(db.select(Product)).scalars().all()
        updated_count = 0
        
        for p in products:
            name_lower = p.name.lower()
            if 'whey' in name_lower or 'protein' in name_lower or 'bcaa' in name_lower or 'glutamin' in name_lower or 'amino' in name_lower or 'iso' in name_lower:
                p.image_url = 'https://images.unsplash.com/photo-1579722820308-d74e571900a9?w=600&q=80'
            elif 'creatine' in name_lower or 'kre-alkalyn' in name_lower or 'creapure' in name_lower:
                p.image_url = 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=600&q=80'
            elif 'pre-workout' in name_lower or 'c4' in name_lower or 'pulse' in name_lower or 'citrulline' in name_lower or 'ghost' in name_lower:
                p.image_url = 'https://images.unsplash.com/photo-1580086319619-3ed498161c77?w=600&q=80'
            elif 'vitamin' in name_lower or 'omega-3' in name_lower or 'zma' in name_lower or 'magnezyum' in name_lower:
                p.image_url = 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80'
            elif 'şeykır' in name_lower or 'eldiveni' in name_lower or 'direnç' in name_lower or 'wrap' in name_lower or 'roller' in name_lower:
                p.image_url = 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80'
            else:
                p.image_url = 'https://images.unsplash.com/photo-1564419320461-6870880221ad?w=600&q=80'
                
            updated_count += 1
            
        db.session.commit()
        print(f"Updated {updated_count} product images successfully!")

if __name__ == '__main__':
    fix_images()
