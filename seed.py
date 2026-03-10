"""
FitMarket — Database Seeder
Seed 5 categories and 25+ sample products.
Run: python seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product, Category

app = create_app('development')

with app.app_context():
    db.create_all()

    # ── Clear existing data ──────────────────────────────────────
    Product.query.delete()
    Category.query.delete()
    User.query.filter_by(is_admin=True).delete()
    db.session.commit()

    # ── Categories ───────────────────────────────────────────────
    categories = [
        Category(name='Protein', slug='protein', description='Whey, Casein ve bitkisel protein tozları', icon='🥛'),
        Category(name='Kreatin', slug='kreatin', description='Güç ve hacim için kreatin takviyeleri', icon='💪'),
        Category(name='Pre-Workout', slug='pre-workout', description='Antrenman öncesi enerji ve odak', icon='⚡'),
        Category(name='Vitaminler', slug='vitaminler', description='Vitamin, mineral ve sağlık takviyeleri', icon='💊'),
        Category(name='Aksesuar', slug='aksesuar', description='Şeykır, bant, eldiven ve daha fazlası', icon='🎽'),
    ]
    for cat in categories:
        db.session.add(cat)
    db.session.flush()

    prot = Category.query.filter_by(slug='protein').first()
    kreat = Category.query.filter_by(slug='kreatin').first()
    pre = Category.query.filter_by(slug='pre-workout').first()
    vit = Category.query.filter_by(slug='vitaminler').first()
    acc = Category.query.filter_by(slug='aksesuar').first()

    # ── Products ─────────────────────────────────────────────────
    products = [
        # Protein
        Product(name='Gold Standard Whey Protein', slug='gold-standard-whey-protein',
                short_description='Dünyanın en çok satan whey proteini. %100 Whey, 24g protein / servis.',
                description='Optimum Nutrition Gold Standard Whey Protein, dünya genelinde milyonlarca sporcu tarafından tercih edilen, yüksek kaliteli whey protein izolat ve konsantresi karışımından oluşmaktadır. Her serviste 24g protein, 5.5g BCAA bulunmaktadır.',
                price=899.90, original_price=1199.90, stock=150, brand='Optimum Nutrition',
                weight='2.27kg (5 lb)', flavor='Çikolata, Vanilya, Çilek, Muz',
                image_url='https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=600&q=80',
                badge='BESTSELLER', is_featured=True, category_id=prot.id),

        Product(name='Dymatize ISO100 Whey Isolate', slug='dymatize-iso100-whey-isolate',
                short_description='%100 Whey Izolat. En saf protein. 25g protein / servis, 0g yağ.',
                description='Dymatize ISO100, hidrolize whey izolat ile üretilmiş, hızlı sindirim ve maksimum emilim sağlayan bir protein takviyelidir.',
                price=1249.90, original_price=1499.90, stock=80, brand='Dymatize',
                weight='1.6kg', flavor='Fudge Brownie, Gourmet Çikolata, Şeftali',
                image_url='https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&q=80',
                badge='NEW', is_featured=True, category_id=prot.id),

        Product(name='BSN Syntha-6 Protein Matrix', slug='bsn-syntha-6-protein-matrix',
                short_description='Çoklu protein kaynakları ile yavaş ve hızlı sindirilen protein matrisi.',
                description='BSN Syntha-6, 6 farklı protein kaynağı içeren, hem antrenman sonrası hem de öğünler arasında kullanılabilen ultra premium protein tozudur.',
                price=749.90, stock=200, brand='BSN',
                weight='2.27kg', flavor='Çikolata Milkshake, Vanilya, Cookies & Cream',
                image_url='https://images.unsplash.com/photo-1576426863848-c21f53c60b19?w=600&q=80',
                is_featured=True, category_id=prot.id),

        Product(name='MyProtein Impact Whey', slug='myprotein-impact-whey',
                short_description='Uygun fiyatıyla kaliteli whey proteini. 21g protein / servis.',
                description='MyProtein Impact Whey Protein, Avrupa\'nın en çok satan whey proteinidir. 80+ lezzet seçeneği ile kişisel tercihinize göre özelleştirilebilir.',
                price=549.90, original_price=699.90, stock=300, brand='MyProtein',
                weight='1kg, 2.5kg', flavor='Çikolata, Vanilya, Karpuz, 80+ seçenek',
                image_url='https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=600&q=80',
                badge='SALE', is_featured=False, category_id=prot.id),

        Product(name='Now Sports Plant Protein', slug='now-sports-plant-protein',
                short_description='Vegan dostu bitkisel protein karışımı. Bezelye + Pirinç bazlı.',
                description='Now Sports Plant Protein, veganlar ve laktozu reddedenler için mükemmel bir protein kaynağıdır.',
                price=649.90, stock=60, brand='Now Sports',
                weight='2lb', flavor='Çikolata, Sade',
                image_url='https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=600&q=80',
                badge='NEW', is_featured=True, category_id=prot.id),

        # Kreatin
        Product(name='Creatine Monohydrate Powder', slug='creatine-monohydrate-powder',
                short_description='%100 Saf Kreatin Monohidrat. Güç, patlayıcılık ve hacim için.',
                description='Micronize kreatin monohidrat ile hazırlanmış, bilimsel olarak kanıtlanmış güç ve performans takviyesi.',
                price=349.90, original_price=449.90, stock=250, brand='Optimum Nutrition',
                weight='600g', flavor='Sade (Lezzetsiz)',
                image_url='https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&q=80',
                badge='BESTSELLER', is_featured=True, category_id=kreat.id),

        Product(name='Kre-Alkalyn EFX Pro', slug='kre-alkalyn-efx-pro',
                short_description='Tamponlu kreatin. Yükleme gerektirmez, mide dostu.',
                description='All American EFX Kre-Alkalyn, patentli tamponlu kreatin formülü ile mide iritasyonunu önler ve %100 emilim sağlar.',
                price=699.90, stock=70, brand='All American EFX',
                weight='120 kapsül', flavor='Kapsül',
                image_url='https://images.unsplash.com/photo-1585435557343-3b092031a831?w=600&q=80',
                is_featured=False, category_id=kreat.id),

        Product(name='Creapure Creatine HCl', slug='creapure-creatine-hcl',
                short_description='Alman Creapure sertifikalı ultra saf kreatin.',
                description='Alman üretim Creapure licenced kreatin monohidrat. Dünyanın en güvenilir kreatin kaynağından elde edilmiş, en saf formülü.',
                price=529.90, stock=90, brand='Creapure',
                weight='500g',
                image_url='https://images.unsplash.com/photo-1594882645126-14020914d58d?w=600&q=80',
                badge='NEW', is_featured=True, category_id=kreat.id),

        # Pre-Workout
        Product(name='C4 Original Pre-Workout', slug='c4-original-pre-workout',
                short_description='Amerika\'nın en çok satan pre-workout takviyesi. Enerji, odak, dayanıklılık.',
                description='Cellucor C4 Original, beta-alanin, kreatin nitrat ve CarnoSyn içeriğiyle antrenman öncesi maksimum performans sağlar.',
                price=799.90, original_price=999.90, stock=120, brand='Cellucor',
                weight='195g (30 servis)', flavor='Watermelon, Cherry Limeade, Fruit Punch',
                image_url='https://images.unsplash.com/photo-1594381898411-846e7d193883?w=600&q=80',
                badge='BESTSELLER', is_featured=True, category_id=pre.id),

        Product(name='Ghost Legend Pre-Workout', slug='ghost-legend-pre-workout',
                short_description='600mg Alpha-GPC, trademarked L-Citrullin ile hacim pumpu.',
                description='Ghost Legend, nootropic ve performans odaklı bileşenleriyle, hem zihinsel odak hem de fiziksel performansı artıran premium bir pre-workout takviyesidir.',
                price=1099.90, stock=55, brand='Ghost',
                weight='323g (40 servis)', flavor='Sour Watermelon, Lemon Crush',
                image_url='https://images.unsplash.com/photo-1580086319619-3ed498161c77?w=600&q=80',
                badge='NEW', is_featured=True, category_id=pre.id),

        Product(name='Pulse Pre-Workout by Legion', slug='pulse-pre-workout-legion',
                short_description='Klinik dozlarda, temiz bileşenler. Dikkat çekici formula.',
                description='Legion Pulse, kafein, L-theanine, beta-alanin ve citrulline malate içeren, şeffaf etiketli clean pre-workout.',
                price=849.90, stock=40, brand='Legion Athletics',
                weight='490g (21 servis)', flavor='Blue Raspberry, Tropical Punch',
                image_url='https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
                category_id=pre.id),

        # Vitaminler
        Product(name='Omega-3 Balık Yağı 1000mg', slug='omega-3-balik-yagi-1000mg',
                short_description='EPA ve DHA bakımından zengin yüksek kaliteli balık yağı.',
                description='Kalp ve beyin sağlığını destekleyen, yüksek EPA/DHA içerikli premium balık yağı kapsülü.',
                price=249.90, stock=400, brand='Now Foods',
                weight='200 softgel',
                image_url='https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80',
                badge='BESTSELLER', is_featured=True, category_id=vit.id),

        Product(name='Vitamin D3 + K2 5000 IU', slug='vitamin-d3-k2-5000iu',
                short_description='D3 ve K2 sinerjisi. Kemik, bağışıklık ve kas sağlığı için.',
                description='Yüksek doz D3 vitamini ve MenaQ7 K2 vitamini kombinasyonu ile maksimum biyoyararlanım.',
                price=299.90, original_price=399.90, stock=180, brand='Thorne',
                weight='90 kapsül',
                image_url='https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80',
                badge='NEW', is_featured=False, category_id=vit.id),

        Product(name='Magnezyum Glisinasyon 400mg', slug='magnezyum-glisinasyon-400mg',
                short_description='Yüksek emilimli magnezyum bisglisinat. Uyku ve kas fonksiyonu için.',
                description='Glisin amino asidi ile şelat edilmiş magnezyum bisglisinat, en iyi emilim ve biyoyararlanım sağlayan formdur.',
                price=219.90, stock=220, brand='Doctor\'s Best',
                weight='120 kapsül',
                image_url='https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80',
                is_featured=True, category_id=vit.id),

        Product(name='Multivitamin Sport Complex', slug='multivitamin-sport-complex',
                short_description='Sporcular için 23 vitamin ve mineral içeren kapsamlı formül.',
                description='Aktif yaşam tarzı için tasarlanmış, antioksidanlar, vitaminler ve mineraller içeren kapsamlı multivitamin paketi.',
                price=399.90, stock=130, brand='Optimum Nutrition',
                weight='150 tablet',
                image_url='https://images.unsplash.com/photo-1564419320461-6870880221ad?w=600&q=80',
                badge='BESTSELLER', is_featured=True, category_id=vit.id),

        # Aksesuar
        Product(name='FitMarket Pro Şeykır 700ml', slug='fitmarket-pro-seykir-700ml',
                short_description='Sızdırmaz tasarım, metal çırpma topu. Premium vortex karıştırıcı.',
                description='BPA-free, gıda güvenli plastikten üretilmiş, 700ml kapasiteli premium protein şeykırı. Paslanmaz çelik çırpma topu ile pürüzsüz karışım.',
                price=149.90, original_price=199.90, stock=500, brand='FitMarket',
                weight='250g', flavor='Siyah, Beyaz, Mavi',
                image_url='https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=600&q=80',
                badge='SALE', is_featured=True, category_id=acc.id),

        Product(name='Ağırlık Kaldırma Eldiveni', slug='agirlik-kaldirma-eldiveni',
                short_description='Neopren pedli, anti-kayma yüzeyli gym eldiveni.',
                description='Ağırlık antrenmanı için tasarlanmış, bilek desteği sağlayan, neopren ayak pedli profesyonel gym elldivenı.',
                price=199.90, stock=80, brand='Harbinger',
                weight='S / M / L / XL',
                image_url='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
                is_featured=False, category_id=acc.id),

        Product(name='Direnç Bandı Seti (5li)', slug='direnc-bandi-seti-5li',
                short_description='5 farklı direnç seviyesi. Latex free. Egzersiz kılavuzu dahil.',
                description='Hafif banddan güçlü banda 5 farklı direnç seviyesi ile ev ve spor salonu egzersizleri için ideal set.',
                price=299.90, stock=150, brand='FitMarket',
                image_url='https://images.unsplash.com/photo-1598971639058-a4f7a36a02a1?w=600&q=80',
                badge='NEW', is_featured=True, category_id=acc.id),

        Product(name='Bilek Sarma Wrapu 60cm', slug='bilek-sarma-wrapu-60cm',
                short_description='Elastik bilek desteği. Powerlifting ve CrossFit için.',
                description='IPF onaylı 60cm elastik bilek wrapu. Güçlü bilek desteği ile ağır kaldırmalarda güvenliği artırır.',
                price=179.90, stock=200, brand='SBD Apparel',
                weight='Çift (2\'li paket)',
                image_url='https://images.unsplash.com/photo-1594882645126-14020914d58d?w=600&q=80',
                is_featured=False, category_id=acc.id),

        Product(name='Foam Roller Masaj Silindir', slug='foam-roller-masaj-silindir',
                short_description='Derin doku masajı. Tüm vücut kas iyileşmesi için.',
                description='Yüksek yoğunluklu EVA köpüğünden üretilmiş, 33cm uzunluğunda foam roller. Kas gerginliğini azaltır ve esnekliği artırır.',
                price=259.90, stock=75, brand='TriggerPoint',
                weight='33cm',
                image_url='https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
                is_featured=False, category_id=acc.id),

        Product(name='BCAA 2:1:1 Amino Asit Tozu', slug='bcaa-2-1-1-amino-asit-tozu',
                short_description='Lösine 2:1:1 oranlı BCAA. Kas koruması ve toparlanma.',
                description='İzolösin, Valin ve Lösinden oluşan 2:1:1 oranlı BCAA takviyesi. Antrenman sırasında ve sonrasında kas protein sentezini destekler.',
                price=449.90, original_price=549.90, stock=160, brand='Scivation',
                weight='348g (30 servis)', flavor='Mango, Üzüm, Watermelon',
                image_url='https://images.unsplash.com/photo-1580086319619-3ed498161c77?w=600&q=80',
                badge='SALE', is_featured=True, category_id=prot.id),

        Product(name='L-Glutamin 500g', slug='l-glutamin-500g',
                short_description='En çok bulunan amino asit. Bağışıklık ve toparlanma desteği.',
                description='Micronize L-Glutamin, yoğun antrenmanlar sonrası kas toparlanmasını hızlandırır ve bağışıklık sistemini destekler.',
                price=329.90, stock=110, brand='Bulk Powders',
                weight='500g',
                image_url='https://images.unsplash.com/photo-1594882645126-14020914d58d?w=600&q=80',
                category_id=prot.id),

        Product(name='Citrulline Malate 2:1 300g', slug='citrulline-malate-300g',
                short_description='Hacim pumpu ve dayanıklılık için klinik doz L-Sitrülin.',
                description='2:1 oranında L-Citrulline Malate, NO artışı ve kas pompası için kullanılan en etkili amino asitlerden biridir.',
                price=279.90, stock=85, brand='Nutricost',
                weight='300g',
                image_url='https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&q=80',
                badge='NEW', is_featured=False, category_id=pre.id),

        Product(name='ZMA Çinko Magnezyum B6', slug='zma-cinko-magnezyum-b6',
                short_description='Uyku kalitesi, testosteron ve kas toparlanması için ZMA formülü.',
                description='Çinko, Magnezyum Aspartat ve B6 vitamini içeren ZMA, antrenman sonrası gece alınan bir toparlanma takviyesidir.',
                price=189.90, stock=140, brand='Now Sports',
                weight='90 kapsül',
                image_url='https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&q=80',
                is_featured=False, category_id=vit.id),
    ]

    for p in products:
        db.session.add(p)

    # ── Admin User ───────────────────────────────────────────────
    admin = User(
        username='admin',
        email='admin@fitmarket.com',
        first_name='Admin',
        last_name='FitMarket',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    db.session.commit()

    print("Veritabani basariyla seed edildi!")
    print(f"   {len(products)} urun eklendi")
    print(f"   {len(categories)} kategori olusturuldu")
    print(f"   Admin: admin@fitmarket.com / admin123")
