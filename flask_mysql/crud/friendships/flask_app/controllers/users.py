from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models import user, friendship

# route root
@app.route('/')
def index():
    return redirect('/friendships')

@app.route('/friendships')
def friendships():
    
    return render_template("index.html", users = user.User.get_all_users(), friendships = user.User.get_friendships())

# CREATE - add new user
# POST localhost:5000/users/new
@app.route('/users/new', methods=["POST"])
def create_user():
    user_id = user.User.create_user(request.form)
    print("NEW USER", user_id)
    return redirect('/')

# CREATE - new friendship
@app.route('/friendships/new', methods=["POST"])
def create_friendship():

    test = user.User.get_one_friendship(request.form)
    print("TEST=========================", test)

    if len(user.User.get_one_friendship(request.form)) == 0 and request.form['user_id'] != request.form['friend_id']:
        
        friendship_id = user.User.create_friendship(request.form)
        print("FRIENDSHIP", friendship_id)

    
    
    return redirect('/')