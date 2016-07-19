from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, BooleanField, DecimalField, FileField, TextAreaField, \
    PasswordField, SubmitField
from wtforms.validators import data_required, Length, Email, Regexp, EqualTo, ValidationError


class LoginForm(Form):
    """
    This form is used to shown the login fields
    """
    email = StringField('Email', validators=[data_required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[data_required()])
    remember_me = BooleanField('Remember me')
