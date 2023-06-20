"""Blogly application."""

from flask import Flask, request, render_template, redirect, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost:5433/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def list_users():
    """Shows list of all users in db"""
    return redirect('/users')


@app.route('/users')
def users_display():
    """Displays the page with all users info"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('blogly.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_form():
    """Shows creating a new user in a form"""

    return render_template('form.html')



@app.route("/users/new", methods=["POST"])
def new_users():
    """form submission to create a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_page(user_id):
    """showing specific user's info"""

    user = User.query.get_or_404(user_id)
    return render_template('new.html', user=user)



@app.route('/users/<int:user_id>/edit')
def edit_users(user_id):
    """Showing the form to edit a current user"""

    user = User.query.get_or_404(user_id)
    return render_template('update.html', user=user)



@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """form submission for updating a current user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_users(user_id):
    """form submission for deleting a current user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

if __name__ == '__main__':
    app.run(debug=True, port=5001)