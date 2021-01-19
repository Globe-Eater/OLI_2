from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, QueryForm
from .. import db
from ..models import Permission, Role, User, hpr

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/query')
    return render_template('index.html', form=form)

@main.route('/query', methods=['GET', 'POST'])
def search():
    form = QueryForm()
    if form.validate_on_submit():
        return render_template('results.html')
    return render_template('query.html', form=form)

@main.route('/results')
def search_results():
    return render_template('results.html')
