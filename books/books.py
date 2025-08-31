import os

from flask import Blueprint, flash
from flask import Flask, render_template, request
from flask_login import current_user

from cl.pog import Pog, letter_lat, is_int, say_text, is_file, is_dir, is_num
from db.models import Books
from db.requests import get_songs_letter, get_count_letter, get_group, get_songs_group, get_songs_name, get_songs_ln, \
    get_count_songs_ln, get_authors, get_authors_id, get_books_id_author, get_book_id_author, get_booktexts, \
    get_count_booktexts, get_booktexts_en, get_books_level, count_userwishlist, set_userwishlist, \
    del_userwishlist, is_id_model
from setting import letters, ITEMS, LN, LNENGRU, level_books

books = Blueprint('books', __name__)

@books.route('/')#methods=['POST','GET']
def books_index():
    authors = get_authors()
    title = f"Авторы книг на аглийском | Книги с переводом с английского на русский "
    keywords = f"Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"Список авторов книг. Аудиокнини. Читаем на аглийском книги. Книги с переводом."
    return render_template('books_authors.html', authors=authors, title=title, keywords=keywords, description=description,
                           level_books=level_books)

@books.route('/author/<int:id>')#methods=['POST','GET']
def books_author(id):
    author = get_authors_id(id)
    books = get_books_id_author(id)
    book = []
    for b in books:
        url_img = "/static/book.jpg"
        url_book = f"/static/imgbooks/books/{b.id}.jpg"
        if is_file(f"static/imgbooks/books/{b.id}.jpg"):
            url_img = url_book
        book.append((b, url_img))
    title = f"Книги {author.author} на аглийском | {author.author} с переводом с английского на русский "
    keywords = f"{author.author}, Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"Слушаем книги {author.author} на аглийском. Аудиокнини {author.author}. Читаем на аглийском книги. Книги с переводом на русский."
    return render_template('books_author.html', author=author,
                           books = book,
                           title=title, keywords=keywords,
                           description=description)

@books.route('/book/<int:id_author>/<int:id_book>', methods=['POST','GET'])
def book_author(id_author, id_book):
    author = get_authors_id(id_author)
    book = get_book_id_author(id_book)
    total_items = get_count_booktexts(id_book)
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    booktexts = p.get_booktexts_pog(page, id_book)

    n = 0
    text = []
    if request.method == 'POST':
        if request.form['sound']:
            t = is_num(request.form['t'])
            name_file = f"static/audiosbooks/{author.id}/{book.id}/{t}.mp3"
            name_author_id = f"static/audiosbooks/{author.id}"
            name_book_id = f"static/audiosbooks/{author.id}/{book.id}"
            if not is_dir(name_author_id):
                os.makedirs(name_author_id)
            if not is_dir(name_book_id):
                os.makedirs(name_book_id)
            if not is_file(name_file):
                text_en = get_booktexts_en(t)
                say_text(text_en.texten, name_file, 'en')
    for t in booktexts:
        file = 0
        if is_file(f"static/audiosbooks/{author.id}/{book.id}/{t.id}.mp3"):
            file = 1
        textru =  t.textru.replace("<p>", "")
        textru = textru.replace("</p>", " ")
        texten = t.texten.strip()
        if len(texten) >0:
          text.append((t.texten, textru, n + 1, file, f"audiosbooks/{author.id}/{book.id}/{t.id}.mp3", t.id))
          n += 1
    wishlist_count = 0
    if current_user.is_authenticated and current_user.email_confirmed:
        wishlist_count = count_userwishlist("books", current_user.id, id_book)

        if request.method == 'GET' and request.args.get('wh'):
            try:
                wh = int(request.args.get('wh'))
            except Exception as e:
                wh = 1
            if is_id_model(Books, wh):
                if wishlist_count == 0:
                    flash('Добавлено в избранное.', "text-primary m-2")
                    set_userwishlist("books", current_user.id, wh)
                else:
                    flash('Удалено из избранного.', "text-danger m-2")
                    del_userwishlist("books", current_user.id, wh)

            wishlist_count = count_userwishlist("books", current_user.id, wh)

    title = f"{book.bookru} - книга {author.author} на аглийском с переводом на русский. Аудиокнига."
    keywords = f"{book.bookru}, {author.author}, Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"Слушаем книгу {book.bookru} {author.author} на аглийском. Аудиокнига. Читаем на аглийском книгу. Книга с переводом на русский."
    return render_template('book.html', author=author, total_items=total_items,
                           book = book, text=text, page=p.page(page), total_pages=p.total_pages(),
                           title=title, keywords=keywords, level_books=level_books,
                           description=description, wishlist_count=wishlist_count)

@books.route('/level/<level>')
def book_level(level):
    if not level in level_books:
        level = "A1"
    books_level = get_books_level(level)
    books = {}

    for b in books_level:
        author = get_authors_id(b.id_author)
        books[author.author] = b

    books = dict(sorted(books.items()))
    title = f"Читаем книги на английском уровень: {level}, с переводом на русский. Аудиокнига."
    keywords = f"Уровень английского {level}, читаем книги, английские книги с переводом, аудиокниги, Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"Слушаем книги уровня {level} на аглийском. Аудиокнига. Читаем на аглийском книгу. Книга с переводом на русский."
    return render_template('books_level.html',
                           title=title, keywords=keywords, level_books=level_books,
                           level=level, books_level=books,
                           description=description)


###########################################booktext####item
@books.route('/book/<int:id_author>/<int:id_book>/<int:id_booktext>', methods=['POST','GET'])
def book_booktext(id_author, id_book, id_booktext):
    author = get_authors_id(id_author)
    book = get_book_id_author(id_book)
    page = request.args.get('page', 1, type=int)
    booktexts = get_booktexts_en(id_booktext)

    n = 0
    text = []
    if request.method == 'POST':
        if request.form['sound']:
            t = is_num(request.form['t'])
            name_file = f"static/audiosbooks/{author.id}/{book.id}/{t}.mp3"
            name_author_id = f"static/audiosbooks/{author.id}"
            name_book_id = f"static/audiosbooks/{author.id}/{book.id}"
            if not is_dir(name_author_id):
                os.makedirs(name_author_id)
            if not is_dir(name_book_id):
                os.makedirs(name_book_id)
            if not is_file(name_file):
                text_en = get_booktexts_en(t)
                say_text(text_en.texten, name_file, 'en')
    t = booktexts
    file = 0
    if is_file(f"static/audiosbooks/{author.id}/{book.id}/{t.id}.mp3"):
        file = 1
    textru =  t.textru.replace("<p>", "")
    textru = textru.replace("</p>", " ")
    texten = t.texten.strip()
    if len(texten) >0:
      text.append((t.texten, textru, n + 1, file, f"audiosbooks/{author.id}/{book.id}/{t.id}.mp3", t.id))
      n += 1
    title = f"'{textru[:40]}' - Отрывок из книги '{book.bookru}', автор {author.author} на аглийском с переводом на русский. Аудиокнига."
    keywords = f"{author.author}, {book.bookru},  Английский по песням, Авторы книг на аглийском, Книги с переводом с английского на русский"
    description = f"'{textru[:50]}' - Слушаем отрывок из книги '{book.bookru}' {author.author} на аглийском, страница: {page}. Аудиокнига. Читаем на аглийском книгу. Книга с переводом на русский."
    return render_template('book_text.html', author=author,
                           book = book, t=text, page=page,
                           title=title, keywords=keywords, level_books=level_books,
                           description=description)
