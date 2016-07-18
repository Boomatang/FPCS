import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'mail-relay.3ireland.ie'
    MAIL_PORT = 25
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SITE_MAIL_SUBJECT_PREFIX = '[FPCS Test Mail]'
    SITE_MAIL_SENDER = 'FPCS Server <server@jfitzpatrick.me>'
    SITE_ADMIN = os.environ.get('SITE_ADMIN')
    SITE_POSTS_PER_PAGE = 20
    SITE_FOLLOWERS_PER_PAGE = 50
    SITE_COMMENTS_PER_PAGE = 30
    SITE_SLOW_DB_QUERY_TIME = 0.5
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
