from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class MenuForm(FlaskForm):
    enter_data = SubmitField('Enter Data')
    search_data = SubmitField('Search Database')
    edit_data = SubmitField('Edit Records')

class EntryForm(FlaskForm):
    propname = StringField('Property Name:', validators=[DataRequired()])
    resname = StringField('Resource Name:')
    address = StringField('Address:')
    city  = StringField('City:')
    vicinity = StringField('Vicinity:')

