from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from ..models.user import User

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    return render_template("users.html", all_users = User.get_all())

@app.route("/users/new")
def new_user():
    return render_template("create_user.html")

@app.route('/users/create', methods=["POST"])
def create_user():
    print(request.form)
    # pass in form data
    User.save(request.form)
    # redirect after saving to the database
    return redirect('/users')

@app.route('/users/<int:id>')
def show(id):
    data = {
        "id": id
    }
    return render_template("show_user.html", user = User.get_one(data))

@app.route('/users/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    return render_template("edit_user.html", user = User.get_one(data))

@app.route('/users/update', methods=["POST"])
def update():
    print(request.form)
    User.edit_user(request.form)
    id = request.form['id']
    return redirect(url_for('show', id=id))

@app.route('/users/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    User.delete_user(data)
    return redirect('/users')