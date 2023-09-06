#!/usr/bin/python3
""" Starts the web application """
from models import storage
from models.user import User
from models.post import Post
from flask import Flask, render_template, request, current_app
from flask_login import LoginManager, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt
from views.auth import auth
from views.view import view


"""Initialize flask app"""
app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(view)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dekeysecreto'

"""Initialize login manager"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Loads user"""
    return storage.get(User, user_id)

@app.route('/')
def gallery():
    """Home route - Displays all images """
    posts = storage.all(Post)
    
    return render_template("gallery.html", posts=posts)

@app.route('/search', methods=["POST"])
def search():
    """Searches based on price"""
    price = request.form.get('price')
    all_posts = storage.all(Post)
    post_dic = {}
    for key, value in all_posts.items():
        if value.price <= int(price):
            post_dic[key] = value
    return render_template("gallery.html", posts=post_dic)

#@app.route('/main', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'DELETE'])
#def main():
#   user_id = current_user.get_id()
#  return render_template('main.html', userId=user_id, cache_id=uuid4())

@app.teardown_appcontext
def close(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)