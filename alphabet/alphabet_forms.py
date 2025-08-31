from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, HiddenField


def at(alphabet44=None, alphabet11=None, alphabet4_hidd=None):
    # data = [('A', 'Aa'), ('B', 'Bb'), ('C', 'Cc'), ('D', 'Dd')]
    class AlphabetTest(FlaskForm):
        alphabet4 = RadioField(choices=alphabet44)
        alphabet1 = HiddenField(alphabet11)
        alphabet4_hidden = HiddenField(alphabet4_hidd)
        submit = SubmitField('Проверить')
    return AlphabetTest()
