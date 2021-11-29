from flask import Flask, render_template, request, redirect
# import the class from user.py
from users import User
app = Flask(__name__)

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
    return redirect('/users')

@app.route('/users/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    User.delete_user(data)
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)