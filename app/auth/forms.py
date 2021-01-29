from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, hpr

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

class EditForm(FlaskForm):
    propname = StringField('Property Name:')
    resname = StringField('Resource Name:')
    address = StringField('Address:')
    city = StringField('City:')
    submit =  SubmitField('Search')

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
    datemoved = StringField('Date Moved:')
    fromwhere = StringField('From where:')
    accessible = StringField('Accessible:')
    arch_style = StringField('Arch Style:')
    other_arch = StringField('Other Arch:')
    foun_mat = StringField('Foundation material:')
    roof_type = StringField('Roof Type:')
    roof_mat = StringField('Roof Material:')
    wall_mat_1 = StringField('Wall Material 1:')
    wall_mat_2 = StringField('Wall Material 2:')
    window_typ = StringField('Window Type:')
    window_mat = StringField('Window Material:')
    door_typ = StringField('Door Type:')
    door_mat = StringField('Door Material:')
    exter_fea = StringField('External Features:')
    inter_fea = StringField('Interal Features:')
    dec_detail = StringField('Dec_detail:')
    condition = StringField('Condition:')
    des_res = StringField('Des_res:')
    comments = StringField('Comments:')
    placement = StringField('Placement:')
    lonr = StringField('Lonr:')
    continuation = StringField('Continuation:')
    nrdata = StringField('National Register:')
    date_updated = StringField('Date Updated')
    lat = StringField('Latitude:')
    lon = StringField('Longitude:')
    utm_zone = StringField('UTM Zone:')
    easting = StringField('Easting:')
    northing = StringField('Northing:')
    p_b_c = StringField('Property/Bridge/Cemetary:')
    year_closed = StringField('Year Closed:')
    submit = SubmitField('Submit')
