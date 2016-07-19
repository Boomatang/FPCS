from . import main
from .. import db

from flask import render_template


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('main/index.html')
