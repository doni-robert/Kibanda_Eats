#!/usr/bin/python3
""" Authentication Blueprint """
from flask import Blueprint, render_template, url_for, redirect, flash, request, current_app
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from models import storage
from models.user import User
from models.post import Post
from uuid import uuid4
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
        
class LoginForm(FlaskForm):
    """Login form"""
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@auth.route('/sign-up', strict_slashes=False, methods=['GET', 'POST'])
def sign_up():
    """Signs up a new user"""
    form = RegisterForm()
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = storage.getUserObj(User, email)
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User(email=email, username=username, password=password1)
            storage.new(user)
            storage.save()
            flash('Registration successful. Please log in.', category='success')
            return redirect(url_for('auth.login'))
    return render_template("signup.html")

@auth.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    """Logs in a user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = storage.getUserObj(User, email)
        if user:
            if user.check_password(password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('gallery'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html')

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Logs out a user"""
    logout_user()   
    return redirect(url_for('auth.login'))
