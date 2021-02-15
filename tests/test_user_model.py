import unittest
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_Roles(self):
        admin_role = Role(name='Administrator')
        mod_role = Role(name='Moderator')
        worker_role = Role(name='User')
        db.session.add_all([admin_role, mod_role, worker_role])
        db.session.commit()
        self.assertTrue(admin_role.name == 'Administrator')
        self.assertTrue(mod_role.name == 'Moderator')
        self.assertTrue(worker_role == 'User')

    def test_Users(self):
        admin = User(username='admin', password='cat', role_id=16,\
                     email='test@example.com', role='Administrator')
        mod = User(username='mod', password='dog', role_id=8,\
                   email='mod@example.com', role='Moderator')
        worky = User(username='worky', password='fish', role_id=4,\
                     email='worky@example.com', role='User')
        db.session.add_all([admin, mod, worky])
        db.session.commit()
        self.assertTrue(admin.password == 'cat')
        self.assertTrue(mod.password == 'dog')
        self.assertTrue(worky.password == 'fish')

    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password ='cat')
        u2 = User(password ='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        worky = User(premission='User')
        self.assertTrue(worky.can(Permission.SEARCH))
        self.assertTrue(worky.can(Permission.ENTRY))
        self.assertTrue(worky.can(Permission.EDIT))
        self.assertFalse(worky.can(Permission.MODERATE))
        self.assertFalse(worky.can(Permission.ADMIN))

    def test_moderator_role(self):
        mod = User(premission='Moderator')
        self.assertTrue(mod.can(Permission.SEARCH))
        self.assertTrue(mod.can(Permission.ENTRY))
        self.assertTrue(mod.can(Permission.EDIT))
        self.assertTrue(mod.can(Permission.MODERATE))
        self.assertFalse(mod.can(Permission.ADMIN))

    def test_administrator_role(self):
        admin = User(premission='Administrator')
        self.assertTrue(admin.can(Permission.SEARCH))
        self.assertTrue(admin.can(Permission.ENTRY))
        self.assertTrue(admin.can(Permission.EDIT))
        self.assertTrue(admin.can(Permission.MODERATE))
        self.assertTrue(admin.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.SEARCH))
        self.assertFalse(u.can(Permission.ENTRY))
        self.assertFalse(u.can(Permission.EDIT))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

