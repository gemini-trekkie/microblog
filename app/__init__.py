from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# The __name__ variable passed to the Flask class is a Python predefined variable,
# which is set to the name of the module in which it is used.
# Flask uses the location of the module passed here as a starting point
# when it needs to load associated resources such as template files.
app = Flask(__name__)
app.config.from_object(Config)

# The database is going to be represented in the application by the database instance.
# The database migration engine will also have an instance. 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# Flask-Login provides a very useful feature that forces users to log in before they can view certain pages of the application.
# If a user who is not logged in tries to view a protected page,
# Flask-Login will automatically redirect the user to the login form, and only redirect back to the page the user wanted to view after the login process is complete. 
# For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins. This can be added in app/__init__.py:
login.login_view = 'login'

# The bottom import is a well known workaround that avoids circular imports,
# a common problem with Flask applications.
# You are going to see that the routes module needs to import the app variable
# defined in this script, so putting one of the reciprocal imports at the bottom
# avoids the error that results from the mutual references between these two files.
from app import routes, models
