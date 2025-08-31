import os
import re

from flask import Blueprint, flash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user

from cl.pog import Pog, letter_lat, is_int, say_text, is_file, is_level, is_dir, is_num, phonetics_eng_in_ru
from db.models import Reading
from db.requests import get_songs_letter, get_count_letter, get_group, get_songs_group, get_songs_name, get_titles_text, \
    get_text_id, count_userwishlist, is_id_model, set_userwishlist, del_userwishlist
from setting import letters, ITEMS, levels, text_phonetics_ru, text_phonetics_eng

text = Blueprint('text', __name__)

@text.route('/')
def text_():
    return redirect(url_for('text.text_index', level="a0"))

@text.route('/<level>')#methods=['POST','GET']
def text_index(level):
    level = is_level(level, levels)
    texts = get_titles_text(level)
    k = ""
    t = ""
    for text in texts:
        k = f"{k}{text[0]}, {text[1]},"
        t = f"{t}{text[0]} | {text[1]} | "
    title = f"Тексты на английском. Слушаем речь на английском. Уровень {level}. {t} "
    keywords = f"Тексты на английском, слушаем английскую речь, погружение в языковую среду, {k}"
    description = f"Тексты на аглийском уровня {level}. Слушаем речь на английском. Уровень {level}. {t} "
    return render_template('text.html',
                           title=title, keywords=keywords, description=description,
                           levels=levels,
                           level=level, texts=texts,
                           )

#
@text.route('/phonetics/<int:id>', methods=['GET', 'POST'])#methods=['POST','GET']
def text_text(id):
    texts = get_text_id(id)
    text_en1 = texts.text
    text_ru1 = texts.textru

    text_en = text_en1.split("\n\n")
    text_ru = text_ru1.split("\n\n")

    if len(text_en) != len(text_ru) or len(text_en)==1:

        text_en = text_en1.replace('. ', '.|@')
        text_ru = text_ru1.replace('. ', '.|@')
        text_en = text_en.replace('!', '!|@')
        text_ru = text_ru.replace('!', '!|@')
        text_en = text_en.replace('?', '?|@')
        text_ru = text_ru.replace('?', '?|@')

        text_en = text_en.split("|@")
        text_ru = text_ru.split("|@")


    if len(text_en) != len(text_ru):

        text_en = text_en1.replace('!', '!|@')
        text_ru = text_ru1.replace('!', '!|@')
        text_en = text_en.replace('?', '?|@')
        text_ru = text_ru.replace('?', '?|@')

        text_en = text_en.split("|@")
        text_ru = text_ru.split("|@")

    if len(text_en) != len(text_ru):

        text_en = []
        text_ru = []
        text_en.append(texts.text)
        text_ru.append(texts.textru)

    n = 0
    text = []
    if request.method == 'POST':
        t = is_num(request.form['t'])
        name_file = "static/audiostext/{}.mp3".format(request.form['name_id'])
        name_dir = "static/audiostext/{}".format(texts.id)
        if not is_dir(name_dir):
            os.makedirs(name_dir)
        if not is_file(name_file):
            say_text(text_en[t-1], name_file)
    for t in text_en:
        t = t.strip()
        file = 0
        if is_file(f"static/audiostext/{texts.id}/{texts.id}_{n+1}.mp3"):
            file = 1
        if len(t)>0:
            text.append((t, text_ru[n], n+1, file, f"audiostext/{texts.id}/{texts.id}_{n+1}.mp3"))
        n += 1
    k = ""
    t = ""
    text_ru_k = text_ru[0].split(" ")
    for ru in text_ru_k:
        ru = ru.replace("\n", "")
        k = f"{k}{ru}, "
        t = f"{t}{ru} | "

    texts_phonetics_ru = phonetics_eng_in_ru(texts.phonetics)
    title = f"Читаем и слушаем текст на английском {texts.titleru} | Уровень {texts.level} | {texts.phonetics} | {t}"
    keywords = (f"текст на английском, слушаем текст на анг, {texts.titleru}, {texts.title}, уровень английского {texts.level}, "
                f" {k}")
    description = f"Текст на английском {texts.titleru} | Читаем и слушаем на английском | Уровень {texts.level} | {texts.phonetics} | {t}"

    wishlist_count = 0
    if current_user.is_authenticated and current_user.email_confirmed:
        wishlist_count = count_userwishlist("reading", current_user.id, id)

        if request.method == 'GET' and request.args.get('wh'):
            try:
                wh = int(request.args.get('wh'))
            except Exception as e:
                wh = 1
            if is_id_model(Reading, wh):
                if wishlist_count == 0:
                    flash('Добавлено в избранное.', "text-primary m-2")
                    set_userwishlist("reading", current_user.id, wh)
                else:
                    flash('Удалено из избранного.', "text-danger m-2")
                    del_userwishlist("reading", current_user.id, wh)

            wishlist_count = count_userwishlist("reading", current_user.id, wh)

    return render_template('text_text.html',
                           id=id, texts=texts, texts_phonetics_ru=texts_phonetics_ru,
                           len=f"{len(text_en)} != {len(text_ru)}",
                           text=text,
                           title=title, keywords=keywords, description=description,
                           wishlist_count=wishlist_count)
