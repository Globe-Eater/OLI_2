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
    countycd = StringField('County:')
    lot = StringField('Lot:')
    block = StringField('Block:')
    platename = StringField('Platename:')
    section = StringField('Section:')
    township = StringField('Township:')
    range = StringField('Range:')
    restype = StringField('Resource Type:')
    hist_func = StringField('Historic Function:')
    curr_func = StringField('Current Function:')
    areasg_1 = StringField('Area of Significance:')
    areasg_2 = StringField('Area of Significance 2:')
    desc_seg = StringField('Desc_seg:')
    doc_source = StringField('Document Source:')
    name_prep = StringField('Prepared Name:')
    survey_pro = StringField('Survey Project:')
    projectname = StringField('Project Name:')
    date_prep = StringField('Date Prepared:')
    photograph = StringField('Photograph:')
    year = StringField('Year:')
    arch_build = StringField('Arc Build:')
    year_build = StringField('Year Built:')
    orig_site = StringField('Original Site:')
    

