#!/usr/bin/python3
""" Starts the web application """
from models import storage
from models.user import User
from models.post import Post
from uuid import uuid4
from flask import Flask, send_from_directory, render_template, url_for, redirect, flash, request, current_app, abort
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import secrets
import os


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dekeysecreto'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)



class RegisterForm(FlaskForm):
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
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[InputRequired()])
	submit = SubmitField("Submit")




def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/img', photo_name)
    photo.save(file_path)
    return photo_name


@app.route('/sign-up', strict_slashes=False, methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        """
        """
        if len(email) < 4:
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
            flash('Registration successful. Please log in.', 'info')
            return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = storage.getUserObj(User, email)
        if user:
            if user.check_password(password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('add_post', cache_id=uuid4()))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html')

@app.route('/post', methods=['GET', 'POST'])
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

@app.route('/post/<post_id>', methods=['GET'])
def post(post_id):
    post = storage.get(Post, post_id)
    if post:
        print(post.image)
    else:
        abort(404)

    return render_template('images.html', file=post)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/img", filename)

@app.route('/')
def gallery():
    posts = storage.all(Post)
    
    return render_template("gallery.html", posts=posts)

@app.route('/search', methods=["POST"])
def search():
    price = request.form.get('price')
    all_posts = storage.all(Post)
    post_dic = {}
    for key, value in all_posts.items():
        if value.price <= int(price):
            post_dic[key] = value
    return render_template("gallery.html", posts=post_dic)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/main', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def main():
    user_id = current_user.get_id()
    return render_template('main.html', userId=user_id, cache_id=uuid4())


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.teardown_appcontext
def close(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)