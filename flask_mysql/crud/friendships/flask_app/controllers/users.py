from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models import user

# route root
@app.route('/')
def index():
    return redirect('/friendships')

# CREATE - add new user
# POST localhost:5000/users/new
@app.route('/users/new', methods=["POST"])
def create_user():
    user_id = user.User.create_user(request.form)
    print("NEW USER", user_id)
    return redirect('/')
