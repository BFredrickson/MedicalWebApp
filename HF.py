from flask import render_template, request, redirect, url_for
from models import User
from forms import SignupForm, LoginForm, UserEditForm
from app import login_manager, app, db
from app import client
import datetime
from flask_mail import Message
from flask_login import login_user, current_user, login_required, logout_user

# CALLBACKS
@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()
# /CALLBACKS

# CONTROLLERS
@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.nickname.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        print(form.errors.items())
    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        user = load_user(login_form.email.data)
        login_user(user)
        return redirect('/home')
    return render_template('login.html', form=login_form)


def send_sms(to, text):
    client.api.account.messages.create(to=to, from_='+18325394311', body=text, media_url=[])


def sendEmail(to, text):
    msg = Message('Alert from Appointment')

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    user_edit_form = UserEditForm(request.form)
    if request.method == 'POST' and user_edit_form.validate():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        user.phone = user_edit_form.phone.data
        user.phone_verified = 1
        user.about = user_edit_form.about_me.data
        user.last_appointment = user_edit_form.last_appointment.data
        user.weight = user_edit_form.weight.data
        user.height = user_edit_form.height.data
        user.medical_history = user_edit_form.medical_history.data
        db.session.commit()
    user = User.query.filter_by(nickname=current_user.nickname).first()
    alert_dentist = False
    alert_physical = False
    if user.last_appointment:
        l_a = datetime.datetime.strptime(user.last_appointment, '%Y-%m-%d')
        now = datetime.datetime.now()
        months = (now.year - l_a.year) * 12 + now.month - l_a.month
        if months > 12:
            alert_dentist = True
            alert_physical = True
        if months > 6:
            alert_physical = True
    if alert_physical and user.phone:
        send_sms(user.phone, 'You need a physical')
        sendEmail(user.email, 'It is time your scheduled physical exam.')
    if alert_dentist and user.phone:
        send_sms(user.phone, 'You need to visit a dentist')
        sendEmail(user.email, 'It is time your scheduled dental exam.')
    return render_template('home.html', form=user_edit_form, alert_physical=alert_physical, alert_dentist=alert_dentist)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

# /CONTROLLERS

if __name__ == '__main__':
    app.run(debug=True)
