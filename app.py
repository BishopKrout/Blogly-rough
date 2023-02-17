"""Blogly application."""
from datetime import datetime
from flask import Flask, request, render_template,  redirect, flash, session, url_for
from models import db, connect_db, User, Post, Tag, PostTag
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
    """Route function to display the list of all users"""
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/add_user', methods=["GET","POST"])
def add_user():
    """Route function to add a new user"""
    if request.method == 'POST':    
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        if not first_name or not last_name or not username:
            flash('Username, First name and last name are required fields', 'error')
            return redirect('/add_user')

        new_user = User(username=username, first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect('/')

    return render_template("add_user.html")

@app.route('/<int:user_id>')
def show_user(user_id):
    """Route function to display details of a user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    """Route function to edit details of a user"""
    user = User.query.get(user_id)
    if request.method == 'POST':
        username = request.form['username']
        user.first = request.form['first_name']
        user.last = request.form['last_name']
        user.image = request.form['image_url']
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=user)
@app.route('/delete_user/<int:id>', methods=["POST"])

def delete_user(id):
    """Delete a user from the database."""
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))


@app.route('/<int:user_id>/add_post', methods=['GET', 'POST'])
def add_post(user_id):
    """Add a new post for a user."""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    if request.method == 'POST':    
        title = request.form['title']
        content = request.form['content']
        tag_ids = request.form.getlist("tags")

        if not title or not content:
            flash('Post must have title and content', 'error')
            return redirect(url_for('show_user', user_id=user_id))

        new_post = Post(title=title, content=content, user_id=user_id)
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            new_post.tags.append(tag)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added successfully', 'success')
        return redirect(url_for('show_user', user_id=user_id))

    return render_template("add_post.html", user=user, tags=tags)

@app.route('/<int:user_id>/<int:post_id>')
def show_post(user_id, post_id):
    """Display a specific post for a user."""
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    if post:
        post_tags = post.tags
    else:
        post_tags = []
    return render_template('post.html', user=user, post=post, post_tags=post_tags)

@app.route('/<int:user_id>/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(user_id, post_id):
    """Edit post for a user with the given post_id."""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        if not post.title or not post.content:
            flash('Post must have title and content', 'error')
            return redirect(url_for('show_user', user_id=user_id))

        post.created_at = datetime.now()

        tag_ids = request.form.getlist("tags")
        post.tags = []

        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)

        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('show_post', user_id=user_id, post_id=post_id))

    return render_template("edit_post.html", user=user, post=post, tags=tags)

@app.route('/delete_post/<int:post_id>', methods=["POST"])
def delete_post(post_id):
    """Delete post with the given post_id."""    
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('show_user', user_id=user_id))

@app.route('/list_tags')
def list_tags():
    """List all tags."""    
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    """Add a new tag."""
    if request.method == 'POST':    
        name = request.form.get('name')

        if not name:
            flash('Name is a required fields', 'error')
            return redirect('/add_tag')

        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash('Tag added successfully', 'success')
        return redirect('/list_tags')

    return render_template("add_tag.html")

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Display details of a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_page.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>")
def display_posts_by_tag(tag_id):
    """Display all posts associated with a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts.all()
    return render_template("posts.html", tag=tag, posts=posts)

@app.route('/delete_tag/<int:tag_id>', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted successfully', 'success')
    tags = Tag.query.all()
    return redirect(url_for('list_tags', tags=tags))
