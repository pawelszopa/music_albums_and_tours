from flask_wtf import FlaskForm
from wtforms import StringField
from flask_babel import lazy_gettext as _l
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=3, max=20, messsage=_l('Username must be between 3 and 20 characters long.')),
    ])
    email = EmailField(_l('Email *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=6, max=30, messsage=_l('Email must be between 3 and 30 characters long.')),
        Email(message='You did not enter a valid email!')
    ])
    username = StringField(_l('Username *'), validators=[
        DataRequired(_l('Data is Required')),
        InputRequired(_l('Input is Required')),
        Length(min=3, max=20, messsage=_l('Username must be between 3 and 28 characters long.')),
    ])
    # * pole wymagane