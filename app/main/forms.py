from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User

class QueryForm(FlaskForm):
    object_id = StringField('ID:')
    property = StringField('Property name:')
    resname = StringField('Resource name:')
    address = StringField('Address: ')
    city = StringField('City name: ')
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    submit = SubmitField('Search')
