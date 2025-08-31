from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, SelectField, HiddenField, StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Email
from flask_wtf import RecaptchaField
from wtforms.widgets import HiddenInput

from setting import form_mes


class login_form(FlaskForm):
    email = StringField('Email', [
        validators.Length(min=6, max=35, message=form_mes['len6-15']),
        DataRequired(form_mes['empty']),
        Email(message=form_mes['noemail'])],
                        description=form_mes['email'])
    password = PasswordField(form_mes['psw'], [
        validators.DataRequired(form_mes['empty']),
        validators.Length(min=6, max=15, message=form_mes['len6-15']),
    ], description=form_mes['psw'])
    remember_me = BooleanField('')

class reg_form(FlaskForm):
    email = StringField('Email', [
        validators.Length(min=6, max=35, message=form_mes['len6-15']),
        DataRequired(form_mes['empty']),
        Email(message=form_mes['noemail'])],
        description=form_mes['email'])
    password = PasswordField(form_mes['psw'], [
        validators.DataRequired(form_mes['empty']),
        validators.Length(min=6, max=15, message=form_mes['len6-15']),
        validators.EqualTo('confirm', message=form_mes['confirm'])
    ], description=form_mes['psw'])
    confirm = PasswordField(form_mes['psw'], [
        validators.DataRequired(form_mes['empty']),
        validators.Length(min=6, max=15, message=form_mes['len6-15']),
        ], description=form_mes['confirm_pl'])
    accept_tos = BooleanField('', [validators.DataRequired(form_mes['empty'])])
    agreement = BooleanField('', [validators.DataRequired(form_mes['empty'])])

class email_confirmed2_form(FlaskForm):
    email = HiddenInput('email')

class forgot_psw_form(FlaskForm):
    email = StringField('Email', [
        validators.Length(min=6, max=35, message=form_mes['len6-15']),
        DataRequired(form_mes['empty']),
        Email(message=form_mes['noemail'])],
                        description=form_mes['email'])

class new_psw_form(FlaskForm):
    password = PasswordField(form_mes['psw'], [
        validators.DataRequired(form_mes['empty']),
        validators.Length(min=6, max=15, message=form_mes['len6-15']),
        validators.EqualTo('confirm', message=form_mes['confirm'])
    ], description=form_mes['psw'])
    confirm = PasswordField(form_mes['psw'], [
        validators.DataRequired(form_mes['empty']),
        validators.Length(min=6, max=15, message=form_mes['len6-15']),
        ], description=form_mes['confirm_pl'])

