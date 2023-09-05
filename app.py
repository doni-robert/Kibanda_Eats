#!/usr/bin/python3
""" Starts the web application """
from models import storage
from models.user import User
from models.post import Post
from uuid import uuid4
from flask import Flask, send_from_directory, render_template, url_for, redirect, flash, request, current_app, abort
from flask_login import login_required, LoginManager, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from views.auth import auth
from views.view import view
import secrets
import os


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(view)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dekeysecreto'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)






class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[InputRequired()])
	submit = SubmitField("Submit")






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
def dashboard():
    return render_template('dashboard.html')

@app.route('/main', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'DELETE'])
def main():
    user_id = current_user.get_id()
    return render_template('main.html', userId=user_id, cache_id=uuid4())







@app.teardown_appcontext
def close(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)