from app import db
from flask_login import UserMixin

# MODELS.
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(40), unique=True)
    about = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    previous_conditions = db.Column(db.Text)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    password = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    phone_verified = db.Column(db.SmallInteger, default=0)
    last_appointment = db.Column(db.Text, nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

    @classmethod
    def get(cls, userid):
        return User.query.filter_by(id=userid).first()

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email
        self.about = ''
        self.medical_history = ''
        self.height = 0.0
        self.weight = 0.0
        self.previous_conditions = ''
        self.role = 0
        self.password = password
        self.phone = ''
        self.phone_verified = 0

    def __repr__(self):
        return '<User %r>' % self.nickname
# /MODELS.