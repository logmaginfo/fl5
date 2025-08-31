import os

import flask
from flask import Blueprint
from flask import Flask, render_template, request

from alphabet.alphabet_forms import at
from cl.pog import Pog, letter_lat, is_int, say_text, is_file, is_dir, is_num
from db.requests import get_songs_letter, get_count_letter, get_group, get_songs_group, get_songs_name, get_songs_ln, \
    get_count_songs_ln, get_authors, get_authors_id, get_books_id_author, get_book_id_author, get_booktexts, \
    get_count_booktexts, get_booktexts_en, get_books_level
from setting import letters, ITEMS, LN, LNENGRU, level_books, alphabet_dict, alphabet_list

alphabet = Blueprint('alphabet', __name__)

@alphabet.route('/')#methods=['POST','GET']
def alphabet_index():

    title = f"Аглийском Алфавит с переводом с английского на русский + произношение"
    keywords = f"Аглийский Алфавит, Английский, Алфавит"
    description = f"Учим английский язык. Аглийском Алфавит с переводом с английского на русский и произношение"
    return render_template('alphabet.html',
                           alphabet_dict=alphabet_dict,
                           title=title, keywords=keywords,
                           description=description,
                           )

@alphabet.route('/test', methods=['POST','GET'])#methods=['POST','GET']
def alphabet_test():
    import random
    alphabet4 = random.sample(alphabet_list, 4)
    alphabet1 = random.sample(alphabet4, 1)
    if request.method == 'POST':

        if "alphabet4" in request.form: #request.form['flexRadioDefault']:

            if request.form['alphabet1'] != request.form['alphabet4']:
                # print(request.form['alphabet1'])
                # print(request.form['alphabet4_hidden'])
                alphabet4 = request.form['alphabet4_hidden']
                alphabet4 = alphabet4.replace("[", "")
                alphabet4 = alphabet4.replace("]", "")
                alphabet4 = alphabet4.replace("'", "")
                alphabet4 = alphabet4.replace(",", "")
                alphabet4 = alphabet4.split()
                alphabet1[0] = request.form['alphabet1']
                flask.flash("Попробуйте ещё раз! 🤨", category="text-danger")
            else:
                flask.flash("Правильно! 👌 ", category="text-primary")



    al = [(a,a) for a in alphabet4]
    # al = [('A', 'Aa'), ('B', 'Bb'), ('C', 'Cc'), ('D', 'Dd')]
    form = at(alphabet44=al, alphabet11=alphabet1, alphabet4_hidd=alphabet4)
    title = f"Тест на знание Аглийского Алфавита с переводом с английского на русский + произношение"
    keywords = f"тест, Аглийский Алфавит, Английский, Алфавит"
    description = f"Учим английский язык. Аглийском Алфавит с переводом с английского на русский и произношение"
    return render_template('alphabet_test.html',
                           alphabet1=alphabet1, alphabet4_hidden=alphabet4,
                           title=title, keywords=keywords,
                           description=description,
                           form=form
                           )
