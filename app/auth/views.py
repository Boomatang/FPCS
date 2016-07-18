from . import auth


@auth.route('/login', methods=['POST', 'GET'])
def login():
    return "This is the log in page"
