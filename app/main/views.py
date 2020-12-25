from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_reponse
from flask_login import login_required, current_user
from flask_sqlalchmey import get_debug_queries
from . import main
from .forms import SearchForm, QueryForm
from .. import db
from ..models import Permission, Role, User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = QueryForm()
    return render_template('query.html', form-form)
