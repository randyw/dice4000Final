from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    permission_level = db.Column(db.Integer, index=True)
    # level 0 = student (read orgs, CRUD self)
    # level 1 = faculty (CRUD orgs, CRUD self)
    # level 2 = admin   (CRUD orgs, CRUD all users)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    bg_check_required = db.Column(db.Boolean, index=True)
    description = db.Column(db.String(1000), index=True)
    keywords = db.Column(db.String(1000), index=True)
    num_volunteers = db.Column(db.Integer)
    mission_statement = db.Column(db.String(1000))
    website = db.Column(db.String(100))
    primary_contact_name = db.Column(db.String(100))
    primary_contact_title = db.Column(db.String(100))
    primary_contact_email = db.Column(db.String(100))
    primary_contact_phone = db.Column(db.String(20))
    street_address = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    alt_contact_name = db.Column(db.String(100))
    alt_contact_email = db.Column(db.String(100))
    application_url = db.Column(db.String(100))
