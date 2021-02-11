from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User, hpr
from .forms import LoginForm, MenuForm, EntryForm, EditForm, UpdateForm 

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
        record = hpr(propname=form.propname.data,
             resname=form.resname.data,
             address=form.address.data,
             city=form.city.data,
             vicinity=form.vicinity.data,
             countycd=form.countycd.data,
             lot=form.lot.data,
             block=form.block.data,
             platename=form.platename.data,
             section=form.section.data,
             township=form.township.data,
             range=form.range.data,
             restype=form.restype.data,
             hist_func=form.hist_func.data,
             curr_func=form.curr_func.data,
             areasg_1=form.areasg_1.data,
             areasg_2=form.areasg_2.data,
             desc_seg=form.desc_seg.data,
             doc_source=form.doc_source.data,
             name_prep=form.name_prep.data,
             survey_pro=form.survey_pro.data,
             projectname=form.projectname.data,
             date_prep=form.date_prep.data,
             photograph=form.photograph.data,
             year=form.year.data,
             arch_build=form.arch_build.data,
             year_build=form.year_build.data,
             orig_site=form.orig_site.data,
             datemoved=form.datemoved.data,
             fromwhere=form.fromwhere.data,
             accessible=form.accessible.data,
             arch_style=form.arch_style.data,
             other_arch=form.other_arch.data,
             foun_mat=form.foun_mat.data,
             roof_type=form.roof_type.data,
             roof_mat=form.roof_mat.data,
             wall_mat_1=form.wall_mat_1.data,
             wall_mat_2=form.wall_mat_2.data,
             window_typ=form.window_typ.data,
             window_mat=form.window_mat.data,
             door_typ=form.door_typ.data,
             exter_fea=form.exter_fea.data,
             inter_fea=form.inter_fea.data,
             dec_detail=form.dec_detail.data,
             condition=form.condition.data,
             des_res=form.des_res.data,
             comments=form.comments.data,
             placement=form.placement.data,
             lonr=form.lonr.data,
             continuation=form.continuation.data,
             nrdata=form.nrdata.data,
             date_updated=form.date_updated.data,
             lat=form.lat.data,
             long=form.lon.data,
             utm_zone=form.utm_zone.data,
             easting=form.easting.data,
             northing=form.northing.data,
             p_b_c=form.p_b_c.data,
             year_closed=form.year_closed.data)
        db.session.add(record)
        db.session.commit()
        flash('Record Sumbitted.')
    return render_template('auth/entry.html', form=form)

@auth.route('/edit_records', methods=['GET', 'POST'])
@login_required
def edit_records():
    form = EditForm()
    if form.validate_on_submit():
        if form.objectid.data:
             posts = hpr.query.filter_by(objectid=form.objectid.data)
        elif form.propname.data:
             posts = hpr.query.filter_by(propname=form.propname.data)
        elif form.resname.data:
             posts = hpr.query.filter_by(resname=form.resname.data)
        elif form.address.data:
             posts = hpr.query.filter_by(address=form.address.data)
        elif form.city.data:
             posts = hpr.query.filter_by(city=form.city.data)
        flash("Query Submitted.")
        return render_template('auth/edit.html', form=form, posts=posts) 
    return render_template('auth/edit.html', form=form)


@auth.route('/result<int:post_id>', methods=['GET', 'POST'])
@login_required
def results(post_id):
    post = hpr.query.get_or_404(post_id)
    form = EntryForm()
    if form.validate_on_submit():
        post.propname = form.propname.data
        db.session.commit()
        flash("Record updated.")
        return redirect(url_for('auth.results', post_id=post.objectid, form=form))
    elif request.method == 'GET':
        form.propname.data = post.propname
        form.resname.data = post.resname
        form.address.data = post.address
    return render_template('auth/results.html', post=post, form=form)

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

