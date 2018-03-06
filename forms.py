from wtforms import *
from models import User
import re

class SignupForm(Form):
    nickname = StringField('Nickname *', [validators.Length(min=4, max=20)])
    email = StringField('Email *', [validators.Email()])
    password = PasswordField('Password *', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password *')

    def validate(self):
        basic_validate = Form.validate(self)
        if not basic_validate:
            return False
        user = User.query.filter_by(nickname=self.nickname)
        if not user:
            self.nickname.errors.append('User already exists')
        return True


class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    def validate(self):
        basic_validate = Form.validate(self)
        if not basic_validate:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('User does not exist')
            return False
        if user.password == self.password.data:
            return True
        else:
            self.password.errors.append('The password is not correct')


class UserEditForm(Form):
    phone = StringField('Phone')
    about_me = TextAreaField('About me in few words')
    height = FloatField('Your height')
    weight = FloatField('Your weight')
    medical_history = TextAreaField('Your medical history')
    last_appointment = DateField('Last check up', format='%Y-%m-%d')
