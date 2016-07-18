from flask import url_for


def test_index(app):
    assert app.get(url_for('main.index'))


def test_login(app):
    assert app.get(url_for('auth.login'))


