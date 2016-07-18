import os


def test_SITE_ADMIN_set():
    SITE_ADMIN = os.environ.get('SITE_ADMIN')
    assert SITE_ADMIN is not None