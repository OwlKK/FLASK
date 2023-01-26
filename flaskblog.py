from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# MAIN STARTER FUNCTION
app = Flask(__name__)

# secret key is needed to keep the client-side sessions secure
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# specify location for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # relative path from current file

db = SQLAlchemy(app)  # database instance


# DB structure as classes (each class is a table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)  # string of len 20 (max from user input)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # relationship between two mapped classes(one-to-many)
                                                                  # lazy -> db loades all the data in one go (all posts)
                                                                  # backref - automates creating a relationship

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # ForeignKey - relationship to user model

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # here - sends message to the next request
        flash(f'Account created for {form.username.data}!', 'success')  # display message for the user
        return redirect(url_for('home'))  # go to this url (with code 200)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # checks that the request is a POST request,
        # and runs the validators you configured
        # for each field.

        if form.email.data == 'admin@blog.com' and form.password.data == 'password':

            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
