from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
import re
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard/")
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user=User.get_one(data)
    messages = Message.get_user_messages(data)
    users=User.get_all()
    return render_template("dashboard.html", users = users, user = user, messages = messages)

@app.route('/register/',methods=['POST'])
def register():
    is_valid = User.validate(request.form)
    if not is_valid: # if is_valid = False then redirect to /
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)
    if not id:
        flash("Something went wrong","register")
        return redirect('/')
    session['user_id'] = id
    flash("You are not logged in")
    return redirect('/dashboard/')
    

@app.route('/login/', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_email(data) # check if the email is in the database
    if not user: # if not let them know
        flash('That email is not in our database, please register')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password')
        return redirect('/')
    session['user_id'] = user.id
    flash("You are now logged in")
    return redirect('/dashboard/')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

