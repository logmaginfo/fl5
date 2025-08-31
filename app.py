from datetime import timedelta, date, datetime

from flask import Flask, render_template, request, send_file, session, current_app
import asyncio
import os
from alphabet.alphabet import alphabet
from app_flask import app
from books.books import books
from cl.pog import Pog
from login.lk import lk
from login.login import loginBlueprint
from search.search import search
from setting import ITEMS, letters, levels, level_books

from songs.songs import songs
from text.text import text
from words.words import words
from flask_mail import Mail, Message

# async def main():
#     await async_main()
# app = Flask(__name__)


app.register_blueprint(songs, url_prefix='/songs')
app.register_blueprint(text, url_prefix='/text')
app.register_blueprint(words, url_prefix='/words')
app.register_blueprint(books, url_prefix='/books')
app.register_blueprint(alphabet, url_prefix='/alphabet')
app.register_blueprint(loginBlueprint, url_prefix='/login')
app.register_blueprint(lk, url_prefix='/lk')
app.register_blueprint(search, url_prefix='/search')


# если нужно увеличить время жизни ссесии
# app.permanent_session_lifetime = timedelta(days=50)

app.config.update(dict(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    WTF_CSRF_SECRET_KEY=os.getenv('WTF_CSRF_SECRET_KEY'),
    SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
))
# current_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# current_app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')

# dt = '1'
# @app.before_request #
# def set_session():
#     session.permanent = True #ссесия будет жить 31 день
#     global dt
#     if 'dt' in session:
#         # dt = session['dt']
#          dt =  datetime.now()
#     else:
#         session['dt'] =  datetime.now()
#         # session.modified = True # если данные ссесии нужно обновить

@app.route('/')
@app.route('/index')
async def hello_world():  # put application's code here
    return render_template('index.html', letters=letters, levels=levels, level_books=level_books)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500

@app.errorhandler(400)
def internal_error(error):
    return render_template('404.html'), 400

@app.route('/sitemap/<sitemap>')
def sitemap(sitemap):
    stm = f"sitemap/{sitemap}"
    return send_file(stm, mimetype='xml')

@app.route('/sitemap/booktext/<sitemap>')
def sitemap_booktext(sitemap):
    stm = f"sitemap/booktext/{sitemap}"
    return send_file(stm, mimetype='xml')

@app.route('/sitemap/songs/<sitemap>')
def sitemap_songs(sitemap):
    stm = f"sitemap/songs/{sitemap}"
    return send_file(stm, mimetype='xml')

@app.route('/<favicon_svg>')
def favicon_svg(favicon_svg):
    svg = f"{favicon_svg}"
    return send_file(svg, mimetype='svg')

@app.route('/robots.txt')
def robots():
    stm = "robots.txt"
    return send_file(stm, mimetype='txt')

if __name__ == '__main__':
    # main()
    app.run(debug=False)
