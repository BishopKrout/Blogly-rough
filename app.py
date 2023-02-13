"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/add_user', methods=["GET","POST"])
def add_user():
    if request.method == 'POST':    
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        if not first_name or not last_name:
            flash('First name and last name are required fields', 'error')
            return redirect('/add_user')

        new_user = User(first_name=first_name, last_name=last_name,     image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect('/')

    return render_template("add_user.html")

@app.route('/<int:user_id>')
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.first = request.form['first_name']
        user.last = request.form['last_name']
        user.image = request.form['image_url']
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:id>', methods=["POST"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))