import os

from flask import Blueprint, flash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user

from cl.pog import Pog, letter_lat, is_int, say_text, is_file, is_dir, is_num
from db.models import Songs
from db.requests import get_songs_letter, get_count_letter, get_group, get_songs_group, get_songs_name, get_songs_ln, \
    get_count_songs_ln, count_userwishlist, set_userwishlist, del_userwishlist, is_id_model
from setting import letters, ITEMS, LN, LNENGRU

songs = Blueprint('songs', __name__)

#@songs.route('/0')#methods=['POST','GET']
@songs.route('/', methods=['GET'])
def songs_():
    return redirect(url_for('songs.songs_index', letter="A"))

@songs.route('/<letter>', methods=['GET'])#methods=['POST','GET']
def songs_index(letter):
    letter = letter_lat(letter)
    total_items = get_count_letter(letter)
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    songs = p.get_songs_letter_pog(page, letter)
    k = ""
    t = ""
    for word in songs[:3]:
        k = f"{k}{word.group}, "
        t = f"{t}{word.group} | "


    title = f"Песни. Исполнители на {letter} | Английский по песням | {t}"
    keywords = f"Английский по песням, {k}"
    description = f"Сайт с переводами песен {k}. Английский по песням"
    return render_template('songs.html', title=title, keywords=keywords,
                           description=description, title2='Исполнители:',
                           letters=letters, letter=letter, songs=songs,
                           total_items=total_items,
                           page=p.page(page), total_pages=p.total_pages())

@songs.route('/group/<int:id_group>', methods=['GET'])
def songs_group(id_group):
    group = get_group(id_group)
    albums = get_songs_group(group.group)
    k = ""
    t = ""
    for album in albums:
        k = f"{k}{album}, "
        t = f"{t}{album} | "
    title = f"{group.group} перевод песен | Английский по песням "
    keywords = f"Английский по песням,{group.group}, {k}"
    description = f"Сайт с переводами песен {group.group} "
    src = f"/static/imgsongs/n.jpg"
    path_img = f"static/imgsongs/{group.letter}/{group.group}.jpg"

    if is_file(path_img):
        src = f"/{path_img}"
    else:
        src = src
    return render_template('song_group.html', src=src,
                           group=group.group, albums=albums, length=len(albums),
                           title=title, keywords=keywords, description=description)

@songs.route('/albums/<int:id_name>', methods=['GET', 'POST'])
def songs_name(id_name):
    song = get_songs_name(id_name)
    text_en1 = song.text
    text_ru1 = song.textru
    text_en = text_en1.split("\n\n")
    text_ru = text_ru1.split("\n\n")
    if len(text_en) == 1:
        text_en = text_en1.split(". ")
        text_ru = text_ru1.split(". ")
    if len(text_en) != len(text_ru):
        text_en = text_en1.split("\n\n")
        text_ru = text_ru1.split("\n\n")

    n = 0
    text = []
    if request.method == 'POST':
        if request.form['sound']:
            t = is_num(request.form['t'])
            name_file = "static/audios/{}.mp3".format(request.form['name_id'])
            name_dir = "static/audios/{}".format(song.id)
            if not is_dir(name_dir):
                os.makedirs(name_dir)
            if not is_file(name_file):
                say_text(text_en[t-1], name_file, ln=song.ln)
    for t in text_en:
        file = 0
        if is_file(f"static/audios/{song.id}/{song.id}_{n+1}.mp3"):
            file = 1
        if len(t)>0:
            text.append((t, text_ru[n], n+1, file, f"audios/{song.id}/{song.id}_{n+1}.mp3"))
        n += 1
    k = ""
    t = ""
    text_ru_k = text_ru[0].split(" ")
    for ru in text_ru_k[:3]:
        ru = ru.replace("\n", "")
        k = f"{k}{ru}, "
        t = f"{t}{ru} | "
    ln = "Английском!"
    if song.ln in LN:
        ln = LN[song.ln]
    lnru = LNENGRU[song.ln]

    title = f"Перевод песни {song.name} | Группа {song.group} | Альбом {song.album} | Английский по песням "
    keywords = f"Английский по песням,{song.name}, {song.group}, {song.album}"
    description = f"{song.name} Перевод песни с английского на русский. Группа {song.group}. Английский по песням. Альбом {song.album}"
    src = f"/static/imgsongs/n.jpg"
    path_img = f"static/imgsongs/{song.letter}/{song.group}.jpg"

    if is_file(path_img):
        src = f"/{path_img}"
    else:
        src = src

    mp3 = "0"
    path_song = f"static/audios/{song.id}/{song.id}.mp3"
    if is_file(path_song):
       mp3 = f"/{path_song}"
    # (session, wish, id_user, id_wishlist):

    wishlist_count = 0
    if current_user.is_authenticated and current_user.email_confirmed:
        wishlist_count = count_userwishlist("songs", current_user.id, song.id)

        if request.method == 'GET' and request.args.get('wh'):
            try:
                wh = int(request.args.get('wh'))
            except Exception as e:
                wh = 1
            if is_id_model(Songs, wh):
                if wishlist_count == 0:
                    flash('Добавлено в избранное.', "text-primary m-2")
                    set_userwishlist("songs", current_user.id, wh)
                else:
                    flash('Удалено из избранного.', "text-danger m-2")
                    del_userwishlist("songs", current_user.id,  wh)

            wishlist_count = count_userwishlist("songs", current_user.id, wh)


    return render_template('song_name.html', song=song, text=text,
                           ln=ln, lnru=lnru, src=src, mp3=mp3,
                           title=title, keywords=keywords, description=description,
                           wishlist_count=wishlist_count
                           )

@songs.route('/country/<ln>', methods=['GET'])
def songs_country(ln):
    if not ln in LNENGRU:
        ln = 'en'
    total_items = get_count_songs_ln(ln)
    p = Pog(total_items=total_items, ITEMS=ITEMS)
    page = request.args.get('page', 1, type=int)
    songs = p.get_songs_ln_pog(page, ln)
    title = f"Песни на языке {LNENGRU[ln]}. Учим иностранный язык по песням"
    keywords = f"{LNENGRU[ln]}, {ln}, Английский по песням"
    description = f"{LNENGRU[ln]} Перевод песен на русский. Английский по песням."

    return render_template('song_country.html', ln=LNENGRU[ln],
                           songs=songs, total_items=total_items,
                           page=p.page(page), total_pages=p.total_pages(),
                           LNENGRU=LNENGRU,
                           title=title, keywords=keywords, description=description,
                           )