#!/usr/bin/python3
""" User view Blueprint"""
from flask import Flask, Blueprint, render_template, flash, request, current_app, abort, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from models import storage
from models.user import User
from models.post import Post
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import os
import secrets


view = Blueprint('view', __name__, template_folder='templates', static_folder='static')

def save_image(photo):
    """Saves a photo"""
    if photo:
        hash_photo = secrets.token_urlsafe(10)
        _, file_extension = os.path.splitext(photo.filename)
        photo_name = hash_photo + file_extension
        file_path = os.path.join(current_app.root_path, 'static/img', photo_name)
        photo.save(file_path)
        return photo_name
    return None

@view.route('/post', methods=['GET', 'POST'])
@login_required
def add_post():
    """Enables a user to add a post"""
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
        return history()

    return render_template('post.html')

@view.route('/history')
def history():
    """Displays the user's post history"""
    from_delete = request.args.get('from_delete', default=0, type=int)
    from_update = request.args.get('from_update', default=0, type=int)

    if from_delete:
        flash('Select a post to delete')
    if from_update:
        flash('Select a post to update')
    user_id = current_user.id
    posts = storage.all(Post)
    
    user_posts = {}
    for k, v in posts.items():
        if v.user_id == user_id:
            user_posts[k] = v
    
    return render_template("gallery.html", from_delete=from_delete, from_update=from_update, posts=user_posts)


@view.route('/update/<post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    """Enables a user to update a post"""
    post = storage.get(Post, post_id)
    default_image = post.image

    if request.method == 'POST':
        post.description = request.form.get('description')
        post.price = request.form.get('price')
        post.location = request.form.get('location')
        post.comment = request.form.get('comment')

        new_image = save_image(request.files.get('photo'))
        if new_image:
            post.image = new_image
        else:
            post.image = default_image

        storage.save()

        flash('Update successful', 'info')
        return history()
    
    return render_template('update.html', post=post)



@view.route('/delete/<post_id>')
@login_required
def delete(post_id):
    """Deletes a users post"""
    storage.delete(Post, post_id)
    storage.save()
    flash('Deleted')
    return history()
    

@view.route('/post/<post_id>', methods=['GET'])
def post(post_id):
    """Displays one post"""
    from_delete = request.args.get('from_delete', default=0, type=int)
    from_update = request.args.get('from_update', default=0, type=int)

    post = storage.get(Post, post_id)
    if post:
        print(post.image)
    else:
        abort(404)

    return render_template('images.html', from_delete=from_delete, from_update=from_update, file=post)
