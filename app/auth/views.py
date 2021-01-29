from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User, hpr
from .forms import LoginForm, MenuForm, EntryForm, EditForm 

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('auth.menu'))
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def acc_logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('main.index'))

@auth.route('/success', methods=['GET', 'POST'])
@login_required
def menu():
    form = MenuForm()
    if form.validate_on_submit():
        if form.enter_data.data:
            return redirect(url_for('auth.data_entry'))
        elif form.search_data.data:
            return redirect(url_for('main.search'))
        elif form.edit_data.data:
            return redirect(url_for('auth.edit_records'))
    return render_template('auth/success.html', form=form)

@auth.route('/record_entry', methods=['GET', 'POST'])
@login_required
def data_entry():
    form = EntryForm()
    if form.validate_on_submit():
        record = hpr(propname=form.propname.data)
        db.session.add(record)
        db.session.commit()
    flash('Record Sumbitted.')
    return render_template('auth/entry.html', form=form)

@auth.route('/edit_records', methods=['GET', 'POST'])
@login_required
def edit_records():
    form = EditForm()
    if form.validate_on_submit():
        posts = hpr.query.filter_by(propname=form.propname.data, 
                                   resname=form.resname.data,
                                   address=form.address.data,
                                   city=form.city.data)
        return render_template('auth/edit.html', form=form, posts=posts)
    return render_template('auth/edit.html', form=form)

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

