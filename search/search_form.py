from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, HiddenField, StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Email
from flask_wtf import RecaptchaField
from wtforms.widgets import HiddenInput

from setting import form_mes
from wtforms import widgets
class search_form(FlaskForm):

    query = StringField('Поиск', [
        validators.Length(min=1, max=30, message=form_mes['len1-30']),
        DataRequired(form_mes['empty']),
        ], description=form_mes['search'])