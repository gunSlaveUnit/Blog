from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from manage import bcrypt, db
from web.users.forms import RegistrationForm, LoginForm, AccountUpdateForm
from web.users.models import User
from web.users.utils import save_user_account_image

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
            next_page = request.args.get('next')
            flash('You have been logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('base.home'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('login.html', form=login_form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('base.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    account_update_form = AccountUpdateForm()
    if account_update_form.validate_on_submit():
        if account_update_form.image.data:
            image_name = save_user_account_image(account_update_form.image.data)
            current_user.image = image_name
        current_user.username = account_update_form.username.data
        current_user.email = account_update_form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        account_update_form.username.data = current_user.username
        account_update_form.email.data = current_user.email
    image = url_for('static', filename='media/users/' + current_user.image)
    return render_template('account.html', title='Account', image=image, form=account_update_form)
