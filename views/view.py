#!/usr/bin/python3
""" Starts the web application """
from models import storage
from models.user import User
from models.post import Post
from uuid import uuid4
from flask import Flask, Blueprint, send_from_directory, render_template, url_for, redirect, flash, request, current_app, abort
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import secrets
import os

view = Blueprint('view', __name__, template_folder='templates', static_folder='static')

def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/img', photo_name)
    photo.save(file_path)
    return photo_name




@view.route('/post', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        description = request.form.get('description')
        price = request.form.get('price')
        location = request.form.get('location')
        comment = request.form.get('comment')
        photo = save_image(request.files.get('photo'))
        user_id = int (current_user.get_id())

        post = Post(description=description, price=price, location=location, comment=comment, image=photo, user_id=user_id)

        storage.new(post)
        storage.save()
        flash('Upload successful', 'info')
        return render_template('post.html')

    return render_template('post.html')

@view.route('/post/<post_id>', methods=['GET'])
def post(post_id):
    post = storage.get(Post, post_id)
    if post:
        print(post.image)
    else:
        abort(404)

    return render_template('images.html', file=post)

@view.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/img", filename)
