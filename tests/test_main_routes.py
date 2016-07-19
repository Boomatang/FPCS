from flask import url_for
from app import create_app, db
import pytest


@pytest.fixture(scope='module')
def app(request):
    appx = create_app('testing')
    app_context = appx.app_context()
    app_context.push()
    client = appx.test_client(use_cookies=True)
    db.create_all()

    def tearDown():
        db.session.remove()
        db.drop_all()
        app_context.pop()

    request.addfinalizer(tearDown)
    return client


def test_index(app):
    assert app.get(url_for('main.index'))


def test_login(app):
    assert app.get(url_for('auth.login'))


