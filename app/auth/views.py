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
    form1 = EditForm()
    form2 = UpdateForm()
    if form1.validate_on_submit():
        if form1.objectid.data:
             posts = hpr.query.filter_by(objectid=form1.objectid.data)
        elif form1.propname.data:
             posts = hpr.query.filter_by(propname=form1.propname.data)
        elif form1.resname.data:
             posts = hpr.query.filter_by(resname=form1.resname.data)
        elif form1.address.data:
             posts = hpr.query.filter_by(address=form1.address.data)
        elif form1.city.data:
             posts = hpr.query.filter_by(city=form1.city.data)
        flash("Query Submitted.")
    # Get Object Id from search.
    # Once found enable form2 to update record.
    if form2.validate_on_submit():
        record = hpr(propname=form2.propname.data,
             resname=form2.resname.data,
             address=form2.address.data,
             city=form2.city.data,
             vicinity=form2.vicinity.data,
             countycd=form2.countycd.data,
             lot=form2.lot.data,
             block=form2.block.data,
             platename=form2.platename.data,
             section=form2.section.data,
             township=form2.township.data,
             range=form2.range.data,
             restype=form2.restype.data,
             hist_func=form2.hist_func.data,
             curr_func=form2.curr_func.data,
             areasg_1=form2.areasg_1.data,
             areasg_2=form2.areasg_2.data,
             desc_seg=form2.desc_seg.data,
             doc_source=form2.doc_source.data,
             name_prep=form2.name_prep.data,
             survey_pro=form2.survey_pro.data,
             projectname=form2.projectname.data,
             date_prep=form2.date_prep.data,
             photograph=form2.photograph.data,
             year=form2.year.data,
             arch_build=form2.arch_build.data,
             year_build=form2.year_build.data,
             orig_site=form2.orig_site.data,
             datemoved=form2.datemoved.data,
             fromwhere=form2.fromwhere.data,
             accessible=form2.accessible.data,
             arch_style=form2.arch_style.data,
             other_arch=form2.other_arch.data,
             foun_mat=form2.foun_mat.data,
             roof_type=form2.roof_type.data,
             roof_mat=form2.roof_mat.data,
             wall_mat_1=form2.wall_mat_1.data,
             wall_mat_2=form2.wall_mat_2.data,
             window_typ=form2.window_typ.data,
             window_mat=form2.window_mat.data,
             door_typ=form2.door_typ.data,
             exter_fea=form2.exter_fea.data,
             inter_fea=form2.inter_fea.data,
             dec_detail=form2.dec_detail.data,
             condition=form2.condition.data,
             des_res=form2.des_res.data,
             comments=form2.comments.data,
             placement=form2.placement.data,
             lonr=form2.lonr.data,
             continuation=form2.continuation.data,
             nrdata=form2.nrdata.data,
             date_updated=form2.date_updated.data,
             lat=form2.lat.data,
             long=form2.lon.data,
             utm_zone=form2.utm_zone.data,
             easting=form2.easting.data,
             northing=form2.northing.data,
             p_b_c=form2.p_b_c.data,
             year_closed=form2.year_closed.data)
     # merge objectid record with new info.
        db.session.merge(record)
        db.session.commit()
        return render_template('auth/edit.html', form1=form1, form2=form2, posts=posts) 
    return render_template('auth/edit.html', form1=form1, form2=form2)

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

