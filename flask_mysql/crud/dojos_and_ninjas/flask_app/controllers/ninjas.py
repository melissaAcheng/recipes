from flask.helpers import url_for
from flask_app import app 
from flask import render_template, request, redirect, url_for
from flask_app.models import dojo, ninja
from flask_app.controllers import dojos




# GET render form to add ninja
@app.route('/ninjas')
def new_ninja():
    dojos = dojo.Dojo.get_all()
    return render_template("new_ninja.html", all_dojos = dojos)

# POST to create new ninja
@app.route('/ninjas/create', methods=["POST"])
def create_ninja():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "dojo_id": request.form["dojo_id"]
    }
    print (data)
    ninja.Ninja.save(data)
    return redirect (url_for('show_dojo', id=data['dojo_id']))


# redirect to the dojo show page

