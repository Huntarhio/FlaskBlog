import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, make_response
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# @app.route('/post/<int:post_id>/comment')
# def comment(post_id):
#     comments = Comment.query.filter_by(post_id=post_id).\
#                 order_by(Comment.created_date.desc()).all()
#     return render_template('post.html', comments=comments)





# @app.route('post/<int:post_id>/comment')