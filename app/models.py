from flask import current_app, request, url_for
from flask_login import UserMixin, AnoymousUserMixin
from app.exepctions import ValidationError
from . import db, login_manager

class Premission:
    SEARCH = 1
    ENTRY = 2
    EDIT = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ == 'roles'
    id = db.Column(db.Integare, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    premissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.premissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.SEARCH, Permission.ENTRY]
            'Moderator': [Permission.SEARCH, Permission.ENTRY, Permission.EDIT,
                          Permission.EDIT, Permission.MODERATE]
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
            self.permission += perm

    def remove_permission(self, perm):
        if self.has_permission(perm)
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

class AnonymoousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class hpr(db.Model):
    __tablename__ = 'hpr'
    objectid = db.Column(db.Integer, primary_key=True)
    propname = db.Column(db.String(64))
    resname = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    
