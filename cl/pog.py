import math
import random
from pydantic import BaseModel
from db.requests import get_songs_letter, get_words_level, phonetics_is_words, get_words_theme, get_songs_ln, \
    get_booktexts, get_wish_item
import os
from gtts import gTTS

from setting import phonetics_list, level_words, LN, text_phonetics_eng, alphabet_list, alphabet_, num_, zn_, \
    lat_ru_num_pr


def is_lat_ru_num_pr(word):
    for w in word:
      if not w in lat_ru_num_pr:
            word = word.replace(w, "")
    return word

def letter_lat(letter):
    letter = letter.replace(" ", "")
    if not letter.isalpha():
        letter = 'A'
    if letter.lower() != "num":
        letter = letter[:1]
        letter = letter.upper()
    return letter

def is_level(level, levels):
    level = level.replace(" ", "")
    level = level[:2]
    if not level.upper() in levels:
        level = "A0"
    return level.lower()

def is_int(i):
    try:
        return True if int(i) == i else False
    except Exception as e:
        return False

def is_num(i):
    try:
        i = int(i)
        return i
    except Exception as e:
        return 1

def is_phonetics(phonetics):
    lat = phonetics.replace(" ", "")
    lat = lat.lower()
    lat = lat[:10]
    if not lat.isalpha():
        lat = 'all'
    if not lat in phonetics_list:
        lat = 'all'
    return lat

def is_theme(theme):
    theme = theme.replace(" ", "")
    theme = theme.lower()
    theme = theme[:80]
    if not theme.replace("_", "").isalpha():
        theme = 'all'
    return theme

class Pog(BaseModel):
    total_items: int
    ITEMS:int

    def total_pages(self):
       # res = round(self.total_items / self.ITEMS)
       res = math.ceil(self.total_items / self.ITEMS)
       if res < 1: res = 1
       return res

    def page(self, page):
        if not isinstance(page, int):
            page = 1
        if page < 1: page = 1
        if page > self.total_pages(): page = self.total_pages()
        return page

    def start(self, pg):
        page = self.page(pg)
        if page == 1:
            start = 0
        else:
            start = (page - 1) * self.ITEMS
        if start < 0: start = 0
        return start

    def end(self, page):
        return self.start(page) + self.ITEMS

    def get_songs_letter_pog(self, page, letter):
        page = self.page(page)
        res = get_songs_letter(letter, self.start(page), self.end(page))
        return res

    def get_words_level_pog(self, page, level, phonetics):
        page = self.page(page)
        level = is_level(level, level_words)
        if phonetics_is_words(phonetics, level)==0:
            phonetics = "all"
        res = get_words_level(level, phonetics, self.start(page), self.end(page))
        return res

    def get_words_theme_pog(self, page, theme):
        page = self.page(page)
        res = get_words_theme(theme, self.start(page), self.end(page))
        return res

    def get_songs_ln_pog(self, page, ln):
        page = self.page(page)
        res = get_songs_ln(ln, self.start(page), self.end(page))
        return res

    def get_booktexts_pog(self, page, id_book):
        page = self.page(page)
        res = get_booktexts(id_book, self.start(page), self.end(page))
        return res

    def get_wish(self, page, model, id_user, wishlist):
        page = self.page(page)
        res = get_wish_item(model, id_user, wishlist, self.start(page), self.end(page))
        return res


# def say_text(text, id):
#     print(id)
#     say = pyttsx3.init('sapi5')
#     say.setProperty('rate', 170)  # скорость речи
#     say.setProperty('volume', 0.9)
#     say.save_to_file(text, "static/audios/{}.mp3".format(id))
#     say.runAndWait()
#     say.stop()

def say_text(text, path, ln='en'):
    if ln in LN:
        ln = ln
    else:ln='en'

    tts = gTTS(text, lang=ln)
    file_name = path
    tts.save(file_name)


def is_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

def is_dir(file_path):
    if os.path.isdir(file_path):
        return True
    else:
        return False

def phonetics_eng_in_ru(k):
    for ph in text_phonetics_eng:
        if ph[0] == k:
            return ph[1]

def new_psw_func():
    r1 = random.sample(alphabet_list, 2)
    r2 = random.sample(alphabet_, 2)
    r3 = random.sample(num_, 2)
    r4 = random.sample(zn_, 1)
    r = r1 + r2 + r3 + r4
    return random.shuffle(r)

def is_russian(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())