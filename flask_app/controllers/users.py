from flask_app import app
from flask import render_template, redirect, session, request
from flask import flash
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# localhost:5000 route root


@app.route('/')
def index():

    return render_template('index.html')

# Login route


@app.route('/signin')
def signin():
    return render_template('login.html')

# Create Registration - POST request form data and IF INFO VALID redirect to dashboard


@app.route('/register', methods=['POST'])
def register():
    # validate information
    # IF NOT then redirect to '/'
    if not user.User.validate_registration(request.form):
        return redirect('/')

    # IF info valid
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    # save user info
    user_id = user.User.register(data)
    # save in sessions
    session['user_id'] = user_id
    return redirect('/dashboard')

# Login route


@app.route('/login', methods=['POST'])
def login():
    # check if the email provided exists in the database
    user_in_db = user.User.get_by_email(request.form)

    # if no email found
    if not user_in_db:
        flash("Invalid Login Credentials", "login_error")
        return redirect('/signin')
    # if password does not match
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Login Credentials", "login_error")
        return redirect('/signin')
    # if login credentials match, set the user_id into session
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

# GET dashboard


@app.route('/dashboard')
def display_dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    user_info = user.User.get_by_id(data)
    users_recipes = recipe.Recipe.get_all_recipes(data)

    return render_template('dashboard.html', user=user_info, recipes=users_recipes)

# Logout


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Read - GET list of recipes with that user id
