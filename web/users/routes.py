from flask import render_template, Blueprint, flash, redirect, url_for

from web.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        flash(f'Account was created for {registration_form.username.data}', 'success')
        return redirect(url_for('base.home'))
    return render_template('registration.html', form=registration_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash('You have been logged in', 'success')
        return redirect(url_for('base.home'))
    else:
        flash('Login unsuccessful. Check username and password', 'danger')
    return render_template('login.html', form=login_form)
