from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_babel import lazy_gettext as _l
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, ValidationError

from app.auth.models import User


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 20 characters long.'))
    ])
    email = EmailField(_l('Email *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=6, max=30, message=_l('Email must be between 3 and 30 characters long.')),
        Email(message=_l('You did not enter a valid email!'))
    ])

    password = PasswordField(_l('Password *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 28 characters long.')),
        EqualTo('password_confirm', message=_l('Password must match!'))
    ])
    password_confirm = PasswordField(_l('Username *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
    ])
    submit = SubmitField(_l('Register'))

    # * pole wymagane

    @staticmethod
    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('Username already exists!'))

    @staticmethod
    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l('email already exists!'))


class LoginForm(FlaskForm):
    email = EmailField(_l('Your email: *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=6, max=30, message=_l('Email must be between 3 and 30 characters long.')),
        Email(message=_l('You did not enter a valid email!'))
    ])
    password = PasswordField(_l('Your password: *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=3, max=20, message=_l('Username must be between 3 and 28 characters long.'))
    ])
    remember_me = BooleanField(_l('Keep me logged in'))
    submit = SubmitField(_l('Log in'))
