from flask import Flask
from app.config import config
from app.extensions import db, login_manager, migrate, csrf
import os


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen giriş yapın.'
    login_manager.login_message_category = 'warning'

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.cart import cart_bp
    from app.routes.checkout import checkout_bp
    from app.routes.profile import profile_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Inject cart count into all templates
    from flask_login import current_user
    from app.models.cart import CartItem

    @app.context_processor
    def inject_cart_count():
        count = 0
        if current_user.is_authenticated:
            count = db.session.query(CartItem).filter_by(user_id=current_user.id).count()
        return dict(cart_count=count)

    @app.context_processor
    def inject_categories():
        from app.models.product import Category
        cats = db.session.execute(db.select(Category)).scalars().all()
        return dict(all_categories=cats)

    return app
