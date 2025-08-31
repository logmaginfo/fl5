# email_confirmed
# lk_no_email.html
import os
import requests
from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request

from cl.pog import is_lat_ru_num_pr, is_russian
from db.requests import get_search_songs_name, get_search_songs_group, get_search_words, get_search_ru_words
from login.login_form import forgot_psw_form
from search.search_form import search_form

site_key = os.getenv('RECAPTCHA_PUBLIC_KEY')
secret_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
google_ver_url = "https://www.google.com/recaptcha/api/siteverify"

search = Blueprint('search', __name__)

@search.route('/', methods=['POST', 'GET'])
def search_songs():
    query = request.args.get("query")

    query_search = ""
    form = search_form(request.form)
    results = ()
    if request.method == 'POST':
      if form.validate_on_submit():
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(
                url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score'] < 0.5:
                return redirect(url_for('search.search_songs'))
            else:
               query_post = form.query.data
               query_post = is_lat_ru_num_pr(query_post)
               results_name = get_search_songs_name(query_post)
               results_group = get_search_songs_group(query_post)
               results = (results_name, results_group)
               query_search = query_post

    if query:
        query = query.strip()

        if query!="":
            query = is_lat_ru_num_pr(query)
            results_name = get_search_songs_name(query)
            results_group = get_search_songs_group(query)
            results = (results_name, results_group)
            return render_template("search/search_results.html", results=results)
        query_search = query

    if query=="":
        results = ()
        return render_template("search/search_results.html", results=results)


    title = f"Поиск песен | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Поиск песен по названию трека, Английский по песням и книгам"

    return render_template('search/search.html', title=title, keywords=keywords,
                           description=description, results=results, form=form, site_key=site_key,
                           query=query_search)

@search.route('/words', methods=['POST', 'GET'])
def search_words():
    query = request.args.get("query")

    query_search = ""
    form = search_form(request.form)
    results = []
    if request.method == 'POST':
      if form.validate_on_submit():
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(
                url=f"{google_ver_url}?secret={secret_key}&response={secret_response}").json()

            if not verify_response['success'] or verify_response['score'] < 0.5:
                return redirect(url_for('search.search_songs'))
            else:
               query_post = form.query.data
               query_post = is_lat_ru_num_pr(query_post)
               if not is_russian(query_post):
                   results = get_search_words(query_post)
               else:
                   results = get_search_ru_words(query_post)

               query_search = query_post

    if query:
        query = query.strip()

        if query!="":
            query = is_lat_ru_num_pr(query)
            if not is_russian(query):
                results = get_search_words(query)
            else:
                results = get_search_ru_words(query)

            return render_template("search/search_words_results.html", results=results)
        query_search = query

    if query=="":
        results = []
        return render_template("search/search_words_results.html", results=results)


    title = f"Поиск песен | Английский по песням и книгам"
    keywords = f"Английский по песням, Английский по книгам, английские слова, eng3.ru "
    description = f"Поиск песен по названию трека, Английский по песням и книгам"

    return render_template('search/search_words.html', title=title, keywords=keywords,
                           description=description, results=results, form=form, site_key=site_key,
                           query=query_search)