import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db as mdb
from app.models import *
from app.email import send_email

app = create_app(os.getenv('SITE_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=mdb, User=User, Company=Company, Contact=Contact, email=send_email)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
