from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadSignature

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

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            # Print to console for testing
            print(f"\n[{user.email}] PASSWORD RESET LINK: {reset_url}\n")
            flash(f'Şifre sıfırlama bağlantısı oluşturuldu! -> Lütfen konsolu kontrol edin veya buraya tıklayın: <a href="{reset_url}" style="text-decoration:underline;">Şifreyi Sıfırla</a>', 'info')
        else:
            flash('Bu e-posta adresine kayıtlı bir hesap bulunamadı.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    try:
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('Şifre sıfırlama bağlantısının süresi dolmuş.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    except BadSignature:
        flash('Geçersiz şifre sıfırlama bağlantısı.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if not password or password != confirm:
            flash('Şifreler eşleşmiyor.', 'danger')
        elif len(password) < 6:
            flash('Şifre en az 6 karakter olmalı.', 'danger')
        else:
            user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
            if user:
                user.set_password(password)
                db.session.commit()
                flash('Şifreniz başarıyla sıfırlandı. Yeni şifrenizle giriş yapabilirsiniz.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Kullanıcı bulunamadı.', 'danger')
                return redirect(url_for('auth.forgot_password'))
    return render_template('auth/reset_password.html')
