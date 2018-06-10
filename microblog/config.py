import os
basedir = os.path.abspath(os.path.dirname(__file__))

# The configuration settings are defined as class variables
# inside the Config class. As the application needs more
# configuration items, they can be added to this class, and
# later if I find that I need to have more than one configuration
# set, I can create subclasses of it.

class Config(object):
    # Flask and some of its extensions use the value of the secret key
    # as a cryptographic key, useful to generate signatures or tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = 1
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = 'scott.underwood.dev@gmail.com'
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = '6%NDZP5O%y^h2KuJdJu3'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['scott.underwood.dev@gmail.com']
    POSTS_PER_PAGE = 25
