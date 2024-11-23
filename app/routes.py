# So what goes in the routes module? The routes handle the different URLs that the application supports.
# In Flask, handlers for the application routes are written as Python functions, called view functions.
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

# To have better control over these links, Flask provides a function called url_for(),
# which generates URLs using its internal mapping of URLs to view functions.
# For example, the expression url_for('login') returns /login, and url_for('index') return '/index.
# The argument to url_for() is the endpoint name, which is the name of the view function.
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)