import os
from datetime import datetime, timedelta, timezone
import secrets
from flask_login import current_user, login_user, logout_user
# from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer

import flask
from flask import Blueprint, render_template, request, redirect, url_for, current_app
import requests
from werkzeug.security import generate_password_hash, check_password_hash

from app_flask import app
from cl.mail import send_email, send_reset_email
from db.requests import get_userseng3_email, add_usereng3, get_userseng3_count_email, set_usereng3_email_confirmed, \
    set_new_psw_usereng3, get_userseng3_reset_token, set_usereng3_token
from login.lk import confirmed_required
from login.login_form import login_form, reg_form, new_psw_form, forgot_psw_form
from newtoken.newtoken import generate_confirmation_token


site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')
secret_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
google_ver_url = "https://www.google.com/recaptcha/api/siteverify"

loginBlueprint = Blueprint('login', __name__)

#@songs.route('/0')#methods=['POST','GET']
@loginBlueprint.route('/login', methods=['POST', 'GET'])
def log_log():
    if current_user.is_authenticated and not current_user.email_confirmed:
        flask.flash('Пожалуйста, подтвердите свой email', "text-danger m-2")
        return redirect(url_for('lk.unconfirmed'))
    if current_user.is_authenticated and current_user.email_confirmed:
        flask.flash('Пожалуйста, подтвердите свой email', "text-danger m-2")
        return redirect(url_for('lk.lk_lk'))
    form = login_form()
    if request.method == 'POST':
        pass
        if form.validate_on_submit():
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(
                url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score'] < 0.5:
                return redirect(url_for('app.not_found_error'))
            email = form.email.data
            if  get_userseng3_count_email(email)==0:
               flask.flash("Пользователь не найден!", category="text-danger m-2")
            else:
                user = get_userseng3_email(email)
                password = form.password.data
                if not check_password_hash(user.password, password):
                    flask.flash("Неверный пароль!", category="text-danger m-2")
                else:
                    login_user(user, remember=form.remember_me.data)
                    flask.flash(f"Добро пожаловать!", category="text-primary m-2")
                    return redirect(url_for('lk.lk_lk'))


            # user = get_userseng3_email(email)
            # password = form.password.data
            # password_h = check_password_hash(hash, password)
            # flask.flash(f"{email}", category="text-primary m-2")
            # flask.flash(f"{password}", category="text-primary m-2")
        else:
           flask.flash("Попробуйте ещё раз! 🤨", category="text-danger m-2")

    title = f"Вход в ЛК на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Вход в личный кабинет на eng3.ru, Английский по песням и книгам"
    return render_template('login.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)

@confirmed_required
@loginBlueprint.route('/reg', methods=['POST', 'GET'])
def log_reg():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if current_user.is_authenticated and current_user.email_confirmed:
        return redirect(url_for('lk.lk_lk'))
    form = reg_form(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():

            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score']<0.5:
                return redirect(url_for('app.not_found_error'))

            email = form.email.data
            if  get_userseng3_count_email(email)>=1:
               flask.flash("Такой Email уже зарегистрирован!", category="text-danger m-2")
            else:
                tok = generate_confirmation_token(email)
                confirm_url = url_for('login.confirm_email', confirmation_token=tok, _external=True)
                send_email(email, 'Подтвердите Email для eng3.ru',
                           f"Подтвердите Email для завершения регистрации на eng3.ru \n {confirm_url}")

                # send_email(email, "Регистрация на сайте eng3.ru",
                #           f"Подтвердите свой email {email}")
                flask.flash("Вы зарегистрированы!", category="text-primary m-2")
                flask.flash(f"Подтвердите свой email, ссылка Вам отправлена на {email}",
                           category="text-primary m-2")
                password = generate_password_hash(form.password.data)
                add_usereng3(form.email.data, password)
                return redirect(url_for('login.log_log'))
        else:
           flask.flash("Попробуйте ещё раз! 🤨", category="text-danger m-2")
    title = f"Регистрация на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Регистрация в личном кабинете на eng3.ru, Английский по песням и книгам"
    return render_template('login_reg.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)


@loginBlueprint.route('/confirm/?confirmation_token=<confirmation_token>')
def confirm_email(confirmation_token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(
            confirmation_token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400
        )
    except:
        flask.flash("Ссылка устарела!", category="text-danger m-2")
        return render_template('invalid_token.html')
    user = get_userseng3_email(email)
    if user.email_confirmed:
        flask.flash("Мы рады Вам!", category="text-primary m-2")
        return redirect(url_for('hello_world'))
    set_usereng3_email_confirmed(user)
    flask.flash(f"Ваш email подтвержден", category="text-primary m-2")
    if not current_user.is_authenticated:
       return redirect(url_for('login.log_log'))
    else:
        return redirect(url_for('lk.lk_lk'))

@loginBlueprint.route('/logout/')
def logout():
    logout_user()
    flask.flash("Вы покинули ЛК", category="text-primary m-2")
    return redirect(url_for('hello_world'))

@loginBlueprint.route('/new_psw/', methods=['POST', 'GET'])
def new_psw():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))
    form = new_psw_form(request.form)
    ################################
    if request.method == 'POST':
        if form.validate_on_submit():

            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score']<0.5:
                return redirect(url_for('app.not_found_error'))

            else:
                password = generate_password_hash(form.password.data)
                if check_password_hash(current_user.password, form.password.data):
                    flask.flash("Вы ввели старый пароль", category="text-danger m-2")
                    return redirect(url_for('login.new_psw'))
                set_new_psw_usereng3(current_user, password)
                flask.flash("Вы поменяли пароль", category="text-primary m-2")
                return redirect(url_for('lk.lk_lk'))
        else:
           flask.flash("Попробуйте ещё раз! 🤨", category="text-danger m-2")
    ################################
    title = f"Поменять пароль в ЛК на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Смена пароля в личном кабинете на eng3.ru, Английский по песням и книгам"
    return render_template('login_new_psw.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)

@loginBlueprint.route('/forgot_psw/', methods=['POST', 'GET'])
def forgot_psw():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if current_user.is_authenticated:
        return redirect(url_for('lk.lk_lk'))
    # new_psw_func
    form = forgot_psw_form(request.form)
    ################################
    if request.method == 'POST':
        if form.validate_on_submit():

            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(
                url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score'] < 0.5:
                return redirect(url_for('app.not_found_error'))

            else:
                email = form.email.data
                user = get_userseng3_email(email)
                if user:
                    if user.reset_token_expiry:
                        if datetime.utcnow() < user.reset_token_expiry:
                            flask.flash('Письмо уже отправлено, проверьте папку СПАМ.', "text-danger m-2")
                            return redirect(url_for('login.log_log'))

                    reset_token = secrets.token_urlsafe(32)  # Generate a secure random token
                    reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
                    set_usereng3_token(user, reset_token, reset_token_expiry)

                    send_reset_email(email, reset_token)
                    flask.flash('Вам было отправлено письмо с инструкциями по сбросу пароля.', "text-primary m-2")
                    return redirect(url_for('login.log_log'))
                else:
                    flask.flash('Учётной записи с таким адресом электронной почты нет. Пожалуйста, сначала зарегистрируйтесь..', 'text-danger m-2')
                    return redirect(url_for('login.log_reg'))

        else:
            flask.flash("Попробуйте ещё раз! 🤨", category="text-danger m-2")
    ################################
    title = f"Ссылка на новый пароль для ЛК на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Восстановление пароля в личном кабинете на eng3.ru, Английский по песням и книгам"
    return render_template('login_forgot_psw.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)


@loginBlueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if current_user.is_authenticated:
        return redirect(url_for('lk.lk_lk'))

    user = get_userseng3_reset_token(token)

    # If token is invalid or expired
    if user is None or not user.verify_reset_token(token):
        flask.flash('Это недействительный или просроченный токен.', 'text-danger m-2')
        return redirect(url_for('login.forgot_psw'))

    form = new_psw_form()

    if form.validate_on_submit():

        if check_password_hash(user.password, form.password.data):
            flask.flash("Вы ввели старый пароль", category="text-danger m-2")
            return redirect(url_for('login.log_log'))

        password = generate_password_hash(form.password.data)
        set_new_psw_usereng3(user, password)

        flask.flash('Ваш пароль обновлён! Теперь вы можете войти.', 'text-primary m-2')
        return redirect(url_for('login.log_log'))

    title = f"Поменять пароль в ЛК на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Смена пароля в личном кабинете на eng3.ru, Английский по песням и книгам"
    return render_template('login_new_psw.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)
