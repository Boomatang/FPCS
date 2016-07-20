import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db as mdb
from app.models import *
from app.email import send_email
from config import Config

COV = None
if os.environ.get('SITE_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('SITE_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=mdb, User=User, Company=Company, Contact=Contact, email=send_email)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def add_admin():
    """This adds the fist user, The Administrator."""
    email = Config.SITE_ADMIN
    password = input('Enter Admin Password >>> ')
    name = input('Enter Display Name >>> ')

    user = User(email, password, name)
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    print("%s has been added to the system as Admin" % user.username)


@manager.command
def test(coverage=False):
    """Run the unit test."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import pytest
    pytest.main('-v')

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
    # app.run()
