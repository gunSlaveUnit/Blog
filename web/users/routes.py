from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user

from manage import bcrypt, db
from web.users.forms import RegistrationForm, LoginForm
from web.users.models import User

users = Blueprint('users', __name__)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('base.home'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        user = User(username=registration_form.username.data,
                    email=registration_form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'You account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('registration.html', form=registration_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            flash('You have been logged in', 'success')
            return redirect(url_for('base.home'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('login.html', form=login_form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('base.home'))


@users.route('/account')
def account():
    return render_template('account.html', title='Account')
