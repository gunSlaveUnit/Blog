from flask import render_template, Blueprint

from web.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm()
    return render_template('registration.html', form=registration_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)
