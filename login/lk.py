# email_confirmed
# lk_no_email.html
import os

import flask
from flask import Blueprint, render_template
from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user

from cl.mail import send_email
from cl.pog import Pog
from db.models import Songs, Books, Reading, Words
from db.requests import get_userseng3_count_email, get_count_wish, get_wish_books, get_authors_id
from login.login_form import email_confirmed2_form
from newtoken.newtoken import generate_confirmation_token
import requests

from setting import wishlist, ITEMS

site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')
secret_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
google_ver_url = "https://www.google.com/recaptcha/api/siteverify"

def confirmed_required(func):

    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.email_confirmed:
            flash('Пожалуйста, подтвердите свой email', "text-danger m-2")
            return redirect(url_for('lk.unconfirmed'))
        elif current_user.is_authenticated and current_user.email_confirmed:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login.log_log'))
    return decorated_function

lk = Blueprint('lk', __name__)

@lk.route('/unconfirmed', methods=['POST', 'GET'])
def unconfirmed():
    form = email_confirmed2_form()
    email = current_user.email
    if request.method == 'POST':
        if form.validate_on_submit():

            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score']<0.5:
                return redirect(url_for('app.not_found_error'))
            if get_userseng3_count_email(email) == 0:
                flask.flash("Такой Email не зарегистрирован!", category="text-danger m-2")
            else:
                if not current_user.email_confirmed:
                    tok = generate_confirmation_token(email)
                    confirm_url = url_for('login.confirm_email', confirmation_token=tok, _external=True)
                    send_email(email, 'Подтвердите Email для eng3.ru',
                               f"Подтвердите Email для завершения регистрации на eng3.ru \n {confirm_url}")
                    flask.flash(f"Подтвердите свой email, ссылка Вам отправлена на {email}",
                                category="text-primary m-2")
                    return redirect(url_for('hello_world'))
        else:
           flask.flash("Попробуйте ещё раз! 🤨", category="text-danger m-2")

    title = f"Подтверждение email на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Вход в личный кабинет на eng3.ru, необходимо подтвердить email, Английский по песням и книгам"
    return render_template('lk/lk_no_email.html', title=title, keywords=keywords,
                           description=description,
                           form=form, site_key=site_key)

@lk.route('/', methods=['POST', 'GET'])
def lk_lk():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))
    wl = [(key, name, get_count_wish(current_user.id, key)) for key, name in wishlist.items()]
    title = f"Подтверждение email на eng3.ru | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Вход в личный кабинет на eng3.ru, необходимо подтвердить email, Английский по песням и книгам"

    return render_template('lk/lk.html', title=title, keywords=keywords,
                           description=description, wishlist=wl
                           )

@lk.route('/songs/', methods=['GET'])
def lk_songs():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))

    wl = [(key, name, get_count_wish(current_user.id, key)) for key, name in wishlist.items()]

    total_items = get_count_wish(current_user.id, "songs")
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    songs = p.get_wish(page, Songs, current_user.id, "songs")

    title = f"Избранное на eng3.ru - Песни. Учим иностранный язык по песням"
    keywords = f"eng3.ru, Английский по песням"
    description = f"Личный кабинет на утп3юкг - Избаранные песни. Перевод песен на русский. Английский по песням."
    return render_template('lk/lk_wish_songs.html', title=title, keywords=keywords,
                           description=description, wishlist=wl, songs=songs, total_items=total_items,
                           page=p.page(page), total_pages=p.total_pages(),
                           )

@lk.route('/books/', methods=['GET'])
def lk_books():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))

    wl = [(key, name, get_count_wish(current_user.id, key)) for key, name in wishlist.items()]

    books_level = get_wish_books(Books, current_user.id, "books")
    books = {}

    for b in books_level:
        author = get_authors_id(b.id_author)
        books[author.author] = b

    books = dict(sorted(books.items()))
    title = f"Избранные книги на eng3.ru. Читаем книги на английском  с переводом на русский. Аудиокнига."
    keywords = f"Уровень английского , читаем книги, английские книги с переводом, аудиокниги, Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"Личный кабинет на eng3.ru - Избарынные книги. Слушаем книги на аглийском. Аудиокнига. Читаем на аглийском книгу. Книга с переводом на русский."
    return render_template('lk/lk_wish_books.html', title=title, keywords=keywords,
                               description=description, wishlist=wl,
                                 books_level=books,
                               )


@lk.route('/reading/', methods=['GET'])
def lk_reading():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))

    wl = [(key, name, get_count_wish(current_user.id, key)) for key, name in wishlist.items()]

    total_items = get_count_wish(current_user.id, "reading")
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    reading = p.get_wish(page, Reading, current_user.id, "reading")


    title = f"Избранное на eng3.ru - Тексты. Учим иностранный язык по песням"
    keywords = f"eng3.ru, Английский по текстам и книгам, Английский по песням"
    description = f"Личный кабинет на eng3.ru - Избаранные тексты. Перевод песен на русский. Английский по песням."
    return render_template('lk/lk_wish_reading.html', title=title, keywords=keywords,
                           description=description, wishlist=wl, reading=reading, total_items=total_items,
                           page=p.page(page), total_pages=p.total_pages(),
                           )


@lk.route('/words/', methods=['GET'])
def lk_words():
    if current_user.is_authenticated and not current_user.email_confirmed:
        return redirect(url_for('lk.unconfirmed'))
    if not current_user.is_authenticated:
        return redirect(url_for('login.log_log'))

    wl = [(key, name, get_count_wish(current_user.id, key)) for key, name in wishlist.items()]

    total_items = get_count_wish(current_user.id, "words")
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)

    words = p.get_wish(page, Words, current_user.id, "words")

    for word in words:
        print(word)

    title = f"Избранные слова на eng3.ru - Песни. Учим иностранный язык по песням"
    keywords = f"eng3.ru, Английский по песням"
    description = f"Таблички слов на английском. Личный кабинет на eng3.ru - Избаранные слова. Перевод песен на русский. Английский по песням."
    return render_template('lk/lk_wish_words.html', title=title, keywords=keywords,
                           description=description, wishlist=wl, words=words, total_items=total_items,
                           page=p.page(page), total_pages=p.total_pages(),
                           )