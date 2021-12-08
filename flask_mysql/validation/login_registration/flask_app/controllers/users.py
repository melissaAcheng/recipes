from flask_app import app 
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#localhost:5000 route root
@app.route('/')
def index():

    return render_template("index.html")

@app.route('/register', methods=["POST"])
def create_user():
    if not user.User.validate_registration(request.form):
        return redirect('/')

    # at this point registration passes
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print("PASSWORD IS", pw_hash)

    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }


    # save user data information
    user_id = user.User.create_user(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect('/users/dashboard')

@app.route('/users/login', methods = ['POST'])
def login():
    # see if the username provided exists in the database

    user_in_db = user.User.get_by_email(request.form)

    # if user is not registered in the db
    if not user_in_db:
        flash("Invalid Login Credentials")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Login Credentials", "login_error")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id

    return redirect('/users/dashboard')

@app.route('/users/dashboard')
def display_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=user.User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')