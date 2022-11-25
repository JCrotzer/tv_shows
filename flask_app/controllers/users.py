from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/users/register', methods=['POST'])
def register_user():

    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session["user_id"] = User.create_user(data)
    return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def login_user():
    this_user = User.read_by_email({"email": request.form['email']})
    if not this_user or not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid username/password")
        return redirect('/')
    session["user_id"] = this_user.id
    return redirect('/dashboard')

# READ

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    this_user = User.read_by_id(data)
    all_shows = Show.read_all_shows()
    return render_template('dashboard.html', user = this_user, all_shows = all_shows)

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect('/')


