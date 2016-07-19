from . import auth
from flask import render_template, url_for, redirect, request, flash
from .forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from tool_lib import build_dict, split_str

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed:

            # todo this should be fixed
            return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Welcome, You have been logged in.', 'info')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/add_user', methods=['POST', 'GET'])
def add_user():

    if request.method == 'POST':
        form = request.form

        form_values = build_dict(split_str(form))

        for i in form_values:
            flash('this data was gotten %r' % i)
        return redirect(url_for('auth.add_user'))

    return render_template('auth/add_users.html')
