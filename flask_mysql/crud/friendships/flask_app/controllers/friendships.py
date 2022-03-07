from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models import user

# Displays friendships
@app.route('/friendships')
def friendships():
    
    return render_template("index.html", users = user.User.get_all_users(), friendships = user.User.get_friendships())

# CREATE - new friendship
@app.route('/friendships/new', methods=["POST"])
def create_friendship():

    if len(user.User.get_one_friendship(request.form)) == 0 and request.form['user_id'] != request.form['friend_id']:
        
        friendship_id = user.User.create_friendship(request.form)
        print("FRIENDSHIP", friendship_id)

    
    return redirect('/')

# DELETE - friendship
@app.route('/friendships/delete/<int:id>')
def delete_friendship(id):

    data = {
        'id': id
    }

    user.User.delete_friendship(data)
    return redirect('/')