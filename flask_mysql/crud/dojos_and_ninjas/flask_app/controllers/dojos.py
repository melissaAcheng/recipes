from flask_app import app 
from flask import render_template, request, redirect
from flask_app.models import dojo, ninja

@app.route('/')
def index():
    return redirect ('/dojos')

@app.route('/dojos')
def dojos():
    dojos = dojo.Dojo.get_all()
    return render_template("index.html", all_dojos = dojos)

# @app.route('/dojos/ninjas')
# def dojos_ninjas():
#     dojos = dojo.Dojo.get_dojo_with_ninjas()
#     return render_template("dojo_show.html", all_dojos = dojos)

# POST creates the new dojo
@app.route('/dojos/create', methods=["POST"])
def create_dojo():
    dojo_id = dojo.Dojo.create_dojo(request.form)
    print(request.form)
    return redirect('/')

# whichever ninja has the dojo id of (1) display on dojo.show_html
@app.route('/dojos/<int:id>')
def show_dojo(id):
    data = {
        "id": id
        }
    get_dojo = dojo.Dojo.get_dojo_with_ninjas(data)
 
    return render_template("dojo_show.html", dojo = get_dojo)
