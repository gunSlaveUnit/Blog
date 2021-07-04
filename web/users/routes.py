from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from services import bcrypt, db, mail, cache
from web.posts.models import Post
from web.users.forms import RegistrationForm, LoginForm, AccountUpdateForm, ResetPasswordForm, RequestResetForm
from web.users.models import User
from web.users.utils import save_user_account_image

users = Blueprint('users', __name__)


@users.route('/registration', methods=['GET', 'POST'])
@cache.cached(timeout=60)
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
@cache.cached(timeout=60)
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
@cache.cached(timeout=60)
def logout():
    logout_user()
    return redirect(url_for('base.home'))


@users.route('/account', methods=['GET', 'POST'])
@cache.cached(timeout=60)
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


@users.route("/user/<string:username>")
@cache.cached(timeout=60)
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
@cache.cached(timeout=60)
def reset_request():
    def send_reset_email(user):
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                      sender='noreply@demo.com',
                      recipients=[user.email])
        msg.body = f'''To reset your password, visit the following link:
        {url_for('reset_token', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
        mail.send(msg)

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
@cache.cached(timeout=60)
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
