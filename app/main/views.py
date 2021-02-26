from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, QueryForm
from .. import db
from ..models import Permission, Role, User, hpr, image

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
         if form.object_id.data:
              posts = hpr.query.filter_by(objectid=form.object_id.data)
         elif form.property.data:
              posts = hpr.query.filter_by(propname=form.property.data)
         elif form.resname.data:
              posts = hpr.query.filter_by(resname=form.resname.data)
         elif form.address.data:
              posts = hpr.query.filter_by(address=form.address.data)
         elif form.city.data:
              posts = hpr.query.filter_by(city=form.city.data)
         flash("Query Submitted.")
         return render_template('query.html', form=form, posts=posts)
    return render_template('query.html', form=form)

@main.route('/record/<int:post_id>', methods=['GET', 'POST'])
def search_results(post_id):
    post = hpr.query.get_or_404(post_id)
    image_name = image.query.filter_by(prop_id=post_id).first()
    if image_name == None:
        image_storage = None
    elif image_name == True:
        image_name = image.query.filter_by(prop_id=post_id).first()    
        image_storage = "../static/Stored_Images/" + image_name.picture
    return render_template('record.html', post_id=post.objectid, post=post, 
                          display_image=image_storage)

@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
