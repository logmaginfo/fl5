import os

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# current_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# current_app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))


