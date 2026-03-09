from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Hoş geldiniz, {user.first_name or user.username}! 🎉', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        
        flash('Geçersiz e-posta veya şifre.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        f = request.form
        username = f.get('username', '').strip()
        email = f.get('email', '').strip().lower()
        first_name = f.get('first_name', '').strip()
        last_name = f.get('last_name', '').strip()
        password = f.get('password', '')
        confirm = f.get('confirm_password', '')

        if password != confirm:
            flash('Şifreler eşleşmiyor.', 'danger')
        elif db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none():
            flash('Bu e-posta zaten kullanımda.', 'danger')
        elif db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none():
            flash('Bu kullanıcı adı zaten alınmış.', 'danger')
        elif len(password) < 6:
            flash('Şifre en az 6 karakter olmalı.', 'danger')
        else:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))
