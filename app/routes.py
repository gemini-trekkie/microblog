# So what goes in the routes module? The routes handle the different URLs that the application supports.
# In Flask, handlers for the application routes are written as Python functions, called view functions.
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

# To have better control over these links, Flask provides a function called url_for(),
# which generates URLs using its internal mapping of URLs to view functions.
# For example, the expression url_for('login') returns /login, and url_for('index') return '/index.
# The argument to url_for() is the endpoint name, which is the name of the view function.
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

# The way Flask-Login protects a view function against anonymous users is
# with a decorator called @login_required.

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)

        # When a user that is not logged in accesses a view function protected with the @login_required decorator,
        # the decorator is going to redirect to the login page, but it is going to include some extra information
        # in this redirect so that the application can then return to the original page.
        # If the user navigates to /index, for example, the @login_required decorator will intercept the request and
        # respond with a redirect to /login, but it will add a query string argument to this URL,
        # making the complete redirect URL /login?next=/index.
        # The next query string argument is set to the original URL, so the application can use that to redirect back after login.
        next_page = request.args.get('next')

        # An attacker could insert a URL to a malicious site in the next argument, so the application only redirects when the URL is relative,
        # which ensures that the redirect stays within the same site as the application.
        # To determine if the URL is absolute or relative, I parse it with Python's urlsplit() function and then check if the netloc component is set or not.
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)