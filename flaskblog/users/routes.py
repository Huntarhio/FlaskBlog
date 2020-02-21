from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog.models import User, Post
from flaskblog import bcrypt
from flaskblog.users.forms import (LoginForm, RegistrationForm, 
                                RequestResetForm, ResetPasswordForm)
                                
from flaskblog.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    # if a user is already logged in and they click on the register button, they should be redirected to the homepage. althoug this was update to be hidden for authethicated users
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): # validates the form for correct entries
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hashes the passowrd for password safetyn purpose
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #instantiate the user with the data colected from the form
        db.session.add(user) #adds user to the database
        db.session.commit() # commits user to the database
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # if a user is already logged in and they click on the log in button, they should be redirected to the homepage. althoug this was update to be hidden for authethicated users
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  #gets the next parameter from the url
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user).\
                order_by(Post.posted_date.desc()).\
                    paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, title='User Posts')


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to {email} for password reset confirmation'.\
                            format(email=user.email), 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is invalid/expired, please try again', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password updated successfully', 'warning')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title = 'Reset Password', form=form)