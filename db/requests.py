
from db.models import *
from sqlalchemy import select, update, delete, desc, func
from sqlalchemy import and_, or_
from setting import text_phonetics_eng, phonetics_list, LN, LNENGRU

def sess(func):
    def con(*args, **kwargs):
        with sync_session() as session:
            return func(session, *args, **kwargs)
    return con
# def sess(func):
#     async def con(*args, **kwargs):
#         async with async_session() as session:
#             return await func(session, *args, **kwargs)
#     return con

# @sess
# async def get_letter(session):
#     # res = await session.scalars(select(Songs).distinct(Songs.letter).where(or_(Songs.text!=''), Songs.text!=None).order_by(Songs.id.asc()).limit(10))
#     res = await session.scalars(select(Songs.letter).distinct(Songs.letter).order_by(Songs.letter))
#     return res.all()
@sess
def get_songs_letter(session, letter, start, end):
    #SELECT DISTINCT songs.group FROM public.songs where letter='A' order by songs.group
    res = session.scalars(select(Songs).distinct(Songs.group).where(Songs.letter==letter).slice(start,end).order_by(Songs.group))
    return res.all()

@sess
def get_words_level(session, level, phonetics, start, end):
    if phonetics == 'all':
       res = session.scalars(select(Words).where(and_(Words.level==level, Words.theme=='')).slice(start,end).order_by(Words.word))
    else:
        res = session.scalars(
            select(Words).where(and_(Words.level == level, Words.theme == '', Words.phonetics == phonetics)).slice(start, end).order_by(Words.word))
    return res.all()

@sess
def get_words_theme(session, theme, start, end):

    if theme == 'all':
        res = session.scalars(
            select(Words).where(Words.theme != '').slice(start, end).order_by(Words.word))
    else:
        res = session.scalars(
            select(Words).where(Words.theme == theme).slice(start, end).order_by(Words.word))
    return res.all()

@sess
def get_count_letter(session, letter):
    res = session.scalars(select(Songs.id).distinct(Songs.group).where(Songs.letter==letter))
    res = res.all()
    return len(res)
    # result = session.execute(select(func.count()).select_from(Songs).where(Songs.letter==letter).distinct(Songs.group)).scalar()
    # return result


@sess
def get_group(session, id):
    return session.scalar(select(Songs).where(Songs.id==id))

@sess
def get_songs_group(session, group):
    res = session.scalars(select(Songs).where(Songs.group==group).order_by(Songs.album))
    res = res.all()
    albums = {}

    for song in res:
        if song.album not in albums:
            albums[song.album] = []

    for song in res:
        # ln = ''
        # if song.ln in LN:
        #     ln = LN[song.ln]
        ln = LNENGRU[song.ln]
        albums[song.album].append((song.name, song.id, ln))
    return albums

@sess
def get_songs_name(session, id_name):
    return session.scalar(select(Songs).where(Songs.id == id_name))

@sess
def get_titles_text(session, level):
    res = []
    for ph in text_phonetics_eng:
        text = session.scalars(select(Reading).where(and_(Reading.level == level, Reading.phonetics==ph[0])).order_by(Reading.phonetics))
        text = text.all()
        if len(text) != 0:
           res.append((ph[0], ph[1], text, len(text)))
    return res

@sess
def get_text_id(session, id):
    return session.scalar(select(Reading).where(Reading.id==id))


@sess
def word_themes(session):
    res = session.scalars(select(Words).where(Words.themeru!='').distinct(Words.themeru).order_by(Words.themeru))
    res = res.all()
    letters = list(set([x.themeru[:1].lower() for x in res]))
    letters.sort()
    letters_dict = {}
    for letter in letters:
        letters_dict[letter] = []
    for r in res:
        letters_dict[r.themeru[:1].lower()].append((r.theme, r.themeru))
    # print(letters_dict)
    return letters_dict

@sess
def get_words_count(session, level, phonetics):
    if phonetics == 'all':
       result = session.execute(select(func.count()).select_from(Words).where(Words.level==level)).scalar()
    else:
        result = session.execute(select(func.count()).select_from(Words).
                                 where(and_(Words.level==level, Words.phonetics==phonetics))).scalar()
    # res = result.scalar()
    return result

@sess
def get_words(session, level):
     res = session.scalars(select(Words).where(Words.level==level))
     return res.all()


@sess
def phonetics_is_words(session, phonetics, level):
    return session.execute(select(func.count()).select_from(Words).
                             where(and_(Words.level == level, Words.phonetics == phonetics))).scalar()
@sess
def get_words_theme_count(session, theme):
    if theme == 'all':
        return session.execute(select(func.count()).select_from(Words).
                               where(Words.theme != '')).scalar()
    else:
        return session.execute(select(func.count()).select_from(Words).
                           where(Words.theme == theme)).scalar()


@sess
def get_phonetics_level_words(session, level):
    res = session.scalars(select(Words.phonetics).distinct(Words.phonetics).where(Words.level==level))
    phonetics = []
    for p in res.all():
        phonetics.append((p, phonetics_list[p].upper()))
    return phonetics


@sess
def get_word_id(session, id):
    id = int(id)
    return session.scalar(select(Words.word).where(Words.id == id))

@sess
def get_word_obj_id(session, id):
    id = int(id)
    return session.scalar(select(Words).where(Words.id == id))

@sess
def get_themeru(session, theme):
    if theme=='all':
        return 'ВСЕ'
    else:
        return session.scalar(select(Words.themeru).where(Words.theme == theme))

@sess
def get_songs_ln(session, ln, start, end):

    res = session.scalars(select(Songs).where(Songs.ln == ln).slice(start, end).order_by(Songs.group))
    return res.all()

@sess
def get_wish_item(session, model, id_user, wishlist, start, end):
    '''SELECT uw.id_wishlist, s.id, s.name, uw.id_user, uw.wishlist
    FROM public.userwishlist uw
    JOIN public.songs s ON s.id = uw.id_wishlist
    WHERE uw.id_user=3'''
    res = session.scalars(
        select(model).
        select_from(UserWishList).
        join(model, model.id == UserWishList.id_wishlist).
        where(UserWishList.id_user == id_user, UserWishList.wishlist == wishlist).slice(start, end).order_by(model.id))
    return res.all()

@sess
def get_wish_books(session, model, id_user, wishlist):

    res = session.scalars(
        select(model).
        select_from(UserWishList).
        join(model, model.id == UserWishList.id_wishlist).
        where(UserWishList.id_user == id_user, UserWishList.wishlist == wishlist).order_by(model.id))
    return res.all()


@sess
def get_count_songs_ln(session, ln):
    return session.execute(select(func.count()).select_from(Songs).
                             where(Songs.ln == ln)).scalar()

@sess
def get_authors(session):
    res = session.scalars(select(Authors))
    return res.all()

@sess
def get_authors_id(session, id):
    return session.scalar(select(Authors).where(Authors.id == id))

@sess
def get_books_id_author(session, id):
    res = session.scalars(select(Books).where(Books.id_author == id))
    return res.all()

@sess
def get_book_id_author(session, id):
    return session.scalar(select(Books).where(Books.id == id))

@sess
def get_booktexts(session, id_book, start, end):
    res = session.scalars(select(Booktexts).where(Booktexts.id_book==id_book).slice(start,end).order_by(Booktexts.id))
    return res.all()

@sess
def get_count_booktexts(session, id_book):
    return  session.execute(select(func.count()).select_from(Booktexts).where(Booktexts.id_book == id_book)).scalar()

@sess
def get_booktexts_en(session, id):
    return session.scalar(select(Booktexts).where(Booktexts.id==id))

@sess
def get_books_level(session, level):
    res = session.scalars(select(Books).where(Books.level==level).order_by(Books.bookru))
    return res.all()

@sess
def get_userseng3_count_email(session, email):
    res = session.execute(
        select(func.count()).select_from(Userseng3).where(Userseng3.email == email))
    return res.scalar()

@sess
def get_userseng3_email(session, email):
    return session.scalar(select(Userseng3).where(Userseng3.email == email))

@sess
def get_userseng3_reset_token(session, reset_token):
    return session.scalar(select(Userseng3).where(Userseng3.reset_token == reset_token))

@sess
def add_usereng3(session, email, password):
    session.add(Userseng3(email=email, password=password))
    session.commit()

@sess
def set_usereng3_email_confirmed(session, user):
    session.add(user)
    user.email_confirmed = True
    session.commit()

@sess
def get_userseng3_id(session, id):
    return session.scalar(select(Userseng3).where(Userseng3.id == id))


@sess
def set_new_psw_usereng3(session, user, password):
    user.password = password
    user.reset_token = None
    user.reset_token_expiry = None
    session.add(user)
    session.commit()


@sess
def set_usereng3_token(session, user, reset_token, reset_token_expiry):
    user.reset_token = reset_token
    user.reset_token_expiry = reset_token_expiry
    session.add(user)
    session.commit()


@sess
def get_count_wish(session, id_user, wish):
    return session.execute(select(func.count()).select_from(UserWishList).
                             where(and_(UserWishList.id_user == id_user, UserWishList.wishlist == wish))).scalar()


@sess
def count_userwishlist(session, wish, id_user, id_wishlist):
    return session.execute(
        select(func.count()).select_from(UserWishList).where(and_(UserWishList.wishlist == wish,
                                                                  UserWishList.id_user == id_user,
                                                                  UserWishList.id_wishlist == id_wishlist
                                                                   ))).scalar()

@sess
def is_id_model(session, model, id):
    try:
        res = session.execute(
            select(func.count()).select_from(model).where(model.id == int(id)))
        if res.scalar() == 0:
            return False
        else:
            return True
    except Exception as e:
        return False

@sess
def set_userwishlist(session, wishlist, id_user, id_wishlist):

    session.add(UserWishList(wishlist=wishlist, id_user=id_user, id_wishlist=id_wishlist))
    session.commit()

@sess
def del_userwishlist(session, wishlist, id_user, id_wishlist):
    print( wishlist, id_user, id_wishlist)
    obj = session.scalar(select(UserWishList).where(and_(UserWishList.id_wishlist==id_wishlist,
                                                         UserWishList.wishlist==wishlist,
                                                      UserWishList.id_user==id_user
                                                      )))
    session.delete(obj)
    session.commit()

@sess
def get_search_songs_name(session, query):
    query = query[:30]
    res = session.scalars(select(Songs).where(Songs.name.ilike(f"%{query}%")).order_by(Songs.name).limit(100))
    return res.all()

@sess
def get_search_songs_group(session, query):
    query = query[:30]
    res = session.scalars(select(Songs).distinct(Songs.group).where(Songs.group.ilike(f"%{query}%")).order_by(Songs.group).limit(100))
    return res.all()

@sess
def get_search_words(session, query):
    query = query[:30]
    res = session.scalars(select(Words).where(Words.word.ilike(f"%{query}%")).order_by(Words.word).limit(100))
    return res.all()

@sess
def get_search_ru_words(session, query):
    query = query[:30]
    res = session.scalars(select(Words).where(Words.trt.ilike(f"%{query}%")).order_by(Words.trt).limit(100))
    return res.all()