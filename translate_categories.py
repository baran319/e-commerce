"""
One-time script to translate category names in the DB from Turkish to English.
Run with: venv\Scripts\python.exe translate_categories.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.product import Category

app = create_app()

# Mapping: Turkish name → English name
TRANSLATIONS = {
    'Protein': 'Protein',
    'Kreatin': 'Creatine',
    'Pre-Workout': 'Pre-Workout',
    'Amino Asitler': 'Amino Acids',
    'Vitaminler': 'Vitamins',
    'Yağ Yakıcılar': 'Fat Burners',
    'Karbonhidrat': 'Carbohydrates',
    'Kilo Alma': 'Mass Gainers',
    'Aksesuar': 'Accessories',
    'Spor Gıda': 'Sports Food',
    'Omega 3': 'Omega 3',
    'Kollajen': 'Collagen',
    'BCAA': 'BCAA',
    'Glutamine': 'Glutamine',
    'Glutamin': 'Glutamine',
    'Multivitamin': 'Multivitamin',
    'Spor Kıyafet': 'Sportswear',
}

with app.app_context():
    cats = Category.query.all()
    changed = 0
    for cat in cats:
        en = TRANSLATIONS.get(cat.name)
        if en and en != cat.name:
            print(f"  {cat.name!r} → {en!r}")
            cat.name = en
            changed += 1
    db.session.commit()
    print(f"\nDone. {changed} categories updated.")
