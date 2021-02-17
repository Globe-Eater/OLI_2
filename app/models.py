from datetime import datetime
from flask import current_app, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import db

class Permission:
    SEARCH = 1
    ENTRY = 2
    EDIT = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.premissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.SEARCH, Permission.ENTRY],
            'Moderator': [Permission.SEARCH, Permission.ENTRY, Permission.EDIT,
                          Permission.EDIT, Permission.MODERATE],
            'Administrator': [Permission.SEARCH, Permission.ENTRY, Permission.EDIT,
                              Permission.EDIT, Permission.MODERATE,
                              Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('hpr', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username

class image(db.Model):
    __tablename__ = 'image'
    index = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.Text)
    prop_id = db.Column(db.Integer, db.ForeignKey('hpr.objectid'))
    prop = db.relationship('hpr', foreign_keys=prop_id)

class hpr(db.Model):
    __tablename__ = 'hpr'
    index = db.Column(db.Integer)
    objectid = db.Column(db.Integer, primary_key=True)
    propname = db.Column(db.String())
    resname = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    vicinity = db.Column(db.String())
    countycd = db.Column(db.Float())
    lot = db.Column(db.String())
    block = db.Column(db.String())
    platename = db.Column(db.String())
    section = db.Column(db.String())
    township = db.Column(db.String())
    range = db.Column(db.String())
    restype = db.Column(db.String())
    hist_func = db.Column(db.String())
    curr_func = db.Column(db.String())
    areasg_1 = db.Column(db.String())
    areasg_2 = db.Column(db.String())
    desc_seg = db.Column(db.String())
    doc_source = db.Column(db.String())
    name_prep = db.Column(db.String())
    survey_pro = db.Column(db.String())
    projectname = db.Column(db.String())
    date_prep = db.Column(db.String())
    photograph = db.Column(db.String())
    year = db.Column(db.String())
    arch_build = db.Column(db.String())
    year_build = db.Column(db.String())
    orig_site = db.Column(db.String())
    datemoved = db.Column(db.String())
    fromwhere = db.Column(db.String())
    accessible = db.Column(db.String())
    arch_style = db.Column(db.String())
    other_arch = db.Column(db.String())
    foun_mat = db.Column(db.Float())
    roof_type = db.Column(db.String())
    roof_mat = db.Column(db.Float())
    wall_mat_1 = db.Column(db.Float())
    wall_mat_2 = db.Column(db.String())
    window_typ = db.Column(db.String())
    window_mat = db.Column(db.Float())
    door_typ = db.Column(db.String())
    door_mat = db.Column(db.Float())
    exter_fea = db.Column(db.String())
    inter_fea = db.Column(db.String())
    dec_detail = db.Column(db.String())
    condition = db.Column(db.Float())
    des_res = db.Column(db.String())
    comments = db.Column(db.String())
    placement = db.Column(db.String())
    lonr = db.Column(db.String())
    continuation = db.Column(db.String())
    nrdata = db.Column(db.String())
    date_updated = db.Column(db.String())
    lat = db.Column(db.Float())
    long = db.Column(db.Float())
    utm_zone = db.Column(db.Float())
    easting = db.Column(db.String())
    northing = db.Column(db.String())
    p_b_c = db.Column(db.String())
    year_closed = db.Column(db.Float())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    duplicate_check = db.Column(db.String())
    duplicate_check_date = db.Column(db.String())
    duplicate_check_user = db.Column(db.Float())
    duplicate_check_comments = db.Column(db.String())
    approved_shpo = db.Column(db.Float())

