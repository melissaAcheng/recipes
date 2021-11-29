from flask import Flask, render_template, request, redirect
# import the class from user.py
from user import User
app = Flask(__name__)

@app.route('/users')
def index():
    users = User.get_all()
    print(users)
    return render_template("users.html", all_users = users)

@app.route("/users/new")
def new_user():
    return render_template("create.html")


from user import User
@app.route('/create_user', methods=["POST"])
def create_user():
    # make a data dictionary from the request.form in our template
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    # pass the data dictionary into the save method from the Friend class
    User.save(data)
    # redirect after saving to the database
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)