from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
# The db instance is from Flask-SQLAlchemy
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# The class inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
# Flask-Login provides a mixin class called UserMixin that includes safe implementations that are appropriate for most user model classes
class User(UserMixin, db.Model):
    # Fields are assigned a type using Python type hints, wrapped with SQLAlchemy's so.Mapped generic type.
    # A type declaration such as so.Mapped[int] or so.Mapped[str] define the type of the column, and also make values required, or non-nullable in database terms.
    # To define a column that is allowed to be empty or nullable, the Optional helper from Python is also added, as password_hash demonstrates.
    # In most cases defining a table column requires more than the column type.
    # SQLAlchemy uses a so.mapped_column() function call assigned to each column to provide this additional configuration.
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # This is not an actual database field, but a high-level view of the relationship between users and posts.
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    # The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Because Flask-Login knows nothing about databases, it needs the application's help in loading a user.
# For that reason, the extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
