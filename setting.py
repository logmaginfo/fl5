ITEMS = 20
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "num"]
levels = ["A0", "A1", "A2", "B1", "B2"]
level_words = ["A0", "A1", "A2", "B1", "B2", "C1"]
text_phonetics_eng = (("dialogue", "Диалоги"), ("joke", "Юмор"), ("storie", "Истории"), ("text", "Рассказы"))
text_phonetics_ru = ["Диалоги", "Юмор", "Истории", "Рассказы"]
phonetics_list = {
            "all":"Все",
            "adjective":"прилагательные",
            "adverb":"наречие",
            "modalverb":"модальные глаголы",
            "noun":"существительные",
            "pronoun":"местоимение",
            "question":"вопросительные",
            "verb":"глаголы",
            "dialogue":"диалоги",
            "joke":"с юмором",
            "storie": "истории",
            "text":"рассказы",
        }
# поддерживаемые языки
LN = {'af': 'Afrikaans', 'am': 'Amharic', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'eu': 'Basque', 'fi': 'Finnish', 'fr-CA': 'French (Canada)', 'fr': 'French', 'gl': 'Galician', 'gu': 'Gujarati', 'ha': 'Hausa', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew', 'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'la': 'Latin', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ms': 'Malay', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi (Gurmukhi)', 'pl': 'Polish', 'pt-PT': 'Portuguese (Portugal)', 'pt': 'Portuguese (Brazil)', 'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak', 'sq': 'Albanian', 'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'yue': 'Cantonese', 'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)'}

level_books = ['A1','A2','B1','B2','C1']
# языки с названием по англ из таблицы songs
LNENGRU = {'aa': 'Afar / Язык народа Афар',
           'ace': 'Achinese / Ахинаский язык',
         'af': 'Afrikaans / Африкаанс',
           'ar': 'Arabic / Арабский язык',
         'av': 'Avaric / Аварийный язык',
           'ay': 'Aymara / Аймара',
           'ba': 'Bashkir / Башкирский язык',
         'ber-Latn': 'Berber / Бербер',
           'bg': 'Bulgarian / Болгарский язык',
         'bn': 'Bengali / Бенгальский язык',
           'br': 'Breton / Бретонский язык',
         'bs': 'Bosnian / Боснийский язык',
           'ca': 'Catalan / Каталонский язык',
         'ce': 'Chechen / Чеченский язык',
           'ch': 'Chamorro / Чаморро',
           'cs': 'Czech / Чешский язык',
         'cy': 'Welsh / Валлийский язык',
           'da': 'Danish / Датский язык',
           'de': 'German / Немецкий язык',
         'din': 'Dinka / Динка',
           'el': 'Greek / Греческий язык',
         'en': 'English / Английский язык',
           'es': 'Spanish / Испанский язык',
           'et': 'Estonian / Эстонский язык',
         'fa': 'Persian / Персидский язык',
           'fi': 'Finnish / Финский язык',
           'fj': 'Fijian / Фиджийский язык',
         'fo': 'Faroese / Фарезезальный язык',
           'fr': 'French / Французский язык',
           'fur': 'Friulian / Фриулианский язык',
         'ga': 'Irish / Ирландский язык',
           'gd': 'Scottish / Шотландский язык',
           'gl': 'Galician / Галицкий язык',
         'gn': 'Guarani / Гуарани язык',
           'gu': 'Gujarati / Гуджаратский язык',
           'gv': 'Manx / Язык Manx',
         'ha': 'Hausa / Хауса язык',
           'haw': 'Hawaiian / Гавайский язык',
           'hi': 'Hindi / Хинди',
           'hmn': 'Hmong / Хмонг',
         'hr': 'Croatian / Хорватский язык',
           'hrx': 'Hunsrik / Язык Хунсрика',
           'hu': 'Hungarian / Венгерский язык',
         'id': 'Indonesian / Индонезийский язык',
           'ilo': 'Ilocana / Илоканский язык',
         'is': 'Icelandic / Исландский язык',
           'it': 'Italian / Итальянский язык',
           'iw': 'Hebrew / Еврейский язык',
         'ja': 'Japanese / Японский язык',
           'jam': 'Creole / Креольский язык',
           'ka': 'Georgian / Грузинский язык',
         'kha': 'Khasi / Хаси язык',
           'kn': 'Kannada / Язык каннада (Карнатака, Республика Индия)',
         'ko': 'Korean / Корейский язык',
         'kri': 'Creole / Креольский язык',
           'ku': 'Kurdish / Курдский язык',
           'la': 'Latin / Латинский язык',
         'lb': 'Luxembourgish / Люксембургисский язык',
           'li': 'Limburgish / Лимбургический язык',
         'lij': 'Ligurian / Лигурийский язык',
           'lmo': 'Lombard / Ломбардский язык',
         'lt': 'Lithuanian / Литовский язык',
         'lus': 'Lushai / Лушаи (лушей)',
         'lv': 'Latvian / Латвийский язык',
           'mad': 'Madurese / Мадуресский язык',
         'mi': 'Maori / Язык маори',
           'mn': 'Mongolian / Монгольский язык',
           'mt': 'Maltese / Мальтийский язык',
         'nl': 'Dutch / Голландский язык',
           'no': 'Norwegian / Норвежский язык',
           'oc': 'Occitan / Оксутанский язык',
         'om': 'Oromo / Язык оромо',
           'pl': 'Polish / Польский язык',
           'pt': 'Portuguese (Brazil) / Португальский (Бразилия) язык',
         'pt-PT': 'Portuguese (Portugal) / Португальский (Португалия) язык',
           'ro': 'Romanian / Румынский язык',
         'ru': 'Russian / Русский язык',
           'scn': 'Sicilian / Сицилийский язык',
           'se': 'Northern Sami / Северный саамский язык',
         'sl': 'Slovenian / Словенский язык',
           'sm': 'Samoan language / Самоанский язык язык',
         'so': 'Somali language / Сомалийский язык',
           'sq': 'Albanian / Албанский язык',
         'sr': 'Serbian / Сербский язык',
           'sv': 'Swedish / Шведский язык',
         'sw': 'Swahili / Суахили язык',
           'ta': 'Tamil / Тамильский язык',
           'te': 'Telugu / Язык телугу',
         'th': 'Thai / Тайский язык',
           'tl': 'Filipino / Филиппинский язык',
           'tr': 'Turkish / Турецкий язык',
         'tt': 'Tatar language / Язык татар',
           'uk': 'Ukrainian / Украинский язык',
           'ur': 'Urdu / Язык урду',
         'vec': 'Venetian language / Язык в венецианском языке',
           'wo': 'Wolof language /Волоф (Республика Гамбия, Исламская Республика Мавритания, Республика Сенегал)',
         'zap': 'Zapotensky / Запотенский язык',
           'zh-CN': 'Chinese (Simplified) / Китайский (упрощенный) язык',
         'zu': 'Zulu / Зулу'}

alphabet_dict = {
"A": "[eɪ] Эй",
"B": "[biː] Би",
"C": "[siː] Си",
"D": "[diː] Ди",
"E": "[iː] И",
"F": "[ɛf] Эф",
"G": "[dʒiː]	Джи",
"H": "[eɪtʃ]	Эйч",
"I": "[aɪ] Ай",
"J": "[dʒeɪ]	Джей",
"K": "[keɪ] Кей",
"L": "[ɛl] Эл",
"M": "[ɛm] Эм",
"N": "[ɛn] Эн",
"O": "[əʊ] Оу",
"P": "[piː] Пи",
"Q": "[kjuː] Кью",
"R": "[ɑr] Ар",
"S": "[ɛs] Эс",
"T": "[tiː] Ти",
"U": "[juː] Ю",
"V": "[viː] Ви",
"W": "[ˈdʌb(ə)l juː] Дабл-ю",
"X": "[ɛks] Экс",
"Y": "[waɪ] Уай",
"Z": "[zɛd] Зэд",
}
alphabet_list = [
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
"L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
"W", "X", "Y", "Z"]

alphabet_ = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

num_ = ["1","2","3","4","5","6","7","8","9","0"]

al_ru = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

pr = [" ", "-"]

lat_ru_num_pr = alphabet_list + alphabet_ + num_ + al_ru + pr


zn_ = ["!","#","$","%","&","*","+"]

form_mes = {
    "empty":"Поле должно быть заполнено.",
    "confirm":"Пароли должны совпадать.",
    "noemail":"Некорректный email.",
    "len6-15": "От 6 до 15 символов.",
    "len1-30": "От 1 до 30 символов.",
    "email":"Email",
    "psw":"Пароль",
    "search":"Поиск",
    "confirm_pl":"Пароль еще раз",
    "sender":"eng3.ru регистрация на сайте",
}



wishlist = {
           "songs":"Треки", "books": "Книги", "reading":"Тексты",  "words": "Слова"
           }