from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User 
from flask_app.models.show import Show

# CREATE

@app.route("/shows/create", methods=['POST'])
def create_show():
    if not Show.validate_show(request.form):
        return redirect('/shows/new')
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Show.create_show(data)
    return redirect('/dashboard')

# READ 

@app.route('/shows/new')
def add_show():
    return render_template("add_show.html")

@app.route('/show/<int:id>')
def display_show(id):
    this_show = Show.read_by_id({"id": id})
    return render_template("display_show.html", show = this_show)

# UPDATE

@app.route('/shows/edit/<int:id>')
def edit_show(id):
    show_to_edit = Show.read_by_id({"id": id})
    return render_template("edit_show.html", show = show_to_edit)

@app.route('/shows/update', methods=['POST'])
def update_show():
    if not Show.validate_show(request.form):
        return redirect('/shows/new')
    data = {
        "id": request.form['id'],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "user_id": request.form['user_id']
    }
    Show.update_show(data)
    return redirect('/dashboard')

# DELETE

@app.route('/shows/delete/<int:id>')
def delete_show(id):
    Show.delete_show({"id": id})
    return redirect('/dashboard')