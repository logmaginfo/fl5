from flask import url_for
from flask_mail import Mail, Message
import os
from app_flask import app


app.config.update(dict(
    DEBUG = False,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
))

mail = Mail(app)

def send_email(to, subject, template):
    print(to, subject, template)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        # sender=form_mes['sender']
        sender="eng3.ru"
    )
    mail.send(msg)


def send_reset_email(email, token):
    """Send a password reset email to the user"""
    # token = user.set_reset_token()
    # with sync_session() as session:
    #     session.add(user)
    #     session.commit()  # Save the token to database

    reset_url = url_for('login.reset_password', token=token, _external=True)
    msg = Message(
        'Запрос на сброс пароля eng3.ru',
        recipients=[email],
        html=f'''Чтобы сбросить пароль, перейдите по следующей ссылке:
                {reset_url}            
                Если вы не отправляли такой запрос, просто проигнорируйте это письмо, и никакие изменения не будут внесены.
                Срок действия этой ссылки истечет через 1 час..
                ''',
        # sender=form_mes['sender']
        sender="eng3.ru"
    )
    mail.send(msg)


