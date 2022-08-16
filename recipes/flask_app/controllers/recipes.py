from flask.helpers import url_for
from flask_app import app 
from flask import render_template, redirect, session, request
from flask import flash
from flask_app.models import recipe, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# GET render the form to add new recipe
@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('add_recipe.html')

# POST to create new recipe
@app.route('/recipes/create', methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
        
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    new_recipe_id = recipe.Recipe.create_recipe(request.form)
    print(new_recipe_id)
    
    return redirect ('/dashboard')

# GET display recipe
@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": id
    }

    this_recipe = recipe.Recipe.get_one_recipe(data)
    print("RECIPE INFO", this_recipe)
    
    return render_template('show_recipe.html', recipe = this_recipe) 

# GET display form to edit recipe
# localhost:5000/recipes/edit/recipe.id
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': id
    }
    user_data = {
        'id':session['user_id']
    }
    this_recipe = recipe.Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', recipe = this_recipe, user = user_data)

# POST update form
# /recipes/update
@app.route('/recipes/update', methods=["POST"])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')

    id = request.form['id']


    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(url_for('edit_recipe', id=id))

    recipe.Recipe.update_recipe(request.form)
    
    return redirect (url_for('show_recipe', id=id))


# DELETE
@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id': id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect('/dashboard')