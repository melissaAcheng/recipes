from flask_app import app
from flask import render_template, request, session, redirect
from flask_app.models import email

# localhost:5000 route
@app.route('/')
def index():
    
    return render_template("index.html") 

@app.route('/enter', methods=['POST'])
def enter():
    if not email.Email.validate_email(request.form):
        return redirect('/')
    email.Email.create_email(request.form)
    return redirect('/success')

# GET displays all emails
@app.route('/success')
def show_emails():
    all_emails = email.Email.get_all()
    return render_template('success.html', all_emails = all_emails)

# Delete
@app.route('/delete/<int:id>')
def delete_email(id):
    data = {
        "id": id
    }
    email.Email.delete_email(data)
    return redirect('/success')