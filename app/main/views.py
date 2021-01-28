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
         post = hpr.query.filter_by(propname=form.property.data)#,
         flash("Query Submitted.")
    #                        #resname=form.resname.data,
    #                        #address=form.address.data,
    #                        #city=form.city.data)
    #    return render_template('query.html', form=form, result=results)
    posts = hpr.query.all()
    return render_template('query.html', form=form, posts=posts)

@main.route('/results')
def search_results():
    #query_result = hpr.query.filter(propname=propname).all()
    return render_template('results.html')
