from flask import render_template, redirect, request, url_for, flash,\
    Response
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.utils import secure_filename 
from . import auth
from .. import db
from ..models import User, hpr, image
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

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg'}
    return '.' in filename and \
           filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/record_entry', methods=['GET', 'POST'])
@login_required
def data_entry():
    form = EntryForm()
    if form.validate_on_submit():
        f = form.image.data
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            form.image.data.save("app/static/Stored_Images/" + filename)
        pic = image(picture=form.image.data.filename,
                    user_id=current_user.id)
        record = hpr(
            propname=form.propname.data,
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
        db.session.add(pic)
        db.session.flush()
        pic.prop_id = record.objectid
        db.session.commit()
        flash('Record Submitted')
        return redirect(url_for('auth.menu'))
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

@auth.route('/results/<int:post_id>', methods=['GET', 'POST'])
@login_required
def results(post_id):
    post = hpr.query.get_or_404(post_id)
    pic = image.query.filter_by(prop_id = post_id).all()
    image_name = image.query.filter_by(prop_id=post_id).first()
    if image_name == None:
        image_storage = None
    elif image_name == True:
        image_name = image.query.filter_by(prop_id=post_id).first()
        image_storage = "../static/Stored_Images/" + image_name.picture
    form = EntryForm()
    if form.validate_on_submit():
        post.propname = form.propname.data
        post.resname=form.resname.data
        post.address=form.address.data
        post.city=form.city.data
        post.vicinity=form.vicinity.data
        post.countycd=form.countycd.data
        post.lot=form.lot.data
        post.block=form.block.data
        post.platename=form.platename.data
        post.section=form.section.data
        post.township=form.township.data
        post.range=form.range.data
        post.restype=form.restype.data
        post.hist_func=form.hist_func.data
        post.curr_func=form.curr_func.data
        post.areasg_1=form.areasg_1.data
        post.areasg_2=form.areasg_2.data
        post.desc_seg=form.desc_seg.data
        post.doc_source=form.doc_source.data
        post.name_prep=form.name_prep.data
        post.survey_pro=form.survey_pro.data
        post.projectname=form.projectname.data
        post.date_prep=form.date_prep.data
        post.photograph=form.photograph.data
        post.year=form.year.data
        post.arch_build=form.arch_build.data
        post.year_build=form.year_build.data
        post.orig_site=form.orig_site.data
        post.datemoved=form.datemoved.data
        post.fromwhere=form.fromwhere.data
        post.accessible=form.accessible.data
        post.arch_style=form.arch_style.data
        post.other_arch=form.other_arch.data
        post.foun_mat=form.foun_mat.data
        post.roof_type=form.roof_type.data
        post.roof_mat=form.roof_mat.data
        post.wall_mat_1=form.wall_mat_1.data
        post.wall_mat_2=form.wall_mat_2.data
        post.window_typ=form.window_typ.data
        post.window_mat=form.window_mat.data
        post.door_typ=form.door_typ.data
        post.exter_fea=form.exter_fea.data
        post.inter_fea=form.inter_fea.data
        post.dec_detail=form.dec_detail.data
        post.condition=form.condition.data
        post.des_res=form.des_res.data
        post.comments=form.comments.data
        post.placement=form.placement.data
        post.lonr=form.lonr.data
        post.continuation=form.continuation.data
        post.nrdata=form.nrdata.data
        post.date_updated=form.date_updated.data
        post.lat=form.lat.data
        post.long=form.lon.data
        post.utm_zone=form.utm_zone.data
        post.easting=form.easting.data
        post.northing=form.northing.data
        post.p_b_c=form.p_b_c.data
        post.year_closed=form.year_closed.data
        db.session.commit()
        flash("Record updated.")
        return redirect(url_for('auth.results', post_id=post.objectid, form=form,
                               display_image=image_storage))
    elif request.method == 'GET':
        form.propname.data = post.propname
        form.resname.data = post.resname
        form.address.data = post.address
        form.vicinity.data = post.vicinity
        form.countycd.data = post.countycd
        form.lot.data = post.lot
        form.block.data = post.block
        form.platename.data = post.platename
        form.section.data = post.section
        form.township.data = post.township
        form.range.data = post.range
        form.restype.data = post.restype
        form.hist_func.data = post.hist_func
        form.curr_func.data = post.curr_func
        form.areasg_1.data = post.areasg_1
        form.areasg_2.data = post.areasg_2
        form.desc_seg.data = post.desc_seg
        form.doc_source.data = post.doc_source
        form.name_prep.data = post.name_prep
        form.survey_pro.data = post.survey_pro
        form.projectname.data = post.projectname
        form.date_prep.data = post.date_prep
        form.photograph.data = post.photograph
        form.year.data = post.year
        form.arch_build.data = post.arch_build
        form.other_arch.data = post.other_arch
        form.foun_mat.data = post.foun_mat
        form.roof_type.data = post.roof_type
        form.roof_mat.data = post.roof_mat
        form.wall_mat_1.data = post.wall_mat_1
        form.wall_mat_2.data = post.wall_mat_2
        form.window_typ.data = post.window_typ
        form.window_mat.data = post.window_mat
        form.door_typ.data = post.door_typ
        form.exter_fea.data = post.exter_fea
        form.inter_fea.data = post.inter_fea
        form.dec_detail.data = post.dec_detail
        form.condition.data = post.condition
        form.des_res.data = post.des_res
        form.comments.data = post.comments
        form.placement.data = post.placement
        form.lonr.data = post.lonr
        form.continuation.data = post.continuation
        form.nrdata.data = post.nrdata
        form.date_updated.data = post.date_updated
        form.lat.data = post.lat
        form.lon.data = post.long
        form.utm_zone.data = post.utm_zone
        form.easting.data = post.easting
        form.northing.data = post.northing
        form.p_b_c.data = post.p_b_c
        form.year_closed.data = post.year_closed
    return render_template('auth/results.html', post=post, form=form,
                           display_image=image_storage)

@auth.route('/image/<int:index>')
def get_img(index):
    img = image.query.filter_by(index=index).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.picture)

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

