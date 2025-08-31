import os
from flask import Blueprint, flash
from flask import Flask, render_template, request
from flask_login import current_user

from cl.pog import Pog, say_text, is_file, is_level, is_phonetics, is_dir, is_theme
from db.models import Words
from db.requests import get_songs_letter, get_count_letter, get_group, get_songs_group, get_songs_name, get_titles_text, \
    get_text_id, word_themes, get_words_count, get_phonetics_level_words, get_word_id, get_words_theme_count, \
    get_themeru, get_word_obj_id, count_userwishlist, is_id_model, set_userwishlist, del_userwishlist
from setting import letters, ITEMS, levels, text_phonetics_ru, text_phonetics_eng, level_words, phonetics_list

words = Blueprint('words', __name__)
@words.route('/')#methods=['POST','GET']
def words_levels_themes():
    themes = word_themes()
    k = ""
    for k, theme in themes.items():
        k = f"{k} {theme}, "
    title = f"Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | Английские слова по темам | Английский с переводом на русский с озвучкой"
    keywords = f"Словарь английских слов, Английские слова по уровням A0 A1 A2 B1 B2 C1, Английские слова по темам, Английский с переводом на русский с озвучкой, {k}"
    description = f"Английские слова по уровням A0 A1 A2 B1 B2 C1 | Словарь (Таблички) английских слов | Английские слова по темам | Английский с переводом на русский с озвучкой"
    return render_template('words.html',
                           level_words=level_words, themes=themes,
                           title=title, keywords=keywords, description=description)

@words.route('/word_level/<level>', methods=['POST', 'GET'])#methods=['POST','GET']
def word_level(level):
    level = is_level(level, level_words)
    phone = request.args.get('phone', 'all', type=str)
    phone = is_phonetics(phone)
    total_items = get_words_count(level, phone)
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    words = []
    words_ = p.get_words_level_pog(page, level, phone)
    if request.method == 'POST':
        if request.form['sound']:
            name_file = f"static/audiosword/{level}/{request.form['id']}.mp3"
            name_dir = "static/audiosword/{}".format(level)
            if not is_dir(name_dir):
                os.makedirs(name_dir)
            if not is_file(name_file):
                sound = get_word_id(request.form['id'])
                say_text(sound, name_file)
    for word in words_:
        file = 0
        if is_file(f"static/audiosword/{level}/{word.id}.mp3"):
            file = 1
        words.append((word, file, f"audiosword/{level}/{word.id}.mp3"))

    phonetics = get_phonetics_level_words(level)

    title = description = (f"Учим английский на слух | Уровень {level.upper()} | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
             f"Английский с переводом на русский с озвучкой")
    keywords = (f"Учим английский на слух, Словарь английских слов, Английские слова по уровням, A0, A1, A2, B1, B2, C1, "
                f"Английские слова по темам, Английский с переводом на русский с озвучкой,")
    description = (f"Уровень {level.upper()} - Учим английский на слух! | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
             f"Английский с переводом на русский с озвучкой")

    return render_template('words_level.html', level=level,
                           level_words=level_words, words=words, phonetics=phonetics,
                           page=p.page(page), total_pages=p.total_pages(), phone=phone,
                           phoneru=phonetics_list[phone].upper(), total_items=total_items,
                           title=title, keywords=keywords, description=description)

@words.route('/word_theme/<theme>', methods=['POST', 'GET'])#methods=['POST','GET']
def word_theme(theme):
    theme = is_theme(theme)
    total_items = get_words_theme_count(theme)
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    words = []

    words_ = p.get_words_theme_pog(page, theme)
    if request.method == 'POST':
        if request.form['sound']:
            name_file = f"static/audiosword/{theme}/{request.form['id']}.mp3"
            name_dir = "static/audiosword/{}".format(theme)
            if not is_dir(name_dir):
                os.makedirs(name_dir)
            if not is_file(name_file):
                sound = get_word_id(request.form['id'])
                say_text(sound, name_file)
    for word in words_:
        file = 0
        if is_file(f"static/audiosword/{theme}/{word.id}.mp3"):
            file = 1
        words.append((word, file, f"audiosword/{theme}/{word.id}.mp3"))

    themes = word_themes()

    title = description = (f"Учим английский на слух | Слова на тему {theme.upper()} | Таблички со словани | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
             f"Английский с переводом на русский с озвучкой")
    keywords = (f"Учим английский на слух, Словарь английских слов, Английские слова по уровням, A0, A1, A2, B1, B2, C1, "
                f"Английские слова по темам, Английский с переводом на русский с озвучкой,")
    description = (f"Слова на тему {theme.upper()} на английском | Таблички со словани | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
             f"Английский с переводом на русский с озвучкой")

    return render_template('words_theme.html', themeru=get_themeru(theme),
                           theme=theme, total_items=total_items,
                           themes=themes, words=words,
                           page=p.page(page), total_pages=p.total_pages(),
                           title=title, keywords=keywords, description=description)


@words.route('/word_word/<int:id>', methods=['POST', 'GET'])#methods=['POST','GET']
def word_word(id):
    word = get_word_obj_id(id)
    phoneticsru = ''
    if word.phonetics!='':
        phoneticsru = phonetics_list[word.phonetics]

    if word.level != '':
        filename = f"audiosword/{word.level}/{word.id}.mp3"
        name_dir = f"audiosword/{word.level}"
    else:
        filename = f"audiosword/{word.theme}/{word.id}.mp3"
        name_dir = f"audiosword/{word.theme}"

    if request.method == 'POST':
        if request.form['sound']:
            name_file = f"static/{filename}"
            name_dir = f"static/{name_dir}"
            if not is_dir(name_dir):
                os.makedirs(name_dir)
            if not is_file(name_file):
                sound = get_word_id(word.id)
                say_text(sound, name_file)

    file = 0
    if word.level != '':
        if is_file(f"static/audiosword/{word.level}/{word.id}.mp3"):
            file = 1
    else:
        if is_file(f"static/audiosword/{word.theme}/{word.id}.mp3"):
            file = 1

    title = description = (
        f"Учим английский на слух | Слово {word.word.upper()} | произношение {word.word.upper()} | транскрипция {word.word.upper()} | перевод на русский {word.word.upper()} {word.trt} | {phoneticsru} {word.level} | Таблички со словани | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
        f"Английский с переводом на русский с озвучкой")
    keywords = (
        f"{word.word}, произношение {word.word.upper()}, транскрипция {word.word.upper()}, Учим английский на слух, Словарь английских слов, Английские слова по уровням, A0, A1, A2, B1, B2, C1, "
        f"Английские слова по темам {phoneticsru}, {word.level}, Английский с переводом на русский с озвучкой,")
    description = (
        f"Учим Слово {word.word.upper()} на английском | произношение  {word.word.upper()} | транскрипция {word.word.upper()} | перевод на русский {word.word.upper()} {word.trt} | {phoneticsru} {word.level} | Таблички со словани | Словарь английских слов | Английские слова по уровням A0 A1 A2 B1 B2 C1 | "
        f"Английский с переводом на русский с озвучкой")
    wishlist_count = 0
    if current_user.is_authenticated and current_user.email_confirmed:
        wishlist_count = count_userwishlist("words", current_user.id, id)

        if request.method == 'GET' and request.args.get('wh'):
            try:
                wh = int(request.args.get('wh'))
            except Exception as e:
                wh = 1
            if is_id_model(Words, wh):
                if wishlist_count == 0:
                    flash('Добавлено в избранное.', "text-primary m-2")
                    set_userwishlist("words", current_user.id, wh)
                else:
                    flash('Удалено из избранного.', "text-danger m-2")
                    del_userwishlist("words", current_user.id, wh)

            wishlist_count = count_userwishlist("words", current_user.id, wh)
    return render_template('words_word.html',
                           word=word, phoneticsru=phoneticsru,
                           file=file, filename=filename,
                           title=title, keywords=keywords, description=description,
                           wishlist_count=wishlist_count)
